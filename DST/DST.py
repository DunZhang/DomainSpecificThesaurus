"""
to create a domain specific thesaurus by using our approach
the input are domain corpus and gengeral corpus and the output is domain specific thesaurus(dst)
"""
import codecs
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import os
from collections import defaultdict
from DST.PhraseDetection import PhraseDetection
from DST.DomainSpecificTerm import DomainSpecificTerm
from DST.SemanticRelatedWords import SemanticRelatedWords
from DST.WordClassification import WordClassification, default_classify_func
from DST.SynonymGroup import SynonymGroup, default_get_new_key


def corpusToVocab(sentences):
    vocab = defaultdict(int)
    for line in sentences:
        for word in line.split():
            vocab[word] += 1
    return vocab


class DST(object):
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
        # some models in DST
        if phrase_detection_domain == "default":
            self.PhraseDetectionDomain = PhraseDetection(savePhraserPaths="", min_count=10, threshold=15.0,
                                                         max_vocab_size=40000000, delimiter=b'_', scoring='default',
                                                         wordNumInPhrase=3)
            savePhraserPaths = []
            for i in range(self.PhraseDetectionDomain.wordNumInPhrase - 1):
                savePhraserPaths.append(os.path.join(self.outputDir, "/Phrases/" + str(i + 2) + "_domain_phrase.model"))
            self.PhraseDetectionDomain.savePhraserPaths = savePhraserPaths

        else:
            self.PhraseDetectionDomain = phrase_detection_domain

        if phrase_detection_general == "default":
            self.PhraseDetectionGeneral = PhraseDetection(savePhraserPaths="", min_count=10, threshold=15.0,
                                                          max_vocab_size=40000000, delimiter=b'_', scoring='default',
                                                          wordNumInPhrase=3)
            savePhraserPaths = []
            for i in range(self.PhraseDetectionGeneral.wordNumInPhrase - 1):
                savePhraserPaths.append(os.path.join(self.outputDir, "/Phrases/" + str(i + 2) + "_domain_phrase.model"))
            self.PhraseDetectionGeneral.savePhraserPaths = savePhraserPaths

        else:
            self.PhraseDetectionGeneral = phrase_detection_general

        if domain_specific_term == "default":
            self.DomainSpecificTerm = DomainSpecificTerm(maxTermsCount=300000, thresholdScore=10.0,
                                                         termFreqRange=(30, float("inf")))
        else:
            self.DomainSpecificTerm = domain_specific_term
        if semantic_related_words == "default":
            self.SemanticRelatedWords = SemanticRelatedWords(self.filePaths["domain_corpus_phrase"],
                                                             self.filePaths["fasttext"], self.filePaths["skipgram"],
                                                             fasttext=None, skipgram=None,
                                                             topn_fasttext=8, topn_skipgram=15, min_count=5, size=200,
                                                             workers=8, window=5
                                                             )
        else:
            self.SemanticRelatedWords = semantic_related_words
        if word_classification == "default":
            self.WordClassification = WordClassification(classify_word_func=default_classify_func,
                                                         synonym_types=["synonym", "abbreviation", "other"])
        else:
            self.WordClassification = word_classification
        if synonym_group == "default":
            self.SynonymGroup = SynonymGroup(group_synonym_type="synonym", get_new_key=default_get_new_key)
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
            self.filePaths["fasttext"] = os.path.join(self.outputDir, "/fasttext/fasttext.model")
            self.filePaths["skipgram"] = os.path.join(self.outputDir, "/skipgram/skipgram.model")
            self.filePaths["semantic_related_words"] = os.path.join(self.outputDir, "semantic_related_words.json")
            self.filePaths["origin_thesaurus"] = os.path.join(self.outputDir, "origin_thesaurus.json")
            self.filePaths["final_thesaurus"] = os.path.join(self.outputDir, "final_thesaurus.json")
            self.steps = ["domain_corpus_phrase", "general_corpus_phrase", "domain_vocab", "general_vocab",
                          "domain_terms", "fasttext", "skipgram", "semantic_related_words", "origin_thesaurus",
                          "final_thesaurus"]

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
            self.domain_terms = self.DomainSpecificTerm.extract_term(domainSpecificVocab=self.domain_vocab,
                                                                     generalVocab=self.general_vocab)
            logger.info("save domain terms to local")
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

            self.final_thesaurus = self.SynonymGroup.group_synonyms(dst=self.origin_thesaurus)
            logger.info("save final thesaurus to local")
            with codecs.open(self.filePaths["final_thesaurus"], mode="w", encoding="utf-8") as fw:
                fw.write(json.dumps(self.final_thesaurus))
        else:
            logger.warning(self.filePaths["final_thesaurus"] + "already exists, program will read it")
            with codecs.open(self.filePaths["final_thesaurus"], mode="r", encoding="utf-8") as fr:
                self.final_thesaurus = json.loads(fr.read())

    def extract(self):
        # phrase detection
        logger.info("begin to detect phrase")
        self.__phraseDetection()
        logger.info("finish phrase detection")
        # extract domain specific term
        # get vocab
        logger.info("get vocabulary from corpus")
        self.__corpusVocab()
        # get domain terms
        logger.info("get domain term")
        self.__domainTerm()
        # get semantic related words
        logger.info("get semantic related words")
        self.__semanticRelatedWords()
        # classify words
        logger.info("classify semantic related words")
        self.__classifyWords()
        # group synonyms and get final thesaurus
        logger.info("group synonyms and get final thesaurus")
        self.__groupSynonyms()
        return self.final_thesaurus


if __name__ == "__main__":
    pass
