import csv
import pprint
import stanfordnlp
import function as f

dic = {}
key = ["amod", "obl1", "nsubj1"] 
UP_LIMIT = 10
nlp = stanfordnlp.Pipeline()
#


reviews = f.get_reviews(UP_LIMIT)

for x in range(UP_LIMIT):
    f.print_dep(reviews[x],key,nlp)
