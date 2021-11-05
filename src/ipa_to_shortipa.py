# Given a source text in IPA, this code returns the simplified form that the shorthand
# will encode.

from text_to_ipa import load_dictionary
import sys

# TODO: REDO THE VOWELS IN ipa_to_shortipa so that each vowel represents a region
# (even if only vertically), so they make more sense than accident!


def main(filename):
    ipa_to_shortipa = load_dictionary("data/ipa_to_shortipa.csv")
    with open(filename) as fileText:
        text = fileText.read()

    return filename


if __name__ == "__main__":
    result = main(sys.argv[1])
