from census import Census
import us
import os
from xml.dom import minidom
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
pd.options.mode.chained_assignment = None


local = 'C:/Users/Diane_HU/Desktop/SURF/Data/'

def export(df,fileName,index_flag):
    df.to_csv(local+fileName+".csv",index=index_flag,encoding='utf-8')

def importFiles():
    #import all inventor_address
    inventor_address = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/Patent Subset/inventor_address.csv',
                        names=['doc_number','year_applied','year_granted','country','state','city'],
                        header=None)
    inventor_address['wait_year']= inventor_address['year_granted']-inventor_address['year_applied']

    #print(inventor_address['wait_year'].value_counts())

    #select those that are in US and state not null 
    #if country='US' and state null ==> military address based not in US, eg: APO AE
    us_patent = inventor_address[(inventor_address['country']=='US') & (inventor_address['state'].notnull())]

    #import city to county and select columns needed:city,city_ascii,state_name,county_name_all,county_fips_all
    city_to_county = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/Geography Related/city_to_county.csv',header=0)
    city_to_county = city_to_county[['city','state_id','county_name_all']]
    city_to_county = city_to_county.rename(columns={"state_id":"state"})
    # export(city_to_county,"city_to_county_1",False)
    # print(city_to_county[city_to_county[['city','state']].duplicated()])
    #import county to MSA and select columns needed: CBSA Code,CBSA Title, Metropolitan/Micropolitan Statistical Area
    #County/County Equivalent, State Name, FIPS State Code, FIPS County Code
    county_to_msa = pd.read_excel(r'C:/Users/Diane_HU/Desktop/SURF/Data/Geography Related/county_to_MSA.xls',header=0)
    county_to_msa = county_to_msa[['CBSA Code','CBSA Title','Metropolitan/Micropolitan Statistical Area',
                                'County/County Equivalent','State Name', 'FIPS State Code', 'FIPS County Code']]
    return (us_patent,city_to_county,county_to_msa)
# export us_patent for reference
def export(df,fileName,index_flag):
    df.to_csv(local+fileName+".csv",index=index_flag,encoding='utf-8')

#match city to county
def city_county_match(a,b):
    res = pd.merge(a,b,on=['city','state'],how='left')
    return res



#==================================================
#implement
#==================================================
def geo_main():
    us_patent,city_to_county,county_to_msa = importFiles()
    # print(us_patent.count()): 1843526
    trail = city_county_match(us_patent,city_to_county)
    # print(trail.count()): 1843526
    trail = trail.rename(columns={"county_name_all":"county"})
    full = trail[trail['county'].notnull()]  #1597115
    empty = trail[trail['county'].isnull()] #246411
    empty = empty.drop(['county'], axis=1) #246411

    addition = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/Geography Related/problem_city.csv',header=0)
    # print(addition[addition[['city','state']].duplicated()])
    empty = pd.merge(empty,addition,on=['city','state'],how='left') ##246411
    county_matched = full.append(empty)
    county_matched_full = county_matched[county_matched['county'].notnull()]
    return county_matched_full



