import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("results_monte_carlo.csv")

x_vars = ["RTE", "Heat_Util", "E_in", "T_h", "T_out_min"]
y_vars = ["p_min", "PR","V"]

df.loc[:,'V'] = df.loc[:,'V']/1000.0
g = sns.pairplot(df,x_vars=x_vars,y_vars=y_vars)
plt.savefig("monte_carlo_raw.png",DPI=1000)

df2 = df[(df.Ebal >= 0.0) & (df.Qbal >= 0.0)]
g = sns.pairplot(df2,x_vars=x_vars,y_vars=y_vars)
plt.savefig("monte_carlo_filter.png",DPI=1000)