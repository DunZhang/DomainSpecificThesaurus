"""
test math
"""
from DST.domain_thesaurus.DomainThesaurus import DomainThesaurus
from DST.datasets.CleanData import cleanEngXml, CleanDataWiki
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
if __name__ == "__main__":
    # cleanEngXml(xmlPath="D:\\Codes\\PythonProj\\EngDict\\data\\Posts.xml", savePath="E:/testEng/clean_eng.txt")
    # cwiki = CleanDataWiki(wiki_data_path="D:\\Codes\\PythonProj\\SEDict\\data\\enwiki-latest-pages-articles.xml",
    #                       clean_data_path="E:/testMath/clean_wiki.txt")
    # cwiki.tranform()
    dst = DomainThesaurus(domain_specific_corpus_path="your domain specific corpus path",
                          general_corpus_path="your general corpus path",
                          outputDir="path of output",
                          filePaths=None,
                          phrase_detection_domain="default",
                          phrase_detection_general="default",
                          domain_specific_term="default",
                          semantic_related_words="default",
                          word_classification="default",
                          synonym_group="default")
    # extract domain thesauruss
    dst.extract()
