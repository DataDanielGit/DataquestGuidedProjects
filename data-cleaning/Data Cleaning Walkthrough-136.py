## 4. Reading in the Data ##

import pandas as pd
data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]
key_name = ["ap_2010", "class_size", "demographics", "graduation", "hs_directory", "sat_results"]
data = {}


for num in range(len(data_files)):
    data[key_name[num]] = pd.read_csv(r"schools/{0}".format(data_files[num]))

    

## 5. Exploring the SAT Data ##

data["sat_results"].head(5)

## 6. Exploring the Remaining Data ##

for i in data:
    print(data[i].head())

## 8. Reading in the Survey Data ##

all_survey = pd.read_csv('schools/survey_all.txt', encoding = "windows-1252", delimiter = '\t')

d75_survey = pd.read_csv('schools/survey_d75.txt', encoding = 'windows-1252', delimiter = '\t')

survey = pd.concat([all_survey, d75_survey], axis = 0)
survey.head()

## 9. Cleaning Up the Surveys ##

survey['DBN'] = survey['dbn']
columns_keep = ["DBN", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11", "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11", "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11"]
survey = survey.loc[:,columns_keep]

data['survey'] = survey

## 11. Inserting DBN Fields ##

data['hs_directory']['DBN'] = data['hs_directory']['dbn']
def pad_csd(x):
    x = str(x)
    if len(x) == 2:
        return x
    elif len(x) < 2:
        return x.zfill(2)
    

data['class_size']['padded_csd'] = data['class_size']['CSD'].apply(pad_csd)

#data['class_size']['padded_csd'].head()

data['class_size']['DBN'] = data['class_size']['padded_csd'] + data['class_size']['SCHOOL CODE']

data['class_size']['DBN'].head()








## 12. Combining the SAT Scores ##

convert_list = ['SAT Math Avg. Score','SAT Critical Reading Avg. Score','SAT Writing Avg. Score']
    
for i in range(3):
    data['sat_results'][convert_list[i]] = pd.to_numeric(data['sat_results'][convert_list[i]], errors = 'coerce')
    #print(data['sat_results'][convert_list[i]].dtypes)   

data['sat_results']['sat_score'] = data['sat_results'][convert_list[0]] + data['sat_results'][convert_list[1]] + data['sat_results'][convert_list[2]]
    
data['sat_results']['sat_score'].head()

## 13. Parsing Geographic Coordinates for Schools ##

import re

def get_lat(x):
    coords = re.findall("\(.+\)", x)
    lat = coords[0].split(",")[0].replace(",", "").replace("(","")
    return lat

data['hs_directory']['lat'] = data['hs_directory']['Location 1'].apply(get_lat)

data['hs_directory'].head()

## 14. Extracting the Longitude ##

import re
# def get_lat(x):
#     coords = re.findall("\(.+\)", x)
#     lat = coords[0].split(",")[0].replace(",", "").replace("(","")
#     return lat

# data['hs_directory']['lat'] = data['hs_directory']['Location 1'].apply(get_lat)

# data['hs_directory'].head()

def get_lon(loc):
    coords = re.findall("\(.+\)", loc)
    lon = coords[0].split(",")[1].replace(")", "").strip()
    return lon

data['hs_directory']['lon'] = data['hs_directory']['Location 1'].apply(get_lon)

data['hs_directory']['lat'] = pd.to_numeric(data['hs_directory']['lat'], errors = 'coerce')
data['hs_directory']['lon'] = pd.to_numeric(data['hs_directory']['lon'], errors = 'coerce')
data['hs_directory'].head()
    