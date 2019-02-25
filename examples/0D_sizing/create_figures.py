import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("results_monte_carlo.csv")
df.loc[:,'V'] = df.loc[:,'V']/1000.0
g = sns.pairplot(df,x_vars=["V", "p_max","T_stor"], y_vars=["RTE", "Heat_Util", "E_stor_max"])
plt.savefig("monte_carlo.png",DPI=1000)