import function as f

s = f.SearchEngine()

print("調べたい単語を入力して")
while(True):
    a = input()
    b = input()
    s.search(a,b)
