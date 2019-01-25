"""
class to get semantic related words for terms
"""

class SemanticRelatedWords(object):
    def __init__(self):
        pass
    def getSemanticRelatedWords(self,terms,most_similar_func,topn=40):
        res={}
        for term in terms:
            res[term] = most_similar_func(term=term,topn=topn)
        return res