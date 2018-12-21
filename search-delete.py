import csv
import re


def search_delete(f_name, in_words_file):
    with open(in_words_file, 'r',encoding="utf-8-sig") as in_f:
        #lines_all = in_f.readlines()
        #print(lines_all)
        i_f = csv.reader(in_f)
        rows = list(i_f)
        list_of_words = [item for sublist in rows for item in sublist]
        #print(list_of_words)
    out_name = f_name.split('.')[0]+'-out.csv'
    with open(f_name, encoding="utf-8-sig") as f: 
         #lines_all = f.readlines()
         lines_all = list(csv.reader(f))
         length = len(lines_all)
         #print("**********")
         print(length) 

         with open(out_name, 'w', encoding="utf-8") as t:
             tw = csv.writer(t)
             skip =0
             for line in lines_all:
                 print(line)
                 cnt = 0   
                 for item in list_of_words:
                     l = [s for s in line if item.lower() in s.lower()]   
                 if l:
                    skip = skip+1
                    #print(line)
                 else:
                    tw.writerow(line)
    print("Total skipped lines - %d ",skip)

#search_delete('test-pins_2.csv', ['INC','LLC', 'LTD'])
#search_delete('full-data.csv', 'in-words.txt')
#search_delete('full-orig-data.csv', 'llc.csv')
#search_delete('full-data-2.csv', 'Gwin_keys_10.csv')
#search_delete('Tax_Cobb_2017.csv', 'llc.csv')

import argparse
import sys

if __name__ == "__main__":
       parser = argparse.ArgumentParser()
       parser.add_argument("full_tax_file", help="Give the exact name of the input file with all the details")
       parser.add_argument("words_file",help="Only one column of search data in the file")
       args = parser.parse_args()
       search_delete(args.full_tax_file, args.words_file)
