"""
class to get semantic related words for terms
"""
import os
import logging

logger = logging.getLogger(__name__)
from gensim.models import Word2Vec, FastText
from gensim.models.word2vec import LineSentence


class SemanticRelatedWord(object):
    """
    class to get semantic related words for terms.
    This class use word2vec and fasttext.
    """

    def __init__(self, domain_corpus_phrase_path, fasttext_path, skipgram_path, file_overwrite=False,
                 topn_fasttext=8, topn_skipgram=15, similarity_threshold_fasttext=0.8,
                 similarity_threshold_skipgram=0.78, min_count=5, size=200, workers=8, window=5
                 ):
        """
        :param domain_corpus_phrase_path: str, path of domain corpus
        :param fasttext_path: str, the path of fasttext to be saved or the path of existing fasttext model
        :param skipgram_path: tstr, he path of skipgram to be saved or the path of existing skipgram model
        :param file_overwrite: str, if the fasttext or skipgram is already existing, whether re-train
        :param topn_fasttext: int, optional,the number of most similar words chosen by fasttext
        :param topn_skipgram: int, optional, the number of most similar words chosen by fasttext
        :param min_count: int, optional
            The model ignores all words with total frequency lower than this.
        :param size: int, optional
            Dimensionality of the word vectors.
        :param workers: int, optional
            Use these many worker threads to train the model (=faster training with multicore machines).
        :param window: int, optional
            The maximum distance between the current and predicted word within a sentence.
        """
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
        self.similarity_threshold_fasttext = similarity_threshold_fasttext
        self.similarity_threshold_skipgram = similarity_threshold_skipgram

    def getSemanticRelatedWords(self, terms):
        """
        get semantic related words
        :param terms: list, collections of terms
        :return: dict, key is term, value is the SemanticRelatedWords of this term, stored in a list
        """
        # get fasttext and skipgram models
        if os.path.exists(self.fasttext_path) and self.file_overwrite == False:  # exist, just load
            logger.warning(self.fasttext_path + " already exists, program will load it.")
            self.fasttext = FastText.load(self.fasttext_path)
        else:  # train
            logger.info("train fasttext...")
            if not os.path.exists(os.path.dirname(self.fasttext_path)):
                os.makedirs(os.path.dirname(self.fasttext_path))
            self.fasttext = FastText(sentences=LineSentence(self.domain_corpus_phrase_path),
                                     min_count=self.min_count, size=self.size, sg=1, workers=self.workers,
                                     window=self.window)
            logger.info("save fasttext to local...")
            self.fasttext.save(self.fasttext_path)

        if os.path.exists(self.skipgram_path) and self.file_overwrite == False:  # exist, just load
            logger.warning(self.skipgram_path + " already exists, program will load it.")
            self.skipgram = Word2Vec.load(self.skipgram_path)
        else:  # not exist, need to train
            logger.info("train skipgram...")
            if not os.path.exists(os.path.dirname(self.skipgram_path)):
                os.makedirs(os.path.dirname(self.skipgram_path))
            self.skipgram = Word2Vec(
                sentences=LineSentence(self.domain_corpus_phrase_path),
                min_count=self.min_count, size=self.size, sg=1, workers=self.workers, window=self.window)
            self.skipgram.delete_temporary_training_data(True)
            logger.info("save skipgram to local...")
            self.skipgram.save(self.skipgram_path)
        # get semantic related words
        res = {}
        for term in terms:
            words_fasttext = self.fasttext.wv.most_similar(term, topn=self.topn_fasttext)
            words_skipgram = self.skipgram.wv.most_similar(term, topn=self.topn_skipgram)
            words1, words2 = [], []
            for i in words_fasttext:
                if i[1] < self.similarity_threshold_fasttext:
                    break
                words1.append(i[0])
            for i in words_skipgram:
                if i[1] < self.similarity_threshold_skipgram:
                    break
                words2.append(i[0])
            res[term] = list(set(words1 + words2))
        return res
