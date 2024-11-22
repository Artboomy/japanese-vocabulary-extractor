# Japanese Vocabulary Extractor

This script allows you to automatically scan through various types of japanese media and generate a csv with all contained words for studying. Currently supported formats are: 

* Manga (as images)
* Subtitles (ASS/SRT files) from anime, shows or movies
* PDF and EPUB files
* Text (txt) files

It also allows you to automatically add the english definitions of each word to the CSV.

The resulting CSV can be imported to Anki (if you add the english definitions) or Bunpro. If you wish to add furigana to your anki deck, use this addon: https://ankiweb.net/shared/info/678316993

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

To add English definitions to the CSV, include the `--add-english` option:
```
jpvocab-extractor --add-english --type TYPE input_path
```

For manga only: If you have a parent folder with multiple volumes in separate folders, add `--parent` before the type:
```
jpvocab-extractor --parent --type manga input_path
```

Bonus: Using this script with manga will also generate `.mokuro` and `.html` files for each volume, allowing you to read the manga with selectable text in your browser. For more details, visit the mokuro GitHub page linked at the bottom.


# Notices

If you run into errors, look into the mokuro repository linked at the bottom. There might be some issues with python version compatibility.

Also important: This script is not perfect. The text recognition can make mistakes and some of the extracted vocab can be wrong. If this proves to be a big issue I will look for a different method to parse vocabulary from the text. Do not be alarmed by the warning about words with no definition, these are likely names, hallucinations/mistakes by the OCR algorithm or chinese symbols (sometimes found in subtitles).


# TODO

* Separate outputs for each volume
* More advanced dictionary lookup functionality
* Support more input formats (Games, VNs?) Please suggest any you might want!
* Support other output formats


# Acknowledgements

This is hardly my work, I just stringed together some amazing libraries:

* mokuro, to extract lines of text from manga - https://github.com/kha-white/mokuro
* mecab-python3, to tokenize japanese text and extract the dictionary forms - https://github.com/SamuraiT/mecab-python3
* unidic_lite, for data necessary for mecab to work - https://github.com/polm/unidic-lite
* jamdict and jmdict, for the dictionary data - https://github.com/neocl/jamdict, https://www.edrdg.org/jmdict/j_jmdict.html
