import numpy as np
from rotational_ex_stack import *
from gale_shapley import *
import random
import numpy as np
import statistics
from tools import kendall_tau_distance
from all_stable import *

# n = 4
# mpref, wpref = generate_pref_test(n) for recursion unwrapping i used slightly different example when n = 4

n = 8
malechoice, femalechoice = generate_pref_test(n)
malechoice, femalechoice = add_dummy(malechoice, femalechoice) # use for other preference profiles
sm = find_all_stable(malechoice, femalechoice, n+1)

# test indices
