from random import random
from spacy.lang.pl import Polish
from spacy.tokenizer import Tokenizer


class Node:
    def __init__(self, steps):
        self.steps = steps
        self.parent = None
        self.todo = 'Stay'


def editDistance(first, second):
    n = len(first)
    m = len(second)
    operations = ['Stay', 'Change', 'Insert', 'Delete']
    table = []
    for i in range(n + 1):
        table.append([])
        for j in range(m + 1):
            table[i].append(Node(0))

    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                table[0][j].parent = table[0][j - 1]
                table[0][j].steps = j
                table[0][j].todo = operations[2]
            elif j == 0:
                table[i][0].parent = table[i - 1][0]
                table[i][0].steps = i
                table[i][0].todo = operations[3]
            else:
                if first[i - 1] != second[j - 1]:
                    same = 1
                else:
                    same = 0
                tmp, val = min([(table[i - 1][j], table[i - 1][j].steps + 1),
                           (table[i][j - 1], table[i][j - 1].steps + 1),
                           (table[i - 1][j - 1], table[i - 1][j - 1].steps + same)], key=lambda a: a[1])
                if table[i - 1][j] == tmp:
                    table[i][j].todo = operations[3]
                elif table[i][j - 1] == tmp:
                    table[i][j].todo = operations[2]
                elif table[i - 1][j - 1] == tmp:
                    if first[i - 1] == second[j - 1]:
                        table[i][j].todo = operations[0]
                    else:
                        table[i][j].todo = operations[1]
                table[i][j].steps = val
                table[i][j].parent = tmp

    print(f'Odleglosc edycyjna wynosi : {table[n][m].steps}')
    ops = []
    current = table[n][m]
    while current.parent is not None:
        ops.append(current.todo)
        current = current.parent

    for i in range(len(ops) // 2):
        ops[i], ops[len(ops) - 1 - i] = ops[len(ops) - 1 - i], ops[i]

    i = 0
    j = 0
    third = first
    print(f'Pierwotne slowo - {first}')
    for op in ops:
        which = operations.index(op)
        if which != 3:
            if which == 1:
                changed = third[i]
                third = third[:i] + second[j] + third[i + 1:]
                print(f'{third} - zmieniono znak {changed} na znak {second[j]}')
            elif which == 2:
                third = third[:i] + second[j] + third[i:]
                print(f'{third} - wstawiono znak {second[j]}')
            else:
                pass
            i += 1
            j += 1
        else:
            deleted = third[i]
            third = third[:i] + third[i + 1:]
            print(f'{third} - usunieto znak {deleted}')

    print(f'Otrzymane finalne slowo - {third}')


testingWords = ['los', 'kloc', 'Łódź', 'Lodz', 'kwintesencja', 'quintessence', 'ATGAATCTTACCGCCTCG','ATGAGGCTCTGGCCCCTG']

print('-----------Podpunkt 3-----------')
# Pierwsza para
editDistance(testingWords[0], testingWords[1])
print('----------------------------------')

# Druga para
editDistance(testingWords[2], testingWords[3])
print('----------------------------------')

# Trzecia para
editDistance(testingWords[4], testingWords[5])
print('----------------------------------')

# Czwarta para
editDistance(testingWords[6], testingWords[7])
print('----------------------------------')


def LCS(first, second):
    n = len(first) + 1
    m = len(second) + 1
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(m):
            matrix[i].append(0)

    for i in range(n):
        for j in range(m):
            if i != 0 and j != 0:
                if first[i - 1] == second[j - 1]:
                    matrix[i][j] = matrix[i - 1][j - 1] + 1
                else:
                    matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])
            else:
                continue
    return matrix


def tokenizeText(text):
    nlp = Polish()
    tokenizer = Tokenizer(nlp.vocab)
    return tokenizer(text)


def randomTokens(text):
    ratio = 3 / 100
    result = []
    for el in text:
        if random() < ratio:
            continue
        else:
            result.append(el)

    return result


with open('romeo-i-julia-700.txt', 'r', encoding='utf-8') as f:
    data = f.read()

tokenized = tokenizeText(data)
first, second = randomTokens(tokenized), randomTokens(tokenized)
tokens = [len(tokenized), len(first), len(second)]
print(f'Oryginalna ilosc tokenow po podzieleniu tekstu na tokeny : {tokens[0]}')
print(f'Ilosc tokenow w pierwszej wersji tekstu po usunieciu pewnych tokenow : {tokens[1]}')
print(f'Ilosc tokenow w drugiej wersji tekstu po usunieciu pewnych tokenow : {tokens[2]}')
print(f'Dlugosc najdłuższego podciągu wspólnych tokenów dla obu wersji tekstow : {LCS(first, second)[tokens[1] - 1][tokens[2] - 1]}')
print('-----------------------------------')

"""

#W celu zapisania stokenizowanych wersji tekstu nalezy odkomentowac dane linie
nlp = Polish()
tokenizer = Tokenizer(nlp.vocab)
tokenized = tokenizer(data)
first, second = randomTokens(tokenized), randomTokens(tokenized)
with open('firstTokenized.txt', 'w', encoding='utf-8') as f:
    for el in first:
        f.write(el.text_with_ws)

with open('secondTokenized.txt', 'w', encoding='utf-8') as f:
    for el in second:
        f.write(el.text_with_ws)
"""


def diff(first, second):
    n = len(first)
    m = len(second)
    matrix = LCS(first, second)
    result = []
    i = n - 1
    j = m - 1

    while i >= 0 and j >= 0:
        if first[i] != second[j]:
            if matrix[i][j - 1] >= matrix[i - 1][j]:
                result.append(f'> [linia {j}] Fragment : {second[j]}')
                j -= 1
            else:
                result.append(f'< [linia {i}] Fragment : {first[i]}')
                i -= 1
        else:
            i -= 1
            j -= 1

    for k in range(j, -1, -1):
        result.append(f'> [linia {k}] Fragment : {second[k]}')

    for k in range(i, -1, -1):
        result.append(f'< [linia {k}] Fragment : {first[k]}')

    for i in range(len(result)-1, -1, -1):
        print(result[i])


diff(first, second)
