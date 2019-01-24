"""
class to get semantic related words for terms
"""

class SemanticRelatedWords(object):
    def __init__(self):
        pass
    def getSemanticRelatedWords(self,terms,most_similar_func=None,topn=40):
        res={}
        for i in terms:
            res[i] = most_similar_func(term=i,topn=topn)
        return res