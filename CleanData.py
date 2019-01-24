"""
class to clean data
"""
import re
from lxml import etree
from bs4 import BeautifulSoup
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


PATTERNS = []
PATTERNS.append(re.compile("\[\[file[\s\S]*?\]\][\r\n]"))  # 匹配[[file开始的段落
PATTERNS.append(re.compile("\[\[image[\s\S]*?\]\][\r\n]"))  # 匹配[[image开始的段落
PATTERNS.append(re.compile("\[\[category[\s\S]*?\]\][\r\n]"))  # 匹配[[category开始的段落
PATTERNS.append(re.compile(r"{{[\s\S]*?}}"))  # filter {{}} 最小匹配
PATTERNS.append(
    re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"))  # filter URL
PATTERNS.append(re.compile("\[\[[^]]*?\|"))  # 过滤[[ content|
PATTERNS.append("[']{2,3}")  # ''  '''
PATTERNS.append(re.compile("[\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]"))  # 一些替换
# 预编译一部分  文章无用section
PATTERNS_SECT = []
PATTERNS_SECT.append(re.compile("[=]{2,8} footnotes [=]{2,8}"))
PATTERNS_SECT.append(re.compile("[=]{2,8} endnotes [=]{2,8}"))
PATTERNS_SECT.append(re.compile("[=]{2,8} references [=]{2,8}"))
PATTERNS_SECT.append(re.compile("[=]{2,8} external links [=]{2,8}"))
PATTERNS_SECT.append(re.compile("[=]{2,8} 	criticisms [=]{2,8}"))
PATTERNS_SECT.append(re.compile("[=]{2,8} 	see also [=]{2,8}"))
PATTERNS_SECT.append(re.compile("[=]{2,8} further reading [=]{2,8}"))
PATTERNS_SECT.append(re.compile("[=]{2,8} sources [=]{2,8}"))
PATTERNS_SECT.append(re.compile("[=]{2,8} bibliography [=]{2,8}"))
PATTERNS_SECT.append(re.compile("[=]{2,8} publications [=]{2,8}"))

def cleanData_Wiki(content):
    words = []
    # Step1 获取HTML文本
    content = content.strip().lower()
    content = BeautifulSoup(content, "lxml").get_text()
    # Step 2正则表达式过滤噪音
    # 先过滤没必要的section
    ins = []
    for pat in PATTERNS_SECT:
        patt = re.search(pat, content)
        if (patt is not None):
            ins.append(patt.span()[0])
    if (len(ins) > 0):
        content = content[0:min(ins)]
    re5 = re.compile("\]")  # 不使用空格替换
    reSplit1 = re.compile("\.[^a-z0-9]|[?!;\n\r]")
    for pat in PATTERNS:
        content = re.sub(pat, " ", content)
    content = re.sub(re5, "", content)
    # 分句分词
    content=content.replace("-","_")
    for sent in re.split(reSplit1, content):
        sen_word = sent.split()
        if (len(sen_word) > 4):
            if (sen_word[0] != "|" and sen_word[0] != "*"):
                words.append(sen_word)
    return words

if __name__ == "__main__":
    context = etree.iterparse("E://a.xml", encoding="utf-8")
    datas = []  # 存储title 和 answers
    # context.
    for _, elem in context:  # 迭代每一个
        print(elem,elem.text)
        elem.clear()