import random
import numpy as np
import generate_profiles as GenProfiles
import math
from tools import kendall_tau_distance, try_insert_left, try_insert_right, find_displ
#
# def generate_k_uniform(n, k):
#     I_table = {}
#     S = []
#     for i in range(1,n+1):
#         I_table[i] = k
#     S.append(generate_random(n)[0][0])  # generate the first preference list u.a.r
#     priority_0 = [item for item in I_table.keys() if I_table[item] != 0]
#     while priority_0 or len(priority_0) != 1:
#         agent = max(I_table, key=I_table.get) # get an agent with the minimum inversions allowed
#         pref_pivot = random.choice(S) # randomly select an existing pref list and try to modify it
#         print(len(S))
#         pref_list, I_table = try_insert_left(agent, k, pref_pivot,I_table)
#         if not pref_list:
#             pref_list, I_table = try_insert_right(agent, k, pref_pivot,I_table)
#         if pref_list:
#             S.append(pref_list)
#         priority_0 = [item for item in I_table.keys() if I_table[item] != 0]
#         print(I_table)
#     if len(S) != n:
#         print(n-(len(S)), " samples randomly copied")
#         pref_list_add = random.sample(S, n - len(S))
#         pref_list = pref_list + pref_list_add
#     return pref_list

def generate_k_uniform(n, k):
    S = []
    left = False
    ref_list = generate_random(n)[0][0] # generate the first preference list u.a.r
    new_list = ref_list.copy()
    for agent in ref_list:
        position = ref_list.index(agent)
        if position + k >= n:
            left = True
        if left:
            temp_agent = ref_list[position-k]
            new_list[position-k] = agent
            new_list[position] = temp_agent
        elif not left:
            temp_agent = ref_list[position + k]
            new_list[position + k] = agent
            new_list[position] = temp_agent
        print(new_list)
        new_list = ref_list.copy()
        print(ref_list)
        S.append(new_list)
    return S

def generate_pref_test(n):
    if n == 8:
        men_pref = [[5, 7, 1, 2, 6, 8, 4, 3],
                    [2, 3, 7, 5, 4, 1, 8, 6],
                    [8, 5, 1, 4, 6, 2, 3, 7],
                    [3, 2, 7, 4, 1, 6, 8, 5],
                    [7, 2, 5, 1, 3, 6, 8, 4],
                    [1, 6, 7, 5, 8, 4, 2, 3],
                    [2, 5, 7, 6, 3, 4, 8, 1],
                    [3, 8, 4, 5, 7, 2, 6, 1]]

        women_pref = [[5, 3, 7, 6, 1, 2, 8, 4],
                      [8, 6, 3, 5, 7, 2, 1, 4],
                      [1, 5, 6, 2, 4, 8, 7, 3],
                      [8, 7, 3, 2, 4, 1, 5, 6],
                      [6, 4, 7, 3, 8, 1, 2, 5],
                      [2, 8, 5, 3, 4, 6, 7, 1],
                      [7, 5, 2, 1, 8, 6, 4, 3],
                      [7, 4, 1, 5, 2, 3, 6, 8]]

    if n == 4:
        men_pref = [[1, 3, 2, 4],
                    [2, 1, 4, 3],
                    [3, 1, 4, 2],
                    [4, 2, 3, 1]]
        women_pref = [[4, 3, 1, 2],
                      [3, 4, 1, 2],
                      [2, 1, 4, 3],
                      [1, 3, 2, 4]]

    return men_pref, women_pref


def generate_random(n):
    men_pref = []
    women_pref = []
    ordered = [i + 1 for i in range(n)]

    for i in range(n):
        mrand = ordered.copy()
        random.shuffle(mrand)
        men_pref.append(mrand)

        wrand = ordered.copy()
        random.shuffle(wrand)
        women_pref.append(wrand)

    return men_pref, women_pref


def generate_single_peaked_test(narcistic=False):
    if narcistic:
        men_pref = [[1, 2, 3, 4, 5, 6, 7, 8],
                    [2, 3, 4, 5, 1, 6, 7, 8],
                    [3, 4, 2, 5, 1, 6, 7, 8],
                    [4, 3, 5, 6, 2, 7, 1, 8],
                    [5, 4, 3, 2, 6, 7, 8, 1],
                    [6, 5, 4, 3, 2, 7, 1, 8],
                    [7, 6, 5, 4, 3, 2, 8, 1],
                    [8, 7, 6, 5, 4, 3, 2, 1]]
        women_pref = [[1, 2, 3, 4, 5, 6, 7, 8],
                      [2, 3, 1, 4, 5, 6, 7, 8],
                      [3, 4, 2, 5, 1, 6, 7, 8],
                      [4, 3, 2, 1, 5, 6, 7, 8],
                      [5, 4, 6, 3, 2, 7, 8, 1],
                      [6, 7, 5, 4, 8, 3, 2, 1],
                      [7, 6, 8, 5, 4, 3, 2, 1],
                      [8, 7, 6, 5, 4, 3, 2, 1]]
    else:
        men_pref = [[1, 2, 3, 4, 5, 6, 7, 8],
                    [2, 3, 4, 5, 1, 6, 7, 8],
                    [3, 4, 2, 5, 1, 6, 7, 8],
                    [4, 3, 5, 6, 2, 7, 1, 8],
                    [5, 4, 3, 2, 6, 7, 8, 1],
                    [6, 5, 4, 3, 2, 7, 1, 8],
                    [7, 6, 5, 4, 3, 2, 8, 1],
                    [8, 7, 6, 5, 4, 3, 2, 1]]
        women_pref = [[8, 7, 6, 5, 4, 3, 2, 1],
                      [1, 2, 3, 4, 5, 6, 7, 8],
                      [2, 3, 1, 4, 5, 6, 7, 8],
                      [4, 3, 2, 1, 5, 6, 7, 8],
                      [5, 4, 6, 3, 2, 7, 8, 1],
                      [3, 4, 2, 5, 1, 6, 7, 8],
                      [6, 7, 5, 4, 8, 3, 2, 1],
                      [7, 6, 8, 5, 4, 3, 2, 1]]

    return men_pref, women_pref


def generate_single_peaked_test2():
    men_pref = [[1, 2, 3, 4, 5, 6],
                [3, 2, 1, 4, 5, 6],
                [5, 4, 6, 3, 2, 1],
                [4, 3, 2, 5, 1, 6],
                [4, 5, 6, 3, 2, 1],
                [3, 4, 5, 2, 6, 1]]
    women_pref = [[4, 1, 6, 2, 3, 5],
                  [1, 6, 2, 4, 3, 5],
                  [2, 3, 6, 1, 5, 4],
                  [2, 3, 5, 6, 1, 4],
                  [2, 3, 6, 1, 4, 5],
                  [3, 5, 2, 6, 1, 4]]

    return men_pref, women_pref


def generate_uniform(n):
    men_pref = []
    women_pref = []
    ordered = [i + 1 for i in range(n)]
    for i in range(n):
        # men's preferences
        mrand = ordered.copy()
        random.shuffle(
            mrand)  # random.shuffle implements Fisher–Yates shuffle algorithm, which is proven to be equally distributed over n! possbile permutations
        men_pref.append(mrand)
        # women's preferences
        wrand = ordered.copy()
        random.shuffle(wrand)
        women_pref.append(wrand)
    return men_pref, women_pref

def generate_asc_desc(n):
    men_pref = []
    women_pref = []
    ordered = [i + 1 for i in range(n)]

    # generate women preferences
    for i in range(n):
        if i < n/2:
            wrand = ordered.copy()
            women_pref.append(wrand)
        else:
            wrand = ordered.copy()
            wrand.reverse()
            women_pref.append(wrand)
        mrand = ordered.copy()
        random.shuffle(
            mrand)  # random.shuffle implements Fisher–Yates shuffle algorithm, which is proven to be equally distributed over n! possbile permutations
        men_pref.append(mrand)
        # women's preferences

    return men_pref, women_pref

def generate_mallow(n, ref_m, ref_w, mix=1.0, phi=0.4):
    candidate_set = GenProfiles.gen_cand_map(n)
    men_pref = []
    women_pref = []
    rmaps_men, rmapcounts_men = GenProfiles.gen_mallows(n, candidate_set, [mix], [phi],
                                                        [ref_m])  # FIX rmapcounts -> account for repeated rankings!)
    rmaps_women, rmapcounts_women = GenProfiles.gen_mallows(n, candidate_set, [mix], [phi], [ref_w])
    # extract agents' preferences from a dictionary rmaps_
    # first for man as rmapcounts_men and _women can have different length
    for i in range(len(rmapcounts_men)):
        count = rmapcounts_men[i]
        pref_dict = rmaps_men[i]
        man_pref = [x for x in pref_dict.keys()]
        for j in range(count):
            men_pref.append(man_pref.copy())

    # extract women preferences
    for i in range(len(rmapcounts_women)):
        count = rmapcounts_women[i]
        pref_dict = rmaps_women[i]
        woman_pref = [x for x in pref_dict.keys()]
        for j in range(count):
            women_pref.append(woman_pref.copy())

    return men_pref, women_pref


def generate_mallow_separate(n, ref_m, ref_w, mix=1.0, phi_m=0.3, phi_w=0.3):
    """ generate mallows distribution with different phi for men and women"""

    candidate_set = GenProfiles.gen_cand_map(n)
    men_pref = []
    women_pref = []
    rmaps_men, rmapcounts_men = GenProfiles.gen_mallows(n, candidate_set, [mix], [phi_m],
                                                        [ref_m])
    rmaps_women, rmapcounts_women = GenProfiles.gen_mallows(n, candidate_set, [mix], [phi_w], [ref_w])
    # extract agents' preferences from a dictionary rmaps_
    # rmapcounts_men and _women can have different length
    for i in range(len(rmapcounts_men)):
        count = rmapcounts_men[i]
        pref_dict = rmaps_men[i]
        man_pref = [x for x in pref_dict.keys()]
        for _ in range(count):
            men_pref.append(man_pref.copy())

    # extract women preferences
    for i in range(len(rmapcounts_women)):
        count = rmapcounts_women[i]
        pref_dict = rmaps_women[i]
        woman_pref = [x for x in pref_dict.keys()]
        for _ in range(count):
            women_pref.append(woman_pref.copy())

    return men_pref, women_pref


def generate_identical(n):
    men_pref = []
    women_pref = []
    ordered = [i + 1 for i in range(n)]
    random.shuffle(
        ordered)
    for i in range(n):
        # men's preferences
        men_pref.append(ordered)
        # women's preferences
        women_pref.append(ordered)
    return men_pref, women_pref


def generate_nonoverlap_pref(n):
    men_pref = []
    women_pref = []
    ordered = [i + 1 for i in range(n)]
    first_choice = ordered.copy()
    random.shuffle(first_choice)
    for i in range(n):
        full_choices = ordered.copy()
        pref = []
        pref.append(first_choice[i])
        full_choices.remove(pref[0])
        random.shuffle(full_choices)
        for j in full_choices:
            pref.append(j)

        men_pref.append(pref)

    for i in range(n):
        full_choices = ordered.copy()
        pref = []
        first_man = first_choice.index(i + 1) + 1
        pref.append(first_man)
        full_choices.remove(pref[0])
        random.shuffle(full_choices)
        for j in full_choices:
            pref.append(j)

        women_pref.append(pref)

    return men_pref, women_pref


def generate_ranking_simple(ref, tau):
    cand = ref.copy()
    n = len(ref)
    ordered = list(range(n))
    normalizator = int(n * (n - 1) / 2)
    tau_abs = math.floor(normalizator * tau)
    dist = 0
    while dist != tau_abs:
        i = random.choice(ordered)
        next = min((i + 1), (n - 1))
        # if cand[i] == 76 or cand[next] == 76:
        #     print(i)
        temp = cand[i]
        cand[i] = cand[next]
        cand[next] = temp
        dist = kendall_tau_distance(ref, cand)  # update the kendal tau distance
        print('need: ', tau_abs, 'get: ', dist)

    return cand


def generate_polar(n, pol):
    men_pref = []
    women_pref = []
    ordered = [i + 1 for i in range(n)]
    hot_size = int(pol * n)  # FIX THIS int(x) is floor(x)
    hot = [i + 1 for i in range(hot_size)]
    cold_size = n - hot_size
    cold = [i + 1 for i in range(hot_size, n)]
    for i in range(n):
        mhot = random.sample(hot, hot_size)
        mcold = random.sample(cold, cold_size)
        m_rand = mhot + mcold
        men_pref.append(m_rand)
        wrand = random.sample(ordered, n)
        women_pref.append(wrand)
    return men_pref, women_pref


def generate_exp(n):
    if n % 2 != 0:
        raise ValueError("n must be even!")
    one = [i + 1 for i in range(0, int(
        n / 2))]  # divide an even set of agents into two parts. Within the set the preferences of both sides are uniform
    two = [i + 1 for i in range(int(n / 2), n)]
    men_pref = np.zeros((n, n), dtype=int)
    women_pref = np.zeros((n, n), dtype=int)

    # generate uniformly distributed preferences separately for each set

    for i in range(0, int(n / 2)):
        mrand_one = one.copy()  # men's preferences ONE
        random.shuffle(mrand_one)  # Fisher–Yates shuffle
        mrand_two = two.copy()  # men's preferences TWO
        random.shuffle(mrand_two)
        men_pref[i,] = mrand_one + mrand_two
        men_pref[i + int(n / 2),] = mrand_two + mrand_one
        # women
        wrand_one = one.copy()  # women's preferences ONE
        random.shuffle(wrand_one)  # Fisher–Yates shuffle
        wrand_two = two.copy()  # women's preferences TWO
        random.shuffle(wrand_two)
        women_pref[i,] = wrand_two + wrand_one
        women_pref[i + int(n / 2),] = wrand_one + wrand_two

    return men_pref.tolist(), women_pref.tolist()


def generate_both_sides_single_peaked(n):
    candidate_set = GenProfiles.gen_cand_map(n)
    men_pref = []
    women_pref = []
    rmaps_men, rmapcounts_men = GenProfiles.gen_single_peaked_impartial_culture_strict(n,
                                                                                       candidate_set)  # rmapcounts the number of repeats for a corresponding preference
    rmaps_women, rmapcounts_women = GenProfiles.gen_single_peaked_impartial_culture_strict(n, candidate_set)
    # extract agents' preferences from a dictionary rmaps_
    # first for man as rmapcounts_men and _women can have different length
    for i in range(len(rmapcounts_men)):
        count = rmapcounts_men[i]
        pref_dict = rmaps_men[i]
        man_pref = [x for x in pref_dict.keys()]
        for j in range(count):
            men_pref.append(man_pref.copy())

    # extract women preferences
    for i in range(len(rmapcounts_women)):
        count = rmapcounts_women[i]
        pref_dict = rmaps_women[i]
        woman_pref = [x for x in pref_dict.keys()]
        for j in range(count):
            women_pref.append(woman_pref.copy())

    return men_pref, women_pref


def generate_single_peaked_uniform(n):
    """ int -> int[][], int[][]
        returns a single peaked preferences for one side (men), uniformly distributed preferences for the other (women)"""
    men_pref = []
    women_pref = []

    # Men preferences are single peaked
    candidate_set = GenProfiles.gen_cand_map(n)
    rmaps_men, rmapcounts_men = GenProfiles.gen_single_peaked_impartial_culture_strict(n,
                                                                                       candidate_set)  # rmapcounts the number of repeats for a corresponding preference
    for i in range(len(rmapcounts_men)):
        count = rmapcounts_men[i]
        pref_dict = rmaps_men[i]
        man_pref = [x for x in pref_dict.keys()]
        for j in range(count):
            men_pref.append(man_pref.copy())

    #  women preferences are distributed uniformly
    ordered = [i + 1 for i in range(n)]
    for i in range(n):
        wrand = ordered.copy()
        random.shuffle(
            wrand)  #
        women_pref.append(wrand)

    return men_pref, women_pref

def generate_single_peaked_mallows(n, mix, phi, ref_w):
    """ int, int, int, int[] -> int[][], int[][]
        returns a single peaked preferences for one side (men), and the Mallows preferences with phi = .5 and random reference ranking for the other (women)"""
    men_pref = []
    women_pref = []

    # Men preferences are single peaked
    candidate_set = GenProfiles.gen_cand_map(n)
    rmaps_men, rmapcounts_men = GenProfiles.gen_single_peaked_impartial_culture_strict(n,
                                                                                       candidate_set)  # rmapcounts the number of repeats for a corresponding preference
    for i in range(len(rmapcounts_men)):
        count = rmapcounts_men[i]
        pref_dict = rmaps_men[i]
        man_pref = [x for x in pref_dict.keys()]
        for j in range(count):
            men_pref.append(man_pref.copy())

    #  women preferences are distributed as Mallows distro
    candidate_set = GenProfiles.gen_cand_map(n)
    rmaps_women, rmapcounts_women = GenProfiles.gen_mallows(n, candidate_set, [mix], [phi], [ref_w])
    # extract womens preferences from a dictionary rmaps
    for i in range(len(rmapcounts_women)):
        count = rmapcounts_women[i]
        pref_dict = rmaps_women[i]
        woman_pref = [x for x in pref_dict.keys()]
        for j in range(count):
            women_pref.append(woman_pref.copy())

    return men_pref, women_pref

def generate_single_peaked_identical(n):
    """ int -> int[][], int[][]
        returns a single peaked preferences for one side (men), identically distributed preferences for the other (women)"""
    men_pref = []
    women_pref = []

    # Men preferences are single peaked
    candidate_set = GenProfiles.gen_cand_map(n)
    rmaps_men, rmapcounts_men = GenProfiles.gen_single_peaked_impartial_culture_strict(n,
                                                                                       candidate_set)  # rmapcounts the number of repeats for a corresponding preference
    for i in range(len(rmapcounts_men)):
        count = rmapcounts_men[i]
        pref_dict = rmaps_men[i]
        man_pref = [x for x in pref_dict.keys()]
        for j in range(count):
            men_pref.append(man_pref.copy())

    #  women preferences are distributed uniformly
    ordered = [i + 1 for i in range(n)]
    wrand = ordered.copy()
    for i in range(n):
        women_pref.append(wrand)

    return men_pref, women_pref


def print_pref(pref):
    for i in range(len(pref)):
        print(str(i + 1) + ': ', end='')
        for j in range(len(pref[i])):
            print(str(pref[i][j]), end=' ')
        print()


def func1(x):
    total = 0
    for i in range(len(x)):
        total += x[i] ** 2
    return total


def add_dummy(mpref, wpref):
    n = len(mpref)
    dummy = [-1] * n
    mpref_add = np.zeros((n + 1, n), dtype=int)
    wpref_add = np.zeros((n + 1, n), dtype=int)
    mpref_add[0] = dummy
    mpref_add[1:n + 1, ] = mpref
    wpref_add[0] = dummy
    wpref_add[1:n + 1, ] = wpref
    return mpref_add.tolist(), wpref_add.tolist()


def pref_minus_one(mpref, wpref):
    n = len(mpref)
    for i in range(0, n):
        for j in range(0, n):
            mpref[i][j] -= 1
            wpref[i][j] -= 1
