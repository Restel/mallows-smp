import itertools
import math
from typing import List, Tuple, Dict

def try_insert_right(i: int, k: int, list: List[int], I:Dict[int,int]) -> (List[int], Dict[int,int]):
    """Returns a preference list if it is possible to move agent i k positions down in the given preferences list.
    Return False otherwise. I is a dictionary with n elements as keys, and their allowed inversions as values"""
    I_table = I.copy()
    r = list.index(i)
    n = len(list)
    if (r + k) >= n:
        return [],I  # can not be moved to an index greater or equal to n
    for ind in range(1, k + 1):  # check all elements to the left from i, if they allow inversions
        elem = list[r + ind]
        if I_table[elem] == 0:  # element elem can not be moved futher, as it does not allow any more inversions
            return [],I  # can not do the insertion

    # Make an insertion
    for ind in range(r, r + k):
        elem = list[ind+1]
        list[ind] = elem
        I_table[elem] -= 1
    list[r + k] = i
    I[i] = 0
    return list, I_table

def try_insert_left(i: int, k: int, list_ori: List[int], I:Dict[int,int]) -> (List[int], Dict[int,int]):
    """Returns a preference list if it is possible to move agent i k positions up in the given preferences list.
    Return False otherwise. I is a dictionary with n elements as keys, and their allowed inversions as values"""
    list = list_ori.copy()
    I_table = I.copy()
    r = list.index(i)
    if (r - k) < 0:
        return [], I  # can not be moved to a negative index
    for ind in range(1, k + 1):  # check all elements to the left from i, if they allow inversions
        elem = list[r - ind]
        if I_table[elem] == 0:  # element elem can not be moved futher, as it does not allow any more inversions
            return [], I  # can not do the insertion

    # Make an insertion
    for ind in range(r, r - k, -1):
        elem = list[ind - 1]
        list[ind] = elem
        I_table[elem] -= 1
    list[r - k] = i
    I_table[i] = 0
    return list, I_table


def find_displ(prefs, target):
    """ int[][], int[] -> int
        A helper function to find the displacement of target in given preferences
        :param prefs: preferences of men or women from 1 to n without DUMMY
        :param target: an agent (m/f), whose displacement is estimated, from 1 to n
        :return displ: the displacement of target in pref
        """
    rank_min = math.inf
    rank_max = -100
    n = len(prefs)
    for agent in range(n):
        rank_min = min(rank_min, prefs[agent].index(target))
        rank_max = max(rank_max, prefs[agent].index(target))
    displ = rank_max - rank_min + 1  # displacement (width) of preferences regarding the target
    return displ


def find_k_parameters(mpref: List[List[int]], wpref: List[List[int]], n: int) -> Tuple[int, int]:
    """
    Function to find the k parameters in k-range models. Returns the k-range for the preferences of men and women
     :param mpref: preferences of men
     :param wpref: preferences of women
     :param n: number of agents
     :pre: preferences do NOT have a dummy agent and range from 1 to n

    """
    k_m = -100
    k_w = -100
    for man in range(1, n + 1):
        displ = find_displ(wpref, man)
        k_w = max(k_w, displ)  # update women's max displacement

    for woman in range(1, n + 1):
        displ = find_displ(mpref, woman)
        k_m = max(k_m, displ)  # update men's max displacement
    return k_m, k_w


def kendall_tau_distance(order_a, order_b, abs=True):  # FIX: make it efficient with counting inversions
    begin = min(order_a)
    end = max(order_a)
    pairs = list(itertools.combinations(range(begin, end + 1), 2))
    distance = 0
    for x, y in pairs:
        a = order_a.index(x) - order_a.index(y)
        b = order_b.index(x) - order_b.index(y)
        if a * b < 0:
            distance += 1
    if not abs:
        n = len(order_a)
        normalizator = int(n * (n - 1) / 2)
        distance = distance / normalizator
        distance = round(distance, 1)
    return distance


def add_one(ref):
    n = len(ref)
    for i in range(n):
        for j in range(n):
            ref[i][j] += 1


def all_matchings(n):
    """ int [] -> int[][]
        returns a list of all permutations of 1...n sequence
    """
    res = list(itertools.permutations(range(1, n + 1)))
    res = [list(i) for i in res]  # convert a list of tuples to a list of lists

    return res


def blocking_pairs(matching, mpref, wpref, n):
    """
        Returns the number of blocking pairs for a given matching and preference profile
        int[], int[][], int[][], int -> int
        - matching [] ranges from 1 to n
        - mpref, wpref [][] each ranges from 1 to n. NO DUMMY AGENTS

        blocking_pairs(matching, mpref, wpref, n)
    """
    # look for blocking pairs from perspective of men
    mblock = 0
    for man in range(n):
        current_woman = matching[man]
        rank = mpref[man].index(current_woman)
        for j in range(0, rank):
            prefered_woman = mpref[man][j]
            current_man = matching.index(
                prefered_woman) + 1  # because index ranges from 0 to n - 1, we need to increment it
            if wpref[prefered_woman - 1].index(current_man) > wpref[prefered_woman - 1].index(man + 1):
                mblock += 1

    # look for blocking pairs from perspective of women
    wblock = 0
    for woman in range(n):
        current_man = matching.index(woman + 1) + 1
        rank = wpref[woman].index(current_man)
        for j in range(0, rank):
            prefered_man = wpref[woman][j]
            current_woman = matching[prefered_man - 1]
            if mpref[prefered_man - 1].index(current_woman) > mpref[prefered_man - 1].index(woman + 1):
                wblock += 1
    if mblock != wblock:  # blocking pairs of men and women have to be equal
        raise ValueError("Problem when counting blocking pairs!")
    return mblock
