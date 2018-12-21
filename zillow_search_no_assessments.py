# Author : Supriya Koduri
# general imports
#import urllib2
import json
import urllib
import requests
import csv

#'year', 'landValue', 'improvementValue','totalValue','marketValueYear', 'marketLandValue','marketImprovementValue','marketTotalValue'

def process_input(in_csv, token='3a6660f85a4e56f19fef7790e48ee55e'):
    #token='3a6660f85a4e56f19fef7790e48ee55e'
    out_file = in_csv.split('.')[0]+'-out.csv'
    with open(out_file, mode = 'w') as zf:
        zf_w = csv.writer(zf, delimiter=',')
        zf_w.writerow(['Address', 'Owner', 'LandUseDesc', 
                       'lotSizeSquareFeet',  'areaSquareFeet', 'yearBuilt', 'totalStories', \
                       'bedrooms', 'fullbaths', 'airConditioning','heating','foundation', \
                       'occupancyStatus', 'Garage', 'Zpid', 'parcelID','LandUseCode', 'LandUseGeneral', \
                       'zestimate', 'rental zestimate', \
                       'year', 'landValue', 'improvementValue', 'totalValue', 'marketValueYear', \
                       'marketLandValue', 'marketImprovementValue', 'marketTotalValue'])
        with open(in_csv, encoding='utf-8') as in_file:
            in_read = csv.reader(in_file, delimiter=',')
            line_count = 0
            next(in_read)
            for row in in_read:
                line_count += 1
                address_r = row[0]
                city_r = row[1]
                state_r = row[2]
                zip_r = zip_5 = row[3]
    
                #print address_r, city_r, state_r, zip_r
                if len(zip_r) > 5:
                    zip_5 = zip_r.split('-')[0]
                parcel_row, pid, zpid = search_zillow(token, address_r, city_r, zip_5)
                
                assessment_row = []
                zestimate_row = []
                #if pid :
                #    assessment_row = get_assessments(token, pid)
                if zpid:
                    zestimate_row =  get_zestimates(token, zpid)

                add_row = parcel_row + zestimate_row + assessment_row
                zf_w.writerow(add_row)

        #print 'Processed '+line_count+" Addresses"
            

def search_zillow(token,street_name,city,zipcode):
    #url = "https://rets.io/api/v2/pub/parcels?access_token={}&address.city.in={}&address.zip.in={}&address.full.in={}"
    data = {}
    data['address.city.in']=city
    data['address.full.in']=street_name
    data['address.zip.in']=zipcode
    data['access_token']=token

    url_v = urllib.parse.urlencode(data) 
    #url2 =  url.format(token,city,zipcode,street_name)
    url ="https://rets.io/api/v2/pub/parcels?"
    f_url = url+url_v

    #print(f_url)
    #print "============================================"
    r = requests.get(f_url)
 #   r = requests.get(f_url)
 
    d_r = r
    #print d_r.__dict__
    #print d_r.__dict__['_content']
    #d_j = json.loads(d_r.__dict__['_content'])
    d_j = json.loads(d_r.content)
    #print "***** %d *******",r.status_code

    row = []
    pid = ''
    zpid = ''
    if d_j['total'] >= 1:
        actual_data = d_j['bundle'][0]
        
        add = actual_data['address']['full']
        owner = ",".join(actual_data['ownerName'])
        lud = actual_data['landUseDescription']
        luc = actual_data['landUseCode']
        lug = actual_data['landUseGeneral']
        lssf = actual_data['lotSizeSquareFeet']
        pid = actual_data['parcelID']
        if actual_data['areas']:
            asf = actual_data['areas'][0]['areaSquareFeet']
        else:
            asf = " "
        if actual_data['building']:
            yb =  actual_data['building'][0]['yearBuilt']
            ts = actual_data['building'][0]['totalStories']
            bed = actual_data['building'][0]['bedrooms']
            baths = actual_data['building'][0]['fullBaths']
            ac = actual_data['building'][0]['airConditioning']
            heat = actual_data['building'][0]['heating']
            f = actual_data['building'][0]['foundation']
            os = actual_data['building'][0]['occupancyStatus']
        else:
            yb = ts=bed=baths=ac=heat=f=os=" "
        if actual_data['garages']:
            car = actual_data['garages'][0]['carCount']
        else:
            car = " "
        zpid = actual_data['zpid']
        row = [add,owner,lud,lssf,asf,yb,ts,bed,baths,ac,heat,f,os,car,zpid, pid,luc,lug]
    else:
        #print "***** %d *******", d_j['total']
        address = "{} {} {}".format(street_name, city, zipcode)
        row = [address]
    return row, pid, zpid
    #print data_json

#search_zillow(212,"5158 meadowlake lane","dunwoody",30338)

def get_assessments(token,parcelId):
    data = {}
    data['access_token']=token


    url_v = urllib.parse.urlencode(data) 
    #url2 =  url.format(token,city,zipcode,street_name)
    url ="https://rets.io/api/v2/pub/parcels/"+str(parcelId)+"/assessments?"

    f_url = url + url_v

    #print f_url
    #print "============================================"
    r = requests.get(f_url)
  #  r = requests.get(f_url)
    d_j = json.loads(r.content)    

    row = []
    try:    
        if d_j['total'] >= 1:  
            actual_data = d_j['bundle']
        
            year_list = [d['year'] for d in actual_data]
            #print d_j['total'], len(actual_data), 
            #print year_list
            max_year = max(year_list)
            element = [i for i , j in enumerate(year_list) if j == max_year]

            my_a = actual_data[element[0]]
            year =my_a['year']
            lv = my_a['landValue']
            iv = my_a['improvementValue']
            tv = my_a['totalValue']	
            mvy = my_a['marketValueYear']	
            mlv = my_a['marketLandValue']	
            miv = my_a['marketImprovementValue']
            mtv = my_a['marketTotalValue']
                
            row = [year, lv, iv, tv, mvy, mlv, miv, mtv]
    except:
        #print("No assessments found for ",str(parcelId))
        #print "No assessments found for "+ str(parcelId)
        pass
    return row

def get_zestimates(token, zpid):
    data = {}
    data['zpid']=zpid
    data['access_token']=token

    url_v = urllib.parse.urlencode(data) 
    #url2 =  url.format(token,city,zipcode,street_name)
    url ="https://rets.io/api/v2/zestimates?"

    f_url = url + url_v

    #print f_url
    #print "============================================"
    r = requests.get(f_url)
  #  r = requests.get(f_url)
    d_j = json.loads(r.content)

    row = []
    
    try:
        if d_j['total'] == 1:  
            actual_data = d_j['bundle']
            zestimate = actual_data[0]['zestimate']
            rental_zest = actual_data[0]['rental']['zestimate']
    
            row = [zestimate, rental_zest]
    except:
        print("No Zestimates found for ",str(zpid))
        #print "No Zestimates found for "+str(zpid)
        #pass
        
    return row

#process_input(in_csv='Test-data.csv')
#process_input(in_csv='Test-data.csv')

import argparse
import sys

if __name__ == "__main__":
       parser = argparse.ArgumentParser()
       parser.add_argument("filename", help="Give the exact name of the input file (name file without spaces)")
       parser.add_argument("--token",help="optional -give token if changed")
       args = parser.parse_args()
       #print(args.filename)
       if args.token:
           process_input(args.filename,args.token)
       else:
           process_input(args.filename)

##    #print sys.argv
##    if len(sys.argv) < 2:
##        sys.exit('Usage: python zillow_search.py <input CSV file name>')
##
##    process_input(sys.argv[1])
