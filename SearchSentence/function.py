import csv
import re

def read_dic(row):
    key = 0
    res = {}
    for x in row:
        res[x] = key
        key += 1
    return res

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

class SearchEngine:

    def __init__(self):
        self.reviews = get_reviews(35000)

    def search(self,w1,w2):
        review_num = 0
        for review in self.reviews:
            review_num += 1
            sentences = re.split(r"\.|!", review)
            for sentence in sentences:
                f_w1 = False
                f_w2 = False
                for word in sentence.split():
                    if w1 == word:
                        f_w1 = True
                    if w2 == word:
                        f_w2 = True
                if f_w1 and f_w2:
                    print(sentence, review_num)
        print("次の単語を入力してください")
#            words = review.split()
 #           for word in words:
  #              w = word.lower()
