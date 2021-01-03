# -*- coding: utf-8 -*-
import logging
from gensim.corpora import WikiCorpus

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, default='zhwiki-20201220-pages-articles.xml.bz2', help='input')
parser.add_argument('-o', '--output', type=str, default='wiki_texts.txt', help='output')
args = parser.parse_args()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    wiki_corpus = WikiCorpus(args.input, dictionary={})

    with open(args.output, 'w', encoding='utf-8') as output:
        for i, text in enumerate(wiki_corpus.get_texts()):
            output.write(' '.join(text) + '\n')
            if i % 10000 == 0:
                logging.info('已處理 {} 篇文章'.format(i))
