import csv
import re
import os


def process_dat_file(f_name):
    out_name = f_name.split('.')[0]+'-out.dat'
    #out_name = 'OWN-Out.dat'
    with open(f_name, 'r') as f: 
        lines_all = f.readlines() 
        length = len(lines_all) 
        print(length) 
        i =0 
        inc =5 
        with open(out_name, 'w') as t: 
            tw = csv.writer(t) 
            while True: 
                row = [] 
                lines = lines_all[i:i+inc] 
                for line in lines: 
                    r = line.strip() 
                    row.extend(re.split(r'\s{2,}',r)) 
              
                tw.writerow(row)  
                i = i+inc 
                if i > length: 
                    break 
                row = []

import argparse
import sys
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("big_dat_file", help="Give the DAT file as input. This will combine 5 lines into one single line")
    args = parser.parse_args()
    process_dat_file(args.big_dat_file)

