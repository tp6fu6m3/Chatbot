# -*- coding: utf-8 -*-
import os
import jieba
import random

from RuleMatcher.rulebase import RuleBase

model_path = 'model/word2vec.model'
rule_path = 'RuleMatcher/rule/'
jieba_path = 'data/jieba_dict/'

class Console(object):
    def __init__(self):
        cur_dir = os.getcwd()
        curPath = os.path.dirname(__file__)
        os.chdir(curPath)
        
        self.init_jieba(jieba_path + 'dict.txt.big', jieba_path + 'userdict.txt')
        self.stopword = self.load_stopword(jieba_path + 'stopword.txt')
        self.rulebase = RuleBase()
        self.rulebase.load_model(model_path)
        self.rulebase.load_rules_from_dic(rule_path)
        print('[Console] Initialized successfully :>')
        os.chdir(cur_dir)

    def init_jieba(self, seg_dic, userdic):
        jieba.load_userdict(userdic)
        jieba.set_dictionary(seg_dic)
        with open(userdic,'r',encoding='utf-8') as input:
            for word in input:
                word = word.strip('\n')
                jieba.suggest_freq(word, True)

    def load_stopword(self, path):
        stopword_set = set()
        with open(path,'r',encoding='utf-8') as stopword_list:
            for sw in stopword_list:
                sw = sw.strip('\n')
                stopword_set.add(sw)
        return stopword_set

    def word_segment(self, sentence):
        words = jieba.cut(sentence, HMM=False)
        keyword = []
        for word in words:
            if word not in self.stopword:
                keyword.append(word)
        return keyword

    def rule_match(self, sentence, best_only=False, search_from=None, segmented=False):
        keyword = sentence if segmented else self.word_segment(sentence)
        result_list,path = self.rulebase.match(keyword,threshold=0.1,root=search_from)
        return [result_list[0], path] if best_only else [result_list, path]

    def get_response(self, rule_id):
        rule = self.rulebase.rules[rule_id]
        res_num = rule.has_response()
        return None if res_num == 0 else rule.response[random.randrange(0,res_num)]

    def write_output(self, org_speech, result, path):
        print('Case# ' + str(org_speech))
        print('------------------')
        for similarity, rule, matchee in result:
            str_sim = '%.4f' % similarity
            print(str_sim + '\t' + path + rule + '\t\t' + matchee)
        print('------------------')
