# -*- coding: utf-8 -*-
"""
@author: https://www.kaggle.com/antmarakis/word-count-and-naive-bayes/notebook, Afnan

Most code on this document is sourced from https://www.kaggle.com/antmarakis/word-count-and-naive-bayes/notebook
some adjustments were made by Afnan for use case
"""

import pandas as pd
import csv
from collections import Counter, defaultdict
from nltk.tokenize import word_tokenize
import decimal
from decimal import Decimal
csv.field_size_limit(100000000)
decimal.getcontext().prec = 1000

def create_dist(text):
    c = Counter(text)

    least_common = c.most_common()[-1][1]
    total = sum(c.values())
    
    for k, v in c.items():
        c[k] = v/total

    return defaultdict(lambda: min(c.values()), c)

def precise_product(numbers):
    result = 1
    for x in numbers:
        result *= Decimal(x)
    return result

def NaiveBayes(dist):
    """A simple naive bayes classifier that takes as input a dictionary of
    Counter distributions and can then be used to find the probability
    of a given item belonging to each class.
    The input dictionary is in the following form:
        ClassName: Counter"""
    attr_dist = {c_name: count_prob for c_name, count_prob in dist.items()}

    def predict(example):
        """Predict the probabilities for each class."""
        def class_prob(target, e):
            attr = attr_dist[target]
            return precise_product([attr[a] for a in e])

        pred = {t: class_prob(t, example) for t in dist.keys()}

        total = sum(pred.values())
        for k, v in pred.items():
            pred[k] = v / total

        return pred

    return predict


def recognize(sentence, nBS):
    try:
        return nBS(word_tokenize(sentence.lower()))
    except:
        return nBS("")

def predictions(test_x, nBS):
    d = []
    for index, row in test_x.iterrows():
        i, t = row['id'], row['text']
        p = recognize(t, nBS)
        d.append({'id': i, 'wheat': float(p['wheat']), 'earn': float(p['earn']), 'housing': float(p['housing'])})
    
    return pd.DataFrame(data=d)

train_x = pd.read_csv("topic_bag_train.csv", sep=',', encoding = "ISO-8859-1", engine='python')
test_x = pd.read_csv("topic_bag_test.csv", sep=',', encoding = "ISO-8859-1", engine='python')


canada, uk, pak = "", "", ""

for i, row in train_x.iterrows():
    a, t = row['topic'], row['text']
    if a == 'wheat':
        canada += " " + t.lower()
    elif a == 'earn':
        uk += " " + t.lower()
    elif a == 'housing':
        pak += " " + t.lower()
        
print (uk[:50])

canada = word_tokenize(canada)
uk = word_tokenize(uk)
pak = word_tokenize(pak)

print (uk[:50])
c_canada, c_uk, c_pak = create_dist(canada),  create_dist(uk),  create_dist(pak)

dist = {'wheat': c_canada, 'earn': c_uk, 'housing' : c_pak}
nBS = NaiveBayes(dist)


submission = predictions(test_x, nBS)
submission.to_csv('submission_topic.csv', index=False)
