# Japanese Vocabulary Extractor

This script allows you to automatically scan through various types of japanese media and generate a csv with all contained words for studying. Currently supported formats are: 

* Manga (as images)
* Subtitles (ASS/SRT files) from anime, shows or movies
* PDF and EPUB files
* Text (txt) files

It also allows you to automatically add the english definitions of each word to the CSV, as well as furigana if desired.

The resulting CSV can be imported to Anki (if you add the english definitions) or Bunpro.

# Installation

You need to have Python installed on your computer. I recommend using Python 3.12.

To install the Japanese Vocabulary Extractor, follow these steps:

1. Open a terminal or command prompt on your computer.
2. Type the following command and press Enter:
    ```
    pip install japanese-vocabulary-extractor
    ```

This will download and install the necessary files for the tool to work.

# Usage

To use the Japanese Vocabulary Extractor, follow these steps:

1. Open a terminal or command prompt on your computer.
2. Type the following command and press Enter:
    ```
    jpvocab-extractor --type TYPE input_path
    ```

Replace `TYPE` with the type of media you are scanning: 'manga', 'subtitle', 'pdf', 'epub', 'txt' or 'generic'. 

Replace `input_path`:
- For manga, provide a folder containing the images.
- For other types, provide the file or a folder with multiple files. Use quotation marks if the path has spaces.

This will create a `vocab.csv` file with all the words found.

## Options

You can add options to the command to change its behavior. For example:
To add English definitions to the CSV, include the `--add-english` option:
```
jpvocab-extractor --add-english --type TYPE input_path
```

Here is a list of all options:
* --add-english: Looks up and adds the English translation of each word to the CSV file.
* --furigana: Add furigana to all words in the CSV file. Note that this is quite primitive, it just adds the reading of the whole word in hiragana in brackets.
* --id: Replaces each word with its JMDict ID in the CSV file. Incompatible with the --furigana flag.

Here are some manga specific options for handling multiple volumes:
* --parent: Only relevant if processing a manga: provided folder contains multiple volumes. Each folder will be treated as its own volume.
* --separate-vol: Only relevant if processing a manga: each volume will be saved to a separate CSV file.
* --combine-vol: Only relevant if processing a manga and using the --separate-vol flag: all volumes will be combined into a single CSV file with their respective chapter name inserted as "#chapter1" above each section.


Here are all the available options shown together:

```
jpvocab-extractor [-h] [--parent] [--add-english] [--furigana] --type TYPE input_path
```

## Bunpro

The setup you'd want for Bunpro isn't known yet, but I'll put the expected 

Bonus: Using this script with manga will also generate `.mokuro` and `.html` files for each volume, allowing you to read the manga with selectable text in your browser. For more details, visit the mokuro GitHub page linked at the bottom.


# Notices

If you run into errors, look into the mokuro repository linked at the bottom. There might be some issues with python version compatibility.

Also important: This script is not perfect. The text recognition can make mistakes and some of the extracted vocab can be wrong. If this proves to be a big issue I will look for a different method to parse vocabulary from the text. Do not be alarmed by the warning about words with no definition, these are likely names, hallucinations/mistakes by the OCR algorithm or chinese symbols (sometimes found in subtitles).


# TODO

* Better furigana after each kanji instead of just the whole word
* More advanced dictionary lookup functionality
* Support more input formats (Games, VNs, Audio files?) Please suggest any you might want, even the ones listed already!
* Support other output formats
* Improve dictionary result accuracy to include one-character-kana words when translating to english (currently filtered out due to mostly useless answers)


# Acknowledgements

This is hardly my work, I just stringed together some amazing libraries:

* mokuro, to extract lines of text from manga - https://github.com/kha-white/mokuro
* mecab-python3, to tokenize japanese text and extract the dictionary forms - https://github.com/SamuraiT/mecab-python3
* unidic_lite, for data necessary for mecab to work - https://github.com/polm/unidic-lite
* jamdict and jmdict, for the dictionary data - https://github.com/neocl/jamdict, https://www.edrdg.org/jmdict/j_jmdict.html
