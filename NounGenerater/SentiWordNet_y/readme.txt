
SentiWordNet

pos: 品詞
offset: ID
pos_score:好感度
neg_score:悪感度 
synset_terms:単語
gloss:使用例

synset: (概念.品詞.数)
wn._synset_from_pos_and_offset(pos,offset)
.antonyms() => 
.hypernyms() => 類義語
.definition()
.lemma_names()


SentiSynset(pos_score, neg_score, synset)

    def senti_synset(self, *vals):        
        if tuple(vals) in self.db:
            pos_score, neg_score = self.db[tuple(vals)]
            pos, offset = vals
            synset = wn._synset_from_pos_and_offset(pos, offset)
            return SentiSynset(pos_score, neg_score, synset)
        else:
            synset = wn.synset(vals[0])
            pos = synset.pos
            offset = synset.offset
            if (pos, offset) in self.db:
                pos_score, neg_score = self.db[(pos, offset)]
                return SentiSynset(pos_score, neg_score, synset)
            else:
                return None

    def senti_synsets(self, string, pos=None):
        sentis = []
        synset_list = wn.synsets(string, pos)
        for synset in synset_list:
            sentis.append(self.senti_synset(synset.name))
        sentis = filter(lambda x : x, sentis)
        return sentis

