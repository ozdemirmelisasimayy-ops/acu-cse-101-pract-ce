"""Checks for the three Week 03 graded challenges.

Call each function with several arguments to check that it uses its parameters.
"""

import pytest

from exercises.week_03_functions.challenge import greet, minutes_to_seconds, square


@pytest.mark.parametrize("name", ["Ada", "Deniz", "Grace Hopper"])
def test_greet(name):
    assert greet(name) == f"Hello, {name}!", "Return the greeting, including punctuation."


@pytest.mark.parametrize("number, expected", [(4, 16), (7, 49), (0, 0), (-3, 9)])
def test_square(number, expected):
    assert square(number) == expected, "Return the number multiplied by itself."


@pytest.mark.parametrize("minutes, expected", [(2, 120), (5, 300), (0, 0), (1.5, 90)])
def test_minutes_to_seconds(minutes, expected):
    assert minutes_to_seconds(minutes) == expected, "Return the duration in seconds."
