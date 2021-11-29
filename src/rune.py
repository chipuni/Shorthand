"""
This class holds the graphic symbols that represent phonemes.
"""

from enum import Enum
import sys


class Slope(Enum):
    """
    The slope of a curve: how steep it is.
    """
    STEEP_UP = 3
    UP = 2
    SHALLOW_UP = 1
    FLAT = 0
    SHALLOW_DOWN = -1
    DOWN = -2
    STEEP_DOWN = -3


steepen_map = {Slope.STEEP_UP: Slope.STEEP_UP,
               Slope.UP: Slope.STEEP_UP,
               Slope.SHALLOW_UP: Slope.UP,
               Slope.FLAT: Slope.SHALLOW_UP,
               Slope.SHALLOW_DOWN: Slope.FLAT,
               Slope.DOWN: Slope.SHALLOW_DOWN,
               Slope.STEEP_DOWN: Slope.DOWN}


def steepen(self):
    """
    Give the next-steepest slope.
    """
    return steepen_map[self]


shallower_map = {Slope.STEEP_DOWN: Slope.STEEP_DOWN,
                 Slope.DOWN: Slope.STEEP_DOWN,
                 Slope.SHALLOW_DOWN: Slope.DOWN,
                 Slope.FLAT: Slope.SHALLOW_DOWN,
                 Slope.SHALLOW_UP: Slope.FLAT,
                 Slope.UP: Slope.SHALLOW_UP,
                 Slope.STEEP_UP: Slope.UP}


def shallower(self):
    """
    Give the less-steep slope.

    Not quite an inverse of steeper, because there's a maximum and minimum steepness.
    """
    return shallower_map[self]


class Curve(Enum):
    """
    Whether the line curves, and in which direction.
    """
    UP = 1
    FLAT = 0
    DOWN = -1


class Length(Enum):
    """
    Whether this line is short or long.
    """
    SHORT = 0
    LONG = 1


class Rune:
    """
    One character or phoneme written down.
    """
    def __init__(self, initial_loop, slope, curve, length, final_loop):
        # pylint: disable=too-many-arguments
        self.initial_loop = initial_loop
        self.slope = slope
        self.curve = curve
        self.length = length
        self.final_loop = final_loop

    def opening_slope(self):
        """
        What is the slope at the beginning of the rune?

        If the previous closing == the current opening,
        (and there isn't a final loop in the previous or an
        opening loop in this one), then
        we might need to make a jag to show that there are two characters.
        """
        if self.curve == Curve.UP:
            return steepen(self.slope)
        if self.curve == Curve.FLAT:
            return self.slope
        if self.curve == Curve.DOWN:
            return shallower(self.slope)

        print("Unknown curve!")
        sys.exit(-1)

    def closing_slope(self):
        """
        What is the slope at the end of this rune?
        """
        if self.curve == Curve.UP:
            return shallower(self.slope)
        if self.curve == Curve.FLAT:
            return self.slope
        if self.curve == Curve.DOWN:
            return steepen(self.slope)

        print("Unknown curve!")
        sys.exit(-1)


all_runes = [Rune(initial_loop, slope, curve, length, final_loop)
             for initial_loop in ([False, True])
             for slope in ([Slope.DOWN, Slope.FLAT, Slope.UP])
             for curve in ([Curve.UP, Curve.FLAT, Curve.DOWN])
             for length in ([Length.LONG, Length.SHORT])
             for final_loop in ([False, True])]
