# Chatbot

## Introduction

This project built a chatbot with word2vec CBOW model by using (traditional) Chinese Wiki dataset.

## Quick Start

1. Clone and navigate to the downloaded repository. Further, install required pip packages.

```
git clone https://github.com/tp6fu6m3/Chatbot.git
cd Chatbot
pip3 install -r requirements.txt
```

2. Download Wiki data and transform it to `.txt` format

```
cd model
wget https://dumps.wikimedia.org/zhwiki/20201220/zhwiki-20201220-pages-articles.xml.bz2
python3 wiki_to_txt.py
```

3. Use Open Chinese Convert (OpenCC) to convert Simplified Chinese into Traditional Chinese

```
cd ../..
git clone https://github.com/BYVoid/OpenCC.git
cd OpenCC
make
make install
opencc --version
cd ../Chatbot/model
opencc -i wiki_texts.txt -o wiki_zh_tw.txt -c s2tw.json
```

4. Do word segmentation by `jieba`.

```
python3 segment.py
```

5. Train the model and save it as `word2vec.model`.

```
python3 train.py
cd ..
```

6. Demonstrate the chatbot with the well-trained model.

```
python3 demo.py
```
