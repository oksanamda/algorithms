from __future__ import division, print_function
import numpy as np
import random
import time


pt = {'match': 2, 'mismatch': -1, 'gap': -1}

#ГЕНЕРАЦИЯ ПОСЛЕДОВАТЕЛЬНОСТЕЙ
def generate_sequence(a, b, n, m):
    for i in range(0, n):
        aux = random.randint(0, 10000) % 4
        if aux == 0:
            a.append('A')
        elif aux == 2:
            a.append('C')
        elif aux == 3:
            a.append('G')
        else:
            a.append('T')
    #последовательность В
    for k in range(0, m):
        aux = random.randint(0, 10000) % 4
        if aux == 0:
            b.append('A')
        elif aux == 2:
            b.append('C')
        elif aux == 3:
            b.append('G')
        else:
            b.append('T')


def mch(alpha, beta):
    if alpha == beta:
        return pt['match']
    elif alpha == '-' or beta == '-':
        return pt['gap']
    else:
        return pt['mismatch']


def water(s1, s2):
    m, n = len(s1), len(s2)
    H = np.zeros((m + 1, n + 1))
    T = np.zeros((m + 1, n + 1))
    max_score = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            sc_diag = H[i - 1][j - 1] + mch(s1[i - 1], s2[j - 1])
            sc_up = H[i][j - 1] + pt['gap']
            sc_left = H[i - 1][j] + pt['gap']
            H[i][j] = max(0, sc_left, sc_up, sc_diag)
            if H[i][j] == 0: T[i][j] = 0
            if H[i][j] == sc_left: T[i][j] = 1
            if H[i][j] == sc_up: T[i][j] = 2
            if H[i][j] == sc_diag: T[i][j] = 3
            if H[i][j] >= max_score:
                max_i = i
                max_j = j
                max_score = H[i][j];

    align1, align2 = '', ''
    i, j = max_i, max_j

    #ТРАССИРОВКА
    while T[i][j] != 0:
        if T[i][j] == 3:
            a1 = s1[i - 1]
            a2 = s2[j - 1]
            i -= 1
            j -= 1
        elif T[i][j] == 2:
            a1 = '-'
            a2 = s2[j - 1]
            j -= 1
        elif T[i][j] == 1:
            a1 = s1[i - 1]
            a2 = '-'
            i -= 1
        align1 += a1
        align2 += a2

    align1 = align1[::-1]
    align2 = align2[::-1]
    sym = ''
    iden = 0
    for i in range(len(align1)):
        a1 = align1[i]
        a2 = align2[i]
        if a1 == a2:
            sym += a1
            iden += 1
        elif a1 != a2 and a1 != '-' and a2 != '-':
            sym += ' '
        elif a1 == '-' or a2 == '-':
            sym += ' '

    identity = iden / len(align1) * 100
    print('Identity = %f percent' % identity)
    print('Score =', max_score)
    print(align1)
    print(sym)
    print(align2)
 
#ГЕНЕРАЦИЯ ЗНАЧЕНИЙ n и m В ЗАДАННОМ ДИАПАЗОНЕ
n_numbers = [10, 100, 1000, 10000]
m_numbers = [10, 100, 1000, 10000]
my_time = []
count_of_experiments = 20
for n in n_numbers:
    for m in m_numbers:
        print(n, m)
        for i in range(0, count_of_experiments):
            a = []
            b = []
            generate_sequence(a, b, n, m)
            #НАЧИНАЕМ ЗАМЕРЯТЬ ВРЕМЯ
            start_time = time.time()
            water(a, b)
            my_time.append(time.time() - start_time)
        #СЧИТАЕМ СРЕДНЕЕ АРИФМИТИЧЕСКОЕ ПО ПОЛУЧЕННЫМ ЗНАЧЕНИЯМ
        t = np.mean(my_time)
        print("----- %s seconds -----" % t)
        my_time = []
