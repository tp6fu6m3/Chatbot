```
git clone https://github.com/tp6fu6m3/Chatbot.git
cd Chatbot
pip3 install -r requirements.txt
cd model
wget https://dumps.wikimedia.org/zhwiki/20201220/zhwiki-20201220-pages-articles.xml.bz2
python3 wiki_to_txt.py zhwiki-20201220-pages-articles.xml.bz2
cd ../..
```

```
git clone https://github.com/BYVoid/OpenCC.git
cd OpenCC
make
make install
opencc --version
cd ..
```

```
cd Chatbot/model
opencc -i wiki_texts.txt -o wiki_zh_tw.txt -c s2tw.json
python3 segment.py
python3 train.py
cd ..
python3 demo.py
```
