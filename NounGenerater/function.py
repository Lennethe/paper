import csv
import stanfordnlp


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

#dependenceをだす
def print_dep(sentence, key, nlp):
    doc = nlp(sentence)
    for x in range(len(doc.sentences)):
        # doc.sentences[x].print_dependencies()
        words = doc.sentences[x].dependencies_string().splitlines()
        sentence = {}
        for i in range(len(words)):
            w = words[i].split("'")
            sentence[str(i+1)] = [w[1],w[3],w[5]]
        for i in range(len(words)):
            to = sentence[str(i+1)][1]
            if sentence[str(i+1)][2] in key:
                print(sentence[str(i+1)][2]," -> ",sentence[to][2], " ", sentence[str(i+1)][0]+" -> "+sentence[to][0])
