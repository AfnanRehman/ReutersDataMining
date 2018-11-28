# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 02:03:02 2018

@author: Matthew Stock w/ Afnan's K-Means as a basis.
"""

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN
csv.field_size_limit(100000000)

# Import Weighted Bag of Words vector from previous lab.
train_x = pd.read_csv("place_bag_train0" + ".csv", sep=',', encoding = "ISO-8859-1", engine='python')

# Since word counts were programmed by hand in the last lab, we used the built-in sklearn library for it this time for brevity
vectorizer = CountVectorizer(stop_words='english')
# This will allow us to use numbers instead of our bag of words approach
X = vectorizer.fit_transform(train_x['text'].values.astype('U')) # Encoding modifier to account for nulls


model = DBSCAN(eps = 20, min_samples = 3, metric='euclidean', n_jobs = -1)
model.fit(X, y=None, sample_weight=None)

core_samples_mask = np.zeros_like(model.labels_, dtype=bool)
core_samples_mask[model.core_sample_indices_] = True
labels = model.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))

terms = vectorizer.get_feature_names()
print(model.labels_)
print(len(model.labels_))

unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
