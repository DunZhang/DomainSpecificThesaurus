"""
class to extrace domain-specific terms
"""


class DomainSpecificTerm(object):
    def __init__(self, maxTermsCount=300000, thresholdScore=10.0, termFreqRange=(30, float("inf"))):
        self.maxTermsCount = maxTermsCount
        self.thresholdScore = thresholdScore
        self.termFreqRange = termFreqRange

    def extract_term(self, domainSpecificVocab, generalVocab):
        # get word count in the two vocabulary
        domainSpecificVocabCount, generalVocabCount = 0.0, 0.0
        for _, v in domainSpecificVocab.items():
            domainSpecificVocabCount += v
        for _, v in generalVocab.items():
            generalVocabCount += v
        # extract domain specific terms
        candidateTerms = []
        for word, freq in self.domainSpecificVocab.items():
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
        return terms


if __name__ == "__main__":
    print(30, 1 < float("inf"))
