import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Style and Color Palette
sns.set_style('white')
sns.set_context('poster')
colors = sns.color_palette()
colors = [(0.380,0.380,0.380),(0.957,0.451,0.125),(.047, 0.149, 0.361),(0.847,0.000,0.067),(0.0,0.0,0.0)]

# Create Figure
nrows = 2
ncols = 1
f,a = plt.subplots(nrows,ncols,sharex=True)


y_var = "eff"
y_label = "Efficiency (%)"


for i in range(nrows):

    ax = a[i]

    # Columns (Cmp, Trb)
    if i == 0:
        df = pd.read_csv("cmp_sizing_results.csv")
        study = "Compressor"
    else:
        df = pd.read_csv("trb_sizing_results.csv")
        study = "Turbine"

    Nstgs = np.unique(df.loc[:, 'Nstg'])

    for n,Nstg in enumerate(Nstgs):
        ind = df.loc[:,'Nstg']==Nstg
        x = df.loc[ind,'RPM']
        y = df.loc[ind,y_var]*100.
        label = str(Nstg) + '-Stg'
        color = colors[n]
        ax.plot(x,y,label=label,color=color,marker='o',linestyle='dashed')

    if i==1:
        ax.legend(loc='center',bbox_to_anchor=(0.5, -0.6),ncol=5,frameon=False)

    # if i==0:
    #     ax.text(0.5,1.1,study, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.set_ylabel(y_label)
    if i==nrows-1:
        ax.set_xlabel('RPM')

    a[0].yaxis.set_ticks([50,70,90])
    a[1].yaxis.set_ticks([70,80,90])
    a[1].xaxis.set_ticks([0,5000,10000,15000])
            
# Save Figure
f.set_size_inches([ 11.5 ,   7.0])
plt.tight_layout()
plt.savefig('machine_sizing.png',dpi=1000,bbox_inches="tight")
