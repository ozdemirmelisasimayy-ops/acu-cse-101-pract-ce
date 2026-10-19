"""Checks for the Week 03 guided workshop."""

import pytest

from exercises.week_03_functions.practice import add, double, say_welcome


def test_say_welcome(capsys):
    say_welcome()
    assert capsys.readouterr().out.strip() == "Welcome to Python!"


@pytest.mark.parametrize("number, expected", [(4, 8), (7, 14), (0, 0)])
def test_double(number, expected):
    assert double(number) == expected, "Return twice the supplied number."


@pytest.mark.parametrize("first, second, expected", [(3, 5, 8), (10, 2, 12), (0, 4, 4)])
def test_add(first, second, expected):
    assert add(first, second) == expected, "Return the sum of both parameters."
