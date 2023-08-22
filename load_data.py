import pandas as pd
def load_data():
  data = pd.read_csv('bank.csv')
  print(data.head())
  return data

print(load_data())
