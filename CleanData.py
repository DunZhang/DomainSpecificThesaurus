"""
class to clean data
"""
import re
def cleanData_SO(strText=""):
    """
    only use to clean data in stack overflow
    :param strText: text, not include tag in html5
    :return:
    """
    reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
    reSub1 = re.compile("[\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]")  # replace with " "
    rePlus = re.compile("[^+]\+[^+]")
    reSplit1 = re.compile("\.[^a-z0-9]|[?!;\n\r]")
    sentences = []
    strText = strText.lower()

    strText = re.sub(reSub0, " ", strText)
    strText = re.sub(reSub1, " ", strText)
    # deal '+', remove single'+', keep two more plus
    for sub in set(re.findall(rePlus, strText)):
        strText = strText.replace(sub, sub[0] + " " + sub[2])
    strText=strText.replace("-","_")
    for sentence in re.split(reSplit1, strText):
        if (len(sentence.split()) > 6):
            sentence += "\n"
            sentences.append(sentence)
    return sentences
def cleanData_Wiki():
    pass