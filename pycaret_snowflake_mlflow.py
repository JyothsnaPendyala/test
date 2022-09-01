import pandas as pd
import numpy as np
import pickle

import snowflake.connector
#import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

#importing from the snowflake
print("Intigrating with Snowflake....")
url = URL(
       user='jyothsna',
    password = 'Jyo1999@',
    account='VHB20271.us-east-1',
    warehouse='compute_wh',
    database='test_db',
    schema='test_table',
)
engine = create_engine(url)
 
connection = engine.connect()

print("Importing the data")
query = "select * from test_2"
 
data = pd.read_sql(query, connection)
 
print(data.head())


features_na = [features for features in data.columns if data[features].isnull().sum() > 0]
for feature in features_na:
    print(feature, np.round(data[feature].isnull().mean()))
else:
    print("no missing value found")
# Find Features with One Value
for column in data.columns:
    print(column,data[column].nunique())
#Exploring the Categorical Features
categorical_features = [feature for feature in data.columns if ((data[feature].dtypes=='O') & (feature not in ['y']))]
print(categorical_features)
for feature in categorical_features:
    print('The feature is {} and number of categories are {}'.format(feature,len(data[feature].unique())))
#list of numerical features
numerical_features = [feature for feature in data.columns if ((data[feature].dtypes != 'O') & (feature not in ['y']))]
print('Number of numerical variables:', len(numerical_features))

#visualize the numerical variables
print(data[numerical_features].head())
#finding outliers in numerical features
print(data['y'].groupby(data['y']).count())
y_no_count, y_yes_count =data['y'].value_counts()
y_yes = data[data['y'] == 'yes']
y_no = data[data['y'] == 'no']
y_yes_over = y_yes.sample(y_no_count,replace=True)
df_balanced = pd.concat([y_yes_over,y_no], axis=0)
print(df_balanced['y'].groupby(df_balanced['y']).count())
df2=df_balanced.copy()
df2.replace({'job':{'management':'0','technician':'1','entrepreneur':'2','blue-collar':'3','unknown':'4','retired':'5','admin.':'6','services':'7','self-employed':'8','unemployed':'9','housemaid':'10','student':'11'}},inplace=True)
df2.replace({'marital':{'single':'0','married':'1','divorced':'2','unknown':'3'}},inplace=True)
df2.replace({'education':{'primary':'0','secondary':'1','tertiary':'2','unknown':'3'}},inplace=True)
df2.replace({'contact':{'cellular':'0','telephone':'1','unknown':'2'}},inplace=True)
df2.replace({'month':{'jan':'0','feb':'1','mar':'2','apr':'3','may':'4','jun':'5','jul':'6','aug':'7','sep':'8','oct':'9','nov':'10','dec':'11'}},inplace=True)
df2.replace({'poutcome':{'failure':'0','success':'1','unknown':'2','other':'3'}},inplace=True)
df2.groupby(['y','defautlt']).size()
df2.drop(['defautlt'],axis=1, inplace=True)
df2.groupby(['y','pdays']).size()
df2.drop(['pdays'],axis=1, inplace=True)
# remove outliers in feature age...
df2.groupby('age',sort=True)['age'].count()
# remove outliers in feature balance...
df2.groupby(['y','balance'],sort=True)['balance'].count()
# these outlier should not be remove as balance goes high, client show interest on deposit
# remove outliers in feature campaign...
df2.groupby(['y','campaign'],sort=True)['campaign'].count()
df3 = df2[df2['campaign'] < 40]
df3.groupby(['y','campaign'],sort=True)['campaign'].count()
df3.groupby(['y','previous'],sort=True)['previous'].count()
df4 = df3[df3['previous'] < 50]
df4.groupby(['y','previous'],sort=True)['previous'].count()
bool_columns = ['housing', 'loan', 'y']
for col in  bool_columns:
    df4[col+'_new']=df4[col].apply(lambda x : 1 if x == 'yes' else 0)
    df4.drop(col, axis=1, inplace=True)

'''print("checking the null values")
print(df.isnull().sum())         #chcking the null values
print(df.shape)

print("Checking the duplicates")
duplicate = df[df.duplicated()]          #checking the duplicates
print(duplicate.shape ) 
print(duplicate.index)

print("Removing the duplicates")
df.drop_duplicates(inplace = True)

from sklearn.preprocessing import LabelEncoder
LE = LabelEncoder()
print(df.gender.unique())
print(df.lung_cancer.unique())


df.gender = LE.fit_transform(df.gender)
df.lung_cancer = LE.fit_transform(df.lung_cancer)

print(df.head())'''
print(df4.head())
#from the pycarrot training
from pycaret.classification import *
training = setup(data = df4, target = 'y_new', log_experiment = True, experiment_name = 'bank-term-deposit-prediction')

print(training)
best = compare_models(cross_validation=True)


final_best = finalize_model(best)
#print(best)

#saving to pickle
print("Pickle file is creating......")
with open("my_model", 'wb') as f:
    pickle.dump(final_best,f)
print("Done _|_")


