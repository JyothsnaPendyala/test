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

    #visualize the numerical variables
    print(data[numerical_features].head())
    #finding outliers in numerical features
    '''plt.figure(figsize=(20,40), facecolor='white')
    plotnumber=1
    for numerical_feature in numerical_features:
        ax = plt.subplot(12,3,plotnumber)
        sns.boxplot(data[numerical_feature])
        plt.xlabel(numerical_feature)
        plotnumber+=1
    plt.show()
    cor_mat = data.corr()
    fig = plt.figure(figsize=(15,7))
    sns.heatmap(cor_mat,annot=True)'''
    print(data['y'].groupby(data['y']).count())
    y_no_count, y_yes_count =data['y'].value_counts()
    y_yes = data[data['y'] == 'yes']
    y_no = data[data['y'] == 'no']
    y_yes_over = y_yes.sample(y_no_count,replace=True)
    df_balanced = pd.concat([y_yes_over,y_no], axis=0)
    print(df_balanced['y'].groupby(df_balanced['y']).count())
    

data_analysis()
