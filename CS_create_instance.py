__author__ = 'Lina Brilliantova'
'''The function to produce a sample of stable marriage instances coming from a certain distribution with n number of agents and other optional parameters. Kendal Tau between reference rankings is always 0
Author: Angelina Brilliantova
Usage: python3 CS_create_instance DistributionType #_agents #_repeats #phi_m #phi_w. The last two arguments are required only for Mallows distribution'''

import ast
import os
import csv
import sys
from GeneratePreference import *
from QS_mallows_phis_KT_random_1000_MW import generate_refs
from typing import List

# Settings
csv.field_size_limit(sys.maxsize)


def check_distro(distro_inp: str) -> str:
    """Check if the distribution is valid. Currently M, P, U
    :param distro_inp: a letter representing a distribution type
    """
    if distro_inp == 'U':
        distro = 'Uniform'
    elif distro_inp == 'P':
        distro = 'Polar'
    elif distro_inp == 'M':
        distro = 'Mallows'
    else:
        sys.exit(distro_inp + ' is an unsupported distribution')
    return distro


def create_file_path(distro: str, n: int, **kwargs) -> str:
    """Returns a filename to save a preference list for a given distro, n, id, gender and noise parameters (in Mallows)
    :param n: number of agents
    :param id: id
    :param gender: gender
    :param distro: the distribution
    :pre: distro is "M", "P", "U"
    :pre: gender is either 'men' or 'women'
    :return filename: a filename
    """
    path = "./data/alg_perf/" + distro + "/" + "n_" + str(n) + "/"
    if distro == "Mallows":
        path = path + "phi_" + str(kwargs['phi_m']) + "_" + str(kwargs['phi_w']) + "/"
    return path


def generate_profile(n: int, distro: str, phis: dict) -> tuple:
    """Generate an instance of Mallows-distributed preference profile for given # of agents and noise parameters.
    Kendal Tau between references is assumed to be 0 """
    if distro == 'M':
        ref_m, ref_w, _ = generate_refs(n, '0')  # k_tau equals 0
        mpref, wpref = generate_mallow_separate(n, ref_m, ref_w, 1.0, phis['phi_m'], phis['phi_w'])
    elif distro == "U":
        mpref, wpref = generate_uniform(n)
    elif distro == "P":
        mpref, wpref = generate_exp(n)
    else:
        raise TypeError("Unsupported distribution. Must be 'P', 'M', or 'U' ")
    return mpref, wpref


def save_profile(out_path: str, gender: str, id: int, n: int, pref: List[List[int]]) -> None:
    """Save a preference list to a txt file"""
    filename = out_path + gender + str(id) + "_n" + str(n) + ".txt"
    file = open(filename, "w+")  # Plus sign indicates both read and write
    for agent in pref:
        agent = [e - 1 for e in agent]  # substract one from each element to merge with the code
        str_pref = ' '.join(str(e) for e in agent)
        file.write(str_pref + "\r\n")
    file.close()


def main() -> None:
    distro_inp = sys.argv[1]  # distribution type
    n = int(sys.argv[2])  # number of agents
    num_repeats = int(sys.argv[3])  # number of repeats
    if distro_inp == 'M':
        phis = {'phi_m': float(sys.argv[4]),
                'phi_w': float(sys.argv[5])}
    else:
        phis = {}
    distro = check_distro(distro_inp)
#    for t in range(num_repeats, 2 * num_repeats + 1): # not sure where this line came from
    for t in range(1, num_repeats+1):
        print(t)
        mpref, wpref = generate_profile(n, distro_inp, phis)
        out_path = create_file_path(distro, n, **phis)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        save_profile(out_path, 'men', t, n, mpref)
        save_profile(out_path, 'women', t, n, wpref)
        print("Done for n = {0}, repeats = {1}, distro = {2}, phis = {3}".format(n, t, distro, phis))

if __name__ == "__main__":
    main()


# dict_data = {'id': t,
#                 'n': n,
#                 'rep': t,
#                 'mpref': mpref,
#                 'wpref': wpref
#                 }
#    try:
#        with open(sys_path + csv_file, 'a') as csvfile:
#            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#            writer.writerow(dict_data)
#    except IOError:
#        print("I/O error")

# with open(sys_path + csv_file, mode='r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     i = 1
#     for row in csv_reader:
#         mpref = ast.literal_eval(row['mpref'])
#         # ast.literal_eval converts a string representation of a list to an object of class list
#         wpref = ast.literal_eval(row['wpref'])
#         rep = int(row['rep']) + 1  # rep initially ranges [0,999], for shell we need [1, 1000]
#         n = len(mpref)
#         # create a txt file for men's preferences of i instance
#         mfile = open(out_path + "men" + str(rep) + "_n" + str(n) + ".txt",
#                      "w+")  # Plus sign indicates both read and write
#         for man in mpref:
#             man = [e - 1 for e in man]  # substract one from each element to merge with the code
#             str_pref = ' '.join(str(e) for e in man)
#             mfile.write(str_pref + "\r\n")
#         mfile.close()
