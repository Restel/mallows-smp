from rotational_ex_stack import *
from gale_shapley import *
import random
import numpy as np
import statistics
from tools import kendall_tau_distance, blocking_pairs
from structure_lattice import *
import sys
import csv

"""Comments:  python3 QS_mallows_phis_KT_random_1000_MW.py 4 0.1 0.3 random does not work"""

def make_file_name(phi_f, phi_v, k, name_general = "./data/phis/mallow_phi_M_W_scores_SE__"):
    """Returns a name for csv file containing the results of the simulation
    :params: phi of men, phi of women, kendal distance between reference rankings of men and women
    :pre: k is a kendal tau distance parameter, should be '0', '1', 'random'
    :outputs: a string with a filename
    """
    if k == 'random':
        csv_file = name_general + phi_f.__str__() + "_" + phi_v.__str__() + "KT_random.csv"
    else:
        csv_file = name_general + phi_f.__str__() + "_" + phi_v.__str__() + "KT_" + k.__str__() + ".csv"

    return csv_file


def generate_refs(n, k_tau):
    """
        Generate reference rankings for men and women for using in Mallows model with specified kendal tau distance.

        int [] -> (int [][], int [][], float[])
        :param n: number of agents
        :type n: int
        :param k_tau: desired kendal tau between reference rankings
        :type k_tau: str
        :return mref: reference rankings
        :return wref: reference ranking for women
        :return k_tau_output: kendal tau distance between generated reference rankings
        :pos: references range from 1 to n

        """
    ref_m = [i + 1 for i in range(n)]
    random.shuffle(ref_m)
    ref_w = ref_m.copy()
    if k_tau == 'random':
        random.shuffle(ref_w)
        k_tau_output = kendall_tau_distance(ref_m, ref_w, abs=False)
    elif k_tau == '1':
        ref_w.reverse()
        k_tau_output = 1
    elif k_tau == '0':
        k_tau_output = 0
    else:
        raise TypeError("Unsupported kendal tau distance")
    return ref_m, ref_w, k_tau_output


def create_files_with_headers(phi_f, phi_v, k, csv_columns, name_general = "./data/phis/mallow_phi_M_W_scores_SE__"):
    csv_file = make_file_name(phi_f, phi_v, k, name_general)
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()  # write column names


def generate_output_statistic(mpref, wpref, n):
    """
    :param mpref: preferences of men
    :param wpref: preferences of women
    :param n: number of agents
    """
    M_men = gale_shapley(mpref, wpref, n, False)
    M_wom = gale_shapley(wpref, mpref, n, True)
    _, rotations = minimal_difference(mpref, wpref)  # find rotation poset
    mpref, wpref = add_dummy(mpref, wpref)
    stable_set = find_all_stable(mpref, wpref, n + 1)  # find all stable matchings
    M_men = change_by_one(M_men, minus=False)  # increment indices of M_men, M_wom
    M_wom = change_by_one(M_wom, minus=False)
    delta = [find_scores(M_men, mpref, wpref, n), find_scores(M_wom, mpref, wpref, n)]
    seqMatching, minSE, _ = findSEmatching(stable_set, mpref, wpref, n)
    SE_man = find_SE(M_men, mpref, wpref, n)
    SE_woman = find_SE(M_wom, mpref, wpref, n)
    SE_is_DA = int(seqMatching == M_men or seqMatching == M_wom)
    SE_is_wom = int(seqMatching == M_wom)
    SE_is_men = int(seqMatching == M_men)
    delta_SE_men = minSE - SE_man
    delta_SE_wom = minSE - SE_woman
    dict_data = {'id': None,
                 'n': n,
                 'R': len(rotations),
                 'L': len(stable_set),
                 'tau': None,
                 'phi_men': None,
                 'phi_women': None,
                 'M_man': delta[0][0],
                 'W_man': delta[0][1],
                 'M_woman': delta[1][0],
                 'W_woman': delta[1][1],
                 'SE_man': SE_man,
                 'SE_woman': SE_woman,
                 'SE_min': minSE,
                 'SE_is_DA': SE_is_DA,
                 'SE_is_wom': SE_is_wom,
                 'SE_is_men': SE_is_men,
                 'delta_SE_men': delta_SE_men,
                 'delta_SE_wom': delta_SE_wom
                 }
    return dict_data

def save_statistic(csv_file, dict_data):
    try:
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writerow(dict_data)
    except IOError:
        print("I/O error")

def generate_0_1_KT(range_phi_small, range_phi, k_tau_inp, n):
    for i in range(1000):
        for phi_fixed in range_phi_small:
            for phi_var in range_phi:
                csv_file = make_file_name(phi_fixed, phi_var, k_tau_inp)
                ref_m, ref_w, k_tau = generate_refs(n, k_tau_inp)
                mpref, wpref = generate_mallow_separate(n, ref_m, ref_w, 1.0, phi_fixed, phi_var)
                dict_data = generate_output_statistic(mpref, wpref, n)
                dict_data['id'] = id
                dict_data['phi_men'] = phi_fixed
                dict_data['phi_women'] = phi_var
                dict_data['tau'] = k_tau_inp
                save_statistic(csv_file, dict_data)
                print(
                    "Phi_fixed = {1}, phi_var = {2}, KT = {3}, repeat = {4}, n = {0}".format(n, phi_fixed, phi_var,
                                                                                             k_tau, i))
def generate_random_KT(n):
    id = 0
    k_tau_counts = np.zeros((6, 6, 11),
                            dtype=np.int)  # table to count the number of accumulated values for each KT distance. 1 parameter - phi_fixed, 2 - phi_var, 3 - k_tau
    while True:  # continue until I break the execution from the console
        # Data generation
        phi_fixed = random.sample(range_phi[start_phi:end_phi], 1)[0]  # parallelize over phi_fixed values
        phi_var = random.sample(range_phi, 1)[0]
        csv_file = make_file_name(phi_fixed, phi_var, 'random')
        ref_m, ref_w, k_tau = generate_refs(n)

        # check if the number of accumulated data for this combination is sufficient
        kt_index = int(k_tau * 10)
        phi_fixed_ind = range_phi.index(phi_fixed)
        phi_var_ind = range_phi.index(phi_var)
        if k_tau_counts[phi_fixed_ind, phi_var_ind, kt_index] >= 500:
            continue
        else:
            id += 1
            k_tau_counts[phi_fixed_ind, phi_var_ind, kt_index] += 1  # update the counter for KT
            mpref, wpref = generate_mallow_separate(n, ref_m, ref_w, 1.0, phi_fixed, phi_var)
            # Running algorithms
            dict_data = generate_output_statistic(mpref, wpref, n)
            dict_data['id'] = id
            dict_data['phi_men'] = phi_fixed
            dict_data['phi_women'] = phi_var
            dict_data['tau'] = k_tau
            save_statistic(csv_file, dict_data)
            print(
                "Sampled phi_fixed = {1}, phi_var = {2}, KT = {3}, n = {0}, total = {4}, kt_acc = {5}".format(n, phi_fixed, phi_var, k_tau, id, k_tau_counts[phi_fixed_ind, phi_var_ind,:]))
# GENERAL INPUTS
if __name__ == "__main__":
    sys.setrecursionlimit(10 ** 6)
    # Main loop
    n = int(sys.argv[1])
    range_phi = [.1, .3, .5, .7, .9, 1.0]   # range for both phis
    start_phi = float(sys.argv[2]) 
    end_phi = float(sys.argv[3])

    range_phi_small = [phi for phi in range_phi if phi >= start_phi and phi <= end_phi] # trim range phi for this thread
    k_tau_inp = sys.argv[4]
    csv_columns = ['id', 'n', 'tau', 'phi_men', 'phi_women', 'L', 'R', 'M_man', 'W_man', 'M_woman', 'W_woman', 'SE_man', 'SE_woman', 'SE_min', 'SE_is_DA', 'SE_is_wom', 'SE_is_men', 'delta_SE_men', 'delta_SE_wom']

    # create new files and write headers
    for phi_f in range_phi_small:
        for phi_v in range_phi:
            create_files_with_headers(phi_f, phi_v, k_tau_inp, csv_columns)

    id = 0

    if k_tau_inp == 'random':
        generate_random_KT(n)
    elif k_tau_inp == '0' or k_tau_inp == '1':
        generate_0_1_KT(range_phi_small, range_phi, k_tau_inp,n)
    else:
        raise TypeError("Unsupported kendal tau distance. Must be '0', '1' or 'random' ")
