import csv
import re
import os
#
#
#
#
#
#
os.chdir('C:\\Users\\supbobba\\Desktop\\Residential2018')

f_name = 'OWNDat.dat'
out_name = 'OWN-Out.dat'
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
