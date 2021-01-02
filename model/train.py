# -*- coding: utf-8 -*-
import logging
from gensim.models import word2vec

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.LineSentence('wiki_seg.txt')
    model = word2vec.Word2Vec(sentences, size=250)
    model.save('word2vec.model')
