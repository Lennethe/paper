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
UP_LIMIT = 35000

WRITE_NOUN = False
WRITE_AD = True
noun_file_name = "noun1.txt"
ad_file_name = "ad.txt"

cal = f.Calc()
#nlp = stanfordnlp.Pipeline()
########
nlp = stanfordnlp.Pipeline()
doc = nlp("価格の割にはいろいろがっかりするホテルである。犬が自由に連れてこれるため常にロビーやエレベーターの中に犬がいる。＝匂いがある。　廊下も部屋もカーペットであるので匂いや汚れが気になる。スタッフはフレンドリーであるがそれ以上のものはない。場所はいいと思う。駅からは遠いが無料のトローリーバスがあるので便利。")
doc.sentences[0].print_dependencies()
#####
reviews = f.get_reviews(UP_LIMIT)
posi = 0
amount = 0
for x in range(UP_LIMIT):
    posi += 1
    print(posi)
    if reviews[x] == "":
        continue
    arr = f.array_review_to_dep(reviews[x], judge, key, not_pair)
    amount += len(arr)
    if WRITE_NOUN:
        cal.count_noun(arr)
    if WRITE_AD: 
        cal.count_ad(arr)
    #for val in arr:
    #    print(val["pos1"]," -> ",val["pos2"], " ", val["word1"]," -> ",val["word2"])

if WRITE_NOUN:
    cal.writer_pos(noun_file_name, "noun")
if WRITE_AD:
    cal.writer_pos(ad_file_name, "ad")
print(amount)