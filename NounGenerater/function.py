import csv
import stanfordnlp
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

class Calc:
    # PMIを求めるにしろ、単語の出現確率、共起率を求める。
    # 
    def __init__(self):
        self.noun_counter = {}

    def count_noun(self, arr):
        for line in arr:
            word = out_noun(line)
            if word == "":
                continue
            if word not in self.noun_counter:
                self.noun_counter[word] = 0
            self.noun_counter[word] += 1

    def print_count_noun(self):
        sum = 0
        counter = sorted(self.noun_counter.items(), key=lambda x:x[1])
        counter.reverse()
        self.writer_arr(counter, 'noun.txt')
        for word_t in counter:
            print(word_t[0]," = ",word_t[1])
            sum += word_t[1]
        print("sum = ",sum)

    def writer_arr(self, counter, file_name):
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
