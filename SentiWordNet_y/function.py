#!/usr/bin/env python

"""
Interface to SentiWordNet using the NLTK WordNet classes.

---Chris Potts
"""

import re
import os
import sys
import codecs

try:
    from nltk.corpus import wordnet as wn
except ImportError:
    sys.stderr.write("Couldn't find an NLTK installation. To get it: http://www.nltk.org/.\n")
    sys.exit(2)

######################################################################

class SentiWordNetCorpusReader:
    def __init__(self, filename):
        """
        Argument:
        filename -- the name of the text file containing the
                    SentiWordNet database
        """        
        self.filename = filename
        # posとidでscoreがわかる
        self.db = {}
        # 入力:pos_scoreとneg_scoreの集合を返します
        # 出力:SentiSynsetを返す
        self.score_to_senti_synset = {}
        # 入力:synset
        # 出力:pos_score,neg_score
        self.synset_to_score = {}
        # 入力: word
        # 出力: pos
        self.word_to_pos = {}
        self.parse_src_file()

    # ファイルの捜査を行い、dbにデータを格納する。
    def parse_src_file(self):
        lines = codecs.open(self.filename, "r", "utf8").read().splitlines()
        lines = filter((lambda x : not re.search(r"^\s*#", x)), lines)
        for i, line in enumerate(lines):
            fields = re.split(r"\t+", line)
            fields = map(str.strip, fields)
            try:            
                #品詞,ID,好感情度,悪感情度,単語,使用例
                pos, offset, pos_score, neg_score, synset_terms, gloss = fields
            except:
                #ここで感情時点の形式が保証される
                sys.stderr.write("Line %s formatted incorrectly: %s\n" % (i, line))

            synset = wn._synset_from_pos_and_offset(pos, int(offset))
            # pos and offsetの意味はわからない。存在の確定？今の所これを満たさないものはなさそう
            if pos and offset:
                offset = int(offset)
                self.db[(pos, offset)] = (float(pos_score), float(neg_score))
            if pos_score and neg_score:
                if (pos_score, neg_score) not in self.score_to_senti_synset:
                    self.score_to_senti_synset[(pos_score, neg_score)] = []
                self.score_to_senti_synset[(pos_score, neg_score)].append(SentiSynset(pos_score,neg_score,synset))
                self.word_to_pos[SentiSynset(pos_score,neg_score,synset).name()] = pos
            if synset:
                self.synset_to_score[synset] = (pos_score, neg_score)

    # 単語からそれに相応するsenti_synsetを返したい

    def senti_synsets(self, word):
        ret = []
        for synset in wn.synsets(word):
            pos = synset.pos
            offset = synset.offset
            if (pos, offset) in self.db:
                pos_score, neg_score = self.db[(pos, offset)]
                ret.append(SentiSynset(pos_score, neg_score, synset))
        return ret

    # 全てのsynsetをだす。一つ一つはSentiSynsetに対応
    def all_senti_synsets(self):
        for key, fields in self.db.items():
            pos, offset = key
            pos_score, neg_score = fields
            synset = wn._synset_from_pos_and_offset(pos, offset)
            yield SentiSynset(pos_score, neg_score, synset)
    
    def similar_senti_words(self, word):
        words = []
        synsets = wn.synsets(word)
        pos = self.word_to_pos[word]
        if word not in self.word_to_pos:
            print("該当する単語はありません")
            return []
        else:
            print(word,"の品詞は",pos,"です")
        for synset in wn.synsets(word): 
            pos_score,neg_score = self.synset_to_score[synset]
            for senti_synset in self.score_to_senti_synset[(pos_score, neg_score)]:
                word = senti_synset.name()
                if word not in words and (pos == self.word_to_pos[word]):
                    words.append(word)
        return sorted(words)

    def antonym_senti_words(self,word):
        words = []
        synsets = wn.synsets(word)
        pos = self.word_to_pos[word]
        if word not in self.word_to_pos:
            print("該当する単語はありません")
            return []
        else:
            print(word,"の品詞は",pos,"です")
        for synset in wn.synsets(word): 
            neg_score,pos_score = self.synset_to_score[synset]
            for senti_synset in self.score_to_senti_synset[(pos_score, neg_score)]:
                word = senti_synset.name()
                if word not in words and (pos == self.word_to_pos[word]):
                    words.append(word)
        return sorted(words)


######################################################################
            
class SentiSynset:
    def __init__(self, pos_score, neg_score, synset):
        self.pos_score = float(pos_score)
        self.neg_score = float(neg_score)
        self.obj_score = 1.0 - (self.pos_score + self.neg_score)
        self.synset = synset
        

    def __str__(self):
        """Prints just the Pos/Neg scores for now."""
        s = ""
        s += self.synset.name() + "\t"
        s += "PosScore: %s\t" % self.pos_score
        s += "NegScore: %s" % self.neg_score
        return s
    
    def to_str(self):
        s = ""
        s += self.name + "\t"
        s += "PosScore: %s\t" % self.pos_score
        s += "NegScore: %s" % self.neg_score
        return s

    def name(self):
        return self.synset.lemma_names()[0]    

    def lemmas(self):
        ret = []
        for lemma in self.synset.lemma_names():
            ret.append(lemma)
        return ret
    def __repr__(self):
        return "Senti" + repr(self.synset)
                    
######################################################################        

if __name__ == "__main__":
    """
    If run as

    python sentiwordnet.py

    and the file is in this directory, send all of the SentiSynSet
    name, pos_score, neg_score trios to standard output.
    """
    SWN_FILENAME = "data/SentiWordNet_3.0.0.txt"
    if os.path.exists(SWN_FILENAME):
        swn = SentiWordNet(SWN_FILENAME)
        for senti_synset in swn.all_senti_synsets():
            print(senti_synset.synset.name, senti_synset.pos_score, senti_synset.neg_score)