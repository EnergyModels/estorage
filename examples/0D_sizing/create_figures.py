import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('white')

df = pd.read_csv("results_monte_carlo.csv")
# df.loc[:,'p_max']=df.loc[:,'p_min']*df.loc[:,'PR']

# y_vars = ["RTE", "Heat_Util", "E_in", "T_h", "T_out_min"]
y_vars = ["RTE","E_in"]
x_vars = ["p_min", "p_max","V"]

#-------
# Plot 1 - Raw Results
#-------
df.loc[:,'V'] = df.loc[:,'V']/1000.0
g = sns.pairplot(df,x_vars=x_vars,y_vars=y_vars)
g.savefig("monte_carlo_raw.png",DPI=1000)

#-------
# Plot 2 - Filtered
#-------
# Filter
df2 = df[(df.Ebal >= 0.0) & (df.Qbal >= 0.0)]

# Identify Target Configurations
RTE_Goal = 70.0
Ein_Goal = 100.0
ind_RTE = df2.loc[:,'RTE']>RTE_Goal
ind_Ein = df2.loc[:,'E_in']>Ein_Goal

df2.loc[:,'Goal'] = 'Neither'
df2.loc[ind_RTE,'Goal'] = 'RTE'
df2.loc[ind_Ein,'Goal'] = 'Ein'
df2.loc[ind_RTE & ind_Ein,'Goal'] = 'RTE + Ein'

# Determine Design condition and mark as such
design_eff = df2.loc[ind_Ein,'RTE'].max()
ind_design = df2.loc[:,'RTE'] == design_eff
df2.loc[ind_design,'Goal'] = 'Design'
df3 = df2.loc[ind_design,:]
df3.to_csv('DesignCase.csv')


# Plot
g = sns.pairplot(df2,hue='Goal',hue_order=['Design','RTE','Ein','Neither'],x_vars=x_vars,y_vars=y_vars)
g.savefig("monte_carlo_filter.png",DPI=1000)