"""
This file creates, shuffles, and scores mappings from
phonemes to runes.

This will just be a simulated annealing, not a genetic
algorithm, because I'm not sure how to combine two maps
and have them not conflict.
"""

import random


def create_dict(phonemes, runes):
    """
    Make a dict from phonemes to runes. The mapping is random.
    """
    rune_copy = runes.copy()
    random.shuffle(rune_copy)

    return dict(zip(phonemes, rune_copy))


def shuffle_dict(phoneme_rune_dict):
    """
    Update a dict by making a random swap. This creates a new dict
    instead of updating the dict.
    """
    phonemes_1 = list(phoneme_rune_dict.keys())
    phoneme_1 = random.choice(phonemes_1)

    phonemes_2 = list(set(phonemes_1) - set(phoneme_1))
    phoneme_2 = random.choice(phonemes_2)

    next_dict = phoneme_rune_dict.copy()
    (next_dict[phoneme_1], next_dict[phoneme_2]) = (next_dict[phoneme_2], next_dict[phoneme_1])

    return next_dict
