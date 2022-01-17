"""A helper function to create csv files for outputs and make headers
Usage: python3 write_headers.py [name_of_output_file] [distro]
Example: python3 write_headers.py polar150_1.csv P
"""
import csv
import sys

if __name__=="__main__":
    csv_file = sys.argv[1]
    distro = sys.argv[2]
    if distro == "P":
        csv_columns = ['id', 'n', 'M_man', 'W_man', 'M_woman', 'W_woman', 'R', 'L']
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()  # write column headers
