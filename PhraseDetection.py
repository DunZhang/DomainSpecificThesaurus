"""
class to detect phrase
just simplely package existing algorithms
"""
import codecs
from gensim.models.phrases import Phrases, Phraser
from gensim.models.word2vec import LineSentence


class TxtIter(object):
    """
    step1.2.2短语迭代器，bigram若为None，就是不经处理直接迭代
    """

    def __init__(self, sentences, ngrams):
        self.ngrams = ngrams
        self.sentences = sentences
        pass

    def __iter__(self):
        if len(self.ngrams) == 0:
            for line in self.sentences:
                yield line.split()
        else:
            for line in self.sentences:
                line = self.ngrams[0][line.split()]
                for gram in self.ngrams[1:]:
                    line = gram[line]
                yield line


class PhraseDetection(object):
    """
    setences to senteces with phrase, use gensim
    
    """

    def __init__(self, savePhraserPaths, min_count=10, threshold=15.0,
                 max_vocab_size=40000000, delimiter=b'_', scoring='default', wordNumInPhrase=3):
        self.ngrams = []
        self.savePhraserPaths = savePhraserPaths
        self.min_count = min_count
        self.threshold = threshold
        self.max_vocab_size = max_vocab_size
        self.delimiter = delimiter
        self.scoring = scoring
        self.wordNumInPhrase = wordNumInPhrase

    def fit(self, sentencesPath):
        for path in self.savePhraserPaths:
            phrase = Phrases(sentences=TxtIter(sentences=LineSentence(sentencesPath), ngrams=self.ngrams),
                             min_count=self.min_count, hreshold=self.threshold, max_vocab_size=self.max_vocab_size,
                             delimiter=self.delimiter, scoring=self.scoring)
            phrase.save(path)
            phraser = Phraser(phrase)
            self.ngrams.append(phraser)

    def transform(self, sentencesPath, savePath):
        with codecs.open(savePath, mode="w", encoding="utf-8") as fr:
            sentences = TxtIter(sentences=LineSentence(sentencesPath), ngrams=self.ngrams)
            lines = []
            for line in sentences:
                lines.append(line + "\n")
                if len(lines) > 500000:
                    fr.writelines(lines)
                    lines = []
            fr.writelines(lines)


if __name__ == "__main__":
    ls = LineSentence("E:/a.txt")
    for i in ls:
        print(i)
