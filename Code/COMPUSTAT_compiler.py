import os 
import pandas as pd 
import geo

def save_xls(list_dfs, xls_path):
    years = list(range(2004,2019+1))
    with pd.ExcelWriter(xls_path) as writer:
        for n, df in enumerate(list_dfs):
            df.to_excel(writer,str(years[n]))
        writer.save()

def extract_compustat():
    # COMPUSTAT = pd.read_excel(r'C:/Users/Diane_HU/Desktop/SURF/Data/COMPUSTAT.xlsx',header=0)
    # US = COMPUSTAT[COMPUSTAT['Current ISO Country Code - Headquarters']=='USA']
    # US_slim = US[['Global Company Key','Data Year - Fiscal','Industry Format',
    #             'Ticker Symbol','Research and Development Expense','Research & Development - Prior',
    #             'Active/Inactive Status Marker','Postal Code','City','County Code',
    #             'North American Industry Classification Code','State/Province']]
    # ctc = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/Geography Related/city_to_county_finalized.csv',header=0)
    # US_slim_city_matched = pd.merge(US_slim,ctc,how="left",left_on=["City","State/Province"],right_on=["city","state"])
    # geo.export(US_slim_city_matched,"US_slim_city_matched",False)
    #==>After exporting the merged file, hand-matched the unmatched ones 
    US_slim_city_matched = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/US_slim_city_matched.csv',header=0)
    ctm = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/Geography Related/county_to_MSA_fitted.csv',header=0)
    US_slim_MSA_matched = pd.merge(US_slim_city_matched,ctm,how="left",left_on=["State/Province","county"],right_on=["state","county"])
    # geo.export(US_slim_MSA_matched,"US_slim_MSA_matched",False)
    US_slim_MSA_unmatched = US_slim_MSA_matched[US_slim_MSA_matched['MSA'].isnull()]
    US_slim_MSA_matched = US_slim_MSA_matched[US_slim_MSA_matched['MSA'].notnull()]

    #format ctm to dictionary
    ctm=ctm.set_index(['state','county'])
    ctm_dict = ctm.to_dict("index")
    for n,row in US_slim_MSA_unmatched.iterrows():
        county_list=row['county'].split("|")
        state = row["State/Province"]
        msa_set = set()
        msa_type_set =set()
        msa_state_set = set()
        for county in county_list:
            loc = ctm_dict[state,county]
            msa = loc['MSA']
            msa_set.add(msa)
            msa_type = loc['MSA_type']
            msa_type_set.add(msa_type)
            msa_state = loc['MSA_state']
            msa_state_set.add(msa_state)
        US_slim_MSA_unmatched.at[n,'MSA']="|".join(msa_set)
        US_slim_MSA_unmatched.at[n,'MSA_type']="|".join(msa_type_set)
        US_slim_MSA_unmatched.at[n,'MSA_state']="|".join(msa_state_set)
    US_slim_MSA_matched = US_slim_MSA_matched.append(US_slim_MSA_unmatched)
    US_slimer_MSA_matched = US_slim_MSA_matched[["Data Year - Fiscal","Research and Development Expense",
                            "Research & Development - Prior","MSA","MSA_type","MSA_state","state"]]
    assert(len((US_slimer_MSA_matched[US_slimer_MSA_matched['MSA'].notnull()]).index)==len(US_slimer_MSA_matched.index))
    years = list(range(2004,2019+1))
    sort_by_year =[]
    for year in years:
        print(year) 
        by_year = US_slimer_MSA_matched[US_slimer_MSA_matched['Data Year - Fiscal']==year]
        by_year = by_year.groupby(['MSA','MSA_type','MSA_state',"state"]).sum()
        sort_by_year.append(by_year)
    save_xls(sort_by_year,'C:/Users/Diane_HU/Desktop/SURF/Data/COMPUSTAT_by_year.xlsx')

###### MAIN #########
extract_compustat()