import pytest
from ..DSUtil import StrSimilarity


def test_similarity():
    assert StrSimilarity("123","1234") == 0.25