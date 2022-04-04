import time


# Algorytm naiwny

def naive(word, pattern):
    res = 0
    for i in range(len(word) - len(pattern) + 1):
        if word[i:i + len(pattern)] == pattern:
            res += 1
    return res


# Algorytm automatu skończonego
def transition_table(pattern):
    result = []
    n = len(pattern)
    signs = []
    for i in range(n):
        if not pattern[i] in signs:
            signs.append(pattern[i])

    for q in range(n + 1):
        result.append({})
        for el in signs:
            k = min(q + 2, n + 1)
            while True:
                k -= 1
                s = pattern[:q] + el
                if pattern[:k] == s[q - k + 1:]:
                    break
            result[q][el] = k

    return result


def finite_auto(word, pattern):
    res = 0
    q = 0  # Stan
    table = transition_table(pattern)  # Funkcja przejscia
    for el in word:
        if el not in table[q]:
            q = 0
        else:
            q = table[q][el]
            if q == len(table) - 1:
                res += 1
    return res


# Algorytm KMP
def prefix_function(pattern):
    prefix = [0]
    k = 0
    for q in range(1, len(pattern)):
        while k > 0 and pattern[k] != pattern[q]:
            k = prefix[k - 1]
        if pattern[k] == pattern[q]:
            k = k + 1
        prefix.append(k)
    return prefix


def kmp(word, pattern):
    pi = prefix_function(pattern)
    q = 0
    res = 0
    for i in range(0, len(word)):
        while q > 0 and pattern[q] != word[i]:
            q = pi[q - 1]

        if pattern[q] == word[i]:
            q = q + 1

        if q == len(pattern):
            res += 1
            q = pi[q - 1]
    return res


# Funkcja zwracająca czas działania dla podanego algorytmu


def get_time(word, pattern, algorithm):
    start = time.time()
    res = algorithm(word, pattern)
    end = time.time()
    return end - start


# Algorytm KMP liczący jedynie czas dopasowywania wzorca


def kmp_without_preproces(word, pattern):
    pi = prefix_function(pattern)
    q = 0
    res = 0
    start = time.time()
    for i in range(0, len(word)):
        while q > 0 and pattern[q] != word[i]:
            q = pi[q - 1]

        if pattern[q] == word[i]:
            q = q + 1

        if q == len(pattern):
            res += 1
            q = pi[q - 1]

    end = time.time()
    return end - start

# Automat skończony liczący jedynie czas dopasowywania wzorca


def finite_auto_without_preproces(word, pattern):
    res = 0
    q = 0  # Stan
    table = transition_table(pattern)  # Funkcja przejscia
    start = time.time()
    for el in word:
        if el not in table[q]:
            q = 0
        else:
            q = table[q][el]
            if q == len(table) - 1:
                res += 1
    end = time.time()
    return end - start

# Funkcja wyświetlająca uzyskane rezultaty czasowe przez poszczególne algorytmy wyszukiwania wzorców


def test_times_and_results(word, pattern):
    t = get_time(word, pattern, naive)
    res = naive(word, pattern)
    print(f'Algorytm naiwny : {t} s')
    print(f'Ilość znalezionych rezultatów : {res}')
    t = get_time(word, pattern, kmp)
    res = kmp(word, pattern)
    print(f'Algorytm KMP : {t} s')
    print(f'Ilość znalezionych rezultatów : {res}')
    t = get_time(word, pattern, finite_auto)
    res = finite_auto(word, pattern)
    print(f'Skonczony automat : {t} s')
    print(f'Ilość znalezionych rezultatów : {res}')
    print('---------------------------------------')

# Funkcja wyswietlająca czas uzyskany przez poszczególne algorytmy czasowe nie licząc czasu preprocessingu


def times_without_preprocessing(word, pattern):
    print('Odpowiedzi do pytania numer 4')
    t = get_time(word, pattern, naive)
    print(f'Algorytm naiwny : {t} s')
    t = kmp_without_preproces(word, pattern)
    print(f'Algorytm KMP : {t} s')
    t = finite_auto_without_preproces(word, pattern)
    print(f'Skonczony automat : {t} s')


# Funkcja wyświetlająca ile czasu zajęło utworzenie funkcji przejścia dla danego algorytmu


def function_times(pattern, function):
    start = time.time()
    function(pattern)
    end = time.time()
    print(end - start)


# Test sprawdzający rezultaty przy szukaniu wzorca "Art" w pliku 1997_714.txt
with open('1997_714.txt', 'r', encoding='utf-8') as f:
    data = f.read()
    test_times_and_results(data, "Art")

# Testy sprawdzające szybkość działania algorytmów
testA = "0iajsd-0fjas-9fjk-asjfg-0aiesdjnmtg-0iesjmtg0iesjw=0ijesr0thnwa9ejnmoaiwtnaseptghn-a0defjk0aisdjg0a]hntg-anp0j" * 666
testB = "aaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbccccccccccccccccccccccccccccddddddddddddddddddddddddddddddd" \
        "eeeeeeeeeeeeeeeeeeeeeeeeeeffffffffffffffgggggggggghhhhhhhhhhhhhhhii" \
        "iiiiiiiiiiijjjjjjjjjjjjjjjkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk" \
        "lllllllllllllmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm" * 777
testC = "Jak zrobic cos by to bylo dobrze zrobione, a jednoczeniesnie by nie bylo to za dobrze. dobrze jedziemy z " \
        "tym xd" * 1111

# Wywołanie testów w celu sprawdzenia osiągniętych rezultatów
test_times_and_results(testA, "0fjas")
test_times_and_results(testB, "aaaaaaa")
test_times_and_results(testC, "dobrze")

# Test sprawdzający rezultaty przy szukaniu wzorca "kruszwil" w pliku wikipedia-tail-kruszwil.txt - fragmencie
# polskiej wikipedii
with open('wikipedia-tail-kruszwil.txt', 'r', encoding='utf-8') as f:
    data = f.read()
    test_times_and_results(data, "kruszwil")

# Test dający odpowiedź na podpunkt 4
(text, pattern) = ("X"*1234567, "X"*66666)
times_without_preprocessing(text, pattern)

# Test dający odpowiedź na podpunkt 5
print("Odpowiedzi do pytania numer 5")
pattern = "Ale dobrzy ruch trczx sfj" * 25
function_times(pattern, transition_table)
function_times(pattern, prefix_function)
