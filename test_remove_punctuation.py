import pytest
import sys
import os


from Website_python import remove_punctuation

class TestClass:
    def test_one(self):
        assert remove_punctuation("hello world") == "hello world"

    def test_two(self):
        assert remove_punctuation("hello%world") == "hello world"

    def test_three(self):
        assert remove_punctuation("!hello world") == " hello world"

    def test_four(self):
        assert remove_punctuation(";hello?world!") == " hello world "

    def test_five(self):
        assert remove_punctuation("hello;world") == "hello world"

    def test_six(self):
        assert remove_punctuation("hello world?") == "hello world "


