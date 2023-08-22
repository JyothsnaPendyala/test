import pandas as pd
import numpy as np

def load_data():
  data = pd.read_csv('bank.csv')
  data = data.replace(np.nan, 0)
  print(data.head())
  return data

print(load_data())
