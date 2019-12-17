import sqlite3
conn = sqlite3.connect("wnjpn.db")

#('pos_def',)
#('link_def',)
#('synset_def',)
#('synset_ex',)
#('synset',)
#('synlink',)
#('ancestor',)
#('sense',)
#('word',) (id, lang, word, )
#('variant',)
#('xlink',)
x = 'xlink'

#cur = conn.execute("select * from %s limit 30" % x)
cur = conn.execute("select * from %s" % x)

count = 0
for row in cur:
    if count < 5:
        tmp = "|"
        for t in row:
            tmp += str(t) + "|"
        print(tmp)
    count+=1
    

print(count)

cur = conn.execute("PRAGMA TABLE_INFO(%s)" % x)
for row in cur:
    print(row)
