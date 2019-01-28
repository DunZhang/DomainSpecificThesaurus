"""
to create a domain specific thesaurus by using our approach
the input are domain corpus and gengeral corpus and the output is domain specific thesaurus(dst)

future optimization：
1. some modules' function should be clear and vivid. May remove or add some functions.
2. the program may re-read some data as input, but the output already exist, it wastes some time
3. the information in logging-info should be more clear
4. unit-test (pytest) should be added.
5. use logger more reasonable
6. domain-thesaurus.word_classification.WordClassification is not good
"""
import codecs
import json
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
PORJ_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(PORJ_PATH)
from DST.phrase_detection.PhraseDetection import PhraseDetection
from DST.domain_term.DomainTerm import DomainTerm
from DST.semantic_related_word.SemanticRelatedWord import SemanticRelatedWord
from DST.word_classification.WordClassification import WordClassification, default_classify_func
from DST.synonym_group.SynonymGroup import SynonymGroup
from DST.utils.VocabUtil import corpusToVocab


class DomainThesaurus(object):
    """
    class to get domain thesaurus automatically
    """

    def __init__(self,
                 domain_specific_corpus_path,
                 general_corpus_path,
                 outputDir=None,
                 filePaths=None,
                 phrase_detection_domain="default",
                 phrase_detection_general="default",
                 domain_specific_term="default",
                 semantic_related_words="default",
                 word_classification="default",
                 synonym_group="default"):
        """
        :param domain_specific_corpus_path: str, the path of domain specific corpus path, should be a text file with one line
                 one sentence.
        :param general_corpus_path: str, the path of general corpus path, should be a text file with one line
                 one sentence.
        :param outputDir: str, optional, the directory of output, the final thesaurus and temporary files  are in the directory

        :param filePaths: dict, optional, specify every path of temporary files. If this parameter is None, filePaths will be generated
                by using outputDir. If the parameter outputDir is None too, the current directory will be the outputDir.
                We suggested that you should specify the ouptputDir or filePaths.

                If you specify filePaths, this dict should have these keys:
                    domain_corpus_phrase: domain corpus with phrase detection

                    general_corpus_phrase: general corpus with phrase detection

                    domain_vocab: vocabulary of domain corpus, it contain all words of this corpus

                    general_vocab: vocabulary of general corpus, it contain all words of this corpus

                    domain_terms: domain terms stored in a text file, one line one term

                    fasttext: the path of fasttext model, if you do not use default class SemanticRelatedWord, it will be
                                unnecessary

                    skipgram: the path of skipgram model, if you do not use default class SemanticRelatedWord, it will be
                                unnecessary

                    semantic_related_words: the path of semantic related words, it is a json file

                    origin_thesaurus: the original thesaurus

                    final_thesaurus: the path of final thesaurus
        :param phrase_detection_domain: class to detect phrase for domain corpus, optional,
                if it is specified, it must be a class with the class functions: fit and transform. The functions must have
                 the same parameters and meaning with the default class

        :param phrase_detection_general: class to detect phrase for general corpus, optional,
                if it is specified, it must be a class with the class functions: fit and transform. The functions must have
                 the same parameters and return with the default class

        :param domain_specific_term: class to extract domain specific terms, optional,
                if it is specified. it must be a class with the class functions: extract_term. The function must have
                the same parameters and return with the default class



        :param semantic_related_words: class to get semantic related words, optional,
                if it is specified. it must be a class with the class functions: getSemanticRelatedWords. The function must have
                the same parameters and return with the default class

        :param word_classification: class to  classify semantic related words, optional,
                if it is specified. it must be a class with the class functions: classifyWords. The function must have
                the same parameters and return with the default class

        :param synonym_group: class to extract group synonyms, optional,
                if it is specified. it must be a class with the class functions: group_synonyms. The function must have
                the same parameters and return with the default class
        """

        self.domain_specific_corpus_path = domain_specific_corpus_path
        self.general_corpus_path = general_corpus_path
        self.outputDir = outputDir
        self.filePaths = filePaths
        self.domain_vocab, self.general_vocab = None, None
        self.domain_terms = None
        self.semantic_related_words = None
        self.origin_thesaurus = None
        self.final_thesaurus = None
        self.__getFilePaths()  # get all file paths
        # some models in DomainThesaurus
        if phrase_detection_domain == "default":
            wordNumInPhrase = 3
            savePhraserPaths = []
            phrasesDir = os.path.join(self.outputDir, "Phrases")
            if not os.path.exists(phrasesDir):
                os.makedirs(phrasesDir)
            for i in range(wordNumInPhrase - 1):
                savePhraserPaths.append(
                    os.path.join(self.outputDir, "Phrases/" + str(i + 2) + "_domain_phrase.model"))
            self.PhraseDetectionDomain = PhraseDetection(savePhraserPaths=savePhraserPaths, file_overwrite=False,
                                                         min_count=10, threshold=15.0, max_vocab_size=40000000,
                                                         delimiter=b'_', scoring='default',
                                                         wordNumInPhrase=wordNumInPhrase)
        else:
            self.PhraseDetectionDomain = phrase_detection_domain

        if phrase_detection_general == "default":
            wordNumInPhrase = 3
            savePhraserPaths = []
            phrasesDir = os.path.join(self.outputDir, "Phrases")
            if not os.path.exists(phrasesDir):
                os.makedirs(phrasesDir)
            for i in range(wordNumInPhrase - 1):
                savePhraserPaths.append(
                    os.path.join(self.outputDir, "Phrases/" + str(i + 2) + "_general_phrase.model"))
            self.PhraseDetectionGeneral = PhraseDetection(savePhraserPaths=savePhraserPaths, file_overwrite=False,
                                                          min_count=10, threshold=15.0, max_vocab_size=40000000,
                                                          delimiter=b'_', scoring='default',
                                                          wordNumInPhrase=wordNumInPhrase)
        else:
            self.PhraseDetectionGeneral = phrase_detection_general

        if domain_specific_term == "default":
            self.DomainTerm = DomainTerm(maxTermsCount=300000, thresholdScore=10.0,
                                         termFreqRange=(30, float("inf")))
        else:
            self.DomainTerm = domain_specific_term
        if semantic_related_words == "default":
            self.SemanticRelatedWords = SemanticRelatedWord(self.filePaths["domain_corpus_phrase"],
                                                            self.filePaths["fasttext"], self.filePaths["skipgram"],
                                                            file_overwrite=False, topn_fasttext=8, topn_skipgram=15,
                                                            min_count=5, size=200, workers=8, window=5
                                                            )
        else:
            self.SemanticRelatedWords = semantic_related_words
        if word_classification == "default":
            self.WordClassification = WordClassification(classify_word_func=default_classify_func,
                                                         synonym_types=["synonym", "abbreviation", "other"])
        else:
            self.WordClassification = word_classification
        if synonym_group == "default":
            self.SynonymGroup = SynonymGroup(group_synonym_type="synonym", domain_vocab=self.domain_vocab)
        else:
            self.SynonymGroup = synonym_group

    def clear(self):
        del self.domain_vocab
        del self.general_vocab
        del self.domain_terms
        del self.semantic_related_words
        del self.origin_thesaurus
        del self.final_thesaurus

        self.domain_vocab = None
        self.general_vocab = None
        self.domain_terms = None
        self.semantic_related_words = None
        self.origin_thesaurus = None
        self.final_thesaurus = None

    def __getFilePaths(self):
        # ouputDir is a directory that contain many temp file and final thesaurus in the process of extracting thesaurus
        if self.filePaths is None:  # use default setting
            if self.outputDir is None:
                self.outputDir = os.path.dirname(__file__)
            self.filePaths = {}
            self.filePaths["domain_corpus_phrase"] = os.path.join(self.outputDir, "domain_corpus_phrase.txt")
            self.filePaths["general_corpus_phrase"] = os.path.join(self.outputDir, "general_corpus_phrase.txt")
            self.filePaths["domain_vocab"] = os.path.join(self.outputDir, "domain_vocab.json")
            self.filePaths["general_vocab"] = os.path.join(self.outputDir, "general_vocab.json")
            self.filePaths["domain_terms"] = os.path.join(self.outputDir, "domain_terms.txt")
            self.filePaths["fasttext"] = os.path.join(self.outputDir, "fasttext/fasttext.model")
            self.filePaths["skipgram"] = os.path.join(self.outputDir, "skipgram/skipgram.model")
            self.filePaths["semantic_related_words"] = os.path.join(self.outputDir, "semantic_related_words.json")
            self.filePaths["origin_thesaurus"] = os.path.join(self.outputDir, "origin_thesaurus.json")
            self.filePaths["final_thesaurus"] = os.path.join(self.outputDir, "final_thesaurus.json")

    def __phraseDetection(self):
        if not os.path.exists(self.filePaths["domain_corpus_phrase"]):
            logger.info("detect phrase for domain specific corpus...")
            self.PhraseDetectionDomain.fit(sentencesPath=self.domain_specific_corpus_path)
            self.PhraseDetectionDomain.transform(sentencesPath=self.domain_specific_corpus_path,
                                                 savePath=self.filePaths["domain_corpus_phrase"])
        else:
            logger.warning(self.filePaths["domain_corpus_phrase"] + "already exist, program will not detect phrase.")
        if not os.path.exists(self.filePaths["general_corpus_phrase"]):
            logger.info("detect phrase for general corpus...")
            self.PhraseDetectionGeneral.fit(sentencesPath=self.general_corpus_path)
            self.PhraseDetectionGeneral.transform(sentencesPath=self.general_corpus_path,
                                                  savePath=self.filePaths["general_corpus_phrase"])
        else:
            logger.warning(self.filePaths["general_corpus_phrase"] + "already exist, program will not detect phrase.")

    def __corpusVocab(self):
        if not os.path.exists(self.filePaths["domain_vocab"]):
            logger.info("get vocabulary from domain corpus")
            with codecs.open(self.filePaths["domain_corpus_phrase"], mode="r", encoding="utf-8") as fr:
                self.domain_vocab = corpusToVocab(fr)
                logger.info("save domain vocabulary to local")
                with codecs.open(self.filePaths["domain_vocab"], mode="w", encoding="utf-8") as fw:
                    fw.write(json.dumps(self.domain_vocab))
        else:
            logger.warning(self.filePaths["domain_vocab"] + " already exists, program will read it")
            with codecs.open(self.filePaths["domain_vocab"], mode="r", encoding="utf-8") as fr:
                self.domain_vocab = json.loads(fr.read())
        if not os.path.exists(self.filePaths["general_vocab"]):
            logger.info("get vocabulary from general corpus")
            with codecs.open(self.filePaths["general_corpus_phrase"], mode="r", encoding="utf-8") as fr:
                self.general_vocab = corpusToVocab(fr)
                logger.info("save general vocabulary to local")
                with codecs.open(self.filePaths["general_vocab"], mode="w", encoding="utf-8") as fw:
                    fw.write(json.dumps(self.general_vocab))
        else:
            logger.warning(self.filePaths["general_vocab"] + " already exists, program will read it")
            with codecs.open(self.filePaths["general_vocab"], mode="r", encoding="utf-8") as fr:
                self.general_vocab = json.loads(fr.read())

    def __domainTerm(self):
        if not os.path.exists(self.filePaths["domain_terms"]):
            self.domain_terms = self.DomainTerm.extract_term(domainSpecificVocab=self.domain_vocab,
                                                             generalVocab=self.general_vocab)
            logger.info("save domain terms to local")
            logging.info(self.domain_terms[0:20])
            with codecs.open(self.filePaths["domain_terms"], mode="w", encoding="utf-8") as fw:
                fw.writelines([term + "\n" for term in self.domain_terms])
        else:
            logger.warning(self.filePaths["domain_terms"] + " alread exists, program will read it")
            with codecs.open(self.filePaths["domain_terms"], mode="r", encoding="utf-8") as fr:
                self.domain_terms = [line.strip() for line in fr.readlines()]

    def __semanticRelatedWords(self):
        if not os.path.exists(self.filePaths["semantic_related_words"]):
            self.semantic_related_words = self.SemanticRelatedWords.getSemanticRelatedWords(terms=self.domain_terms)
            # save semantic_related_words
            logger.info("save semantic related words to local")
            with codecs.open(self.filePaths["semantic_related_words"], mode="w", encoding="utf-8") as fw:
                fw.write(json.dumps(self.semantic_related_words))
        else:
            logger.warning(self.filePaths["semantic_related_words"] + "already exists, program will read it")
            with codecs.open(self.filePaths["semantic_related_words"], mode="r", encoding="utf-8") as fr:
                self.semantic_related_words = json.loads(fr.read())

    def __classifyWords(self):
        if not os.path.exists(self.filePaths["origin_thesaurus"]):
            self.origin_thesaurus = self.WordClassification.classifyWords(vocab=self.semantic_related_words)
            # save origin_thesaurus
            logger.info("save origin thesaurus to local")
            with codecs.open(self.filePaths["origin_thesaurus"], mode="w", encoding="utf-8") as fw:
                fw.write(json.dumps(self.origin_thesaurus))
        else:
            logger.warning(self.filePaths["origin_thesaurus"] + "already exists, program will read it")
            with codecs.open(self.filePaths["origin_thesaurus"], mode="r", encoding="utf-8") as fr:
                self.origin_thesaurus = json.loads(fr.read())

    def __groupSynonyms(self):
        if not os.path.exists(self.filePaths["final_thesaurus"]):
            if isinstance(self.SynonymGroup, SynonymGroup):  # if use default synonym group class
                self.SynonymGroup.domain_vocab = self.domain_vocab
                # logger.info(str(len(self.domain_vocab)))
            self.final_thesaurus = self.SynonymGroup.group_synonyms(dst=self.origin_thesaurus)
            logger.info("save final thesaurus to local")
            with codecs.open(self.filePaths["final_thesaurus"], mode="w", encoding="utf-8") as fw:
                fw.write(json.dumps(self.final_thesaurus))
        else:
            logger.warning(self.filePaths["final_thesaurus"] + "already exists, program will read it")
            with codecs.open(self.filePaths["final_thesaurus"], mode="r", encoding="utf-8") as fr:
                self.final_thesaurus = json.loads(fr.read())

    def extract(self):
        """
        get domain thesaurus automatically
        Warning: this may take a long time, the time depends on the size of corpus and the CPU's performance .
        Take Stack Overflow as an example,t may take several days.
        When the program finish a part job( can be watched by logging info), you can stop. If you do not delete the
        temporary files, it can continue this job.
        :return: the final thesaurus
        """
        # phrase detection
        logger.info("begin to detect phrase")
        self.__phraseDetection()
        logger.info("finish phrase detection")
        # extract domain specific term
        # get vocab
        logger.info("get vocabulary from corpus")
        self.__corpusVocab()
        logger.info("finish")
        # get domain terms
        logger.info("get domain term")
        self.__domainTerm()
        logger.info("finish get domain terms")
        # get semantic related words
        logger.info("get semantic related words")
        self.__semanticRelatedWords()
        logger.info("finish get semantic related words")
        # classify words
        logger.info("classify semantic related words")
        self.__classifyWords()
        logger.info("finish classify semantic related words")
        # group synonyms and get final thesaurus
        logger.info("group synonyms and get final thesaurus")
        self.__groupSynonyms()
        logger.info("finish group synonyms and get final thesaurus")
        return self.final_thesaurus


if __name__ == "__main__":
    pass
