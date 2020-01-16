from NounGenerater import function as att_f
from ReturnWord import function as rw
from SearchSentence import function as sf
from NextSentencePredict import function as nexter
from StanfordNLP import function as sentiment

returnf = rw.Calc()
returnf.you_can_use_words()
searcher = sf.SearchEngine()

ATT_NUM = 3 # 想定される属性語の次の候補
EMO_NUM = 3 # 属性語と結びつきやすい評判語の候補数
STR_NUM = 5 # 検索された文章数
#候補となる文章は ATT_NUM * EMO_NUM * STR_NUM




###########
print("文章を入力してください")
input_sentence = input()

# attribute_word -> 属性語
# emotion -> 感情

# Stanford Sentiment Treeebank
att_words = att_f.sentence_to_atts(input_sentence)
emotion = sentiment.judge_emo(input_sentence)
print("Stanford Sentiment Treeebank")
print(att_words)
print(emotion)
print()
# ReturnWord
next_attribute_words = []
for att in att_words:
    next_attribute_words.extend(returnf.attribute_words(att_words, num=ATT_NUM))
print("Return Word1")
print(next_attribute_words)
print()
# 全ての単語がユニークであると仮定

# att_and_emo_pairs -> 属性語と評判語のペア

# ReturnWord
att_and_emo_pairs = []
for att_word in next_attribute_words:
    att_and_emo_pairs.extend(att_word, returnf.emotional_words(att_word, EMO_NUM))
print("Return Word2")
print(att_and_emo_pairs)
print()
# sentences -> 文章の候補
# SearchSentence 

sentences1 = []
for att, emo in att_and_emo_pairs:
    sentences1.extend(searcher.search(att,emo, num=STR_NUM))
print("Search Sentence")
print(sentences1)
print()
#TODO5 JudgeSentenceEmo
sentence2 = []
for sentence in sentences1:
    if emotion != sentiment.judge_emo(sentence):
        sentence2.append(sentence)

print("Judge Sentence Emo")
print(sentence2)
print()
# NextSentencePrediction
result = []
for sentence in sentences2:
    result.append(sentence, nexter.predictor(input_sentence, sentence))

print("Next Sentence Prediction")
print(result)
print()
#TODO7 自作
sort(result)

for v in result:
    print(v[0])
    print(v[1])
    print()
