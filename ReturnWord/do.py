import function as f

cal = f.Calc()

cal.you_can_use_words()

for i in range(100):
    word = input()
    print("次の文章の属性語になる確率")
    print(cal.attribute_words(word,num=15))
    print("属性語と共起する属性語の確率")
    print(cal.emotional_words(word,num=15))