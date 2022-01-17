import numpy as np
import sys
import csv
import ast
import os
csv.field_size_limit(sys.maxsize)
import pandas
import csv

# READ DATA
# FIX sys path and csv_file
N = [150, 200]
num_repeats = 1000
sys_path = "/Users/lina/Documents/Data_for_SMP_java/Uniform/"
for i in range(1, len(N) + 1):
    n = N[i - 1]  # vary the number of agents
    out_path = "/Users/lina/Documents/Data_for_SMP_java/Uniform/n_" + str(n) + "_reps_" + str(num_repeats) + "/"
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    csv_file = "uniform_n_" + str(n) + "_rep_" + str(num_repeats) + ".csv"
    with open(sys_path + csv_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        i = 1
        for row in csv_reader:

            mpref = ast.literal_eval(row['mpref'])
            # ast.literal_eval converts a string representation of a list to an object of class list
            wpref = ast.literal_eval(row['wpref'])
            rep = int(row['rep']) + 1  #rep initially ranges [0,999], for shell we need [1, 1000]
            n = len(mpref)
            # create a txt file for men's preferences of i instance
            mfile = open(out_path + "men" + str(rep) + "_n" + str(n) + ".txt", "w+") # Plus sign indicates both read and write
            for man in mpref:
                man = [e - 1 for e in man] # substract one from each element to merge with the code
                str_pref = ' '.join(str(e) for e in man)
                mfile.write(str_pref + "\r\n")
            mfile.close()

            # create a txt file for women's preferences of i instance
            wfile = open(out_path + "women" + str(rep) + "_n" + str(n) + ".txt", "w+")

            for woman in wpref:
                woman = [e - 1 for e in woman] # substract one from each element to merge with the code
                str_pref = ' '.join(str(e) for e in woman)
                wfile.write(str_pref + "\r\n")
            wfile.close()
            print(i)
            i += 1



# READ DATA for n = 20, 50, 100
# FIX sys path and csv_file
N = [200]
num_repeats = 1000
sys_path = "/Users/lina/Documents/Data_for_SMP_java/Uniform/"
for i in range(1, len(N) + 1):
    n = N[i - 1]  # vary the number of agents
    out_path = "/Users/lina/Documents/Data_for_SMP_java/Uniform/n_" + str(n) + "_reps_" + str(num_repeats) + "/"
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    csv_file = "uniform_n_" + str(n) + "_rep_" + str(num_repeats) + ".csv"
    with open(sys_path + csv_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        i = 1
        for row in csv_reader:

            mpref = ast.literal_eval(row['mpref'])
            # ast.literal_eval converts a string representation of a list to an object of class list
            wpref = ast.literal_eval(row['wpref'])
            rep = int(row['rep']) + 1  #rep initially ranges [0,999], for shell we need [1, 1000]
            n = len(mpref)
            # create a txt file for men's preferences of i instance
            mfile = open(out_path + "men" + str(rep) + "_n" + str(n) + ".txt", "w+") # Plus sign indicates both read and write
            for man in mpref:
                man = [e - 1 for e in man] # substract one from each element to merge with the code
                str_pref = ' '.join(str(e) for e in man)
                mfile.write(str_pref + "\r\n")
            mfile.close()

            # create a txt file for women's preferences of i instance
            wfile = open(out_path + "women" + str(rep) + "_n" + str(n) + ".txt", "w+")

            for woman in wpref:
                woman = [e - 1 for e in woman] # substract one from each element to merge with the code
                str_pref = ' '.join(str(e) for e in woman)
                wfile.write(str_pref + "\r\n")
            wfile.close()
            print(i)
            i += 1


