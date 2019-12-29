import stanfordnlp

### INITIAL_VALUE
key = ["amod", "obl1", "nsubj1"] 

####
nlp = stanfordnlp.Pipeline()

def print_dep(sentence):
    nlp = stanfordnlp.Pipeline()
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


print('----------')

print_dep("We stayed here for four nights in October. The hotel staff were welcoming, friendly and helpful. Assisted in booking tickets for the opera. The rooms were clean and comfortable- good shower, light and airy rooms with windows you could open wide. Beds were comfortable. Plenty of choice for breakfast.Spa at hotel nearby which we used while we were there.")

# nsubj -> root, Staff friendly
# nsubj -> conj, breakfast great

# amod -> root, lovely hotel
# amod -> obl, top floar
# conj -> root

# 感情
# amod 形容詞修飾語 lovely,top (-> obl,root)
# conj 結合子 helpful,great


# amod -> root, Pleasant walk

# obl -> conj, surprised bath
# nsubj -> root, min walk ??
# nsubj -> root hotel comfortable
# root, friendly

#def fun(string):

#print(dir(doc.sentences[1]))
#doc.sentences[0].print_tokens()
#doc.sentences[0].print_words()

 
