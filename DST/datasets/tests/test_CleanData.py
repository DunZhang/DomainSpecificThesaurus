import pytest
from os.path import dirname
import sys
sys.path.append(dirname(dirname(__file__)))
from CleanData import CleanDataWiki


def test_wrong_wiki_path():
    cdw = CleanDataWiki("","")
    cdw.tranform()