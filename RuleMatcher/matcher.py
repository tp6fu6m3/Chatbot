import logging
import os
import jieba

class Matcher(object):
    def __init__(self, segLib='jieba'):
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
        self.titles = []
        self.segTitles = []

        self.stopwords = set()
        self.similarity = 1.

        if segLib == 'Taiba':
            self.useTaiba = True
        else:
            self.useTaiba = False

    def jiebaCustomSetting(self, dict_path, usr_dict_path):
        jieba.set_dictionary(dict_path)
        with open(usr_dict_path, 'r', encoding='utf-8') as dic:
            for word in dic:
                jieba.add_word(word.strip('\n'))

    def loadStopWords(self, path):
        with open(path, 'r', encoding='utf-8') as sw:
            for word in sw:
                self.stopwords.add(word.strip('\n'))

    def loadTitles(self, path):
        with open(path,'r',encoding='utf-8') as data:
            self.titles = [line.strip('\n') for line in data]

    def match(self, query):
        result = None
        for index, title in enumerate(self.titles):
            if title == query:
                return title,index

    def getSimilarity(self):
        return self.similarity

    def wordSegmentation(self, string):
        return [word for word in jieba.cut(string,cut_all=True)]

    def TitlesSegmentation(self, cleanStopwords=False):
        if not os.path.exists(self.path + '/data/SegTitles.txt'):
            count = 0
            self.segTitles = []
            for title in self.titles:
                if cleanStopwords:
                    clean = [word for word in self.wordSegmentation(title)
                            if word not in self.stopwords]
                    self.segTitles.append(clean)
                else:
                    self.segTitles.append(self.wordSegmentation(title))
                count += 1
            logging.info('已斷詞完 %d 篇文章' % count)
            with open(self.path + '/data/SegTitles.txt','w',encoding='utf-8') as seg_title:
                for title in self.segTitles:
                    seg_title.write(' '.join(title) + '\n')
            logging.info('完成標題斷詞，結果已暫存至 data/SegTitles.txt')
        else:
            with open(self.path + '/data/SegTitles.txt','r',encoding='utf-8') as seg_title:
                for line in seg_title:
                    line = line.strip('\n')
                    seg = line.split()

                    if cleanStopwords:
                        seg = [word for word in seg
                               if word not in self.stopwords]
                    self.segTitles.append(seg)
                logging.info('%d 個標題已完成載入' % len(self.segTitles))
