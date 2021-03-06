low_memory=False
import pandas as pd
filename = 'C:/data/properties_2017.csv'
df = pd.read_csv(filename)

# to get null counts for the dataframe columns
#print(df.isnull().sum())


# to see the distinct values with counts of a particular column
#print(df.bathroomcnt.value_counts(dropna=False))


# list of columns to use on the new dataframe
use_col_list = ['bathroomcnt',
'bedroomcnt', 
'calculatedbathnbr',
'calculatedfinishedsquarefeet',
'finishedsquarefeet12', 
'fips',  
'fireplacecnt', 
'fireplaceflag',
'fullbathcnt',
'hashottuborspa',
'latitude',
'longitude',
'lotsizesquarefeet',
'numberofstories',
'parcelid',
'poolcnt',
'pooltypeid10',
'pooltypeid2',
'pooltypeid7',
'regionidcounty',
'regionidcity',
'regionidzip',
'roomcnt',
'unitcnt',
'yardbuildingsqft17',
'yardbuildingsqft26',
'yearbuilt',
'taxvaluedollarcnt',
'structuretaxvaluedollarcnt',
'landtaxvaluedollarcnt',
'taxamount',
'assessmentyear',
'taxdelinquencyflag']
   
# creating the new dataframe
#df_new = df[use_col_list]
df_new = df

# dropping null records column list
drop_null_col_list = ['bathroomcnt',
'bedroomcnt',
'calculatedfinishedsquarefeet',
'finishedsquarefeet12',
'fips',
'latitude',
'longitude',
'lotsizesquarefeet',
'regionidcounty',
'regionidcity',
'regionidzip',
'roomcnt',
'yearbuilt',
'taxvaluedollarcnt',
'structuretaxvaluedollarcnt',
'landtaxvaluedollarcnt',
'taxamount',
'assessmentyear']


# dropping nulls from column's i'm identifying
df_new_remove_nulls = df_new.dropna(axis=0, subset=drop_null_col_list)

# count number of records left
#print(df_new_remove_nulls.shape)

# replace NaN with 0 column list
replace_nan_with_zero_col_list = ['calculatedbathnbr',
'fireplacecnt',
'fullbathcnt',
'poolcnt',
'pooltypeid10',
'pooltypeid2',
'pooltypeid7',
'fireplaceflag',
'hashottuborspa',
'taxdelinquencyflag'
]

# replacing NaN with 0 from column's i'm identifying
df_new_remove_nulls[replace_nan_with_zero_col_list] = df_new_remove_nulls[replace_nan_with_zero_col_list].fillna(0)

# changing the name of the df to make more sense
df_change_nans_to_zero = df_new_remove_nulls

# see the results of the replace
#print(df_change_nans_to_zero.fireplaceflag.value_counts(dropna=False))


# replace True with 1 column list
replace_true_with_1_col_list = ['fireplaceflag',
'hashottuborspa',
'taxdelinquencyflag']

# replacing True with 1 from column's i'm identifying
df_change_nans_to_zero[replace_true_with_1_col_list] = df_change_nans_to_zero[replace_true_with_1_col_list].replace(True,1)

# changing the name of the df to make more sense
df_replace_true_with_1 = df_change_nans_to_zero

# see the results of the replace
#print(df_replace_true_with_1.hashottuborspa.value_counts(dropna=False))


# change float columns to int
float_col = ['fips',
'latitude',
'longitude',
'parcelid',
'regionidcounty',
'regionidcity',
'regionidzip',
'yearbuilt',
'assessmentyear']

df_replace_true_with_1[float_col] = df_replace_true_with_1[float_col].astype(int) 


# changing the name of the df to make more sense
df_convert_float_to_int = df_replace_true_with_1



# check for bad data. find columns with values < 0
bad_col_check = ['bathroomcnt',
'bedroomcnt',
'calculatedbathnbr',
'calculatedfinishedsquarefeet',
'finishedsquarefeet12',
'fips',
'fireplacecnt',
'fireplaceflag',
'fullbathcnt',
'hashottuborspa',
'latitude',
'longitude',
'lotsizesquarefeet',
'numberofstories',
'parcelid',
'poolcnt',
'pooltypeid10',
'pooltypeid2',
'pooltypeid7',
'regionidcounty',
'regionidcity',
'regionidzip',
'roomcnt',
'unitcnt',
'yardbuildingsqft17',
'yardbuildingsqft26',
'yearbuilt',
'taxvaluedollarcnt',
'structuretaxvaluedollarcnt',
'landtaxvaluedollarcnt',
'taxamount',
'assessmentyear',
'taxdelinquencyflag']

for col in bad_col_check:
    if df_convert_float_to_int[col].all() < 0:
        print(col, " has unexpected values")


# creating zscore dataframe
df_analysis = df_convert_float_to_int 

from scipy.stats import zscore
cols = ['bathroomcnt',
'bedroomcnt',
'calculatedbathnbr',
'calculatedfinishedsquarefeet',
'finishedsquarefeet12',
'fireplacecnt',
'fullbathcnt',
'lotsizesquarefeet',
'numberofstories',
'poolcnt',
'pooltypeid10',
'pooltypeid2',
'pooltypeid7',
'roomcnt',
'unitcnt',
'yardbuildingsqft17',
'yardbuildingsqft26',
'taxvaluedollarcnt',
'structuretaxvaluedollarcnt',
'landtaxvaluedollarcnt',
'taxamount']

for col in cols:    
    col_zscore = col + 'z_score'
    df_analysis[col_zscore] = zscore(df_analysis[col])
    df_analysis[col_zscore] = abs(df_analysis[col_zscore])
    #outliers = df_analysis[col_zscore] > 3
    #df_outliers = df_analysis.loc[outliers]
    
    
# outlier removal on df. in a for loop
df_outlier_removal = df_analysis 



# removing outliers from certain columns with abs(zscore) > 1.5
df_outlier_removal = df_outlier_removal[df_outlier_removal['taxvaluedollarcntz_score'] < 1.5]
df_outlier_removal1 = df_outlier_removal[df_outlier_removal['lotsizesquarefeetz_score'] < 1.5]
#df_outlier_removal2 = df_outlier_removal1[df_outlier_removal['roomcntz_score'] < 1.5]


#df_explore['taxvaluedollarcntz_score'].sort_values(ascending=False).head(5)



df_explore = df_outlier_removal1


df_sample = df_explore.sample(500)
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


#histogram
bin_edges = [0,100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000,1100000,1200000,1300000,1400000,1500000]
df_sample['taxvaluedollarcnt'].plot('hist', bins=bin_edges)
plt.ylabel('count of homes')
plt.xlabel('home value')
plt.show()

# swarmplot
df_sample = df_explore.sample(1000)
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
var_x = 'bathroomcnt'
var_y = 'taxvaluedollarcnt'
_ = sns.swarmplot(x=var_x,y=var_y, data =df_sample)
_ = plt.xlabel('# of bathrooms')
_ = plt.ylabel('tax assessed price')
plt.show()


