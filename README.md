# Japanese Vocabulary Extractor

This script allows you to automatically scan through various types of japanese media and generate a CSV with all contained words for studying. Currently supported formats are: 

* Manga (as images)
* Subtitles (ASS/SRT files) from anime, shows or movies
* PDF and EPUB files
* Text (txt) files

It allows you to automatically add the english definitions of each word to the CSV, as well as furigana if desired. It also allows creating individual CSVs for each file/volume and creates another large CSV with all vocab divided by file/volume (useful for Bunpro Units).

The resulting CSV can be imported to Anki or Bunpro. 

*You may of course **share/upload** any lists created with this tool, but please leave a link to this repository whenever you do so other people can use it as well!*

# Installation

You need to have Python installed on your computer. I recommend using Python 3.12 (Make sure to tick the "Add Python to PATH" checkbox during the installation).
I encountered errors during the installation on Windows with Python 3.13 so in that case, try Python 3.12.

To install the Japanese Vocabulary Extractor, follow these steps:

1. Open a terminal or command prompt on your computer.
2. Type the following command and press Enter:
    ```
    pip install japanese-vocabulary-extractor
    ```

This will download and install the necessary files for the tool to work.

**NOTICE**: There is currently a bug within the dependencies that you might encounter when processing manga. If you get an error saying `AttributeError: module 'numpy' has no attribute 'bool8'. Did you mean: 'bool'?`, run this command to downgrade numpy: `pip install numpy==1.26.4`. 

## Updating

To update, run the following command:
    ```
    pip install --upgrade japanese-vocabulary-extractor
    ``` 

# Before you start
## Clean up your source
Manga may contain some texts about publication, preface text or anything else you may not be interested in.
It is suggested to delete pages with this info or put black bars over, so extracted vocab will be smaller.

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

This will create a `vocab_all.csv` file with all the words found.

## Options

You can add options to the command to change its behavior. For example:
To add English definitions to the CSV, include the `--add-english` option:
```
jpvocab-extractor --add-english --type TYPE input_path
```

Here is a list of all options:
* `--add-english`: Looks up and adds the English translation of each word to the CSV file.
* `--furigana`: Add furigana to all words in the CSV file. Note that this is quite primitive, it just adds the reading of the whole word in hiragana in brackets.
* `--id`: Replaces each word with its JMDict ID in the CSV file. Incompatible with the `--furigana` flag.
* `--separate`: Each volume/file will be saved to a separate CSV file. This also creates one big combined `vocab_combined.csv` file with all vocab for each file/chapter in its own section, with duplicates removed. Make sure the folders are alphabetically sorted for a correct section order! Requires `--parent` for manga.
* `--freq-order`: Vocab will not be stored in order of appearance but in order of frequency in the given source material.

There is one option only used for manga:
* `--parent`: Only relevant if processing a manga: provided folder contains multiple volumes. Each folder will be treated as its own volume.

## Bunpro

This command for manga will work best for Bunpro:

```
jpvocab-extractor --parent --separate --id --type manga input_path
```

`--parent` marks that the folder contains other folders containing volumes.
`--separate` creates a separate CSV file for each volume, and then combines them into a neat sectioned combined CSV file. This basically automatically creates Units in Bunpro for each volume.
`--id` replaces each word with its JMDict ID, making importing much more consistent.

For general creation of decks for media other than manga, you would only add the `--separate` and `--id` flag:

```
jpvocab-extractor --separate --id --type TYPE input_path
```

This will separate all vocab into sections for each file within the CSV. If you do not have multiple files or the need for sections in your deck, leave out `--separate`.

**Tip***: Rename the files or volume folders you are turning into units to the exact name you want for the Unit on Bunpro. This will make sure the unit has exactly that name after the import and you don't need to edit them. Use a renaming utility to batch-rename the files if doing it manually is too tedious.

## Mokuro files

Bonus: Using this script with manga will also generate `.mokuro` and `.html` files for each volume, allowing you to read the manga with selectable text in your browser. For more details, visit the mokuro GitHub page linked at the bottom.


# Notices/Limitations

I think the biggest issue currently is quality of source material. If you have an ebook with 5 pages of random stuff about the authors at the beginning, your vocabulary list is going to be filled with useless words in the beginning. I often found subtitles that contain furigana after the kanji and the program occasionally came up with silly matches for those too. So if you want a consistent, good result, clean up your input as much as you can.

If you run into errors, look into the mokuro repository linked at the bottom. There might be some issues with python version compatibility.

Also important: This script is not perfect. The text recognition can make mistakes and some of the extracted vocab can be wrong. If this proves to be a big issue I will look for a different method to parse vocabulary from the text. Do not be alarmed by the warning about words with no definition, these are likely names, hallucinations/mistakes by the OCR algorithm or chinese symbols (sometimes found in subtitles).


# TODO

* Better furigana (after each kanji instead of just the whole word)
* More advanced dictionary lookup functionality
* Support more input formats (Games, VNs, Audio files?) Please suggest any you might want, even the ones listed already!
* Support other output formats
* Improve dictionary result accuracy to include one-character-kana words when translating to english (currently filtered out due to mostly useless answers)

# Development

1. Install python
2. Install Rust - required to build some packages `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
3. Install `sudo apt-get install pkg-config libssl-dev`
4. If using Windows - install [WSL](https://learn.microsoft.com/en-us/windows/wsl/install). Nagisa [does not work](https://github.com/taishi-i/nagisa/issues/24) with latest Python on Windows
5. Create venv - `python3 -m venv .venv` and activate it - `source ./venv/bin/activate`
6. Install dependencies - `pip install -r requirements.txt`
7. Sample command - `cd src && python3 -m sample --type manga "./input/manga" --wk-key <your api key> --freq-order --furigana --add-english --bunpro-words "./input/bunpro.txt"`

python3 -m sample 
    --type manga 
    "./input/manga" 
    --wk-key <your api key> 
    --freq-order --furigana --add-english --bunpro-words "./input/bunpro.txt"

# Acknowledgements

This is hardly my work, I just stringed together some amazing libraries:

* mokuro, to extract lines of text from manga - https://github.com/kha-white/mokuro
* ginza, to tokenize japanese text and extract the dictionary forms - https://github.com/megagonlabs/ginza
* unidic_lite, for data necessary for mokuro to work - https://github.com/polm/unidic-lite
* jamdict and jmdict, for the dictionary data - https://github.com/neocl/jamdict, https://www.edrdg.org/jmdict/j_jmdict.html

# Support me

If you find this program helpful and would like to support what I'm doing, feel free to buy me a coffee (or tea, i prefer tea...) on kofi! https://ko-fi.com/fluttr
