from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
def data_preprocess():
    data = pd.read_csv('balanced_data.csv')
    X = data.drop(['y_new'],axis=1)
    y = data['y_new']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=0)
    

data_preprocess()    
