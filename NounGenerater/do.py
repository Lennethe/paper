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

# どれか一個だけTrueにしたほうがいい
WRITE_NOUN = False
WRITE_AD = False
WRITE_PMI = True

noun_file_name = "noun1.txt"
ad_file_name = "ad.txt"
pmi_file_name = "pmi.txt"
pmi_noun_file_name = "pmi_noun.txt"
cal = f.Calc()
cal.read_words()

#nlp = stanfordnlp.Pipeline()
########
nlp = stanfordnlp.Pipeline()
doc = nlp("This film doesn't care about cleverness, wit or any other kind of intelligent humor.")
doc.sentences[0].print_dependencies()
x = 3/0
#####
reviews = f.get_reviews(UP_LIMIT)
posi = 0
amount = 0

# PMI感情する名刺を登録
cal.read_words()

# 一つあたりの文章をみる
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
    if WRITE_PMI:
        cal.count_noun(arr)
        cal.count_ad(arr)
        cal.count_pmi(arr)
        cal.count_pmi_noun(arr)
    #for val in arr:
    #    print(val["pos1"]," -> ",val["pos2"], " ", val["word1"]," -> ",val["word2"])


if WRITE_NOUN:
    cal.writer_pos(noun_file_name, "noun")
if WRITE_AD:
    cal.writer_pos(ad_file_name, "ad")
if WRITE_PMI:
    cal.calc_pmi(amount)
    cal.calc_noun_pmi(UP_LIMIT)
    cal.write_pmi(pmi_file_name)
    cal.write_pmi_noun(pmi_noun_file_name)
    cal.write_error_log()
print(amount)