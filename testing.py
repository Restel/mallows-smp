from rotational_ex_stack import *
from gale_shapley import *
import random
import numpy as np
import statistics
from tools import kendall_tau_distance, blocking_pairs, all_matchings
from all_stable import *
from structure_lattice import *
import sys
import itertools


def lattice_identical_pref(num_repeats, N_max, step):
    N = []  # new range
    for i in range(2, N_max, step):
        N.append(i)
    data = np.zeros((len(N) * num_repeats, 3), dtype=np.float32)  #

    for i in range(1, len(N) + 1):
        n = N[i - 1]  # vary the number of agents
        for t in range(0, num_repeats):
            mpref, wpref = generate_identical(n)
            mpref, wpref = add_dummy(mpref, wpref)
            stable_set = find_all_stable(mpref, wpref, n + 1)
            index_pos = (i - 1) * num_repeats + t
            data[index_pos, 0] = len(stable_set)
            data[index_pos, 1] = n
            if len(stable_set) != 1:
                raise ValueError('The stable lattice is not a singleton!')
            print("Done for n = {0}, repeats = {1}".format(N[i - 1], t))
    return data


def lattice_nonoverlap_pref(num_repeats, N_max, step):
    N = []  # new range
    for i in range(2, N_max, step):
        N.append(i)
    data = np.zeros((len(N) * num_repeats, 3), dtype=np.float32)  #

    for i in range(1, len(N) + 1):
        n = N[i - 1]  # vary the number of agents
        for t in range(0, num_repeats):
            mpref, wpref = generate_nonoverlap_pref(n)
            mpref, wpref = add_dummy(mpref, wpref)
            stable_set = find_all_stable(mpref, wpref, n + 1)
            index_pos = (i - 1) * num_repeats + t
            data[index_pos, 0] = len(stable_set)
            data[index_pos, 1] = n
            if len(stable_set) != 1:
                raise ValueError('The stable lattice is not a singleton! Stable set: ', *stable_set, ' preferences of men ', *mpref, ' preferences of women ' *wpref)
            print("Done for n = {0}, repeats = {1}".format(N[i - 1], t))
    return data

def lattice_all_permutations(num_repeats, N_max, step):
    """ int, int, int -> bool
        Generate preferences according to the Uniform model num_repeats times. For each instance computes the stable lattice and searches over all posible permutations to find the stable matchings. Checks if the produced set corresponds to the stable lattice.

        success = lattice_all_permutations(50, 8, 1)
    """
    N = []  # new range
    for i in range(2, N_max, step):
        N.append(i)

    for i in range(1, len(N) + 1):
        n = N[i - 1]  # vary the number of agents
        for t in range(0, num_repeats):
            mpref, wpref = generate_uniform(n)
            mpref, wpref = add_dummy(mpref, wpref)
            matchings_set = all_matchings(n)
            stable_checked = []
            for marriage in matchings_set:
                if blocking_pairs(marriage, mpref[1:n+1], wpref[1:n+1], n) == 0:
                    stable_checked.append(marriage)
            stable_set = find_all_stable(mpref, wpref, n + 1)
            compare = set(tuple(t) for t in stable_checked) & set(tuple(t) for t in stable_set)
            if len(compare) != len(stable_checked) or len(compare) != len(stable_set):
                raise ValueError("Stable set does not correspond to the result of the exhaustive search! ")
            print("Done for n = {0}, repeats = {1}".format(N[i - 1], t))
    return True

# test_data = lattice_identical_pref(50, 100, 1) # WORKS FINE
# test_data = lattice_nonoverlap_pref(50, 100, 1) # WORKS FINE
# success = lattice_all_permutations(50, 8, 1) # WORKS