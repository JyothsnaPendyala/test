import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
import git
import warnings
import sys

import pandas as pd
import numpy as np
import pickle
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score

#import dvc.api
import mlflow
import mlflow.sklearn

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    data = pd.read_csv('bank.csv')
    print(data)

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
    df2.groupby(['y','default']).size()
    df2.drop(['default'],axis=1, inplace=True)
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
    df3.groupby(['y','previous'],sort=True)['previous'].count()
    bool_columns = ['housing', 'loan', 'y']
    for col in  bool_columns:
        df4[col+'_new']=df4[col].apply(lambda x : 1 if x == 'yes' else 0)
        df4.drop(col, axis=1, inplace=True)
    X = df4.drop(['y_new'],axis=1)
    y = df4['y_new']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=0)
    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)
    decision_tree= dt.score(X_test, y_test)
    rt = RandomForestClassifier(n_estimators=100, n_jobs=1)
    rt.fit(X_train, y_train)
    random_forest = rt.score(X_test, y_test)
    lr= make_pipeline(StandardScaler(),LogisticRegression())
    lr.fit(X_train, y_train)
    logistic_regression = lr.score(X_test, y_test)
    results = [decision_tree, random_forest, logistic_regression ]
    maximum = max(results)
    if maximum == decision_tree:
        a = decision_tree
        b = dt
    elif maximum == random_forest:
        a = random_forest
        b = rt
    else:
        a = logistic_regression
        b = lr
    print(a,b)

    with mlflow.start_run():
        b.fit(X_train, y_train)
        filename = 'finalised_model.pkl'
        pickle.dump(b,open(filename,'wb'))
        loaded_model = pickle.load(open(filename,'rb'))
        result1 = loaded_model.score(X_test, y_test)
        result2 = loaded_model.predict(X_test)
        f1_score = f1_score(y_test, result2)
        print(result1, result2)
        print(f1_score)

        mlflow.log_metric("f1_score",f1_score)
        mlflow.log_param("Decision_Tree",decision_tree)
        mlflow.log_param("Random_Forest",random_forest)
        mlflow.log_param("Logistic_Regression",logistic_regression)


        mlflow.sklearn.log_model(dt,"Decision_Tree")
        mlflow.sklearn.log_model(rt,"Random_Forest")
        mlflow.sklearn.log_model(lr,"Logistic_Regression")

pickle_in = open('finalised_model.pkl', "rb")
classifier = pickle.load(pickle_in)

header = st.container()
header_two = st.container()

def prediction(age,job,marital,education,balance,contact,day,month,duration,campaign,previous,poutcome,housing_new,loan_new):
    predict = classifier.predict([[age, job, marital, education, balance, contact, day, month, duration, campaign, previous, poutcome, housing_new,	loan_new]])
    return predict   
    

with header:
    st.title("BANK TERM DEPOSIT PREDICTION")

with header_two:
    st.header("Predicts whether a person takes deposit in bank")
    age = st.text_input("Age (Enter your age)")
    job = st.text_input("Job (management = 0, technician = 1, entrepreneur = 2, blue-collar = 3, unknown = 4, retired = 5, admin. = 6, services = 7, self-employed = 8, unemployed = 9, housemaid = 10, student = 11)")            
    marital = st.text_input("Marital Status (single=0, married=1, divorced=2, unknown=3)")
    education = st.text_input("Education(primary=0, secondary=1, tertiary=2, unknown=3))")
    balance = st.text_input("Balance (Enter youy balance)")
    contact = st.text_input("Contact  (cellular=0, telephone=1, unknown=2)")
    day = st.text_input("Number of days passed (enter number)")
    month = st.text_input("Last contact month (jan=0, feb=1, mar=2, apr=3, may=4, jun=5, jul=6, aug=7, sep=8. oct=9, nov=10, dec=11)")
    duration = st.text_input("Last contact duration (in sec)")
    campaign = st.text_input("Number of contacts performed in present campaign (Enter a number)")
    previous = st.text_input("Number of contacts performed in previous campaign (Enter a number)")
    poutcome = st.text_input("Outcome of the previous campaign(failure=0, success=1, unknown=2, other=3)")
    housing_new = st.text_input("Have housing loan? (Yes = 1, No = 0)")
    loan_new = st.text_input("Have personal loan? (Yes = 1, No = 0)")
    result = ''
    if st.button("Predict"):
        result = prediction(age,job,marital,education,balance,contact,day,month,duration,campaign,previous,poutcome,housing_new,loan_new)
        if result == 1:
            st.text("Customer may take term deposit in the bank" + str(result))
        else:
            st.text("Customer may not take term deposit in the bank"+ str(result))
            
            #st.success("The Output is {} ".format(result))

       

    # Read the wine-quality csv file (make sure you're running this from the root of MLflow!)
    
