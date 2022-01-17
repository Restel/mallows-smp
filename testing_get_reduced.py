from GeneratePreference import *
from rotational_ex_stack import *
from gale_shapley import *
from gs_extended import *
import copy
from collections import defaultdict
import random
import numpy as np

n = 8
mpref, wpref = generate_pref_test(n)
n = len(mpref)  # number of agents
M_men = gale_shapley(mpref, wpref, n, False)
M_wom = gale_shapley(wpref, mpref, n, True)
SM, rotations = minimal_difference(mpref, wpref)
D = construct_digraph(mpref, wpref, rotations, n, M_men, M_wom)
for rho in rotations:
    print(rho)

def print_array(A):
    for i in range(len(A)):
        print(str(i) + ': ', end='')
        for j in range(len(A[i])):
            print(str(A[i][j]), end=' ')
        print()

print_array(D)
transitive_reduction(D)
print_array(D)



