from math import floor
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.tag.perceptron import PerceptronTagger
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from utilities import DataClean
from utilities import load_data, cross_validate

tagger = PerceptronTagger()

class Sentiword:
    # def __init__(self):

    def fit(self, X, y):
        self.labels = list(set(y))
        self.labels.sort()
        return self

    def compute_score(self,sentence):
        taggedsentence = []
        sent_score = []
        taggedsentence.append(tagger.tag(sentence.split()))
        wnl = nltk.WordNetLemmatizer()
        for idx, words in enumerate(taggedsentence):
            for idx2, t in enumerate(words):
                newtag = ''
                lemmatizedsent = wnl.lemmatize(t[0])
                if t[1].startswith('NN'):
                    newtag = 'n'
                elif t[1].startswith('JJ'):
                    newtag = 'a'
                elif t[1].startswith('V'):
                    newtag = 'v'
                elif t[1].startswith('R'):
                    newtag = 'r'
                else:
                    newtag = ''
                if (newtag != ''):
                    synsets = list(swn.senti_synsets(lemmatizedsent, newtag))
                    score = 0.0
                    if (len(synsets) > 0):
                        for syn in synsets:
                            score += syn.pos_score() - syn.neg_score()
                        sent_score.append(score / len(synsets))
            if (len(sent_score)==0 or len(sent_score)==1):
                return (float(0.0))
            else:
                return (sum([word_score for word_score in sent_score]) / (len(sent_score)))

    def predict(self, X):
        scores = [self.compute_score(x) for x in X]
        scores_max = max(scores)
        scores_min = min(scores)
        scores_normalized = []
        num_labels = len(self.labels)
        for score in scores:
            norm_score = float(score - scores_min) / float(scores_max - scores_min)
            if norm_score == 1.0:
                norm_score -= 0.001
            elif norm_score == 0.0:
                norm_score += 0.001
            scores_normalized.append(norm_score)
        ypred = [self.labels[int(floor(score * num_labels))] for score in scores_normalized]
        return ypred


if __name__ == '__main__':
    ids, X, y = load_data("cornell")
    pipeline = Pipeline([
        ('cleaner', DataClean(clean_list=[
            ["[^a-z]", " "],  # only letters
            [" [ ]+", " "],  # remove extra spaces
        ], html_clean=True)),
        ('classifier', Sentiword()),
    ])
    cross_validate((X, y), pipeline, accuracy_score)
    
    # cornell -Rotten tomatoes
    # accuracy_score : 0.509938455158 +/- 0.00150353362297
    # Confusion Matrix
    #  [[  3.70000000e+01   7.52000000e+02   5.84200000e+03   4.22000000e+02  1.90000000e+01]
    #   [  8.30000000e+01   2.00400000e+03   2.31280000e+04   1.97800000e+03  8.00000000e+01]
    #   [  9.20000000e+01   2.40400000e+03   7.23050000e+04   4.55900000e+03  2.22000000e+02]
    #   [  1.50000000e+01   8.55000000e+02   2.65150000e+04   5.05700000e+03  4.85000000e+02]
    #   [  0.00000000e+00   1.70000000e+02   6.93900000e+03   1.91900000e+03  1.78000000e+02]]
    #
    # stanford - ImdB
    # accuracy_score : 0.56732 +/- 0.0341631614462
    #  Confusion Matrix
    #  [[ 8542.  3958.]
    #   [ 6859.  5641.]]
    