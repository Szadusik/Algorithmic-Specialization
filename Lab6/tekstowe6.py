from queue import Queue
from PIL import Image
import time


# Zadanie 1
class Node:
    def __init__(self):
        self.state = 0
        self.connected = None
        self.connections = {}


class Automata:
    def __init__(self, pattern):
        self.states = []
        self.automata = {}
        self.parent = Node()
        self.current = None
        self.pattern = pattern

    def initializer(self):
        self.current = self.parent
        counter = 1
        n = len(self.pattern)
        m = len(self.pattern[0])
        unique = set()
        queue = Queue()
        i = 0
        while i < m:
            tmp = self.parent
            j = 0
            while j < n:
                sign = self.pattern[j][i]
                if sign in tmp.connections:
                    pass
                else:
                    unique.add(sign)
                    tmp.connections[sign] = Node()
                    tmp.connections[sign].state = counter
                    counter += 1
                tmp = tmp.connections[sign]
                j += 1
            i += 1

        for el in unique:
            passes = self.parent.connections
            if el not in passes:
                passes[el] = self.parent
            else:
                passes[el].connected = self.parent
                queue.put(passes[el])

        while not queue.empty():
            taken = queue.get()
            passes = taken.connections
            for el in unique:
                if el not in passes:
                    pass
                else:
                    next = passes[el]
                    queue.put(next)
                    parent = taken.connected
                    while el not in parent.connections:
                        parent = parent.connected
                    next.connected = parent.connections[el]

        i = 0
        while i < m:
            self.states.append(0)
            j = 0
            while j < n:
                self.states[len(self.states) - 1] = self.getChar(self.pattern[j][i])
                j += 1
            self.current = self.parent
            i += 1

        for el in self.states:
            if el in self.automata.keys():
                pass
            else:
                self.automata[el] = [0] * (len(self.states) + 1)

        counter = 0
        self.automata[self.states[0]][0] = 1
        for i in range(len(self.automata)):
            for el in self.automata.values():
                el[i] = el[counter]
            if i >= len(self.states):
                pass
            else:
                self.automata[self.states[i]][i] = i + 1
                counter = self.automata[self.states[i]][counter]

    def getChar(self, sign):
        if self.current is None:
            return None

        while sign not in self.current.connections.keys():
            self.current = self.current.connected
            if self.current is not None:
                pass
            else:
                self.current = self.parent
                return self.current.state

        self.current = self.current.connections[sign]
        return self.current.state

    def parser(self, line):
        res = []
        n = len(line)
        which = 0
        i = 0
        while i < n:
            if line[i] in self.automata:
                which = self.automata[line[i]][which]
                if which == len(self.states):
                    res.append(i)
            else:
                which = 0
                i += 1
                continue
            i += 1
        return res

    def find(self, word):
        res = []
        output = []
        length = 0
        found = []

        for el in word:
            if len(el) <= length:
                pass
            else:
                length = len(el)
            found.append([])

        i = 0
        while i < length:
            j = 0
            while j < len(word):
                if i >= len(word[j]):
                    pass
                else:
                    found[j].append(self.getChar(word[j][i]))
                j += 1
            self.current = self.parent
            i += 1

        i = 0
        while i < len(found):
            parsed = self.parser(found[i])
            if len(parsed) == 0:
                pass
            else:
                res.append((i, parsed))
            i += 1

        for el in res:
            for sign in el[1]:
                output.append((el[0] - len(self.pattern) + 1, sign - len(self.pattern[0]) + 1))

        return output


def imageProcess(image):
    laodedimage = image.load()
    res = []
    n = image.height
    m = image.width
    i = 0
    while i < n:
        pixels = []
        j = 0
        while j < m:
            pixels.append(laodedimage[j, i][0])
            j += 1
        res.append(pixels)
        i += 1
    return res


def checkOccurances(text, pattern):
    res = Automata(pattern)
    res.initializer()
    print(f'Coordinates of occurances : {res.find(text)}')
    print(f'All occurances : {len(res.find(text))}')


def checkOccurancesImage(text, patternname):
    with Image.open(patternname, 'r') as f:
        pattern = imageProcess(f)

    res = Automata(pattern)
    res.initializer()
    print(f'Coordinates of occurances : {res.find(text)}')
    print(f'All occurances : {len(res.find(text))}')


def getTime(word, pattern):
    start = time.time()
    res = Automata(pattern)
    res.initializer()
    end = time.time()
    builder = end - start
    start = time.time()
    res.find(word)
    end = time.time()
    finder = end - start
    return builder, finder


def printTime(word, pattern):
    builded, found = getTime(word, pattern)
    print(f'Building time : {builded} s')
    print(f'Finding time : {found} s')


def divider(text, amount):
    res = []
    for i in range(amount):
        res.append(text[i::amount])
    return res


def timeWithDivide(text, amount):
    timer = 0
    for el in text:
        builded, founded = getTime(el, second)
        timer += founded
    print(f'Founding time : {timer} s')


# Zadanie 2
with open('haystack.txt', 'r') as f:
    lines = f.readlines()

unique = []
for el in lines:
    for sign in el:
        if sign not in unique:
            unique.append(sign)

res = []
for sign in unique:
    pattern = [[sign], [sign]]
    automat = Automata(pattern)
    automat.initializer()
    res.extend(automat.find(lines))

print(res)
print(len(res))

# Zadanie 3
checkOccurances(lines, [['t', 'h'], ['t', 'h']])
checkOccurances(lines, [['t', ' ', 'h'], ['t', ' ', 'h']])
print('----------------------------------')
# Zadanie 4
with Image.open('haystack.png', 'r') as f:
    lines = imageProcess(f)

checkOccurancesImage(lines, 'm.png')
checkOccurancesImage(lines, 's.png')
checkOccurancesImage(lines, 'i.png')
print('----------------------------------')

# Zadanie 5
# checkOccurancesImage(lines, 'pattern.png')
# print('----------------------------------')

# Zadanie 6
with Image.open('first.png', 'r') as f:
    first = imageProcess(f)

with Image.open('second.png', 'r') as f:
    second = imageProcess(f)

with Image.open('third.png', 'r') as f:
    third = imageProcess(f)

printTime(lines, first)
printTime(lines, second)
printTime(lines, third)
print('----------------------------------')

# Zadanie 7
divided = divider(lines, 2)
timeWithDivide(divided, second)
divided = divider(lines, 4)
timeWithDivide(divided, second)
divided = divider(lines, 8)
timeWithDivide(divided, second)
print('----------------------------------')
