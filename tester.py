# 全部を実行するファイル
import nltk
from nltk.corpus import wordnet as wn
from NounGenerater.SentiWordNet_y.function import SentiWordNetCorpusReader, SentiSynset
swn_filename = 'NounGenerater/SentiWordNet_y/data/SentiWordNet_3.0.0.txt'
swn = SentiWordNetCorpusReader(swn_filename)

## 定数
SEARCH_LIM = 30
OUTPUT_WID = 6
##


print("SWN使用準備完了")
print("使用したいモードを選んで下さい")
print("1 -> 感情的反意語")
print("2 -> 単語の感情")
print("quit() - > 終了")

def main():
    inp = input()
    if inp == "1":
        print("感情的な反意語を出します")
        print("やめたい場合はquit()と入力して下さい")
        senti_anti()
    elif inp == "2":
        print("")
        check_senti()
    elif inp == "quit()":
        print("システムを終了します")
        print("お疲れ様でした")
        print()
    else:
        print("該当するモードはありません")
        print("使用したいモードを選んで下さい")
        print()
        main()

def check_senti():
    string = input()
    if string == "quit()":
        print("モード選択へ戻ります")
        main()
    else:
        print(swn.print_word_senti(string))
        print("次の単語を入力して下さい")
        check_senti()

### 入力したものに対して反対の感情を返す
def senti_anti():
    string = input()
    if string == "quit()":
        print("モード選択へ戻ります")
        main()
    else:
        words = swn.antonym_senti_words(string)
        if len(words) != 0:
            print("全部で",len(words),"あるので上位",min(SEARCH_LIM,len(words)),"件を表示します")
            idx = 0
            for j in range(OUTPUT_WID):
                print(words[idx:min(len(words),idx+OUTPUT_WID)])
                if len(words)<idx+OUTPUT_WID:
                    break
                idx+=OUTPUT_WID
        print()
        print("次の単語を入力して下さい")
        senti_anti()

main()