import logging


class BunproWrapper:
    def __init__(self, filename):
        self.filename = filename
        self.cache = set()
        self.populate()

    def is_ready(self):
        return bool(self.filename)

    def populate(self):
        if not self.is_ready():
            return
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                words_set = {line.strip() for line in file if line.strip()}
            self.cache = words_set
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        logging.info(f"Bunpro cache size: {len(self.cache)}")

    def has_word(self, word):
        return word in self.cache
