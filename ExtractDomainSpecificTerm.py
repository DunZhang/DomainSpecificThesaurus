"""
class to extrace domain-specific terms
"""
class ExtractDomainSpecificTerm(object):
    def __init__(self, domainSpecificVocab, generalVocab):
        self.domainSpecificVocab = domainSpecificVocab
        self.generalVocab = generalVocab
        self.domainSpecificVocabCount, self.generalVocabCount = 0.0, 0.0
        for _, v in domainSpecificVocab.items():
            self.domainSpecificVocabCount += v
        for _, v in generalVocab.items():
            self.generalVocabCount += v

    def getTerms(self, maxTermsCount=300000, thresholdScore=10.0, termFreqRange=(30, float("inf"))):
        candidateTerms = []
        for word, freq in self.domainSpecificVocab.items():
            if freq < termFreqRange[0] or freq > termFreqRange[1]:
                continue
            if word not in self.generalVocab:
                candidateTerms.append((word, float("inf")))
            else:
                score = (freq / self.domainSpecificVocabCount) / (self.generalVocab[word] / self.generalVocabCount)
                if score > thresholdScore:
                    candidateTerms.append((word, score))
        candidateTerms.sort(key=lambda x :x[1],reverse=True)
        terms = candidateTerms[0:maxTermsCount]
        return terms
print(__file__)
if __file__ == "__main__":
    print(30, 1 < float("inf"))
