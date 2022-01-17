"""The function to find the lattice size and the scores of optimal matchings under the mallows model
Usage: python3 mallows.py [#number of agents] [phi_m] [phi_w] [k_tau] [id of instance ] [#filename]
Example: python3 mallows.py 150 0.5 0.5 1 ./data/Polar/CS_mallows_150_1.csv
"""
from rotational_ex_stack import *
from gale_shapley import *
import random
import numpy as np
import statistics
from tools import kendall_tau_distance, blocking_pairs
from structure_lattice import *
from polar import check_stability
from QS_mallows_phis_KT_random_1000_MW import generate_refs
import sys
import csv

# GENERAL INPUTS
if __name__ == "__main__":
    sys.setrecursionlimit(10 ** 6)
    csv_columns = ['id', 'n', 'M_man', 'W_man', 'M_woman', 'W_woman', 'R', 'L']
    n = int(sys.argv[1])
    phi_m = float(sys.argv[2])
    phi_w = float(sys.argv[3])
    k_tau_inp = sys.argv[4]
    id = int(sys.argv[5])
    csv_file = sys.argv[6]
    start = time.clock()
    ref_m, ref_w, k_tau = generate_refs(n, k_tau_inp)
    mpref, wpref = generate_mallow_separate(n, ref_m, ref_w, 1.0, phi_m, phi_w)
    M_men = gale_shapley(mpref, wpref, n, False)
    M_wom = gale_shapley(wpref, mpref, n, True)
    _, rotations = minimal_difference(mpref, wpref)  # find rotation poset
    mpref, wpref = add_dummy(mpref, wpref)
    stable_set = find_all_stable(mpref, wpref, n + 1)  # find all stable matchings
    check_stability(stable_set, mpref, wpref, n)
    M_men = change_by_one(M_men, minus=False)  # increment indices of M_men, M_wom
    M_wom = change_by_one(M_wom, minus=False)
    delta = [find_scores(M_men, mpref, wpref, n), find_scores(M_wom, mpref, wpref, n)]
    # SAVE DATA TO LOG FILE
    dict_data = {'id': id,
                 'n': n,
                 'R': len(rotations),
                 'L': len(stable_set),
                 'M_man': delta[0][0],
                 'W_man': delta[0][1],
                 'M_woman': delta[1][0],
                 'W_woman': delta[1][1],
                 }
    try:
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writerow(dict_data)
    except IOError:
        print("I/O error")
    print("Done for n = {0}, repeats = {1}, time elapsed = {2}".format(n, id, time.clock() - start))