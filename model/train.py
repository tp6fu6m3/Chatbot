# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from gensim.models.callbacks import CallbackAny2Vec

import numpy as np
import matplotlib.pyplot as plt
import copy
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, default='wiki_seg.txt', help='input')
args = parser.parse_args()

class callback(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 1
        self.losses = []
        self.cumu_loss = 0.0
        self.previous_epoch_time = time.time()
        self.best_model = None
        self.best_loss = 1e+30

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        norms = [np.linalg.norm(v) for v in model.wv.vectors]
        now = time.time()
        epoch_seconds = now - self.previous_epoch_time
        self.previous_epoch_time = now
        self.cumu_loss += float(loss)
        print(f'Loss after epoch {self.epoch}: {loss} (cumulative loss so far: {self.cumu_loss}) '+\
              f'-> epoch took {round(epoch_seconds, 2)} s - vector norms min/avg/max: '+\
              f'{round(float(min(norms)), 2)}, {round(float(sum(norms)/len(norms)), 2)}, {round(float(max(norms)), 2)}')
        self.epoch += 1
        self.losses.append(float(loss))
        model.running_training_loss = 0.0
        if loss < self.best_loss:
            self.best_model = copy.deepcopy(model)
            self.best_loss = loss
        if self.epoch==5:
            self.plot('loss.png')

    def plot(self, path):
        fig, (ax1) = plt.subplots(ncols=1)
        ax1.plot(self.losses)
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend()
        plt.savefig(path)
        plt.close()

if __name__ == '__main__':
    sentences = LineSentence(args.input)
    model = Word2Vec(sentences, iter=10, size=100, min_count=1, 
        window=5, compute_loss=True, callbacks=[callback()])
    model.save('word2vec.model')
