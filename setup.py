from setuptools import setup, find_packages

setup(
    name="japanese-vocabulary-extractor",
    version="1.4.4",
    description="A utility to extract vocabulary lists from manga.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Fluttrr",
    author_email="ySZ39@proton.me",
    url="https://github.com/Fluttrr/japanese-vocabulary-extractor",
    license="GLPv3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "regex",
        "mokuro",
        "mecab-python3",
        "unidic-lite",
        "pypdf",
        "ebooklib",
        "tqdm",
        "jamdict",
        "jamdict-data-fix",
        "colorlog",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "jpvocab-extractor=sample:main",
        ],
    },
)
