# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 02:03:02 2018

@author: Afnan
"""

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
csv.field_size_limit(100000000)

def word_count(str):
    counts = dict()
    words = str.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

train_x = pd.read_csv("place_bag_train0" + ".csv", sep=',', encoding = "ISO-8859-1", engine='python')
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(train_x['text'].values.astype('U')) 

text_list = train_x.text.tolist()
master_word_list = []
for element in text_list:
    array = word_count(element) # vector for that country
    i = 0
    for word in array:
        if word[0] not in master_word_list:
            master_word_list.append[word[0]]

master_word_list = sorted(master_word_list)
master_word_dict = {}
index = 0
for element in master_word_list:
    master_word_dict[element] = index
    index += 1

for element in text_list:
    array = word_count(element) # vector for that country
    for word in array:
        if word[0] in master_word_dict:
            word[0] = master_word_dict[word[0]]
    # Now feature vector is in coordinate points that we can graph and cluster
    x, y = zip(*array) # unpack a list of pairs into two tuples
    plt.plot(x,y)

plt.show()

