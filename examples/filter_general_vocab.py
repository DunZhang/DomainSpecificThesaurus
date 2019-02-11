import json
import codecs

if __name__ == "__main__":
    with codecs.open("E:/docs_data1/general_vocab.json","r",encoding="utf-8") as fr:
        origin_vocab=json.loads(fr.read())

    new_vocab={}
    for k,v in origin_vocab.items():
        if v>7:
            new_vocab[k]=v
    print(len(origin_vocab),len(new_vocab))
    with codecs.open("E:/docs_data1/general_vocabb.json","w",encoding="utf-8") as fw:
        json.dump(new_vocab,fw)