import geo
import pandas as pd 
import us

local = 'C:/Users/Diane_HU/Desktop/SURF/Data/'

def getAllCounty(county_list,state_list):
    res=set()
    for index,county in county_list.items():
        split_c = county.split('|')
        append_state = state_list[index]
        # print(append_state)
        split_c = [append_state+"|"+county for county in split_c]
        res.update(split_c)
    return res

def getCountyMSAMatch(data, all_county):
    #credit to: https://gist.github.com/rogerallen/1583593
    us_state_abbrev = {'Alabama': 'AL','Alaska': 'AK','American Samoa': 'AS',
        'Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO',
        'Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC',
        'Florida': 'FL','Georgia': 'GA','Guam': 'GU','Hawaii': 'HI','Idaho': 'ID',
        'Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY',
        'Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA',
        'Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO',
        'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH',
        'New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC',
        'North Dakota': 'ND','Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK',
        'Oregon': 'OR','Pennsylvania': 'PA','Puerto Rico': 'PR','Rhode Island': 'RI',
        'South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX',
        'Utah': 'UT','Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA',
        'Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}

    # thank you to @kinghelix and @trevormarburger for this idea
    abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

    msa_match = [None]*(len(all_county))
    msa_type= [None]*(len(all_county))
    msa_state = [None]*(len(all_county))
    for index_c,county in enumerate(all_county):
        a = county.split('|')
        state = a[0]
        county = a[1] 
        for index_r, row in county_to_msa.iterrows():
            if (row['County/County Equivalent'].find(county) != -1 and abbrev_us_state[state]==row['State Name']):
                msa_match[index_c] = row['CBSA Title']
                msa_type[index_c] = row['Metropolitan/Micropolitan Statistical Area'] 
                msa_state[index_c] = row['State Name']

    all_county = pd.Series(list(all_county))
    frame = {'county':all_county,'MSA':pd.Series(msa_match),'MSA_type':pd.Series(msa_type),'MSA_state':pd.Series(msa_state)}
    res = pd.DataFrame(frame)
    geo.export(res,'res',False)

def getCount(year_type,data,all_county):
    if year_type=='year_applied':
        applied_year = list(data.year_applied.unique())
    else:applied_year = list(data.year_granted.unique())
    applied_year.sort()
    columns = list(all_county)
    columns.sort()
    df = pd.DataFrame(index = columns,columns=applied_year)
    df = df.fillna(0) 
    counter = 0
    for index, patent in data.iterrows():
        counter+=1
        if (counter%1000==0):print(counter)
        year_applied = int(patent[year_type])
        county = patent['county'].split('|')
        num_county = len(county)
        add = 1/num_county
        state = patent['state']
        location = [state+"|"+c for c in county]
        for loc in location:
            df.loc[loc,year_applied]+=add
    geo.export(df,'count_by_'+year_type,True)

#==================================================
#implement
#==================================================
# data = geo.geo_main()
# data = data.reset_index(drop=True)
# county_to_msa = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/msa.csv',header=0)
# all_county = getAllCounty(data['county'],data['state'])
# getCountyMSAMatch(data,all_county)
# ==> output res.csv that pair up 'state|county' and its MSA/muSA 
# ==> Input by hand: None if not in any MSA/muMA, 
#     'state name' column always filled with the correct state name
# getCount('year_applied',data,all_county)
# ==> output count_by_year_applied.csv or count_by_year_granted
# ==> get count by 'state|county' and by year granted/ year applied
# Combine by hand count_by_year_applied.csv and res.csv with sorted 'state|county' name

# count_combined = pd.read_csv(r'C:/Users/Diane_HU/Desktop/SURF/Data/count_by_year_granted.csv',header=0)
# count_final = count_combined.groupby(['MSA','MSA_type','MSA_state']).sum()
# geo.export(count_final,'count_final_by_year_granted',True)


