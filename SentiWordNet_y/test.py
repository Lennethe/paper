import nltk
from nltk.corpus import wordnet as wn
from function import SentiWordNetCorpusReader, SentiSynset
swn_filename = 'data/SentiWordNet_3.0.0.txt'
swn = SentiWordNetCorpusReader(swn_filename)

#print(swn.senti_synset('breakdown.n.03'))


#print(swn.score[(0.0,0.0)][0].__str__())


print(wn.synsets("able"))
print(swn.senti_synsets("able"))
print("33")
count = 0
for senti_synset in swn.all_senti_synsets():
    count += 1
    if count>1:
        break
    words = swn.similar_senti_words(senti_synset.name())
    for i in range(10):
        print(words[i])
    print(len(words))
    print()
    #print(senti_synset.synset.name, senti_synset.pos_score, senti_synset.neg_score)
#sentence = "Iphone6 camera is awesome for low light "
#token = nltk.word_tokenize(sentence)
#tagged = nltk.pos_tag(token)
#print(tagged)


