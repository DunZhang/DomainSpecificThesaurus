import os
import codecs

# you can set your own path
DEFAULT_OUT_DIR = "E:/docs_data1"
from DST.domain_thesaurus.DomainThesaurus import DomainThesaurus
from DST.datasets.DownloadData import DownloadData

if __name__ == "__main__":
    # first, you should get clean domain corpus and clean general corpus. This may take a long time.
    # we already provide clean domain corpus and general vocabulary, so you can download and use them.

    download_data = DownloadData()
    # download the domain corpus
    download_data.download_data(os.path.join(DEFAULT_OUT_DIR, "eng_corpus.zip"), download_file_name="eng_corpus", overwrite=False)
    # download general vocab
    download_data.download_data(os.path.join(DEFAULT_OUT_DIR, "general_vocab.zip"), download_file_name="general_vocab",
                                overwrite=False)
    # since we already get the general vocabulary, we need not to do a phrase detection for general corpus
    # we create a empty file named 'general_corpus_phrase.txt', so the program will skip phrase detection for general corpus
    # !!! Note that: if you want a better performance, you must provide a clean and well-processed corpus
    with codecs.open(filename=os.path.join(DEFAULT_OUT_DIR, "general_corpus_phrase.txt"), mode="w", encoding="utf-8") as fw:
        pass
    # start to extract domain thesaurus
    # for different datasets,  you should set different parameters
    dst = DomainThesaurus(domain_specific_corpus_path=os.path.join(DEFAULT_OUT_DIR, "cleanEng.txt"),
                          general_vocab_path="",
                          outputDir=DEFAULT_OUT_DIR)
    eng_domain_thesaurus = dst.extract()
