 """
to create a domain specific thesaurus by using our approach
the input are domain corpus and gengeral corpus and the output is domain specific thesaurus(dst)
"""
import codecs
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import os, sys
from collections import defaultdict
from PhraseDetection import PhraseDetection
from DomainSpecificTerm import DomainSpecificTerm
from SemanticRelatedWords import SemanticRelatedWords
from WordClassification import WordClassification, default_classify_func
from SynonymGroup import SynonymGroup, default_get_new_key


def corpusToVocab(sentences):
    vocab = defaultdict(int)
    for line in sentences:
        for word in line.split():
            vocab[word] += 1
    return vocab


class DST(object):
    def __getFilePaths(self):
        # ouputDir is a directory that contain many temp file and final thesaurus in the process of extracting thesaurus
        if self.filePaths is None:  # use default setting
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

    def __steps(self):
        """
        make sure which steps should be run
        """
        self.stepStatus = {}
        for i in self.steps:
            self.stepStatus[i] = os.path.exists(self.filePaths[i])
        for i in range(len(self.steps)):
            if not self.stepStatus[self.steps[i]]:
                break
        for j in range(0, i):
            self.stepStatus[self.steps[j]] = "PASS"
        self.stepStatus[self.steps[i]] = "READ"
        for j in range(i + 1, len(self.steps)):
            self.stepStatus[self.steps[j]] = "RUN"

    def __init__(self,
                 domain_specific_corpus_path,
                 general_corpus_path,
                 filePaths=None,
                 phrase_detection_domain="default",
                 phrase_detection_general="default",
                 domain_specific_term="default",
                 semantic_related_words="default",
                 word_classification="default",
                 synonym_group="default"):

        self.domain_specific_corpus_path = domain_specific_corpus_path
        self.general_corpus_path = general_corpus_path
        self.filePaths = filePaths
        self.__getFilePaths()  # get all file paths
        self.__steps()  # make sure which steps shoule be run
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

    def extract(self):
        # phrase detection for domain specific corpus
        self.PhraseDetectionDomain.fit(sentencesPath=self.domain_specific_corpus_path)
        self.PhraseDetectionDomain.transform(sentencesPath=self.domain_specific_corpus_path,
                                             savePath=self.filePaths["domain_corpus_phrase"])
        # phrase detection for general corpus
        self.PhraseDetectionGeneral.fit(sentencesPath=self.general_corpus_path)
        self.PhraseDetectionGeneral.transform(sentencesPath=self.general_corpus_path,
                                              savePath=self.filePaths["general_corpus_phrase"])

        # extract domain specific term
        # get vocab for domain specific
        with codecs.open(self.filePaths["domain_corpus_phrase"], mode="r", encoding="utf-8") as fr:
            domain_vocab = corpusToVocab(fr)
            with codecs.open(self.filePaths["domain_vocab"], mode="w", encoding="utf-8") as fw:
                fw.write(json.dumps(domain_vocab))

            # get vocab for general
        with codecs.open(self.filePaths["general_corpus_phrase"], mode="r", encoding="utf-8") as fr:
            general_vocab = corpusToVocab(fr)
            with codecs.open(self.filePaths["general_vocab"], mode="w", encoding="utf-8") as fw:
                fw.write(json.dumps(general_vocab))
        # get domain terms
        domain_terms = self.DomainSpecificTerm.extract_term(domainSpecificVocab=domain_vocab,
                                                            generalVocab=general_vocab)
        # save domain terms
        with codecs.open(self.filePaths["domain_terms"], mode="w", encoding="utf-8") as fw:
            fw.writelines([term + "\n" for term in domain_terms])

        # get semantic related words
        semantic_related_words = self.SemanticRelatedWords.getSemanticRelatedWords(terms=domain_terms)
        # save semantic_related_words
        with codecs.open(self.filePaths["semantic_related_words"], mode="w", encoding="utf-8") as fw:
            fw.write(json.dumps(semantic_related_words))
        # classify words
        origin_thesaurus = self.WordClassification.classifyWords(vocab=semantic_related_words)
        # save origin_thesaurus
        with codecs.open(self.filePaths["origin_thesaurus"], mode="w", encoding="utf-8") as fw:
            fw.write(json.dumps(origin_thesaurus))
        # froup synonyms and get final thesaurus
        final_thesaurus = self.SynonymGroup.group_synonyms(dst=origin_thesaurus)
        with codecs.open(self.filePaths["final_thesaurus"], mode="w", encoding="utf-8") as fw:
            fw.write(json.dumps(final_thesaurus))

if __name__ == "__main__":
    pass
