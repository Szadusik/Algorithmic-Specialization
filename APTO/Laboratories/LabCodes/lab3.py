import random

def generate_formula(n,k,a):
    res = []
    S = [1,-1]
    for i in range(a*n): #Generate one clause
        clause = []
        for j in range(k):
            v = range(1,n+1)
            clause.append(random.choice(v)*random.choice(S))
        res.append(clause)
    return res

def run_formula_tests(n,k,T):
    for i in range(T):
        for j in range(0,10,0.1):
            formula = generate_formula(n,k,j)

    return
if __name__ == '__main__':
    #print(generate_formula(5,3,4))