import math
from .matcher import Matcher

class QuickSearcher(object):
    def __init__(self, docs=None):
        self.inverted_word_dic = dict()

    def buildInvertedIndex(self, docs):
        for doc_id,doc in enumerate(docs):
            for word in doc:
                if word not in self.inverted_word_dic.keys():
                    self.inverted_word_dic[word] = set()
                self.inverted_word_dic[word].add(doc_id)

    def quickSearch(self, query):
        result = set()
        for word in query:
            if word in self.inverted_word_dic.keys():
                result = result.union(self.inverted_word_dic[word])
        return result

class bestMatching(Matcher):
    def __init__(self, segLib="Taiba", removeStopWords=False):
        super().__init__(segLib)
        self.cleanStopWords = removeStopWords
        self.D = 0

        self.wordset = set()
        self.words_location_record = dict()
        self.words_idf = dict()

        self.f = []
        self.df = {}
        self.idf = {}
        self.k1 = 1.5
        self.b = 0.75

        self.searcher = QuickSearcher()

        if removeStopWords:
            self.loadStopWords("../data/stopwords/chinese_sw.txt")
            self.loadStopWords("../data/stopwords/specialMarks.txt")

    def initialize(self,ngram=1):
        assert len(self.titles) > 0, "請先載入短語表"
        self.TitlesSegmentation() # 將 self.titles 斷詞為  self.segTitles
        
        self.D = len(self.segTitles)
        self.avgdl = sum([len(title) + 0.0 for title in self.segTitles]) / self.D

        for seg_title in self.segTitles:
            tmp = {}
            for word in seg_title:
                if not word in tmp:
                    tmp[word] = 0
                tmp[word] += 1
            self.f.append(tmp)
            for k, v in tmp.items():
                if k not in self.df:
                    self.df[k] = 0
                self.df[k] += 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D-v+0.5)-math.log(v+0.5)
        self.searcher.buildInvertedIndex(self.segTitles)


    def sim(self, doc, index):
        score = 0
        for word in doc:
            if word not in self.f[index]:
                continue
            d = len(self.segTitles[index])
            score += (self.idf[word]*self.f[index][word]*(self.k1+1)
                      / (self.f[index][word]+self.k1*(1-self.b+self.b*d
                                                      / self.avgdl)))
        return score

    def match(self, query):
        seg_query = self.wordSegmentation(query)
        max = -1
        target = ''
        target_idx = -1
        target_index = self.searcher.quickSearch(seg_query) #  只取出必要的 titles

        for index in target_index:
            score = self.sim(seg_query, index)
            if score > max:
                target_idx = index
                max = score

        # normalization
        max = max / self.sim(self.segTitles[target_idx],target_idx)
        target = ''.join(self.segTitles[target_idx])
        self.similarity = max * 100 #百分制
        return target,target_idx
