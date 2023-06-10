from load_data import load_data
'''import numpy as np
import pandas as pd'''
'''import seaborn as sns'''
'''import matplotlib.pyplot as plt'''
def data_analysis():
    data = load_data()
    #data = pd.read_csv('bank.csv')
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
    return data
    

data_analysis()
