import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('white')






#================================

#================================

#

# %%=============================================================================#
# Figure Monte Carlo Simulation
results_filename = "results_monte_carlo.csv"
savename = "Poster_Fig_Monte_Carlo.png"
# =============================================================================#
sns.set_style('white')
sns.set_context('poster')
# sns.set_context('talk',font_scale=1.5)
# Import results
df = pd.read_csv("results_monte_carlo.csv")

# Filter Results
df = df[(df.Ebal >= 0.0) & (df.Qbal >= 0.0)& (df.RTE <= 90.0)]

# Prepare results for plotting
# Identify Target Configurations
RTE_Goal = 70.0
Ein_Goal = 100.0
ind_RTE = df.loc[:,'RTE']>RTE_Goal
ind_Ein = df.loc[:,'E_in']>Ein_Goal

df.loc[:,'Goal'] = 'Neither'
df.loc[ind_RTE,'Goal'] = 'RTE'
df.loc[ind_Ein,'Goal'] = 'Ein'
df.loc[ind_RTE & ind_Ein,'Goal'] = 'RTE + Ein'

# Determine Design condition and mark as such
design_eff = df.loc[ind_Ein,'RTE'].max()
ind_design = df.loc[:,'RTE'] == design_eff
df.loc[ind_design,'Goal'] = 'Design'

# Plotting Inputs
x_vars = ["p_max","V"]
x_labels = ["Max Pressure (bar)","Cavern Volume (1E3 m3)"]
x_converts = [1,1E-3]
x_ticks = [[0,50,100],[0,15,30]]
x_lims = [[0,100],[0,30]]

y_vars = ["RTE","E_in"]
y_labels = ["RTE (%)", "Storage (MWh)"]
y_converts = [1,1]
y_ticks = [[40,65,90],[0,350,700]]
y_lims = [[40,90],[0,700]]

series_var = 'Goal'
series_vals = ['Neither','RTE','Ein','Design']
series_labels = ['Neither','RTE Goal','Storage Goal','Design']
series_colors = [(0.380,0.380,0.380),(0.957,0.451,0.125),(.047, 0.149, 0.361),(0.847,0.000,0.067)]
series_markers = ['x', '+','o','*']
series_marker_sizes = [40,40,40,300]

DPI = 1000

# Create Plots
nrows = len(y_vars)
ncols = len(x_vars)

# f, ax = plt.subplots(nrows, ncols,figsize=(6,5))
f, ax = plt.subplots(nrows, ncols)


# Iterate Rows (Y variables)
for i,y_var,y_label,y_convert, y_tick,y_lim in zip(range(nrows),y_vars,y_labels,y_converts,y_ticks,y_lims):

    # Itereate Columns (X variables)
    for j, x_var, x_label, x_convert, x_tick,x_lim in zip(range(ncols), x_vars, x_labels, x_converts,x_ticks,x_lims):

        # Iterate Series
        for series_val,label,color,marker,size in zip(series_vals,series_labels,series_colors,series_markers,series_marker_sizes):

            # Select entries of interest
            df2 = df[(df.loc[:,series_var] == series_val)]

            # Plot
            x = df2.loc[:, x_var] * x_convert
            y = df2.loc[:, y_var] * y_convert
            ax[i,j].scatter(x.values, y.values, c=color, s=size, marker=marker, label=label,edgecolors='none')

        # X-axis Labels (Only bottom)
        if i == nrows-1:
            ax[i,j].set_xlabel(x_label)
        else:
            ax[i,j].get_xaxis().set_visible(False)

        # Y-axis labels (Only left side)
        if j == 0:
            ax[i,j].set_ylabel(y_label)
            ax[i,j].yaxis.set_label_coords(-0.25, 0.5)
        else:
            ax[i,j].get_yaxis().set_visible(False)

        # Set X and Y Limits
        if len(x_lim)== 2:
            ax[i,j].set_xlim(left=x_lim[0], right=x_lim[1])
        if len(y_lim) ==2 :
            ax[i,j].set_ylim(bottom=y_lim[0],top=y_lim[1])

        if len(x_tick) > 2:
            ax[i,j].xaxis.set_ticks(x_tick)

        if len(y_tick) > 2:
            ax[i,j].yaxis.set_ticks(y_tick)
        #        ax.set_xticks(xticks)
        #        ax.set_xticklabels = xtick_labels


# Legend (only for middle bottom)
# leg = ax[nrows-1,0].legend(bbox_to_anchor=(1.0, -0.3), loc='center',ncol=len(series_labels), prop={'size': 12}, frameon = False)
leg = ax[nrows-1,0].legend(bbox_to_anchor=(1.0, -0.5), loc='center',ncol=len(series_labels), frameon = False, scatterpoints = 1)

# Adjust layout


f.subplots_adjust(wspace = 0.2,hspace=0.2)
f.set_size_inches([ 10.0,   7.25 ])
f.set_size_inches([ 10.0,   8.0 ])
plt.tight_layout()

# Save Figure
plt.savefig(savename, dpi=DPI, bbox_inches="tight")
plt.close()