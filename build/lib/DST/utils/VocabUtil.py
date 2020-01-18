from collections import defaultdict
def corpusToVocab(sentences):
    vocab = defaultdict(int)
    for line in sentences:
        for word in line.split():
            vocab[word] += 1
    return vocab
