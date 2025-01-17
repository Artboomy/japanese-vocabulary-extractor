import json
import logging
import questionary
import requests

from sample import dictionary

api_port = "8765"

CARD_TYPE = {
    "new": 0,  # New cards
    "learning": 1,  # Cards in learning phase
    "review": 2,  # Cards in review phase
    "relearn": 3,  # Cards being re-learned
    "buried": 4  # Buried cards (manually or automatically buried)
}

model_name = "Kaishi 1.5k - jve"


class AnkiWrapper:
    def __init__(self, url):
        self.url = url
        self.cache = set()

    def __make_request(self, action, params=None):
        request_payload = {
            "action": action,
            "version": 6
        }
        if params:
            request_payload["params"] = params
        response = requests.request(method="POST", url=self.url,
                                    data=json.dumps(request_payload))

        if response.status_code != 200:
            logging.error(response.text)
            raise Exception(response.text)
        response = response.json()
        if response["error"]:
            logging.error(response["error"])
            raise Exception(response["error"])
        return response["result"]

    def is_ready(self):
        return bool(self.url)

    def check_connection(self):
        try:
            logging.info(requests.get(self.url))
        except requests.exceptions.ConnectionError as e:
            logging.error("Failed to connect to Anki. Please check:"
                          "\n1. Anki is running"
                          "\n2. AnkiConnect addon is installed - https://foosoft.net/projects/anki-connect/"
                          "\n3. AnkiConnect settings changed to \"webBindAddress\": \"0.0.0.0\""
                          "\n4. Firewall permissions for Anki are granted")
            logging.error(e)
            return False
        return True

    def check_model_exist(self):
        if not self.check_connection():
            return False
        result = self.__make_request("modelNames")
        return model_name in result

    def create_model(self):
        if not self.check_connection():
            return False
        if self.check_model_exist():
            return True
        in_order_fields = ['Word', 'Word Reading', 'Word Meaning', 'Word Furigana', 'Word Audio', 'Sentence',
                           'Sentence Meaning', 'Sentence Furigana', 'Sentence Audio', 'Notes', 'Pitch Accent',
                           'Pitch Accent Notes', 'Frequency', 'Picture']
        # Extracted from Kaishi 1.5k deck
        card_templates = [
            {
                "Front": """<div lang="ja">
{{Word}}
<div style='font-size: 20px;'>{{Sentence}}</div>
</div>""",
                "Back": """
<div lang="ja">
{{furigana:Word Furigana}}

<!-- This part enables pitch accent.

{{#Pitch Accent}}
	<br><div style='font-size: 24px'>{{Pitch Accent}}</div>
{{/Pitch Accent}} 

-->

<div style='font-size: 25px; padding-bottom:20px'>{{Word Meaning}}</div>
<div style='font-size: 25px;'>{{furigana:Sentence Furigana}}</div>
<div style='font-size: 25px; padding-bottom:10px'>{{Sentence Meaning}}</div>

{{Word Audio}}
{{Sentence Audio}}
<br>
{{Picture}}

{{#Notes}}
	<br>
	<div style="font-size: 20px; padding-top:12px">Note: {{Notes}}</div>
{{/Notes}}

<!-- This part enables pitch accent notes.

{{#Pitch Accent Notes}}
<div style="font-size: 20px; width: fit-content; max-width:40vw; margin: auto">
	<details><summary>Pitch Accent Notes</summary>
		<br>{{Pitch Accent Notes}}
	</details>
</div>
{{/Pitch Accent Notes}}

-->

</div>"""
            }
        ]

        css = """.card {
 font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "Noto Sans JP", Osaka, "メイリオ", Meiryo, "ＭＳ Ｐゴシック", "MS PGothic", "MS UI Gothic", sans-serif;
 font-size: 44px;
 text-align: center;
}

img {
max-width: 300px;
max-height: 250px;
}

.mobile img {
max-width: 50vw;
}

/* This part defines the bold color. */
b{color: #5586cd}"""
        params = {
            "modelName": model_name,
            "inOrderFields": in_order_fields,
            "cardTemplates": card_templates,
            "css": css
        }
        self.__make_request("createModel", params)
        logging.info("Anki model created")
        return True

    def export(self, deck_name, notes):
        logging.info(f"Exporting {len(notes)} notes to {deck_name}")
        self.create_deck(deck_name)
        self.create_model()
        self.create_notes(deck_name, notes)

    def create_deck(self, deck_name):
        if deck_name in self.get_deck_names():
            logging.warning(f"Deck name {deck_name} already exists")
            return False
        self.__make_request("createDeck", {"deck": deck_name})
        logging.info(f"Anki deck \"{deck_name}\" created")
        return True

    def create_notes(self, deck_name, words):
        jamdict = dictionary.get_jamdict_instance()
        fails = []
        for word in words:
            word_info = dictionary.get_word_info(word, jamdict)
            try:
                if not word_info["definition"]:
                    raise Exception(f"Word has no definitions")
                self.__make_request("addNote", {
                    "note": {
                        "deckName": deck_name,
                        "modelName": model_name,
                        "fields": {
                            "Word": word,
                            "Word Reading": word_info["kana"],
                            "Word Meaning": word_info["definition"],
                            "Word Furigana": f'{word}[{word_info["kana"]}]'
                        },
                        "options": {
                            "allowDuplicate": False,
                            "duplicateScope": "deck",
                            "duplicateScopeOptions": {
                                "deckName": deck_name,
                                "checkChildren": False,
                                "checkAllModels": False
                            }
                        },
                        "tags": ["jve"]
                    }
                })
            except Exception as e:
                fails.append(word)
                logging.error(f"Failed to add note {word}: {e}")
        logging.info(f"Created {len(words) - len(fails)} words, fails: {fails}")

    def get_deck_names(self):
        if not self.check_connection():
            return []
        return self.__make_request("deckNames")

    def get_filtered_cards(self, deck_id):
        # Step 1: Get all cards in the selected deck
        all_card_ids = self.__make_request("findCards", {
            # https://github.com/FooSoft/anki-connect/issues/80#issuecomment-394154441
            "query": f'"deck:{deck_id}"'
        })

        # Step 2: Fetch card information to filter by status
        card_info_list = self.__make_request("cardsInfo", {"cards": all_card_ids})

        # Step 3: Filter out cards with status 'new' or 'buried'
        filtered_cards = [
            card for card in card_info_list
            if card['type'] not in [CARD_TYPE["new"]]
        ]
        logging.info(f"Found {len(filtered_cards)} cards")
        return filtered_cards

    def select_deck(self):
        if not self.url or not self.check_connection():
            return
        names = self.get_deck_names()
        if len(names) == 0:
            logging.warning("No deck names found")
            return
        decks = questionary.checkbox(
            "Select decks to check for known words",
            choices=names,
        ).ask()
        final_set = set()
        for deck in decks:
            final_set.update(set([x["fields"]["Word"]["value"] for x in self.get_filtered_cards(deck)]))
            print("Selected decks: " + str(decks), len(final_set))
        self.cache = final_set

    def has_word(self, word):
        return word in self.cache
