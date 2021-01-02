# coding=utf-8

import json
import logging
import os
import random

from .bestMatch import bestMatching
from .evaluate import Evaluator

class Answerer(object):
    def __init__(self):
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        self.matcher = bestMatching()
        self.matcher.loadTitles(self.path + '/data/Titles.txt')
        self.matcher.initialize()
        self.evaluator = Evaluator()
        self.moduleTest()

    def moduleTest(self):
        try:
            self.matcher.wordSegmentation('測試一下斷詞')
        except Exception as e:
            logging.info(repr(e))
            logging.info('模塊載入失敗，請確認data與字典齊全')

    def getResponse(self, sentence):
        _, index = self.matcher.match(sentence)
        jsonFile = open(self.path+'/data/ptt/'+str(index//1000)+'.json','r',encoding='utf-8')
        res = json.load(jsonFile)
        candiates = self.evaluator.getBestResponse(res[index%1000], topk=3)
        
        reply = random.choice(candiates)
        sim = self.matcher.getSimilarity()
        return reply[0],sim
