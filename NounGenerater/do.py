import csv
import pprint
import stanfordnlp
import function as f
import warnings
warnings.filterwarnings('ignore')
# たまには外してエラー文を見よう

#########
dic = {}
key = ["amod", "conj1", "nmod1", "nsubj1", "obj1", "obl1", "root1"] 
judge = ["pos"] #sentiが含んでいいやつ None,N,pos,negからなる
UP_LIMIT = 30
#nlp = stanfordnlp.Pipeline()
########


reviews = f.get_reviews(UP_LIMIT)

for x in range(UP_LIMIT):
    f.print_dep(reviews[x],key,judge)
