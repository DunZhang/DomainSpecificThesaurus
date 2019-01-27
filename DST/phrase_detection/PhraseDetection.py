"""
class to detect phrase
just simplely package existing algorithms
"""
import codecs
import gc
import logging
import os

logger = logging.getLogger(__name__)
from gensim.models.phrases import Phrases, Phraser
from gensim.models.word2vec import LineSentence


class TxtIter(object):
    """
    step1.2.2短语迭代器，bigram若为None，就是不经处理直接迭代
    """

    def __init__(self, sentences, ngrams):
        self.ngrams = ngrams
        self.sentences = sentences

    def __iter__(self):
        if len(self.ngrams) == 0:
            for line in self.sentences:
                yield line.split()
            self.sentences.close()
        else:
            for line in self.sentences:
                line = self.ngrams[0][line.split()]
                for gram in self.ngrams[1:]:
                    line = gram[line]
                yield line
            self.sentences.close()


class PhraseDetection(object):
    """
    setences to senteces with phrase, use gensim
    
    """

    def __init__(self, savePhraserPaths, file_overwrite=False, min_count=10, threshold=15.0,
                 max_vocab_size=40000000, delimiter=b'_', scoring='default', wordNumInPhrase=3):
        self.phrasers = []
        self.savePhraserPaths = savePhraserPaths
        self.file_overwrite = file_overwrite
        self.min_count = min_count
        self.threshold = threshold
        self.max_vocab_size = max_vocab_size
        self.delimiter = delimiter
        self.scoring = scoring
        self.wordNumInPhrase = wordNumInPhrase

    def fit(self, sentencesPath):
        self.phrasers = []
        for path in self.savePhraserPaths:
            if not os.path.exists(path):  # need train
                self.phrasers = None
                break
        if self.phrasers is not None and self.file_overwrite == False:
            logging.info("models are already exist, will read it")
            for path in self.savePhraserPaths:
                self.phrasers.append(Phraser(Phrases.load(path)))
            return True
        self.phrasers = []
        c = 2
        for path in self.savePhraserPaths:
            logging.info("get %d-gram phrase" % c)
            c += 1
            phrase = Phrases(
                sentences=TxtIter(sentences=codecs.open(sentencesPath, mode="r", encoding="utf-8"),
                                  ngrams=self.phrasers),
                min_count=self.min_count, threshold=self.threshold, max_vocab_size=self.max_vocab_size,
                delimiter=self.delimiter, scoring=self.scoring)
            phrase.save(path)
            phraser = Phraser(phrase)
            self.phrasers.append(phraser)
            del phrase

    def transform(self, sentencesPath, savePath):
        with codecs.open(savePath, mode="w", encoding="utf-8") as fr:
            sentences = TxtIter(sentences=codecs.open(sentencesPath, mode="r", encoding="utf-8"), ngrams=self.phrasers)
            lines = []
            for line in sentences:
                lines.append(" ".join(line) + "\n")
                if len(lines) > 500000:
                    fr.writelines(lines)
                    lines = []
            fr.writelines(lines)
        logger.info("delete all phraser")
        for i in self.phrasers:
            del i
        del self.phrasers
        self.phrasers = None
        gc.collect()


if __name__ == "__main__":
    ls = LineSentence("E:/a.txt")
    for i in ls:
        print(i)
