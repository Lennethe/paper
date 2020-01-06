import csv
import stanfordnlp
import math
from SentiWordNet_y.function import SentiWordNetCorpusReader, SentiSynset
swn_filename = 'SentiWordNet_y/data/SentiWordNet_3.0.0.txt'
swn = SentiWordNetCorpusReader(swn_filename)
nlp = stanfordnlp.Pipeline()
sub = {"i","we","a","the","you","it","us","due","with","of"}

## ファイル開く時用,private
def read_dic(row):
    key = 0
    res = {}
    for x in row:
        res[x] = key
        key += 1
    return res

# num分だけレビューを取ってきます
def get_reviews(num):
    res = []
    first = True
    with open('7282_1.csv') as f:
        reader = csv.reader(f)
        cnt = 0
        for row in reader:
            if first:
                first = False
                dic = read_dic(row)
                continue
            cnt += 1
            res.append(row[dic['reviews.text']])
            if cnt == num:
                return res

#ひとつの文章に着き、dependenceをだす。
def array_review_to_dep(sentence, judge, key, not_pair = True):
    doc = nlp(sentence)
    res = []
    for x in range(len(doc.sentences)):
        # doc.sentences[x].print_dependencies()
        words = doc.sentences[x].dependencies_string().splitlines()
        sentence = {}
        for i in range(len(words)):
            w = words[i].split("'")
            sentence[str(i+1)] = [w[1],w[3],w[5]]
        for i in range(len(words)):
            to = sentence[str(i+1)][1]
            if to not in sentence:
                continue
            if swn.print_word_senti(sentence[to][0].lower()) not in judge and swn.print_word_senti(sentence[str(i+1)][0].lower()) not in judge:
                continue
            pos1 = sentence[str(i+1)][2]
            pos2 = sentence[to][2]
            word1 = sentence[str(i+1)][0]
            word2 = sentence[to][0]
            if word1.lower() in sub or word2.lower() in sub:
                continue
            if pair_in_key(pos1, pos2, key, not_pair):
                tmp = {}
                tmp["pos1"] = pos1
                tmp["pos2"] = pos2
                tmp["word1"] = word1
                tmp["word2"] = word2
                res.append(tmp)
    return res

# nmodとかそういうのが含まれているかを判定
def pair_in_key(pos1, pos2, key, not_pair = True):
    if not_pair:
        return pos1 in key
    for x in key:
        if len(x) == 1:
            if pos1 == x[0] or pos2 == x[0]:
                return True
        else:
            if pos1 == x[0] and pos2 == x[1]:
                return True
    return False

def out_noun(line):
    noun = ["obl", "obj", "nsubj","nmod"]
    sub_pair = [("amod", "root"), ("conj","root"), ("amod", "conj")]
    if line["pos1"] in noun:
        return line["word1"]
    if line["pos2"] in noun:
        return line["word2"]
    if (line["pos1"],line["pos2"]) in sub_pair:
        return line["word2"]
    return ""

def out_ad(line):
    ad = ["amod"]
    sub_pair = [("obl","root"), ("conj","root"), ("nsubj","root"), ("nsubj", "conj")]
    if line["pos1"] in ad:
        return line["word1"]
    if line["pos2"] in ad:
        return line["word2"]
    if (line["pos1"],line["pos2"]) in sub_pair:
        return line["word2"]
    return ""

def calc_pmi(ab,a,b,num):
    if ab == 0:
        return 0    
    return math.log2(num*ab/a/b)

class Calc:
    # PMIを求めるにしろ、単語の出現確率、共起率を求める。
    # 
    def __init__(self):
        self.noun_counter = {}
        self.ad_counter = {}
        self.pair_noun_counter = {} # 共起した回数
        self.pair_noun_rate = {} # 共起率
        self.pair_counter = {} # 同じ文にあった確率
        self.pair_rate = {}
        self.use_noun = []
        self.use_ad = []
        self.error_log_calc_pmi = []
        self.error_log_calc_pmi_noun = []

    def read_words(self):
        for line in open("noun.txt"):
            x = line.split()
            if x[2] == "4":
                break
            self.use_noun.append(x[0].lower())
        for line in open("ad.txt"):
            x = line.split()
            if x[2] == "4":
                break
            self.use_ad.append(x[0].lower())
        
 
    def count_noun(self, arr):
        for line in arr:
            word = out_noun(line).lower()
            if word == "":
                continue
            if word not in self.noun_counter:
                self.noun_counter[word] = 0
            self.noun_counter[word] += 1
    
    def count_ad(self, arr):
        for line in arr:
            word = out_ad(line).lower()
            if word == "":
                continue
            if word not in self.ad_counter:
                self.ad_counter[word] = 0
            self.ad_counter[word] += 1
    
    def count_pmi_noun(self, arr):
        noun_words = []
        for line in arr:
            word = out_noun(line).lower()
            if word == "":
                continue
            noun_words.append(word)
        for i in range(0,(len(noun_words))):
            for j in range((i+1),(len(noun_words))):
                if (noun_words[i], noun_words[j]) not in self.pair_noun_counter:
                    self.pair_noun_counter[(noun_words[i], noun_words[j])] = 0
                    self.pair_noun_counter[(noun_words[j], noun_words[i])] = 0
                self.pair_noun_counter[(noun_words[i], noun_words[j])] += 1
                self.pair_noun_counter[(noun_words[j], noun_words[i])] += 1
    
    def count_pmi(self, arr):
        for line in arr:
            word1 = line["word1"].lower()
            word2 = line["word2"].lower()
            if (word1, word2) not in self.pair_counter:
                self.pair_counter[(word1, word2)] = 0
                self.pair_counter[(word2, word1)] = 0
            self.pair_counter[(word1, word2)] += 1
            self.pair_counter[(word2, word1)] += 1                           

    def print_count_noun(self):
        sum = 0
        counter = sorted(self.noun_counter.items(), key=lambda x:x[1])
        counter.reverse()
        for word_t in counter:
            print(word_t[0].lower()," = ",word_t[1])
            sum += word_t[1]
        print("sum = ",sum)

    def calc_pmi(self,num):
        for noun in self.use_noun:
            for ad in self.use_ad:
                if (noun,ad) not in self.pair_counter:
                    self.error_log_calc_pmi.append(noun + " " + ad + " " + "calc_pmi")                   
                    continue
                elif noun not in self.noun_counter:
                    self.error_log_calc_pmi.append(noun + " " + "calc_pmi")
                    continue
                elif ad not in self.ad_counter:
                    self.error_log_calc_pmi.append(ad + " " + "calc_pmi")
                    continue
                else:
                    self.error_log_calc_pmi.append("")
                ab = self.pair_counter[(noun,ad)]
                a = self.noun_counter[noun]
                b = self.ad_counter[ad]
                rate = calc_pmi(ab,a,b,num)
                self.pair_rate[(noun,ad)] = rate
    
    def calc_noun_pmi(self,num):
        for i in range(0,(len(self.use_noun))):
            for j in range((i+1), len(self.use_noun)):
                if (self.use_noun[i],self.use_noun[j]) not in self.pair_noun_counter:
                    self.error_log_calc_pmi_noun.append(self.use_noun[i] + " " + self.use_noun[j] + " " + "calc_pmi")
                    continue
                elif self.use_noun[i] not in self.noun_counter:
                    self.error_log_calc_pmi_noun.append(self.use_noun[i] + " " + "calc_pmi")
                    continue
                elif self.use_noun[j] not in self.noun_counter:
                    self.error_log_calc_pmi_noun.append(self.use_noun[j] + " " + "calc_pmi")
                    continue
                else:
                    self.error_log_calc_pmi_noun.append("")
                ab = self.pair_noun_counter[(self.use_noun[i], self.use_noun[j])]
                a = self.noun_counter[self.use_noun[i]]
                b = self.noun_counter[self.use_noun[j]]
                rate = calc_pmi(ab,a,b,num)
                self.pair_noun_rate[(self.use_noun[i],self.use_noun[j])] = rate

    def writer_pos(self, file_name, pos):
        if pos == "noun":
            counter = sorted(self.noun_counter.items(), key=lambda x:x[1])
            counter.reverse()
        elif pos == "ad":
            counter = sorted(self.ad_counter.items(), key=lambda x:x[1])
            counter.reverse()
        else:
            print("何も出力しませんでした")
            return 
        file = open(file_name, 'w')
        sum = 0
        for word_t in counter:
            file.write(word_t[0])
            file.write(" = ")
            file.write(str(word_t[1]))
            file.write("\n")
            sum += word_t[1]
        file.write("\n")
        file.write("sum = ")
        file.write(str(sum))
        file.close()
    
    def write_pmi(self, file_name):
        rates = sorted(self.pair_rate.items(), key=lambda  x:x[1])
        rates.reverse()
        file = open(file_name, 'w')
        for rate in rates:
            file.write(str(rate[0]))
            file.write(" = ")
            file.write(str(rate[1]))
            file.write("\n")
        file.close()

    def write_pmi_noun(self, file_name):
        rates = sorted(self.pair_noun_rate.items(), key=lambda  x:x[1])
        rates.reverse()
        file = open(file_name, 'w')
        for rate in rates:
            file.write(str(rate[0]))
            file.write(" = ")
            file.write(str(rate[1]))
            file.write("\n")
        file.close()

    def write_error_log(self):
        file = open("error_pmi", "w")
        for error in self.error_log_calc_pmi:
            file.write(error)
            file.write("\n")
        file.close()
        file = open("error_pmi_noun", "w")
        for error in self.error_log_calc_pmi_noun:
            file.write(error)
            file.write("\n")
        file.close()
        
 