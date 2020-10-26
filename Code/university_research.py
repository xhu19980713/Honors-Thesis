import pandas as pd 
import geo

local = 'C:/Users/Diane_HU/Desktop/SURF/Data/'
def getStateUniFunding():
    HERD = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/HERD_Export_2020-08-04T05_33_51.591Z.csv')

    state_funding = HERD[(HERD['Institution Name']=='Total') & (HERD['Broad Field']=='Total')]
    state_funding = state_funding.drop(['Institution Name','Broad Field'],axis=1)
    geo.export(state_funding,'state_funding',False)

    uni_funding = HERD[(HERD['Institution Name']!='Total') & (HERD['Broad Field']=='Total')]
    uni_funding = uni_funding.drop(['Broad Field'],axis=1)

    uni_to_MSA = pd.read_excel(r'C:/Users/Diane_HU/Desktop/SURF/Data/University_to_MSA.xlsx')
    uni_funding = pd.merge(uni_funding,uni_to_MSA,on=['Institution Name'],how='left')
    geo.export(uni_funding,'uni_funding',False)

# fill in the corresponding MSA by hand in uni_funding.csv. 

def removeMSA(metro):
    if metro[-3:]=='MSA':
        return metro[:-4]
    else: return metro

def getU():
    uni_funding = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/uni_funding.csv',header=0)
    uni_funding['Metro Area'] = uni_funding['Metro Area'].apply(removeMSA)
    geo.export(uni_funding,'uni_funding_V2',False)
    uni_funding1= uni_funding[['State','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
    uni_funding2= uni_funding[['Metro Area','2010','2011','2012','2013','2014','2015','2016','2017','2018']]
    U_state = uni_funding1.groupby(['State']).sum()
    U_metro = uni_funding2.groupby(['Metro Area']).sum()
    geo.export(U_state,'university_funding_by_state',True)
    geo.export(U_metro,'university_funding_by_metro',True)
