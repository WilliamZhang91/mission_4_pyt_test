import pytest

def remove_punctuation(word):
    for x in word:
        if ((ord(x) >= 33 and ord(x) <= 47) or (ord(x) >= 58 and ord(x) <= 64) or (ord(x) >= 91 and ord(x) <= 96) or (ord(x) >= 123 and ord(x) <= 127)):
            word = word.replace(x," ")
    return word



