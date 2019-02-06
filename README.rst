DomainThesaurus
================

Introduction
------------

**DomainThesaurus** is a python package offering a techniques of extracting domain-specific
thesaurus which is commonly used in *Natural Language Processing*. Here is one item of generated
thesaurus::

    { "javascript":
    {"abbreviation":["js"],
    "synonym":["javavscript", "javascriprt", "javasrcript", "javascripit"],
    "other":["coffeescript"]}
    }

Except for domain-specific thesaurus, the package also provide several useful modules,
for example, **DomainTerm** for extracting domain-specific term and **WordClassification**
for classifying words (e.g. abbreviation, synonyms).

Domain-Specific term
::::::::::::::::::::::::::::::

**DomainTerm** can automatically extract domain-specific terms from domain corpus.
For example, *Javascript* in computer science and technology and *karush kuhn tucker* in
mathematics.

Abbreviations and Synonyms
:::::::::::::::::::::::::::

The module **WordClassification** can divide semantic-related words into different types.
For example, *ie* is the abbreviation of *internet explorer* and *javascripts* is
the synonym of *javascript*.

Installation
------------

**DomainThesaurus** is tested to work under *Python 3.x*.
We will try to support *Python 2.x*.

Dependency requirements:

* gensim(>=3.6.0)
* networkx(>=2.1)

**DomainThesaurus** is currently available on the PyPi's repository and you can
install it via `pip`::

  pip install DomainThesaurus

If you prefer, you can clone it and run the setup.py file. Use the following
command to get a copy from GitHub::

 git clone https://github.com/DunZhang/DomainSpecificThesaurus.git


Usage
----------

A simple example::
    >>> dst = DomainThesaurus(domain_specific_corpus_path="your domain specific corpus path",
    >>>                       general_corpus_path="your general corpus path",
    >>>                       outputDir="path of output")
    >>> # extract domain thesauruss
    >>> dst.extract()

The code design is flexible, you can replace the default `function class` with your own `function class` to get a better
performance.
You can can find more usages in https://github.com/DunZhang/DomainSpecificThesaurus/blob/master/docs/notebooks

