
import argparse
from console import Console
from chatbot import Chatbot

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--relation', action='store_true'
    , help='Use relation mode to calculate cosine similarity between word vectors.')
args = parser.parse_args()

if args.relation:
    console = Console()
    while True:
        print('Calculate the similarity between word vectors.')
        sentence = input('Input a sentence:')
        res, path = console.rule_match(sentence)
        console.write_output(sentence, res, path)
else:
    print('Press \'c\' if you wanna chat with a bot.')
    print('Press \'q\' if you wanna ask a question with a bot.')
    mode = input('[c/q]')
    chatbot = Chatbot(mode=='c')
    chatbot.run()
