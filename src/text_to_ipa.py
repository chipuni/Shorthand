"""Convert English text to (more or less) IPA
This is only a rough conversion, because that's all I need for shorthand."""

import csv
from nltk.stem import WordNetLemmatizer
import re
import sys


def main(filename):
    """The main routine, which calls everything else."""
    word_to_ipa = load_dictionary("../data/word_to_ipa.csv")
    with open(filename) as file:
        text = file.read()
    split_word = list(filter(lambda word: (len(word) > 0 and word.isalpha()), split_by_word(text)))
    split_ipa = list(zip(*[convert_word_to_ipa(word.lower(), word_to_ipa) for word in split_word]))
    split_ipa[0] = split_ipa[0]
    split_ipa[1] = split_ipa[1]
    return split_ipa


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


lemmatizer = WordNetLemmatizer()


def convert_word_to_ipa(word, word_to_ipa):
    """Convert an individual word to its IPA equivalent."""
    if word in word_to_ipa:
        return word_to_ipa[word], ""

    # TODO:
    # 1. Find the word ending that's lost from lemmatization.
    # 2. Convert those word endings to IPA.
    # 3. Add them.

    for pos in ['n', 'v', 'a', 'r', 's']:
        stem = lemmatizer.lemmatize(word, pos=pos)
        if stem in word_to_ipa:
            print(f"Found by stemming (type = {pos}): {word} -> {stem}")
            return word_to_ipa[stem], ""

    print(f"NOT found by stemming: {word}")

    return "", word


if __name__ == "__main__":
    result = main(sys.argv[1])
    unknown_words = sorted(list(set(result[1])))

    print("The words not in the dictionary are:")
    print(unknown_words)
