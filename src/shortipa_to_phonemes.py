"""Given a file in shortipa, this program chooses and creates a specific
   number of phonemes (which will correspond to individual characters in
   the shorthand). It outputs
      - the conversion from phonemed shortipa to shortipa

The inputs are:
  - Whatever file you want to add phonemes to
  - The maximum number of phonemes
  - An output filename, that holds the maps of characters to phonemes
  - An output filename, that holds the words and their counts
"""

import sys


def main():
    """The main function, which handles everything else."""
    result = compute(sys.argv[1], int(sys.argv[2]))

    with open(sys.argv[3], "w") as file:
        map_char_phoneme = result[0]

        for new_char, phoneme in map_char_phoneme.items():
            file.write(f'"{new_char}","{phoneme}"\n')

    with open(sys.argv[4], "w") as file:
        map_word_frequency = result[1]

        for word, frequency in map_word_frequency.items():
            file.write(f'"{word}",{frequency}\n')


def compute(filename, max_phonemes):
    """Read the text file, perform all computations."""
    # Read the text file.
    with open(filename, "r") as file_text:
        text = file_text.read()

    # Get the map of words to count (to speed up all future calculations)
    count_words = get_count_words(text)

    # Count the number of characters already used
    count_phonemes = count_the_letters(count_words)

    # Using the arrows as new letters, because they print well.
    next_phoneme = "\u2190"
    phonemes = {}

    # While the number of characters is less than the number we want:
    while count_phonemes < max_phonemes:
        # Find the pair of characters that appears the most in the map
        most_common_pair = find_most_common_pair(count_words)

        # Add that pair to the list of phonemes
        phonemes[next_phoneme] = most_common_pair

        # Change the map, so that it's using the new phoneme.
        count_words = substitute(count_words, most_common_pair, next_phoneme)

        # (Also update the phonemes)
        next_phoneme = chr(ord(next_phoneme) + 1)
        count_phonemes += 1

    # Return the map of characters to phonemes and the count of words
    # (using the new phonemes).
    return phonemes, count_words


def count_the_letters(count_words):
    """Find the number of distinct letters."""
    letters = {}
    for word in count_words.keys():
        for letter in word:
            letters.setdefault(letter, 0)
            letters[letter] += count_words[word]

    return len(letters.keys())


def get_count_words(text):
    """Converts from a text to a dict of words -> their count."""
    count_words = {}
    for line in text.splitlines():
        for word in line.split():
            count_words.setdefault(word, 0)
            count_words[word] += 1

    return count_words


def find_most_common_pair(count_words):
    """Look for the most common pair of characters in a count_words."""
    pairs = {}

    for word in count_words.keys():
        for pos in range(len(word) - 1):
            pair = word[pos:pos + 2]

            pairs.setdefault(pair, 0)
            pairs[pair] += count_words[word]

    most_common = max(pairs, key=pairs.get)
    print(
        f"Most common pair is {most_common}, with count {pairs[most_common]}"
    )
    return most_common


def substitute(count_words, original, revised):
    """Create a dictionary that substitutes original -> revised."""
    print(f"Substituting: '{revised}' for '{original}'")

    new_dict = {}

    for key in count_words.keys():
        if original in key:
            revised_key = key.replace(original, revised)
            if revised_key in count_words:
                new_dict[revised_key] = count_words[revised_key]
            else:
                new_dict[revised_key] = 0

            new_dict[revised_key] += count_words[key]
        else:
            new_dict[key] = count_words[key]

    return new_dict


if __name__ == "__main__":
    main()
