# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 00:33:51 2018

@author: Afnan
"""
import pandas as pd
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
csv.field_size_limit(100000000) # Increase field limit to account for large field size

#We use training and test data from lab 2 to cluster and test the results
train_x = pd.read_csv("place_bag_train0" + ".csv", sep=',', encoding = "ISO-8859-1", engine='python')

# Since word counts were programmed by hand in the last lab, we used the built-in sklearn library for it this time for brevity
vectorizer = CountVectorizer(stop_words='english')
# This will allow us to use numbers instead of our bag of words approach
X = vectorizer.fit_transform(train_x['text'].values.astype('U')) # Encoding modifier to account for nulls

# We use the nifty K-means cluster built into sklearn as well here
# K = 147, or the number of countries we are wroking with
model = KMeans(n_clusters=147, init='k-means++', max_iter=300, n_init=1)
model.fit(X)

print("Top terms per cluster:")
# Finding centroids and sorting them
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

# Here, I print the clusters and their top centroids out, in order to see how words from the vectors are being clustered
for i in range(147):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])

print("\n")
print("Prediction")

# Here we import some premade vectors from our lab 2 solution to use for testing our clustering prediction
test_x = pd.read_csv("place_bag_test0" + ".csv", sep=',', encoding = "ISO-8859-1", engine='python')

Y = vectorizer.transform(test_x['text'].values.astype('U'))
prediction = model.predict(Y)
print(prediction)
print(test_x['id'])