"""
class to get semantic related words for terms
"""
import os
import logging

logger = logging.getLogger(__name__)
from gensim.models import Word2Vec, FastText
from gensim.models.word2vec import LineSentence


class SemanticRelatedWord(object):
    def __init__(self, domain_corpus_phrase_path, fasttext_path, skipgram_path, file_overwrite=False,
                 topn_fasttext=8, topn_skipgram=15, min_count=5, size=200, workers=8, window=5
                 ):
        self.domain_corpus_phrase_path = domain_corpus_phrase_path
        self.fasttext_path = fasttext_path
        self.skipgram_path = skipgram_path
        self.file_overwrite = file_overwrite
        self.topn_fasttext = topn_fasttext
        self.topn_skipgram = topn_skipgram
        self.min_count = min_count
        self.size = size
        self.workers = workers
        self.window = window

    def getSemanticRelatedWords(self, terms):
        # get fasttext and skipgram models
        if os.path.exists(self.fasttext_path) and self.file_overwrite == False:  # exist, just load
            logger.warning(self.fasttext_path + " already exists, program will load it.")
            self.fasttext = FastText.load(self.fasttext_path)
        else:  # train
            logger.info("train fasttext")
            if not os.path.exists(os.path.dirname(self.fasttext_path)):
                os.makedirs(os.path.dirname(self.fasttext_path))
                self.fasttext = FastText(sentences=LineSentence(self.domain_corpus_phrase_path),
                                      min_count=self.min_count, size=self.size, sg=1, workers=self.workers,
                                      window=self.window)
            logger.info("save fasttext to local")
            self.fasttext.save(self.fasttext_path)

        if os.path.exists(self.skipgram_path) and self.file_overwrite == False:  # exist, just load
            logger.warning(self.skipgram_path + " already exists, program will load it.")
            self.skipgram = Word2Vec.load(self.skipgram_path)
        else:  # not exist, need to train
            logger.info("train skipgram")
            if not os.path.exists(os.path.dirname(self.skipgram_path)):
                os.makedirs(os.path.dirname(self.skipgram_path))
                self.skipgram = Word2Vec(
                sentences=LineSentence(self.domain_corpus_phrase_path),
                min_count=self.min_count, size=self.size, sg=1, workers=self.workers, window=self.window)
                self.skipgram.delete_temporary_training_data(True)
            logger.info("save skipgram to local")
            self.skipgram.save(self.skipgram_path)
        # get semantic related words
        logger.info("get semantic related words")
        res = {}
        for term in terms:
            res[term] = list(set([i[0] for i in self.fasttext.wv.most_similar(term, topn=self.topn_fasttext)] + \
                                 [i[0] for i in self.skipgram.wv.most_similar(term, topn=self.topn_skipgram)]))
        return res
