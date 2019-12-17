import sqlite3
conn = sqlite3.connect("wnjpn.db")

def SearchAntynumWords(word):

    # 問い合わせしたい単語がWordnetに存在するか確認する
    cur = conn.execute("select wordid from word where lemma='%s'" % word)
    word_id = 99999999  #temp 
    for row in cur:
        word_id = row[0]

    # Wordnetに存在する語であるかの判定
    if word_id==99999999:
        print("「%s」は、Wordnetに存在しない単語です。" % word)
        return
    else:
        print("【「%s」の類似語を出力します】\n" % word)

    # 入力された単語を含む概念を検索する
    cur = conn.execute("select synset from sense where wordid='%s'" % word_id)
    synsets = []
    for row in cur:
        synsets.append(row[0])
    
    # 概念に含まれる単語を検索して画面出力する
    no = 1
    for synset in synsets:
        cur1 = conn.execute("select name from synset where synset='%s'" % synset)
        for row1 in cur1:
            print("%sつめの概念 : %s" %(no, row1[0]))
        #cur2 = conn.execute("select synset1 from synlink where (synset2='%s' and link='syns')" % synset)
        #cur2 = conn.execute("select synset2 from synlink where (synset1='%s' and link='syns')" % synset)
        cur2 = conn.execute("select * from synlink where link='ants'" )
        
        sub_no = 1
        for row2 in cur2:
            print(sub_no)
            print("意味%s : %s" %(sub_no, row2[0]))
            sub_no += 1
        #cur3 = conn.execute("select wordid from sense where (synset='%s' and wordid!=%s)" % (synset,word_id))
        #sub_no = 1
        #for row3 in cur3:
        #    target_word_id = row3[0]
        #    cur3_1 = conn.execute("select lemma from word where wordid=%s" % target_word_id)
        #    for row3_1 in cur3_1:
        #        print("類義語%s : %s" % (sub_no, row3_1[0]))
        #        sub_no += 1
        #print("\n")
        #no += 1


# 特定の単語を入力とした時に、類義語を検索する関数
def SearchSimilarWords(word):

    # 問い合わせしたい単語がWordnetに存在するか確認する
    cur = conn.execute("select wordid from word where lemma='%s'" % word)
    word_id = 99999999  #temp 
    for row in cur:
        word_id = row[0]

    # Wordnetに存在する語であるかの判定
    if word_id==99999999:
        print("「%s」は、Wordnetに存在しない単語です。" % word)
        return
    else:
        print("【「%s」の類似語を出力します】\n" % word)

    # 入力された単語を含む概念を検索する
    cur = conn.execute("select synset from sense where wordid='%s'" % word_id)
    synsets = []
    for row in cur:
        synsets.append(row[0])

    # 概念に含まれる単語を検索して画面出力する
    no = 1
    for synset in synsets:
        cur1 = conn.execute("select name from synset where synset='%s'" % synset)
        for row1 in cur1:
            print("%sつめの概念 : %s" %(no, row1[0]))
        cur2 = conn.execute("select def from synset_def where (synset='%s' and lang='jpn')" % synset)
        sub_no = 1
        for row2 in cur2:
            print("意味%s : %s" %(sub_no, row2[0]))
            sub_no += 1
        cur3 = conn.execute("select wordid from sense where (synset='%s' and wordid!=%s)" % (synset,word_id))
        sub_no = 1
        for row3 in cur3:
            target_word_id = row3[0]
            cur3_1 = conn.execute("select lemma from word where wordid=%s" % target_word_id)
            for row3_1 in cur3_1:
                print("類義語%s : %s" % (sub_no, row3_1[0]))
                sub_no += 1
        print("\n")
        no += 1



def Out_hierarchy_duct():
    # 下位-上位の関係にある概念の抽出
    cur = conn.execute("select synset1,synset2 from synlink where link='hypo'")

    hierarchy_dict = {}  # key:下位語(String), value:上位語(String)

    for row in cur:
        b_term = row[0]
        n_term = row[1]

        if n_term not in hierarchy_dict:
            hierarchy_dict[n_term] = b_term
    return hierarchy_dict


# 特定の単語を入力とした時に、上位語を検索する関数
def SearchTopConceptWords(word, hierarchy_dict):

    # 問い合わせしたい単語がWordnetに存在するか確認する
    cur = conn.execute("select wordid from word where lemma='%s'" % word)
    word_id = 99999999  #temp 
    for row in cur:
        word_id = row[0]

    # Wordnetに存在する語であるかの判定
    if word_id==99999999:
        print("「%s」は、Wordnetに存在しない単語です。" % word)
        return
    else:
        print("【「%s」の最上位概念を出力します】\n" % word)

    # 入力された単語を含む概念を検索する
    cur = conn.execute("select synset from sense where wordid='%s'" % word_id)
    synsets = []
    for row in cur:
        synsets.append(row[0])

    # 概念に含まれる単語を検索して画面出力する
    no = 1
    for synset in synsets:
        cur1 = conn.execute("select name from synset where synset='%s'" % synset)
        for row1 in cur1:
            print("%sつめの概念 : %s" %(no, row1[0]))
        cur2 = conn.execute("select def from synset_def where (synset='%s' and lang='jpn')" % synset)
        sub_no = 1
        for row2 in cur2:
            print("意味%s : %s" %(sub_no, row2[0]))
            sub_no += 1

        # 上位語の検索部分
        b_term = ""
        while(synset in hierarchy_dict.keys()):
            synset = hierarchy_dict[synset]

        cur1 = conn.execute("select name from synset where synset='%s'" % synset)
        for row1 in cur1:
            print("最上位概念 : %s" % row1[0])

        cur2 = conn.execute("select def from synset_def where (synset='%s' and lang='jpn')" % synset)
        sub_no = 1
        for row2 in cur2:
            print("意味%s : %s" %(sub_no, row2[0]))
            sub_no += 1

        # 更新          
        print("\n")
        no += 1