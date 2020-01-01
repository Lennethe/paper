import csv
import pprint
import stanfordnlp
import function as f
import warnings
warnings.filterwarnings('ignore')
# たまには外してエラー文を見よう

#########
dic = {}
key = ["amod", "conj", "nmod", "nsubj", "obj", "obl"] 
key = [["nsubj"], ["obl"], ["obj"],["nmod"], ["conj", "root"], ["amod", "root"], ["amod", "conj"] ]
not_pair = False
judge = ["pos"] #sentiが含んでいいやつ None,N,pos,negからなる
UP_LIMIT = 30
#nlp = stanfordnlp.Pipeline()
########
#nlp = stanfordnlp.Pipeline()
#doc = nlp("Pleasant 10 min walk along the sea front to the Water Bus. restaurants etc. Hotel was comfortable breakfast was good - quite a variety. Room aircon didn't work very well. Take mosquito repelant!")
#doc.sentences[0].print_dependencies()
#####
reviews = f.get_reviews(UP_LIMIT)
posi = 0
amount = 0
for x in range(UP_LIMIT):
    posi += 1
    print(posi)
    arr = f.array_review_to_dep(reviews[x], judge, key, not_pair)
    amount += len(arr)
    for val in arr:
        print(val["pos1"]," -> ",val["word1"], " ", val["pos2"]," -> ",val["word2"])

print(amount)