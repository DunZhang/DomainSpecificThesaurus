"""
test math
"""
from DST.domain_thesaurus.DomainThesaurus import DomainThesaurus
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
if __name__ == "__main__":
    #
    # cleanMathXml(xmlPath="D:\\Codes\\PythonProj\\MathDict\\data\\Posts.xml", savePath="E:/testMath/clean_math.txt")
    # cwiki = CleanDataWiki(wiki_data_path="D:\\Codes\\PythonProj\\SEDict\\data\\enwiki-latest-pages-articles.xml",
    #                       clean_data_path="E:/testMath/clean_wiki.txt")
    # cwiki.tranform()
    dst = DomainThesaurus(domain_specific_corpus_path="E:/testMath/clean_math.txt",
                          general_corpus_path="",
                          outputDir="E:/testMath",
                          filePaths=None,
                          phrase_detection_domain="default",
                          phrase_detection_general="default",
                          domain_specific_term="default",
                          semantic_related_words="default",
                          word_classification="default",
                          synonym_group="default")
    print(dst.filePaths)
