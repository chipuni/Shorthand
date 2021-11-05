"""Convert English text to (more or less) IPA
This is only a rough conversion, because that's all I need for shorthand."""

# To do:
# Create a test framework. Include contractions, "getting", and "traditionally".

# Not needed for this project:
# 1. Final "s" pronunciation depends on whether the previous letter was voiced or unvoiced.

import csv
import re
import sys

from nltk.stem import WordNetLemmatizer


def main(filename):
    """The main routine, which calls everything else."""
    word_to_ipa = load_dictionary("data/word_to_ipa.csv")
    suffix_to_ipa = load_dictionary("data/suffix_to_ipa.csv")
    with open(filename) as fileText:
        text = fileText.read()

    split_word = list(
        filter(lambda word: (len(word) > 0 and word.isalpha()), split_by_word(text))
    )
    split_ipa = list(
        zip(
            *[
                convert_word_to_ipa(word.lower(), word_to_ipa, suffix_to_ipa)
                for word in split_word
            ]
        )
    )
    return split_ipa


def load_dictionary(filename):
    """Get a dictionary from a file."""
    word = {}

    with open(filename, newline="") as fileDict:
        dict_reader = csv.reader(fileDict)
        for row in dict_reader:
            word[row[0]] = row[1]

    return word


def split_by_word(text):
    """Split the text by \b."""
    return re.split(r"[^a-zA-Z0-9_']", text)


lemmatizer = WordNetLemmatizer()


def convert_word_to_ipa(word, word_to_ipa, suffix_to_ipa):
    """Convert an individual word to its IPA equivalent."""
    if word in word_to_ipa:
        return word_to_ipa[word], "", ""

    lemma = lemmatize(word)
    if lemma in word_to_ipa:
        # Find how long there are letters in common; everything after is the suffix.
        for triple in zip(word, lemma, range(len(word))):
            first_not_matching = triple[2]
            if triple[0] != triple[1]:
                break
        if word[first_not_matching] == lemma[first_not_matching]:
            first_not_matching += 1

        suffix = word[first_not_matching:]

        # Handle suffixes that don't double their letters, for example traditionally
        if lemma[-1] == suffix[0] and suffix in suffix_to_ipa:
            return word_to_ipa[lemma] + suffix_to_ipa[suffix][1:], "", ""

        # Handle suffixes that double their letters, for example getting
        if lemma[-1] == suffix[0] and suffix[1:] in suffix_to_ipa:
            return word_to_ipa[lemma] + suffix_to_ipa[suffix[1:]], "", ""

        if suffix in suffix_to_ipa:
            return word_to_ipa[lemma] + suffix_to_ipa[suffix], "", ""

        return "", "", f"{suffix} ({word}, {lemma})"

    print(f"NOT found by stemming: {word}")
    return "", word, ""


def lemmatize(word):
    "Turns a word into its lemma. Necessary since NLTK doesn't handle ly."
    for pos in ["n", "v", "a", "r", "s"]:
        lemma = lemmatizer.lemmatize(word, pos=pos)
        if lemma != word:
            return lemma

    # lemmatizer has problems with "ly" words.
    if word.endswith("ly"):
        return word[:-2]

    return word


if __name__ == "__main__":
    result = main(sys.argv[1])

    with open(sys.argv[1], "w") as file:
        file.write(result[0])

    print("The words not in the dictionary are:")
    unknown_words = sorted(list(set(result[1])))
    print(unknown_words)

    print("The suffixes not in the dictionary are:")
    unknown_suffixes = sorted(list(set(result[2])))
    print(unknown_suffixes)
