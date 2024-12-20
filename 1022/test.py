import pandas as pd

df = pd.read_csv(r"C:\Users\ruben\Desktop\Universidade\3ºAno\PLCD\ex1-dash.csv")

print(df.info())

df['teste'] = df['pop'] * df['lifeExp']
print(df.head())