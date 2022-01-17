from rotational_ex_stack import *
from gale_shapley import *
import random
import numpy as np
import statistics
from tools import kendall_tau_distance
from all_stable import *
import sys
import time


def change_pref(mpref, wpref, n, plus=False):
    """ int [][], int[][], int, boolean -> int[][], int[][]
        Return incremented or decremented preferences of agents based on plus parameter (T/F)

      """

    mpref_c = copy.deepcopy(mpref)  # do not change the initial preferences
    wpref_c = copy.deepcopy(wpref)
    if plus:
        for x in range(n):
            for y in range(n):
                mpref_c[x][y] += 1
                wpref_c[x][y] += 1
    else:
        for x in range(n):
            for y in range(n):
                mpref_c[x][y] -= 1
                wpref_c[x][y] -= 1
    return mpref_c, wpref_c


def change_by_one(vector, minus):
    """ int [], bool -> int []
        Returns decremented preferences (if minus = T), or incremented preferences (minus = F) of a list of integers
    """

    res = vector.copy()
    if minus:
        for i in range(len(res)):
            res[i] -= 1
    else:
        for i in range(len(res)):
            res[i] += 1

    return res


def exposed_rotation(mpref, wpref, marriage, rot, n):
    """ int[][], int[][], int[], Rotation, int -> bool Determines if rotation rot is exposed in given marriage: for each
    man m[i] in rot checks if w[i] is his first choice in women-improving shortlist (WIS), w[i+1] is his second
    choice in WIS. - mpref and wpref contain preferences of n agents (each range from 1 to n) and a dummy woman and a
    man, total n + 1 rows and n columns. - marriage is a man oriented row of matches. marriage[i] is a woman to whom
    man i is married - rot is an object of custom class Rotation

    """
    mpref_red, wpref_red = change_pref(mpref[1:n + 1], wpref[1:n + 1], n)  # get decremented preferences. Do not
    # return preferences of dummy players
    mpref_red, wpref_red = get_reduced(mpref_red, wpref_red, change_by_one(marriage, minus=True),
                                       n)  # get women-improving
    # shortlists
    visited = [False] * rot.size

    def check_next(index):  # recursive function to check if a man in rot[index] has woman in rot[index] as his 1st
        # choice in WIS, woman at rot[index] as his second choice
        man = rot.men[index]  # m[i]
        woman = rot.women[index]  # w[i]
        next = rot.getNextIndex(index)  # next index
        next_woman = rot.women[next]  # next woman in rotation w[i+1]
        if (woman in mpref_red[man] and next_woman in mpref_red[man]) and mpref_red[man].index(woman) == 0 and \
                mpref_red[man].index(
                        next_woman) == 1:  # check is w[i] and w[i+1] are in m[i] shortlist, then if they have the corresponding positions
            visited[index] = True
            if visited[next]:
                res = True
            else:
                # print('Checking next man', rot.men[next])
                res = check_next(next)

        else:
            # print('False')
            res = False
        return res

    suc = check_next(0)
    return suc


def eliminate_rotation(marriage, rho):
    """ int[], Rotation -> int[] """

    rho_new = copy.deepcopy(rho)
    rho_new.increment()
    n = len(marriage)
    new_marriage = [0] * n
    for i in range(0, n):
        if (i + 1) in rho_new.men:
            index_man = rho_new.men.index(i + 1)
            next = rho_new.getNextIndex(index_man)
            new_marriage[i] = rho_new.women[next]
        else:
            new_marriage[i] = marriage[i]
    return new_marriage


# CODE TO GET A LATTICE STRUCTURE FROM KNOWN ROTATION POSET AND STABLE SET
# n = 8
# mpref, wpref = generate_pref_test(n)
# M_men = gale_shapley(mpref, wpref, n, False)
# M_wom = gale_shapley(wpref, mpref, n, True)
# SM, rotations = minimal_difference(mpref, wpref)
# # mpref, wpref = change_pref(mpref, wpref, n, True)
# mpref, wpref = add_dummy(mpref, wpref)
# stable_set = find_all_stable(mpref, wpref, n + 1)
#
# for rho in rotations:
#     print(rho)
#
# lat_poset = np.zeros((len(stable_set), len(stable_set)), dtype=int)
#
# for sm_index in range(0, len(stable_set)):
#     marriage = stable_set[sm_index]
#     for rho in rotations:
#         if exposed_rotation(mpref, wpref, marriage, rho, n):
#             next_marriage = eliminate_rotation(marriage, rho)
#             id_next = stable_set.index(next_marriage)
#             lat_poset[sm_index][id_next] = 1
# #
# print(lat_poset)
# print(stable_set)

def Graph_lattice(poset):
    n = len(poset)
    graph = Graph(n)
    for x in range(n):
        for y in range(n):
            if poset[x, y] == 1:
                graph.addEdge(x, y)


def findSEmatching(set, mpref, wpref, n):
    """ int [][], int[][], int[][], int -> int[], int
    !!! mpref, wpref from 1 to n, with dummy agents
    Finds equitable matching with the lowest absolute difference between men's and women's welfares (sum of partners' positions)"""
    start = time.clock()
    min = float("+inf")
    best = None
    for marriage in set:
        M_score = 0
        W_score = 0
        for i in range(1, n + 1):  # loop for pairs
            man = i
            woman = marriage[i - 1]
            m_index = mpref[man].index(woman)
            w_index = wpref[woman].index(man)
            M_score += m_index
            W_score += w_index
        # print("M_score: ", M_score)
        # print("W_score: ", W_score)
        if abs(M_score - W_score) < min:
            min = abs(M_score - W_score)
            best = marriage

    return best, min, time.clock() - start


# se_matching, se_cost, time = findSEmatching(stable_set, mpref, wpref, n)

def find_SE(marriage, mpref, wpref, n):
    """ int[], int [][], int[][], int -> int
    !!! mpref, wpref from 1 to n, with dummy agents
    Computes SE cost of a marriage"""
    M_score = 0
    W_score = 0
    for i in range(1, n + 1):  # loop for pairs
        man = i
        woman = marriage[i - 1]
        m_index = mpref[man].index(woman) + 1
        w_index = wpref[woman].index(man) + 1
        # print("Woman: ", woman)
        # print("Man:", man)
        # print(w_index)
        M_score += m_index
        W_score += w_index
    return abs(M_score - W_score)


def find_scores(marriage, mpref, wpref, n):
    """ int[], int [][], int[][], int -> int
    !!! mpref, wpref from 1 to n, with dummy agents
    Computes SE cost of a marriage"""
    M_score = 0
    W_score = 0
    for i in range(1, n + 1):  # loop for pairs
        man = i
        woman = marriage[i - 1]
        m_index = mpref[man].index(woman) + 1
        w_index = wpref[woman].index(man) + 1
        # print("Woman: ", woman)
        # print("Man:", man)
        # print(w_index)
        M_score += m_index
        W_score += w_index
    return [M_score, W_score]