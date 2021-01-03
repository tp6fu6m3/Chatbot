# -*- coding: utf-8 -*-
import os
import jieba
import logging

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, default='wiki_zh_tw.txt', help='input')
parser.add_argument('-o', '--output', type=str, default='wiki_seg.txt', help='output')
args = parser.parse_args()

jieba_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/data/jieba_dict/'

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    jieba.set_dictionary(jieba_path + 'dict.txt.big')
    stopword_set = set()
    with open(jieba_path + 'stopword.txt', 'r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))

    output = open(args.output, 'w', encoding='utf-8')
    with open(args.input, 'r', encoding='utf-8') as content:
        for i, line in enumerate(content):
            words = jieba.cut(line.strip('\n'), cut_all=False)
            for word in words:
                if word not in stopword_set:
                    output.write(word + ' ')
            output.write('\n')
            if i % 10000 == 0:
                logging.info('已完成前{}行的斷詞'.format(i))
    output.close()

