domain-thesaurus
================
Introduction
------------

**domain-thesaurus** is a python package offering a techniques of extracting domain-specific
thesaurus which is commonly used in *Natural Language Processing*.

Installation
------------

**domain-thesaurus** is tested to work under *Python 3.x*.
We will try to support *Python 2.x*.

Dependency requirements:

* gensim(>=3.6.0)
* networkx(>=2.1)

**domain-thesaurus** is currently available on the PyPi's repository and you can
install it via `pip`::

  pip install domain-thesaurus

If you prefer, you can clone it and run the setup.py file. Use the following
command to get a copy from GitHub::

 git clone https://github.com/DunZhang/DomainSpecificThesaurus.git


Usage
----------

A simple example::
    >>> dst = DomainThesaurus(domain_specific_corpus_path="your domain specific corpus path",
    >>>                       general_corpus_path="your general corpus path",
    >>>                       outputDir="path of output",
    >>>                       filePaths=None,
    >>>                       phrase_detection_domain="default",
    >>>                       phrase_detection_general="default",
    >>>                       domain_specific_term="default",
    >>>                       semantic_related_words="default",
    >>>                       word_classification="default",
    >>>                       synonym_group="default")
    >>> # extract domain thesauruss
    >>> dst.extract()

The code design is flexible, you can replace the default `function class` with your own `function class` to get a better
performance.


