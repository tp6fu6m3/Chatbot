
import argparse
from console import Console
from chatbot import Chatbot

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--chatbot', action='store_true', help='Chat with a bot')
args = parser.parse_args()

if args.chatbot:
    print('Press \'c\' if you wanna chat with a bot.')
    print('Press \'q\' if you wanna ask a question with a bot.')
    mode = input('[c/q]')
    chatbot = Chatbot(mode=='c')
    chatbot.run()
else:
    console = Console()
    while True:
        print('Calculate the similarity between word vectors.')
        sentence = input('Input a sentence:')
        res, path = console.rule_match(sentence)
        console.write_output(sentence, res, path)

