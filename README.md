# Manga Wordlist Extractor

This script allows you to automatically scan through manga and generate a csv with all contained words.

It is intended to be used with the community deck feature of Bunpro, hence the csv format. Once the csv import feature will be published, I will adjust the format of the csv. If any other outputs are desired, let me know!


# Installation

You need to have python installed (ideally Python 3.12).

## Using pip

Install the package using
```
pip install manga-wordlist-extractor
```

## Using the source code directly

Download this repository (using the "code -> download zip" option above the files list at the top). Open a command prompt in the downloaded folder after extracting. 

Run this to install all dependencies:

```
pip install -r requirements.txt
```

You can now run the tool from the src/main/main.py file.


# Usage

```
manga-wordlist-extractor "FOLDER_PATH"
```

Replace FOLDER_PATH with the path containing the manga files. If you enter a parent folder containing multiple volumes, add "--parent" before the folder path.

This will generate a vocab.csv file containing all words.


# Notices

If you run into errors, look into the mokuro repository linked at the bottom. There might be some issues with python version compatibility.

Also important: This script is not perfect. The text recognition can make mistakes and some of the extracted vocab can be wrong. If this proves to be a big issue I will look for a different method to parse vocabulary from the text.


# TODO

* Upload to PyPi and make usage much easier and simpler
* Live Output from Mokuro (it can take very long)
* Separate outputs for each volume
* Added translations through dictionary lookup?


# Acknowledgements

This is hardly my work, I just stringed together some amazing libraries:

* mokuro, to extract lines of text from manga - https://github.com/kha-white/mokuro
* nagisa, to extract words from those lines of text - https://pypi.org/project/nagisa/

