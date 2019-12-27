import stanfordnlp
 
# stanfordnlp.download('en')  # モデルのダウンロード(一回実行すれば、以降は不要)
 
# lang(仕様言語)とtreebank(ツリーバンク=コーパスの一種)を指定
nlp = stanfordnlp.Pipeline()
doc = nlp("Really lovely hotel. Stayed on the very top floor and were surprised by a Jacuzzi bath we didn't know we were getting! Staff were friendly and helpful and the included breakfast was great! Great location and great value for money. Didn't want to leave!")
doc.sentences[0].print_dependencies()

print('----------')
 
words = doc.sentences[0].words
word = ''
 
for w in words:
    word += w.text + ' '
 
print(word)