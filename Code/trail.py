import us
import csv
import pandas as pd
import fuzzy_pandas as fpd 
import geo


# trail =pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/trail1.csv',header=0)
# trail = trail[trail['city_ascii'].isnull()]
# res = trail.groupby(['city','state']).size().reset_index().rename(columns={0:'count'})
# res.to_csv('C:/Users/Diane_HU/Desktop/SURF/Data/problem_city.csv',index=False)

# trail = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/remain.csv',header=0)

# def getCounty(word):
#     if word[-6:]=='County': return word[:-7]
# trail['county']=trail['city'].apply(removeCounty)

# # zipcode = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/zip_code_database.csv',header=0)
# # /zipcode = zipcode.groupby(['city','state','county']).size().reset_index().rename(columns={0:'new_count'})
# # print("lala")
# # res =fpd.fuzzy_merge(trail,zipcode,on=['state','city'],method='metaphone',threshold=0.6,ignore_case=True, ignore_nonalpha=True,join='left-outer')
# # print("hoho")
# trail.to_csv('C:/Users/Diane_HU/Desktop/SURF/Data/problem_city.csv',index=False
# BOOK3 = pd.read_excel(r'C:/Users/Diane_HU/Desktop/SURF/Data/Book3.xlsx',header=0)
# county_to_msa = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/Geography Related/county_to_MSA_subset.csv',header=0)

# BOOK3 = pd.merge(BOOK3,county_to_msa,on=['State Name','County/County Equivalent'],how="left")
# geo.export(BOOK3,'BOOK4',False)

# book1 = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/city_to_county_.csv',header=0)
# book2 = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/Geography Related/problem_city.csv',header=0)
# book = book1.append(book2)
# print(book[book[['city','state']].duplicated()])

ctc = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/Geography Related/city_to_county_finalized.csv',header=0)
ctm = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/Geography Related/county_to_MSA_fitted.csv',header=0)
city_to_msa = pd.merge(ctc,ctm,on=["county","state"],how="left")
geo.export(city_to_msa,"city_to_MSA",False)