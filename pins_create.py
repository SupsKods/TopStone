import csv


#def create_pin_file(in_pin_csv, in_all_csv)
def create_pin_file():
    with open('pids-file.csv',mode='rb') as f:
        f_r = csv.reader(f, delimiter=',')
        rows = [row for row in f_r]
        flat_list = [item for sublist in rows for item in sublist]

    with open('full-orig-data.csv',mode='rb') as f:
        with open('out-pids.csv', mode = 'wb') as zf:
            f_r = csv.reader(f, delimiter=',')
            zf_w = csv.writer(zf, delimiter=',')
            header = next(f_r)
            zf_w.writerow(header)
            
            for row in f_r:
                #print row
                for item in flat_list:
			#print item
                    if item in row:
				#print 'Found matching ' + item
                        zf_w.writerow(row)
                #print '***************'

        
create_pin_file()
 
##with open('full-data.csv',mode='rb') as f:
##        with open('test-pins_2.csv', mode = 'wb') as zf:
##            f_r = csv.reader(f, delimiter=',')
##            zf_w = csv.writer(zf, delimiter=',')
##            header = next(f_r)
##            zf_w.writerow(header)
##            for row in f_r:
##                print row
##                for item in flat_list:
##			print item
##			if item in row:
##				print 'Found matching ' + item
##                                zf_w.writerow(row)
##                print '***************'
##                
## with open('pins-1.csv',mode='rb') as f:
##	f_r = csv.reader(f, delimiter=',')
##	rows = [row for row in f_r]
##	flat_list = [item for s:Qublist in rows for item in sublist]
