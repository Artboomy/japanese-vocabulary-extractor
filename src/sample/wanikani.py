import json
import time
from pathlib import Path
import requests
import os.path
import logging

user_api_endpoint = "https://api.wanikani.com/v2/user"

api_endpoint = "https://api.wanikani.com/v2/subjects?types=vocabulary,kanji"


class WaniKani:
    def __init__(self, api_key):
        logging.info("Initializing WaniKani with API key: {}".format(api_key))
        logging.info("Used items: known vocabulary, kanji (for one-kanji words)")
        self.user_level = 0
        self.api_key = api_key
        self.cache_root = Path.home() / ".cache" / "jve-wk-cache"
        self.cache_root.mkdir(parents=True, exist_ok=True)
        self.cache = {}
        logging.debug("WaniKani cache path: {}".format(self.cache_root))
        self.populate()

    def is_ready(self):
        return bool(self.api_key)

    def __cache_exist(self):
        return os.path.isfile(self.cache_root / "cache.json")

    def __get_data(self, url=api_endpoint):
        logging.info("Downloading WaniKani data from " + url)
        response = requests.get(url,
                                headers={"Authorization": f'Bearer {self.api_key}', "Wanikani-Revision": "20170710"})
        if response.status_code != 200:
            raise RuntimeError(f"Request failed with status code {response.status_code}")
        data = response.json()
        for subject in data["data"]:
            if subject["data"]["level"] <= self.user_level:
                self.cache[subject["data"]["characters"]] = subject["id"]
        if data["pages"]["next_url"]:
            time.sleep(2)
            self.__get_data(data["pages"]["next_url"])

    def populate(self):
        if not self.api_key:
            return
        if self.__cache_exist():
            logging.info("Loading cached WaniKani data")
            self.cache = json.load(open(self.cache_root / "cache.json"))
            print("WaniKani cache size: ", len(self.cache))
            return self.cache
        logging.info("Downloading WaniKani data")
        response = requests.get(user_api_endpoint,
                                headers={"Authorization": f'Bearer {self.api_key}', "Wanikani-Revision": "20170710"})
        if response.status_code != 200:
            raise RuntimeError(f"Request failed with status code {response.status_code}")
        self.user_level = response.json()["data"]["level"]
        self.__get_data()

        with open(self.cache_root / "cache.json", "w", encoding="utf-8") as f:
            logging.info("Writing WaniKani data to file")
            f.write(json.dumps(self.cache, ensure_ascii=False))
        return self.cache

    def update(self):
        logging.error("Not implemented")
        pass

    def has_word(self, word):
        return word in self.cache
