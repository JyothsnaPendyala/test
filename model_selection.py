from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from data_preprocess import data_preprocess
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
def model_selection():
    data = pd.read_csv('balanced_data.csv')
    X = data.drop(['y_new'],axis=1)
    y = data['y_new']
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
    b.fit(X_train, y_train)
    filename = 'finalised_model.pkl'
    pickle.dump(b,open(filename,'wb'))
    '''loaded_model = pickle.load(open(filename,'rb'))
    result1 = loaded_model.score(X_test, y_test)
    result2 = loaded_model.predict(X_test)
    f1_score = f1_score(y_test, result2)
    print(result1, result2)
    print(f1_score)'''
    

model_selection()
