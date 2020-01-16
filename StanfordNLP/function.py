from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')



def judge_emo(sentence):
    res = nlp.annotate(sentence ,
                    properties={
                        'annotators': 'sentiment',
                        'outputFormat': 'json',
                        'timeout': 1000,
                    })
    for s in res["sentences"]:
        return s["sentiment"]