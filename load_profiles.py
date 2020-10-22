#-*- coding: utf-8 -*-
"""
Create generic nutrition profiles based on age, gender, and/or pregnancy status
by importing dietary reference intakes provided by the Food and Nutrition Board,
Institute of Medicine, National Academies. Default URLs are good as of May, 2019.
"""
import pandas as pd
import requests, pickle

"""
Source urls for profiles:

url_macros = 'https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t4/?report=objectonly'
url_vitamins_rda = 'https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t2/?report=objectonly'
url_vitamins_ul = 'https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t7/?report=objectonly'
url_minerals_rda = 'https://www.ncbi.nlm.nih.gov/books/NBK545442/table/appJ_tab3/?report=objectonly'
url_minerals_ul = 'https://www.ncbi.nlm.nih.gov/books/NBK545442/table/appJ_tab9/?report=objectonly'

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
"""

if __name__ == '__main__':

    macros_rda = './profiles/2019 macro rda.ods'
    vitamins_rda = './profiles/2019 vitamin rda.ods'
    vitamins_ul = './profiles/2019 vitamin UL.ods'
    minerals_rda = './profiles/2019 mineral rda.ods'
    minerals_ul = './profiles/2019 mineral UL.ods'

    default_profiles = [macros_rda, vitamins_rda, vitamins_ul,
                    minerals_rda, minerals_ul]

    gender = ['Infant']*3
    gender.extend(['Child']*3)
    gender.extend(['Male']*7)
    gender.extend(['Female']*7)
    gender.extend(['Pregnant']*4)
    gender.extend(['Lactating']*4)
    
    dfs = [pd.read_excel(x, engine='odf') for x in default_profiles]
        
    for x in range(0, len(dfs)):        
        # Add appropriate gender for each row. Used later for indexing.
        dfs[x]['Gender'] = gender
    
        # Drop rows that only gender.
        dfs[x] = dfs[x].set_index('Age Range').drop(set(gender))
        dfs[x].reset_index(inplace=True)
            
        # Multi-index age range then gender
        dfs[x].set_index(['Age Range', 'Gender'], inplace=True)
        
        if x in [2,4]:
            dfs[x].rename(columns=lambda x: x + ' UL', inplace=True)
            
        dfs[x].fillna('n/a', inplace=True)
        
    # merge all dataframes
    merged = dfs[0]
    for x in range(1, len(dfs)):
        merged = merged.merge(dfs[x], left_index=True, right_index=True)
    
    # create custom dictionary from dataframe
    res_dict = {}
    for x,y in merged.groupby(level=0):
        index = y.index.values
        for x in index:
            gender = {x[1]: y.loc[x].to_dict()}
            if x[0] in res_dict:
                res_dict[x[0]].update(gender)
            else:
                res_dict[x[0]] = gender
    
    desired_order = ['0-6 mo','7-12 mo','1-3 yr','4-8 yr','9-13 yr',
                     '14-18 yr','19-30 yr','31-50 yr','51-70 yr','>70 yr']
    
    res_dict = {x: res_dict[x] for x in desired_order}
    
    pickle.dump(res_dict, open('profiles.p','wb'))
