import pandas as pd

def dvc():
  data = pd.read_csv('balanced_data.csv')
  data.to_csv("reference.csv")
  
dvc()
