from itertools import *
from dimacs import *
import random

def VC(G, k):
    for el in combinations(range(len(G)), k):
        if isVC(edgeList(G),el):
            return el

    return None

def clearEdges(G,u):
    for el in G:
        el.remove(u)
    G[u].clear()
    return G

def betterVC(G,k,S):
    if k < 0:
        return None

    if len(edgeList(G)) == 0:
        return S

    if k == 0:
        return None

    V = list(range(1,len(G)))
    for u in V:
        if u not in S:
            chosen = u
            break

    v = random.choice(G[chosen])
    GU = G.copy()
    GV = G.copy()

    for el in GU:
        el.remove(chosen)
    GU[chosen].clear()

    for el in GV:
        el.remove(v)

    GU[v].clear(0)

    S1 = betterVC(GU,k-1,S + [chosen])
    S2 = betterVC(GV,k-1,S + [v])

    if S1:
        return S1
    else:
        return S2

if __name__ == '__main__':
    G = loadGraph('graph/e20')
    V = len(G)
    E = edgeList(G)
    # for i in range(1,V):
    #     res = VC(G, i)
    #     if res is not None:
    #         saveSolution('res.sol', res)
    #         break
    best = list(range(1,V-1))
    for i in range(V-1,0,-1):
        res = betterVC(G,i,[])
        if res is not None:
            best = res

    print(best)

