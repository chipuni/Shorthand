"""Given a source text in IPA, this code returns the simplified form that
 the shorthand will encode.
"""

import sys

from text_to_ipa import load_dictionary


def main():
    """The main routine, which calls everything else."""
    result = compute(sys.argv[1])

    with open(sys.argv[2], "w") as file:
        file.write("".join(result))


def compute(filename):
    """Convert, character by character, from ipa to shortipa."""
    ipa_to_shortipa = load_dictionary("data/ipa_to_shortipa.csv")
    with open(filename) as file_text:
        text = file_text.read()

    result = ""

    for char in list(text):
        if char in ipa_to_shortipa:
            result += ipa_to_shortipa[char]
        else:
            result += char

    return result


if __name__ == "__main__":
    main()
