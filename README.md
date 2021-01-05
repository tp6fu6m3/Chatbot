# Chatbot

This repository contains a [**gensim**](https://github.com/RaRe-Technologies/gensim) implementation of word2vec CBOW model running on (traditional) [**Chinese Wiki dataset**](https://zh.wikipedia.org/wiki/Wikipedia:%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8B%E8%BD%BD).

We use PTT Gossiping as knowledge base of our system. By matching the most related article title with respect to user input, we choose the most confident response in the response set.

## Quick Start

1. Clone and navigate to the downloaded repository. Further, install required pip packages.

```
git clone https://github.com/tp6fu6m3/Chatbot.git
cd Chatbot
pip3 install -r requirements.txt
```

2. Download zhwiki dump progress on 2020/12/20.

```
cd model
wget https://dumps.wikimedia.org/zhwiki/20201220/zhwiki-20201220-pages-articles.xml.bz2
```

3. Transform the dump `.xml.bz2` file into `.txt` format. We only consider the articles whose contents are more than 50 words.

```
python3 wiki_to_txt.py
```

4. Use [**Open Chinese Convert**](https://github.com/BYVoid/OpenCC) to convert Simplified Chinese into Traditional Chinese.

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

5. Use [**jieba**](https://github.com/fxsjy/jieba) to conduct word segmentation with our own dictionary and stopwords.

```
python3 segment.py
```

6. Train the model and save it as `word2vec.model`.

```
python3 train.py
cd ..
```

7. Demonstrate the chatbot with the well-trained model.

```
python3 demo.py
```
- `-r` or `--relation` : calculate cosine similarity between word vectors  

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


