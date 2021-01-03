# -*- coding: utf-8 -*-
import logging
from gensim.models import word2vec

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, default='wiki_seg.txt', help='input')
args = parser.parse_args()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.LineSentence(args.input)
    model = word2vec.Word2Vec(sentences, size=250)
    model.save('word2vec.model')
