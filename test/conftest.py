import pytest as pt

from pylox import Lox


@pt.fixture
def lox():
    interpreter = Lox()
    yield interpreter
    del interpreter
