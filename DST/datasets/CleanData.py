"""
Class  and methods to clean data.
We provide four methods to seperately clean data
"""
import codecs
import re
import logging

logger = logging.getLogger(__name__)
from lxml import etree
from bs4 import BeautifulSoup


class CleanDataSO(object):
    def __init__(self, so_xml_path, clean_data_path):
        self.__reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
        self.__reSub1 = re.compile("[\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]")  # replace with " "
        self.__rePlus = re.compile("[^+]\+[^+]")
        self.__reSplit1 = re.compile("\.[^a-z0-9]|[?!;\n\r]")
        self.so_xml_path = so_xml_path
        self.clean_data_path = clean_data_path

    def __clean_data(self, strText):
        sentences = []
        strText = strText.lower()
        strText = re.sub(self.__reSub0, " ", strText)
        strText = re.sub(self.__reSub1, " ", strText)
        # deal '+', remove single'+', keep two more plus
        for sub in set(re.findall(self.__rePlus, strText)):
            strText = strText.replace(sub, sub[0] + " " + sub[2])
        strText = strText.replace("-", "_")
        for sentence in re.split(self.__reSplit1, strText):
            if (len(sentence.split()) > 6):
                sentence += "\n"
                sentences.append(sentence)
        return sentences

    def transform(self):
        logger.info("clean stack overflow data")
        context = etree.iterparse(self.so_xml_path, encoding="utf-8")
        fw = codecs.open(self.clean_data_path, mode="w", encoding="utf-8")

        clean_data = []  # 存储title 和 answers
        c = 0
        for _, elem in context:  # 迭代每一个
            c += 1
            if (c % 100000 == 0):
                logger.info("already clean record:" + str(c / 10000) + "W")
            title, body, typeId = elem.get("Title"), elem.get("Body"), elem.get("PostTypeId")
            elem.clear()
            if typeId is None:
                continue
            if int(typeId) != 1 and int(typeId) != 2:
                continue
            if body is not None:
                soup = BeautifulSoup(body, "lxml")
                for pre in soup.find_all("pre"):
                    if (len(pre.find_all("code")) > 0):
                        pre.decompose()
                clean_data.extend(self.__clean_data(soup.get_text()))
            if title is not None:
                clean_data.extend(self.__clean_data(BeautifulSoup(title, "lxml").get_text()))
            if len(clean_data) > 100000:  # write to local
                fw.writelines(clean_data)
                clean_data = []
        if len(clean_data) > 0:
            fw.writelines(clean_data)
        fw.close()


class CleanDataWiki(object):
    def __init__(self, wiki_data_path, clean_data_path):
        self.wiki_data_path, self.clean_data_path = wiki_data_path, clean_data_path
        self.__PATTERNS = []
        self.__PATTERNS.append(re.compile("\[\[file[\s\S]*?\]\][\r\n]"))  # 匹配[[file开始的段落
        self.__PATTERNS.append(re.compile("\[\[image[\s\S]*?\]\][\r\n]"))  # 匹配[[image开始的段落
        self.__PATTERNS.append(re.compile("\[\[category[\s\S]*?\]\][\r\n]"))  # 匹配[[category开始的段落
        self.__PATTERNS.append(re.compile(r"{{[\s\S]*?}}"))  # filter {{}} 最小匹配
        self.__PATTERNS.append(
            re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"))  # filter URL
        self.__PATTERNS.append(re.compile("\[\[[^]]*?\|"))  # 过滤[[ content|
        self.__PATTERNS.append("[']{2,3}")  # ''  '''
        self.__PATTERNS.append(re.compile("[\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]"))  # 一些替换
        # 预编译一部分  文章无用section
        self.__PATTERNS_SECT = []
        self.__PATTERNS_SECT.append(re.compile("[=]{2,8} footnotes [=]{2,8}"))
        self.__PATTERNS_SECT.append(re.compile("[=]{2,8} endnotes [=]{2,8}"))
        self.__PATTERNS_SECT.append(re.compile("[=]{2,8} references [=]{2,8}"))
        self.__PATTERNS_SECT.append(re.compile("[=]{2,8} external links [=]{2,8}"))
        self.__PATTERNS_SECT.append(re.compile("[=]{2,8} 	criticisms [=]{2,8}"))
        self.__PATTERNS_SECT.append(re.compile("[=]{2,8} 	see also [=]{2,8}"))
        self.__PATTERNS_SECT.append(re.compile("[=]{2,8} further reading [=]{2,8}"))
        self.__PATTERNS_SECT.append(re.compile("[=]{2,8} sources [=]{2,8}"))
        self.__PATTERNS_SECT.append(re.compile("[=]{2,8} bibliography [=]{2,8}"))
        self.__PATTERNS_SECT.append(re.compile("[=]{2,8} publications [=]{2,8}"))

    def __clean_data(self, content):
        words = []
        # Step1 获取HTML文本
        content = content.strip().lower()
        content = BeautifulSoup(content, "lxml").get_text()
        # Step 2正则表达式过滤噪音
        # 先过滤没必要的section
        ins = []
        for pat in self.__PATTERNS_SECT:
            patt = re.search(pat, content)
            if (patt is not None):
                ins.append(patt.span()[0])
        if (len(ins) > 0):
            content = content[0:min(ins)]
        re5 = re.compile("\]")  # 不使用空格替换
        reSplit1 = re.compile("\.[^a-z0-9]|[?!;\n\r]")
        for pat in self.__PATTERNS:
            content = re.sub(pat, " ", content)
        content = re.sub(re5, "", content)
        # 分句分词
        content = content.replace("-", "_")
        for sent in re.split(reSplit1, content):
            sen_word = sent.split()
            if (len(sen_word) > 4):
                if (sen_word[0] != "|" and sen_word[0] != "*"):
                    sen_word.append("\n")
                    words.append(" ".join(sen_word))
        return words

    def tranform(self):
        context = etree.iterparse(self.wiki_data_path, encoding="utf-8")
        fw = codecs.open(self.clean_data_path, mode="w", encoding="utf-8")
        clean_data = []
        c = 0
        for _, elem in context:
            tag, content = elem.tag, elem.text
            elem.clear()
            # print(elem)
            if tag is None or content is None or str(tag)[-4:] != "text" or len(content) < 200:
                continue
            c += 1
            if c % 10000 == 0:
                logger.info("already clean passages:" + str(c / 10000) + "W")
            clean_data.extend(self.__clean_data(content=content))
            if len(clean_data) > 100000:  # write to local
                fw.writelines(clean_data)
                clean_data = []
        if len(clean_data) > 0:
            fw.writelines(clean_data)
        fw.close()


def cleanMathXml(xmlPath="../data/Posts.xml", savePath="../result/cleanMath.txt"):
    """
    clean math data
    """
    counts = [0, 0, 0]
    reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
    reSub1 = re.compile("[,/'\[\]\\\\|}{:\"><~`@#$%^&*()_+=}]")  # replace with " "
    reSplit1 = re.compile("[.?!;\n\r]")
    sentences = []
    context = etree.iterparse(xmlPath, encoding="utf-8")
    datas = []  # 存储title 和 answers
    c = 0
    for _, elem in context:  # 迭代每一个
        c += 1
        if (c % 50000 == 0):
            logger.info("already pasrse record:" + str(c / 10000) + "W")
        title, body, typeId = elem.get("Title"), elem.get("Body"), elem.get("PostTypeId")
        elem.clear()
        if (typeId is None):
            continue
        if (int(typeId) != 1 and int(typeId) != 2):
            continue
        counts[int(typeId)] += 1
        if (body is not None):
            soup = BeautifulSoup(body, "lxml")
            # 去除长短公式证明
            for p in soup.find_all("p"):
                if p.get_text().startswith("$$"):
                    p.decompose()
            datas.append(soup.get_text())
        if (title is not None):
            datas.append(BeautifulSoup(title, "lxml").get_text())
        # 开始处理获取的数据
    logger.info("start to clean data")
    fw = codecs.open(savePath, "w", encoding="utf-8")
    for strText in datas:
        strText = strText.lower()
        strText = re.sub(reSub0, " ", strText)
        strText = re.sub(reSub1, " ", strText)

        strText = strText.replace("-", "_")
        for sentence in re.split(reSplit1, strText):
            if (len(sentence.split()) > 6):
                sentence += "\n"
                sentences.append(sentence)
        if (len(sentences) > 500000):
            fw.writelines(sentences)
            sentences = []
    if (len(sentences) > 0):
        fw.writelines(sentences)
    fw.close()
    return counts


def cleanEngXml(xmlPath="Posts.xml", savePath="cleanEng.txt"):
    """
    clean eng data
    """
    counts = [0, 0, 0]
    reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
    reSub1 = re.compile("[\[\]<>`~$\^&*+=|%@(){},:\"/'\\\\]")  # replace with " "
    reSplit1 = re.compile("[.?!;\n\r]")
    sentences = []
    context = etree.iterparse(xmlPath, encoding="utf-8")
    datas = []  # 存储title 和 answers
    c = 0
    for _, elem in context:  # 迭代每一个
        c += 1
        if (c % 50000 == 0):
            logging.info("already pasrse record:", str(c / 10000) + "W")
        title, body, typeId = elem.get("Title"), elem.get("Body"), elem.get("PostTypeId")
        elem.clear()
        if (typeId is None):
            continue
        if (int(typeId) != 1 and int(typeId) != 2):
            continue
        counts[int(typeId)] += 1
        if (body is not None):
            soup = BeautifulSoup(body, "lxml")
            #            for pre in soup.find_all("pre"):
            #                if (len(pre.find_all("code")) > 0):
            #                    pre.decompose()
            datas.append(soup.get_text())
        if (title is not None):
            datas.append(BeautifulSoup(title, "lxml").get_text())
        # 开始处理获取的数据
    logging.info("clean data")
    fw = codecs.open(savePath, "w", encoding="utf-8")
    for strText in datas:
        strText = strText.lower()
        strText = re.sub(reSub0, " ", strText)
        strText = re.sub(reSub1, " ", strText)

        strText = strText.replace("-", "_")
        for sentence in re.split(reSplit1, strText):
            if (len(sentence.split()) > 6):
                sentence += "\n"
                sentences.append(sentence)
        if (len(sentences) > 500000):
            fw.writelines(sentences)
            sentences = []
    if (len(sentences) > 0):
        fw.writelines(sentences)
    fw.close()
    return counts


if __name__ == "__main__":
    context = etree.iterparse("E://a.xml", encoding="utf-8")
    datas = []  # 存储title 和 answers
    # context.
    for _, elem in context:  # 迭代每一个
        print(elem.tag + ":" + elem.text)
        elem.clear()
