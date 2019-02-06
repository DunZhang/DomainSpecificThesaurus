"""
class to detect phrase
"""
import codecs
import gc
import logging
import os

logger = logging.getLogger(__name__)
from gensim.models.phrases import Phrases, Phraser
from gensim.models.word2vec import LineSentence


class TxtIter(object):
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
    class to detect phrase
    using Phrases in gensim
    see more details in https://arxiv.org/abs/1310.4546 and https://svn.spraakdata.gu.se/repos/gerlof/pub/www/Docs/npmi-pfd.pdf
    
    """

    def __init__(self, savePhraserPaths, file_overwrite=False, min_count=10, threshold=15.0,
                 max_vocab_size=40000000, delimiter=b'_', scoring='default', wordNumInPhrase=3):
        """
        :param savePhraserPaths: list, the paths of phrases to save
        :param file_overwrite: str, if the phrase is existing, whether overwrite
        :param min_count: float, optional
            Ignore all words and bigrams with total collected count lower than this value.
        :param threshold: float, optional
            Represent a score threshold for forming the phrases (higher means fewer phrases).
            A phrase of words `a` followed by `b` is accepted if the score of the phrase is greater than threshold.
            Heavily depends on concrete scoring-function, see the `scoring` parameter.
        :param max_vocab_size: int, optional
            Maximum size (number of tokens) of the vocabulary. Used to control pruning of less common words,
            to keep memory under control. The default of 40M needs about 3.6GB of RAM. Increase/decrease
            `max_vocab_size` depending on how much available memory you have.
        :param delimiter:str, optional
            Glue character used to join collocation tokens, should be a byte string (e.g. b'_').
        :param scoring:{'default', 'npmi', function}, optional
            Specify how potential phrases are scored. `scoring` can be set with either a string that refers to a
            built-in scoring function, or with a function with the expected parameter names.
            Two built-in scoring functions are available by setting `scoring` to a string:

            #. "default" - :func:`~gensim.models.phrases.original_scorer`.
            #. "npmi" - :func:`~gensim.models.phrases.npmi_scorer`.
        :param wordNumInPhrase: word number in a phrase, Note that `wordNumInPhrase-1` must be equal to length of savePhraserPaths
        """
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
        """
        train phrases
        :param sentencesPath:the path of text file, the text file should be the format: one line one sentence
        """
        self.phrasers = []
        # path detect
        for path in self.savePhraserPaths:
            if not os.path.exists(os.path.dirname(path)):
                raise FileNotFoundError(os.path.dirname(path)+" not exist")
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
        """
        use trained phrases to transform sentences
        :param sentencesPath: the path of text file, the text file should be the format: one line one sentence
        :param savePath: the path of transformed text file, the text file are the format: one line one sentence
        """
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
