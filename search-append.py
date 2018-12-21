import csv


#def create_pin_file(in_pin_csv, in_all_csv)
def create_pin_file(full_data_file,pid_file):
    with open(pid_file,mode='r',encoding="utf-8") as f:
        f_r = csv.reader(f, delimiter=',')
        rows = [row for row in f_r]
        flat_list = [item for sublist in rows for item in sublist]

    with open(full_data_file,mode='r',encoding="utf-8") as f:
        out_file = full_data_file.split('.')[0]+'-out.csv'
        with open(out_file, mode = 'w') as zf:
            f_r = csv.reader(f, delimiter=',')
            zf_w = csv.writer(zf, delimiter=',')
            header = next(f_r)
            zf_w.writerow(header)
            
            found_list = []
            for row in f_r:
                #print row
                wrote = 0
                for item in flat_list:
                        #print item
                    if item in row:
                                #print 'Found matching ' + item
                        #wrote = 1
                        zf_w.writerow(row)
                        found_list.append(item)
                        #break   
                #if wrote == 0:
            not_found = [i for i in flat_list if i not in found_list]
            print(not_found)    
            for item in not_found:
                zf_w.writerow([item])
        
import argparse
import sys

if __name__ == "__main__":
       parser = argparse.ArgumentParser()
       parser.add_argument("full_tax_file", help="Give the exact name of the input file with all the details")
       parser.add_argument("pid_file",help="Only one column of search data in the file")
       args = parser.parse_args()
       create_pin_file(args.full_tax_file, args.pid_file)
