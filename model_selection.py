from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from data_preprocess import data_preprocess
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
def model_selection():
    data = pd.read_csv('balanced_data.csv')
    X = data.drop(['y_new'],axis=1)
    y = data['y_new']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=0) 
    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)
    print(dt.score(X_test, y_test))
    rt = RandomForestClassifier(n_estimators=100, n_jobs=1)
    rt.fit(X_train, y_train)
    print(rt.score(X_test, y_test))
    lr= make_pipeline(StandardScaler(),LogisticRegression())
    lr.fit(X_train, y_train)
    print(lr.score(X_test, y_test))

model_selection()
