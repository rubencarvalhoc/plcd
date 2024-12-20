import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("ex1-dash.csv")

# Resolução sem ter em conta tamanho da população
# grouped = df.groupby("year")["lifeExp"].mean()
# grouped.plot(kind="line")
# plt.show()

# Resolução tendo em conta o tamanho da população
resposta = []

for year in df['year'].unique():
    df2 = df[df['year'] == year]

    dividendo = (df2['pop'] * df2['lifeExp']).sum()
    divisor = df2['pop'].sum()
    resposta.append(dividendo/divisor)

plt.plot(list(df['year'].unique()), resposta)
plt.show()


# Resolução professor
num={}
den = {}

for i in df.index:
    ano = df['year'][i]
    if ano in num:
        num[ano] += df['pop'][i]*df['lifeExp'][i]
        den[ano] += df['pop'][i]
    else:
        num[ano] = df['pop'][i]*df['lifeExp'][i]
        den[ano] = df['pop'][i]

y = {}
for ano in num:
    y[ano] = num[ano]/den[ano]
print(y)

plt.plot(list(y.keys()), list(y.values()))
plt.show()