from collections import Counter
from math import sqrt
import numpy as np
from scipy.spatial.distance import euclidean
import nltk
from nltk.corpus import stopwords
from scipy import spatial
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import cdist


def LCSMetric(first, second):
    n = len(first)
    m = len(second)
    table = []
    res = 0
    for i in range(n + 1):
        table.append([])
        for j in range(m + 1):
            table[i].append(0)

    for i in range(n):
        for j in range(m):
            if first[i] == second[j]:
                table[i + 1][j + 1] = table[i][j] + 1
                res = max(res, table[i + 1][j + 1])

    return 1 - res / max(n, m)


def ngram(word, n):
    m = len(word)
    s = set()
    for i in range(m - n + 1):
        s.add(word[i:i + n])
    return s


def DICE(first, second):
    x = ngram(first, 2)
    y = ngram(second, 2)
    denominator = len(x) + len(y)
    counter = 0
    for el in x:
        if el in y:
            counter += 1

    return 2 * counter / denominator


def vecFromWord(word):
    unique = Counter(word)
    letters = set(unique)
    occurances = unique.values()
    res = 0
    for val in occurances:
        res += val**2

    return unique, letters, sqrt(res)


def cosDistance(first, second):
    x = vecFromWord(first)
    y = vecFromWord(second)
    sx = x[1]
    sy = y[1]
    occcurancesx = x[0]
    occcurancesy = y[0]
    both = sx.intersection(sy)
    res = 0
    for el in both:
        res += occcurancesx[el] * occcurancesy[el]

    res /= x[2]
    res /= y[2]
    return res


def DaviesBouldin(X, Y):
    n = len(np.bincount(Y))
    clusters = [X[Y == i] for i in range(n)]
    centroids = []
    for el in clusters:
        centroids.append(np.mean(el, axis=0))

    vars = [np.mean([euclidean(el, centroids[i]) for el in tab]) for i, tab in enumerate(clusters)]
    res = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            else:
                res.append((vars[i] + vars[j]) / euclidean(centroids[i], centroids[j]))

    val = np.max(res)/n
    return val


def createStopList(text):
    text = nltk.word_tokenize(text)
    stopw = set(stopwords.words('english'))
    stoplist = []
    for w in text:
        if w in stopw:
            stoplist.append(w)

    return stoplist


def createStopListv2(text): #Przeciwienstwo stoplisty
    text = nltk.word_tokenize(text)
    stopw = set(stopwords.words('english'))
    stoplist = []
    for w in text:
        if w not in stopw:
            stoplist.append(w)

    return stoplist


def maxDistance(points):
    if points.shape[0] <= 1:
        return 0
    elif points.shape[0] == 2:
        return ((points[0] - points[1])*(points[0] - points[1])).sum()
    else:
        samples = points[spatial.ConvexHull(points).vertices]
        return spatial.distance_matrix(samples, samples).max()


def Dunn(points, labels, centroidslength):
    unique = np.unique(labels)
    maxdistance = max(maxDistance(points[labels == el]) for el in unique)
    mindistance = centroidslength.min()
    return mindistance / maxdistance


def clusterization(text, metric, stoplist=None):
    text = text.copy()
    if stoplist is None:
        pass
    else:
        for i, s in enumerate(text):
            words = s.split()
            tab = []
            for el in words:
                if el not in stoplist:
                    tab.append(el)

            text[i] = " ".join(tab)

    clusteredtext = np.array(text, dtype=object).reshape(-1, 1)
    distancetable = cdist(clusteredtext, clusteredtext, metric=lambda first, second: metric(first[0], second[0]))
    scan = DBSCAN(eps=1, min_samples=2)
    res = scan.fit(distancetable).labels, distancetable
    return res
