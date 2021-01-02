# -*- coding: utf-8 -*-
import logging
import sys
from gensim.corpora import WikiCorpus

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Usage: python3 {} wiki_data_path'.format(sys.argv[0]))
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    wiki_corpus = WikiCorpus(sys.argv[1], dictionary={})

    with open('wiki_texts.txt','w',encoding='utf-8') as output:
        for i, text in enumerate(wiki_corpus.get_texts()):
            output.write(' '.join(text) + '\n')
            if i % 10000 == 0:
                logging.info('已處理 {} 篇文章'.format(i))
