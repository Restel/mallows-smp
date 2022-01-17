from GeneratePreference import *
from rotational_ex_stack import *
from gale_shapley import *
from gs_extended import *
import copy
from collections import defaultdict
import random
import numpy as np
import generate_profiles as GenProfiles
import statistics
import math
from tools import kendall_tau_distance

random.seed(5)

n = 50
base_ref = list(range(n))
random.shuffle(base_ref)  # output [2, 3, 1, 0, 8, 7, 6, 5, 4, 9]


def generate_ranking_simple(ref, tau):
    cand = ref.copy()
    n = len(ref)
    ordered = list(range(n))
    normalizator = int(n * (n - 1)/2)
    tau_abs = math.floor(normalizator * tau)
    dist = 0
    while dist != tau_abs:
        i = random.choice(ordered)
        next = min((i+1), (n - 1))
        # if cand[i] == 76 or cand[next] == 76:
        #     print(i)
        temp = cand[i]
        cand[i] = cand[next]
        cand[next] = temp
        dist = kendall_tau_distance(ref, cand)  # update the kendal tau distance
        print('need: ', tau_abs, 'get: ', dist)

    return cand

a = generate_ranking_simple(base_ref, 0.6)
