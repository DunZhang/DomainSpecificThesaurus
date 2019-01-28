"""
class to extract domain-specific terms
for examples, 'JavaScript' in CS and 'limit' in math
"""
import logging

logger = logging.getLogger(__name__)


class DomainTerm(object):
    """
    class to extract domain-specific terms
    """

    def __init__(self, maxTermsCount=300000, thresholdScore=10.0, termFreqRange=(30, float("inf"))):
        """
        :param maxTermsCount: the max number of domain terms
        :param thresholdScore: word larger than thresholdScore will be recognized as domain term
        :param termFreqRange: tuple-like object(minFreq,maxFreq), if word is not in the range, it will be not considered
                as term
        """
        self.maxTermsCount = maxTermsCount
        self.thresholdScore = thresholdScore
        self.termFreqRange = termFreqRange

    def extract_term(self, domainSpecificVocab, generalVocab):
        """
        extract domain term
        :param domainSpecificVocab: all words in domain-corpus, dict object, {"word1":word1Count,"word1":word1Count,...}
        :param generalVocab: all words in general-corpus, dict object, {"word1":word1Count,"word1":word1Count,...}
        :return: terms of list.[term1,term2,term3 ....]
        """
        # get word count in the two vocabulary
        domainSpecificVocabCount, generalVocabCount = 0.0, 0.0
        for _, v in domainSpecificVocab.items():
            domainSpecificVocabCount += v
        for _, v in generalVocab.items():
            generalVocabCount += v
        # extract domain specific terms
        candidateTerms = []
        for word, freq in domainSpecificVocab.items():
            if freq < self.termFreqRange[0] or freq > self.termFreqRange[1]:
                continue
            if word not in generalVocab:
                candidateTerms.append((word, float("inf")))
            else:
                score = (freq / domainSpecificVocabCount) / (generalVocab[word] / generalVocabCount)
                if score > self.thresholdScore:
                    candidateTerms.append((word, score))
        candidateTerms.sort(key=lambda x: x[1], reverse=True)
        terms = candidateTerms[0:self.maxTermsCount]
        logging.info("extract %d terms in total" % len(terms))
        return [term[0] for term in terms]


if __name__ == "__main__":
    print(30, 1 < float("inf"))
