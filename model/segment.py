# -*- coding: utf-8 -*-
import jieba
import logging

jieba_path = '../jieba_dict/'

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    jieba.set_dictionary(jieba_path + 'dict.txt.big')
    stopword_set = set()
    with open(jieba_path + 'stopwords.txt','r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))

    output = open('wiki_seg.txt', 'w', encoding='utf-8')
    with open('wiki_zh_tw.txt', 'r', encoding='utf-8') as content:
        for i, line in enumerate(content):
            words = jieba.cut(line.strip('\n'), cut_all=False)
            for word in words:
                if word not in stopword_set:
                    output.write(word + ' ')
            output.write('\n')
            if i % 10000 == 0:
                logging.info('已完成前 %d 行的斷詞'.format(i))
    output.close()

