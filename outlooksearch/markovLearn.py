import random
import MeCab
 
# MeCab使用してテキストデータを単語に分割する
def wakati(text):
    t = MeCab.Tagger("-Owakati")
    m = t.parse(text)
    result = m.rstrip(" \n").split(" ")
    return result
def markov(): 
    filename = "/Users/administrator/pythonWorkplace/mail_automation/test.text"
    src = open(filename, "r").read()
    wordlist = wakati(src)
 
    # マルコフ連鎖用のテーブルを作成する
    markov = {}
    w1 = ""
    w2 = ""
    for word in wordlist:
        if w1 and w2:
            if (w1, w2) not in markov:
                markov[(w1, w2)] = []
                #print('w1 not in markov ', w1)
                #print('w2 not in markov ', w2)
            markov[(w1, w2)].append(word)
            #print('w1 append:', w1)
            #print('w2 append:', w2)
        w1, w2 = w2, word
        #print('w1:', w1)
        #print('w2:', w2)
 
    # 文章の自動作成
    count = 0
    sentence = ""
    w1, w2  = random.choice(list(markov.keys()))
    while count < len(wordlist):
        tmp = random.choice(markov[(w1, w2)])
        sentence += tmp
        w1, w2 = w2, tmp
        count += 1
        if len(sentence)>250 and tmp=="。":
            break 
    return sentence