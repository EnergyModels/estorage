import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Style and Color Palette
sns.set_style('white')
colors = sns.color_palette()

# Create Figure
nrows = 2
ncols = 2
f,a = plt.subplots(nrows,ncols,sharex=True)

for j in range(ncols): 
    
    # Columns (Cmp, Trb)
    if j==0:
        df = pd.read_csv("cmp_sizing_results.csv")
        study = "Compressor"
    else:
        df = pd.read_csv("trb_sizing_results.csv")
        study = "Turbine"
        
    Nstgs = np.unique(df.loc[:,'Nstg'])
        
    for i in range(nrows): 
        
        ax = a[i,j]
        
        # Rows (eff,D)
        if i==0:
            y_var = "eff"
            y_label = "Efficiency (%)"
        elif i==1:
            y_var = "D"
            y_label = "Diameter (m)"
        
        for n,Nstg in enumerate(Nstgs):
            ind = df.loc[:,'Nstg']==Nstg
            x = df.loc[ind,'RPM']
            y = df.loc[ind,y_var]
            label = str(Nstg) + '-Stg'
            color = colors[n]
            ax.plot(x,y,label=label,color=color,marker='o',linestyle='dashed')
            
        if i==1:
            ax.legend()
        
        if i==0:
            ax.text(0.5,1.1,study, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        if j==0:
            ax.set_ylabel(y_label)
        if i==nrows-1:
            ax.set_xlabel('RPM')
            
# Save Figure
plt.savefig('machine_sizing.png',dpi=1200)