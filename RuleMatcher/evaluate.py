import logging
import os
import math

from collections import defaultdict
from gensim import corpora
from .matcher import Matcher

class Evaluator(Matcher):
    def __init__(self,segLib='Taiba'):
        super().__init__(segLib)
        self.responses = []
        self.segResponses = []
        self.totalWords = 0

        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        self.debugLog = open(self.path + '/log/evaluate.txt','w',encoding='utf-8')

        self.filteredWords = set()
        self.counterDictionary = defaultdict(int)
        self.tokenDictionary = None

        # 中文停用詞與特殊符號加載
        self.loadStopWords(path=self.path + '/data/stopwords/chinese_sw.txt')
        self.loadStopWords(path=self.path + '/data/stopwords/specialMarks.txt')
        self.loadFilterdWord(path=self.path + '/data/stopwords/ptt_words.txt')

    def getBestResponse(self, responses, topk, debugMode=False):
        self.responses = []
        self.segResponses = []
        self.totalWords = 0
        
        self.buildResponses(responses)
        self.segmentResponse()
        self.buildCounterDictionary()
        candiateList = self.evaluateByGrade(topk, debug=debugMode)
        return candiateList

    def loadFilterdWord(self,path):
        with open(path, 'r', encoding='utf-8') as sw:
            for word in sw:
                self.filteredWords.add(word.strip('\n'))

    def buildResponses(self, responses):
        self.responses = []
        for response in responses:
            clean = True
            r = response['Content']
            for word in self.filteredWords:
                if word in r:
                    clean = False
            if clean:
                self.responses.append(response['Content'])

    def segmentResponse(self):
        self.segResponses = []
        for response in self.responses:
            keywordResponse = [keyword for keyword in self.wordSegmentation(response)
                               if keyword not in self.stopwords
                               and keyword != ' ']
            self.totalWords += len(keywordResponse)
            self.segResponses.append(keywordResponse)

    def buildCounterDictionary(self):
        for reply in self.segResponses:
            for word in reply:
                self.counterDictionary[word] += 1

    def buildTokenDictionary(self):
        self.tokenDictionary = corpora.Dictionary(self.segResponses)
        logging.info('詞袋字典建置完成，%s' % str(self.tokenDictionary))

    def evaluateByGrade(self,topk,debug=False):
        bestResponse = ''
        candiates = []
        default = [
            ['是嗎?', 0], 
            ['有道理', 0], 
            ['我認同', 0], 
            ['我不太明白你的意思', 0], 
            ['原來如此', 0]
        ]

        try:
            if self.totalWords==0:
                return default
            else:
                avgWords = self.totalWords/len(self.segResponses)
        except ZeroDivisionError as z:
            print(z)
            print(self.totalWords)
            print(len(self.segResponses))

        for i in range(0, len(self.segResponses)):
            wordCount = len(self.segResponses[i])
            sourceCount = len(self.responses[i])
            meanful = 0

            if wordCount == 0 or sourceCount > 24:
                continue

            cur_grade = 0.

            for word in self.segResponses[i]:
                wordWeight = self.counterDictionary[word]
                if wordWeight > 1:
                    meanful += math.log(wordWeight,10)
                cur_grade += wordWeight

            try:
                if avgWords==1:
                    cur_grade = 0
                else:
                    cur_grade = cur_grade * meanful / (math.log(len(self.segResponses[i])+1,avgWords) + 1)
            except ZeroDivisionError as z:
                print(z)
                print(len(self.segResponses[i]))
                print(avgWords)
            candiates.append([self.responses[i],cur_grade])

            if debug:
                result = self.responses[i] + '\t' + str(self.segResponses[i]) + '\t' + str(cur_grade)
                self.debugLog.write(result+'\n')
                print(result)

        candiates = sorted(candiates,key=lambda candiate:candiate[1],reverse=True)
        if len(candiates)==0:
            return default
        else:
            return candiates[:topk]

