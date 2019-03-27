import sys
def _check_type(s):
    if sys.version_info[0] == 3 and not isinstance(s, str):
        raise TypeError('expected str or unicode, got %s' % type(s).__name__)
    elif not sys.version_info[0] == 3 and not isinstance(s, unicode):
        raise TypeError('expected unicode, got %s' % type(s).__name__)



def levenshtein_distance(s1, s2):
    """
    compute levenshtein distance
    :param s1: str
    :param s2: str
    :return: levenshtein_distance
    """
    _check_type(s1)
    _check_type(s2)

    if s1 == s2:
        return 0
    rows = len(s1)+1
    cols = len(s2)+1

    if not s1:
        return cols-1
    if not s2:
        return rows-1

    prev = None
    cur = range(cols)
    for r in range(1, rows):
        prev, cur = cur, [r] + [0]*(cols-1)
        for c in range(1, cols):
            deletion = prev[c] + 1
            insertion = cur[c-1] + 1
            edit = prev[c-1] + (0 if s1[r-1] == s2[c-1] else 1)
            cur[c] = min(edit, deletion, insertion)

    return cur[-1]
def StrSimilarity(s1,s2):
    return levenshtein_distance(s1,s2)/max((len(s1),len(s2)))
if __name__ =="__main__":
    print(StrSimilarity("123","1234"))