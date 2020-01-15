import function as f

cal = f.Calc()

cal.you_can_use_words()

for i in range(100):
    word = input()
    print("別の文章の単語になる確率")
    print(cal.return_similar_noun(word,num=15))
    print("一つの文で共起する確率")
    print(cal.return_pair_word(word,num=15))