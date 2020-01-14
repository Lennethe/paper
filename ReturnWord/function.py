import re

class Calc:
    # PMIに応じて単語を出すやつ
    def __init__(self):
        self.use_noun = []
        self.use_ad = []
        self.pair_noun = {}
        self.pair_sentence = {}
        self.res_noun = {}
        self.res_sentence = {}
        self.read_words()

    def you_can_use_words(self):
        print(self.use_noun)

    def return_similar_noun(self, word, num=10):
        if word not in self.pair_noun:
            return "ないよ"
        return self.pair_noun[word][0:num]
    
    def return_pair_word(self, word, num=10):
        if word not in self.pair_sentence:
            return "ないよ"
        return self.pair_sentence[word][0:num]    

    # private
    def read_words(self):
        for line in open("noun.txt"):
            x = line.split()
            self.use_noun.append(x[0].lower())
        for line in open("ad.txt"):
            x = line.split()
            self.use_ad.append(x[0].lower())
        
        for n in self.use_noun:
            self.pair_noun[n] = {}
            self.pair_sentence[n] = {}
        for a in self.use_ad:
            self.pair_sentence[a] = {}
        
        for line in open("pmi.txt"):
            x = re.split(r"\s|'", line)
            word1 = x[1]
            word2 = x[4]
            pmi = float(x[7])
            #self.pair_sentence[word1].append((word2, pmi))
            self.pair_sentence[word1][word2] = pmi
            #self.pair_sentence[word2].append((word1, pmi))
            self.pair_sentence[word2][word1] = pmi

        for line in open("pmi_noun.txt"):
            x = re.split(r"\s|'", line)
            noun1 = x[1]
            noun2 = x[4]
            pmi = float(x[7])
            #self.pair_noun[noun1].append((noun2,pmi))
            #self.pair_noun[noun2].append((noun1,pmi))
            self.pair_noun[noun1][noun2] = pmi
            self.pair_noun[noun2][noun1] = pmi        
        
        s = 0
        for noun in self.use_noun:
            s += 1
            print(noun)
            print(s, type([]))
            print(type(self.pair_sentence[noun]))
            if type(self.pair_sentence[noun]) == type([]):
                continue
            if type(self.pair_noun[noun]) == type([]):
                continue
            
            #self.pair_sentence[noun] = sorted(self.pair_sentence[noun].items(), key=lambda  x:x[1])
            self.pair_sentence[noun] = sorted(self.pair_sentence[noun].items(), key=lambda  x:x[1])
            self.pair_sentence[noun].reverse()
            self.pair_noun[noun] = sorted(self.pair_noun[noun].items(), key=lambda  x:x[1])
            self.pair_noun[noun].reverse()
        for ad in self.use_ad:
            if type(self.pair_sentence[ad]) == type([]):
                continue
            self.pair_sentence[ad] = sorted(self.pair_sentence[ad].items(), key=lambda  x:x[1])
            self.pair_sentence[ad].reverse()
            
        
        
        
