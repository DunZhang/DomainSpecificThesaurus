



import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.getLogger("gensim").setLevel(logging.WARNING)

from gensim.models.phrases import Phrases
from gensim.models.word2vec import LineSentence
if __name__ == "__main__":
    logger.info("12312312321")
    tt = Phrases(LineSentence(open(file="E:/docs_data/cleanEng.txt",mode="r",encoding="utf-8")))
