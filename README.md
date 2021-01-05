# Chatbot

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

## Repository Structure

```
Chatbot_seq2seq
├── data
│   ├── jieba_dict
│   │   ├── dict.txt.big
│   │   ├── stopword.txt
│   │   └── userdict.txt
│   ├── ptt
│   │   ├── 0.json
│   │   ├── ...
│   │   └── 248.json
│   ├── stopwords
│   │   ├── chinese_sw.txt
│   │   ├── gossiping.tag
│   │   ├── ptt_words.txt
│   │   └── specialMarks.txt
│   ├── SegTitles.txt
│   ├── Titles.txt
│   └── User_info.txt
├── log
│   └── match.txt
├── model
│   ├── segment.py
│   ├── train.py
│   └── wiki_to_txt.py
├── RuleMatcher
│   ├── rule
│   │   ├── alarm_rule.json
│   │   ├── entertainment.json
│   │   ├── hotel_locale_reason.json
│   │   ├── hotel_rules.json
│   │   ├── hotel_time_reason.json
│   │   ├── medical_description_reason.json
│   │   ├── medical_rules.json
│   │   ├── medical_subject_reason.json
│   │   ├── purchase_rules.json
│   │   └── rule.json
│   ├── answerer.py
│   ├── bestMatch.py
│   ├── evaluate.py
│   ├── matcher.py
│   └── rulebase.py
├── chatbot.py
├── console.py
├── demo.py
├── README.md
└── requirements.txt

```


