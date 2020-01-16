
from ReturnWord import function as rw
from SearchSentence import function as sf
from NextSentencePredict import function as nexter

returnf = rw.Calc()
returnf.you_can_use_words()
searcher = sf.SearchEngine()

ATT_NUM = 3 # 想定される属性語の次の候補
EMO_NUM = 3 # 属性語と結びつきやすい評判語の候補数
STR_NUM = 5 # 検索された文章数
#候補となる文章は ATT_NUM * EMO_NUM * STR_NUM




###########

input_sentence = input()

# attribute_word -> 属性語
# emotion -> 感情

#TODO1 Stanford Sentiment Treeebank
attribute_word, emotion = f.hoge(input_sentence)

# ReturnWord
next_attribute_words = returnf.attribute_words(attribute_word, num=ATT_NUM)
# 全ての単語がユニークであると仮定

# att_and_emo_pairs -> 属性語と評判語のペア

# ReturnWord
att_and_emo_pairs = []
for att_word in next_attribute_words:
    att_and_emo_pairs.extend(att_word, returnf.emotional_words(att_word, EMO_NUM))

# sentences -> 文章の候補
# SearchSentence 
sentences1　= []
for att, emo in att_and_emo_pairs:
    sentences1.extend(searcher.search(att,emo, num=STR_NUM))

#TODO5 JudgeSentenceEmo
for sentence in sentences1:
    if emo != f.hoge(sentence):
        sentence2.append(sentence)

# NextSentencePrediction
result = []
for sentence in sentences2:
    result.append(sentence, nexter.predictor(input_sentence, sentence))

#TODO7 自作
sort(result)

for v in result:
    print(v[0])
    print(v[1])
    print()
