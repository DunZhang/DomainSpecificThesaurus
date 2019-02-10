DomainThesaurus
================

Introduction
------------

**DomainThesaurus** is a python package offering a techniques of extracting domain-specific
thesaurus which is commonly used in *Natural Language Processing*. Here is one item of generated
thesaurus::

    { "internet explorer":
    {"abbreviation":["ie"],
    "synonym":["internet explorers", "internet explorere", "internetexplorer"],
    "other":["firefox","chrome","opera"]}
    }

Except for domain-specific thesaurus, the package also provides several useful modules,
for example, **DomainTerm** for extracting domain-specific term and **WordDiscrimination**
for discriminate words (e.g. abbreviation, synonyms).

Domain-Specific term
::::::::::::::::::::::::::::::

**DomainTerm** can automatically extract domain-specific terms from domain corpus.
For example, *Javascript* in the domain of  computer science and technology and *karush kuhn tucker* in
domain of mathematics.

Abbreviations and Synonyms
:::::::::::::::::::::::::::

The module **WordDiscrimination** can divide semantic-related words into different types.
The default module can recognize semantic related words as `abbreviation` and `synonym`. Note that,
in our module, the `synonym` means that two words are semantic related word and they are morphological similar.
For example, *ie* is the abbreviation of *internet explorer* and *javascripts* is
the synonym of *javascript*.

Installation
------------

**DomainThesaurus** is tested to work under `Python 3.x`. Please use it in `Python 3.x`.
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

If you don't have any datasets, you can copy and run this code:
https://github.com/DunZhang/DomainSpecificThesaurus/blob/master/docs/notebooks/domain_thesaurus.ipynb .
This code will automatically download datasets for you.
The code design is flexible, you can replace the default `function class` with your own `function class` to get a better
performance.
You can can find more usages in https://github.com/DunZhang/DomainSpecificThesaurus/blob/master/docs/notebooks

Acknowledgements
-----------------

In this project, we use `Levenshtein Distance` and `GoogleDriveDownloader` from https://pypi.org/project/jellyfish/
and  https://github.com/ndrplz/google-drive-downloader. Thanks for their code.
