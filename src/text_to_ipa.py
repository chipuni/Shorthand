"""Convert English text to (more or less) IPA
This is only a rough conversion, because that's all I need for shorthand."""

import csv
import re
import sys


def main(filename):
    """The main routine, which calls everything else."""
    word_to_ipa = load_dictionary("../data/word_to_ipa.csv")
    with open(filename) as file:
        text = file.read()
    split_word = split_by_word(text)
    split_ipa = [convert_word_to_ipa(word, word_to_ipa) for word in split_word]
    ipa = "".join(split_ipa)
    return ipa


def load_dictionary(filename):
    """Get the word_to_ipa dictionary."""
    word = {}

    with open(filename, newline="") as file:
        dict_reader = csv.reader(file)
        for row in dict_reader:
            word[row[0]] = row[1]

    return word


def split_by_word(text):
    """Split the text by \b."""
    return re.split(r"\b", text)


def convert_word_to_ipa(word, word_to_ipa):
    """Convert an individual word to its IPA equivalent."""
    if word in word_to_ipa:
        return word_to_ipa[word]

    return " "


if __name__ == "__main__":
    print(main(sys.argv[1]))
