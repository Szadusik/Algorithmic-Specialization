from dimacs import *
import random
from os import listdir
from os.path import isfile, join

def first(G):
    E = edgeList(G)
    res = []
    while len(E) > 0:
        u,v = random.choice(E)
        copy = []
        for el in E:
            if u == el[0] or v == el[0] or u == el[1] or v == el[1]:
                continue
            else:
                copy.append(el)
        res.append(u)
        res.append(v)
        E = copy

    return res

def second(G):
    # dominant ->(vertex , degree)
    V = len(G)
    res = []
    while len(edgeList(G)) > 0:
        dominant = (0, 0)
        for i in range(V):
            if len(G[i]) > dominant[1]:
                dominant = (i,len(G[i]))

        for el in G[dominant[0]]:
            G[el].remove(dominant[0])

        G[dominant[0]].clear()
        res.append(dominant[0])

    return res


if __name__ == '__main__':
    G = loadGraph('graph/k330_a')
    onlyFiles = [f for f in listdir("graph") if isfile(join("graph", f))]
    for el in onlyFiles:
        G = loadGraph("graph/" + el)
        print("2Approx - " + el + " : " + str(len(first(G))))
        print("LogApprox - " + el + " : " + str(len(second(G))))
