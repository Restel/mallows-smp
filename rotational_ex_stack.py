from GeneratePreference import *
from gale_shapley import *
from gs_extended import *
from structure_lattice import change_pref
import copy
from collections import defaultdict
import random
import numpy as np


# M_z, mpref_z, wpref_z = gs_extended(wpref, mpref, n) # find optimal for women m. and the shorlists (FGS)
# Mx, GS_men, GS_women = gs_extended(wpref_0, mpref_0, n) # find (GS) list applying women-proposing algorithm to MGS


# Python implementation of Kosaraju's algorithm to print all SCCs
# This class represents a directed graph using adjacency list representation
class Graph:

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = defaultdict(list)  # default dictionary to store graph

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)
        # A function used by DFS

    def DFSUtil(self, v, l, visited):
        # Mark the current node as visited and print it
        visited[v] = l
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == -1:
                visited[i] = l
                self.DFSUtil(i, l, visited)

    def fillOrder(self, v, l, visited, stack):
        # Mark the current node as visited
        visited[v] = l
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == -1:
                self.fillOrder(i, l, visited, stack)
        stack = stack.append(v)

        # Function that returns reverse (or transpose) of this graph

    def getTranspose(self):
        g = Graph(self.V)

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph:
            for j in self.graph[i]:
                g.addEdge(j, i)
        return g

        # The main function that finds and prints all strongly

    # The main function that finds and prints all strongly
    # connected components
    def getSCCs(self):
        stack = []
        # Mark all the vertices as not visited (For first DFS)
        visited = [-1] * (self.V)
        # Fill vertices in stack according to their finishing
        # times
        for i in range(self.V):
            if visited[i] == -1:
                self.fillOrder(i, i, visited, stack)
        # Create a reversed graph
        gr = self.getTranspose()

        # Mark all the vertices as not visited (For second DFS)
        visited = [-1] * (self.V)

        #save stack to list to have the order of vertices
        order = stack
        # Now process all vertices in order defined by Stack
        while stack:
            i = stack.pop()
            if visited[i] == -1:
                gr.DFSUtil(i, i, visited)
                # print("")
        return visited

    def getorder(self):
        stack = []
        # Mark all the vertices as not visited (For first DFS)
        visited = [-1] * (self.V)
        # Fill vertices in stack according to their finishing
        # times
        for i in range(self.V):
            if visited[i] == -1:
                self.fillOrder(i, i, visited, stack)
        order = [x for _, x in sorted(zip(stack, range(0, len(stack))))]
        return order


def makeGraph(match, mpref):
    n = len(match)
    g = Graph(n)
    for man in list(range(n)):
        rank_first = mpref[man].index(match[man])  # find a position of man's current match in his reduced list
        len_pref = len(mpref[man])  # a length of man's reduced list
        if rank_first > len_pref - 2:
            continue
        else:
            next_woman = mpref[man][rank_first + 1]
            next = match.index(next_woman)
            g.addEdge(man, next)
    return g


def findRotation(M, mpref):
    g = makeGraph(M, mpref)
    scc = g.getSCCs()
    order = g.getorder()
    for item in scc:
        if scc.count(item) > 1:
            rotation_set = [i for i, x in enumerate(scc) if x == item] # rotation set is a set of men who is a part of an exposed rotation (in arbitrary order)
            break
    order_reversed = [x for i,x in enumerate(order) if i in rotation_set] # the reversed order of man in the strongly connected component corresponding to rotation
    rotation = [x for _, x in sorted(zip(order_reversed, rotation_set), reverse= True)]# the direct order of man in a rotation
    women = [M[i] for i in rotation]  # get corresponding women for men in rotations
    rotation = [rotation, women]  # first element for men in rotation, second for  women
    return (rotation)


def eliminate(r, M, mpref, wpref):
    new_matches = M.copy()
    size = r.size
    for man in r.men:
        index_man = r.men.index(man)
        next = r.getNextIndex(index_man)
        p_next = r.women[next]  # partner of the next person in the sequence
        new_matches[man] = p_next
        man_rank = wpref[p_next].index(man)

        # next = r[(r.index(man) + 1) % size]
        # p_next = M[next]  # partner of the next person in the sequence
        # new_matches[man] = p_next
        # man_rank = wpref[p_next].index(man)

        successors = [x for i, x in enumerate(wpref[p_next]) if
                      i > man_rank]  # choose the succesors of a new partner of p_next
        wpref[p_next] = [x for x in wpref[p_next] if
                         x not in successors]  # remove all the sucessors of man from p_next list
        for s in successors:
            mpref[s].remove(p_next)

    return new_matches, mpref, wpref


def minimal_difference(mpref_ref, wpref_ref):
    n = len(mpref_ref)  # number of agents
    mpref = copy.deepcopy(mpref_ref)
    wpref = copy.deepcopy(wpref_ref)
    M_men = gale_shapley(mpref, wpref, n, False)
    M_wom = gale_shapley(wpref, mpref, n, True)
    for x in range(n):
        for y in range(n):
            mpref[x][y] -= 1
            wpref[x][y] -= 1
    mpref_men, wpref_men = get_reduced(mpref, wpref, M_men, n)  # find optimal for men m. and the shorlists (MGS)
    #mpref_wom, wpref_wom = get_reduced(mpref, wpref, M_wom)  # find optimal for women m. and the shorlists (FGS)
    sm = []  # set of stable matchings and exposed rotations
    M = []  # set of
    lst = []  # set of reduced lists
    rotations = []  # set of rotations
    M.append(M_men)
    lst.append([mpref_men, wpref_men])
    i = 0
    while M[i] != M_wom:
        m_list = copy.deepcopy(lst[i][0])
        w_list = copy.deepcopy(lst[i][1])
        rho = findRotation(M[i], m_list)  # find an exposed rotation given a previous matching and men's reduced list
        rotation = Rotation(rho, i)
        rotations.append(rotation)
        M_new, m_list, w_list = eliminate(rotation, M[i], m_list,
                                          w_list)  # lst[i][0] - mens reduced list, lst[i][1] - women reduced list
        M.append(M_new)
        lst.append([m_list, w_list])
        sm.append([M[i], rho])  # append a matching and an exposed rotation in matching
        i += 1
    sm.append(M_wom)  # complete a maximal chain of stable matchings
    return sm, rotations



class Rotation:

    def __init__(self, pairs, id):
        self.men = pairs[0]
        self.women = pairs[1]
        self.id = id
        self.size = len(pairs[0])

    def get_data(self):
        return (self.men, self.women)

    def __str__(self):
        return ("Rotation {}, men: {}, women {}".format(self.id, self.men, self.women))
    def increment(self):
        for i in range(self.size):
            self.men[i] += 1
            self.women[i] += 1

    def getNextIndex(self, index):
        if index > self.size - 1 or index < 0:
            raise SystemExit('Index exceeds the range of the rotation')
        elif index == self.size - 1:
            return 0
        return index + 1

    def getPrevIndex(self, index):
        if index > self.size - 1 or index < 0:
            raise SystemExit('Index exceeds the range of the rotation')
        elif index == 0:
            return self.size - 1
        return index - 1

    # Second two functions are used to calculate the weight of rotations
    def getNextWoman(self, index_of_pair):
        next_ind = self.getNextIndex(index_of_pair)
        return self.women[next_ind]

    def getPrefMan(self, index_of_pair):
        next_ind = self.getNextIndex(index_of_pair)
        return self.men[next_ind]



def construct_digraph(mpref_ori, wpref_ori, rotations, n, Mopt, Wopt):
    ''' int[], int[], Rotations list, int, int[], int[] -> int[][]
    Returns the dominance relationship between the rotations
    mpref, wpref must contain a dummy agent and range from 1 to n
    Find example in testing_get_reduced.py
    '''

    mpref, wpref = change_pref(mpref_ori[1:n + 1], wpref_ori[1:n + 1], n)
    labels = np.ones((n, n), dtype=int) * -100
    label_types = np.ones((n, n), dtype=int) * -100
    r = len(rotations)
    D = np.zeros((r, r), dtype=int)
    for rho in rotations:
        for i in range(0, rho.size):
            man = rho.men[i]
            woman = rho.women[i]
            index = mpref[man].index(woman)
            labels[man][index] = rho.id
            label_types[man][index] = 1
            next_mate_of_woman = rho.men[rho.getPrevIndex(i)] # looks like greeks have an error in the code                 next_mate_of_woman = r.men.get(r.getNextIndex(i));
            for j in range(wpref[woman].index(next_mate_of_woman) + 1, wpref[woman].index(man)):
                man1 = wpref[woman][j]
                index = mpref[man1].index(woman)
                labels[man1][index] = rho.id
                label_types[man1][index] = 2

    for i in range(0, n):
        latest_type1_label = -100
        maleOptMatch_of_i = mpref[i].index(Mopt[i])
        femaleOptMatch_of_i = mpref[i].index(Wopt[i])
        for j in range(maleOptMatch_of_i, femaleOptMatch_of_i):
            if label_types[i][j] == 1:
                if latest_type1_label != -100: D[latest_type1_label][labels[i][j]] = 1
                latest_type1_label = labels[i][j]
            elif label_types[i][j] == 2:
                if latest_type1_label != -100: D[labels[i][j]][latest_type1_label] = 1

    return D

def transitive_reduction(m):
    """ Performs transitive reduction, i.e. transforms a given directed acyclic graph into its minimal equivalent """
    n = len(m)
    for j in range(n):
        for i in range(n):
            if m[i][j]:
                for k in range(n):
                    if m[j][k]:
                        m[i][k] = 0

def print_array(A):
    ''' int[][] -> None
    prints a list of lists as a 2D array'''
    for i in range(len(A)):
        print(str(i) + ': ', end='')
        for j in range(len(A[i])):
            print(str(A[i][j]), end=' ')
        print()


def compute_M_score(marriage, mpref):
    M_score = 0
    for man in range(len(marriage)):
        woman = marriage[man]
        add_i = mpref[man].index(woman) + 1
        M_score += add_i
    return M_score

def compute_W_score(marriage, wpref):
    W_score = 0
    for woman in range(len(marriage)):
        man = marriage.index(woman+1) + 1
        add_i = wpref[woman].index(man) + 1
        W_score += add_i
    return W_score


def calculate_weight_for_men(rotation, mpref):
    '''mpref is 1:n without dummy agent.
    Calculate the change in M score by the given women-improving Rotation. The value is positive as men are worse off after eliminating wi Rotation'''
    weight = 0
    for i in range(rotation.size):
        man = rotation.men[i]
        current = rotation.women[i]
        next = rotation.getNextWoman(i)
        add_i = mpref[man].index(next+1) - mpref[man].index(current+1)
        weight += add_i
    return weight

def calculate_weight_for_women(rotation, wpref):
    '''wpref is 1:n without dummy agent.
    Calculate the change in M score by the given women-improving Rotation. The value is positive as men are worse off after eliminating wi Rotation'''
    weight = 0
    for i in range(rotation.size):
        woman = rotation.women[i]
        current = rotation.men[i]
        next = rotation.getPrefMan(i)
        add_i = wpref[woman].index(current+1) - wpref[woman].index(next+1)
        weight += add_i
    return weight