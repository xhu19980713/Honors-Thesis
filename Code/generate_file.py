import os 
import pandas as pd 
import geo 


def generate_file(year):
    #year: {2015,2016,2017}/None, if NULL, ignore time 
    
    #import
    GDP = pd.read_excel(r'C:/Users/Diane_HU/Desktop/SURF/Data/metro_gdp.xls',header=0)
    POP = pd.read_excel(r'C:/Users/Diane_HU/Desktop/SURF/Data/metro_population.xlsx',header=0) 
    U = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/university_rd_exp_by_metro.csv',header=0)
    I = pd.read_excel(r'C:/Users/Diane_HU/Desktop/SURF/Data/bus_expenditure.xlsx',header=1)
    I = I.iloc[:130,:]#Index(['CBSA', 'Metro?', 2015, 'Unnamed: 3', 2016, 'Unnamed: 5', 2017,'Unnamed: 7'],
    K = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/count_final_by_year_applied.csv',header=0)
    FIPS = pd.read_excel(r'C:/Users/Diane_HU/Desktop/SURF/Data/cbsa_fips.xls',header=0)
    Weight = pd.read_excel(r'C:/Users/Diane_HU/Desktop/SURF/Data/weight.xlsx',sheet_name=1,header=0)
    
    #subset 
    I_subset = I[(I[year].notnull()) & (I['Metro?']==1)]
    MSA_list = I_subset[['CBSA',year]]
    n = len(MSA_list)
    
    U_subset = U[['Metro Area',str(year)]]
    U_subset = U_subset.rename(columns={str(year):"U"})

    K_subset = K[['Metro Area',str(year)]]
    K_subset = K_subset.rename(columns={str(year):"K"})

    GDP_subset = GDP[['Metro Area',str(year)]]
    GDP_subset = GDP_subset.rename(columns={str(year):"GDP"})
    
    POP_subset = POP[['Metro Area',year]] 
    POP_subset = POP_subset.rename(columns={year:"POP"})

    
    FIPS = FIPS.rename(columns={'CBSA':'Metro Area'})


    #reconstruct
    frame = {'Metro Area':MSA_list['CBSA'],"I":MSA_list[year]}
    result = pd.DataFrame(frame)
    result = pd.merge(result,U_subset,on=["Metro Area"],how='left')
    result = pd.merge(result,K_subset,on=["Metro Area"],how='left')
    result = pd.merge(result,GDP_subset,on=["Metro Area"],how='left')
    result = pd.merge(result,POP_subset,on=["Metro Area"],how='left')
    result = pd.merge(result,FIPS,on=["Metro Area"],how='left')

    geo.export(result,"result_"+str(year),True)
    geo.export(result['FIPS'],"fips_subset",False)
    FIPS_set = set(result['FIPS'].values.tolist())

    text_file = open("sample_"+str(year)+"_2.txt", "w")
    first_line = "0 "+str(n)+" tl_2019_us_cbsa CBSAFP"+"\n"
    text_file.write(first_line)
    for index, row in Weight.iterrows():
        o = row["Origin"]
        d = row["Destination"]
        w = row["Weight"]
        if ((o in FIPS_set) and (d in FIPS_set)): 
            num_space = 19 - len(str(w))
            space = " "*num_space
            line = str(int(o))+" "+str(int(d))+space+str(w)+"\n"
            text_file.write(line)
    text_file.close()

    

###### MAIN #########
#generate_file(2017)