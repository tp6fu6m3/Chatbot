# -*- coding: utf-8 -*-
import os
import random

from console import Console
from RuleMatcher.answerer import Answerer

class Chatbot(object):
    def __init__(self, isChat):
        self.speech_domain = ''      # The domain of speech.
        self.root_domain = None      # The root domain of user's input.
        self.isChat = isChat
        if isChat:
            self.console = Console()
        self.answerer = Answerer()

        self.default_response = [
            '是嗎?', 
            '有道理', 
            '我認同', 
            '我不太明白你的意思', 
            '原來如此'
        ]

    def run(self):
        print('Hello, I am ChiChi')
        while True:
            """
            first, if the sentence is like a question, retrun qa_response
            second, match the sentence with our rules
            third, if the sentence is not like chatting, retrun qa_response
            last, retrun default_response
            """
            sentence = input()
            qa_threshold = 35 if self.isChat else 0
            
            qa_response, qa_sim = self.answerer.getResponse(sentence)
            if qa_sim <= qa_threshold:
                qa_response, qa_sim = (random.choice(self.default_response), 0)
            
            if not self.isChat:
                print('%s (confident rate:%d)' % (qa_response, qa_sim))
            elif qa_sim > 60:
                print(qa_response)
            elif self.rule_match(sentence, threshold=0.4):
                response = self.console.get_response(self.speech_domain)
                print(response) if response else print(qa_response)
            elif qa_sim > qa_threshold:
                print(qa_response)
            else:
                print(random.choice(self.default_response))

    def rule_match(self, speech, threshold):
        (domain_similarity, self.speech_domain, _), last_path = self.console.rule_match(speech, best_only=True)
        self.root_domain = self.speech_domain if last_path == '' else last_path.split('>')[0]
        return domain_similarity >= threshold

