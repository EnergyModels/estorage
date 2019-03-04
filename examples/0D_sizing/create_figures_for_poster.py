import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('white')

#================================
# Transient Simulation
#================================
sns.set_style('white')

# Import results
df = pd.read_csv("single_run_results.csv")


f, ax = plt.subplots(nrows=3, ncols=2, figsize=(8, 5))

# ----
# Charging
# ----
x = self.dfC['t']
# Temp
convert = 273.15
ax[0, 0].plot(x, self.dfC['T1'] - convert, label='T1', marker='o')
ax[0, 0].plot(x, self.dfC['T2'] - convert, label='T2', marker='v')
ax[0, 0].plot(x, self.dfC['T3'] - convert, label='T3', marker='x')
ax[0, 0].plot(x, self.dfC['T_cav'] - convert, label='T_cav', marker='<')
ax[0, 0].plot(x, self.dfC['T_c'] - convert, label='T_c', marker='>')
ax[0, 0].plot(x, self.dfC['T_h'] - convert, label='T_h', marker='*')
ax[0, 0].legend()
ax[0, 0].set_ylabel('Temp [C]')
# Press
convert = 1E-5
ax[1, 0].plot(x, self.dfC['p1'] * convert, label='p1', marker='o')
ax[1, 0].plot(x, self.dfC['p2'] * convert, label='p2', marker='v')
ax[1, 0].plot(x, self.dfC['p3'] * convert, label='p3', marker='x')
ax[1, 0].plot(x, self.dfC['p_cav'] * convert, label='p_cav', marker='<')
ax[1, 0].legend()
ax[1, 0].set_ylabel('Pressure [bar]')
# Mass Storage
ax[4, 0].plot(x, self.dfC['m_cav'], label='m_cav', marker='o')
ax[4, 0].plot(x, self.dfC['m_h'], label='m_h', marker='x')
ax[4, 0].legend()
ax[4, 0].set_ylabel('Mass Storage [kg]')

# ----
# Discharging
# ----
x = self.dfD['t']
# Temp
convert = 273.15
ax[0, 1].plot(x, dfD['T4'] - convert, label='T4', marker='o')
ax[0, 1].plot(x, dfD['T5'] - convert, label='T5', marker='v')
ax[0, 1].plot(x, dfD['T6'] - convert, label='T6', marker='x')
ax[0, 1].plot(x, dfD['T_cav'] - convert, label='T_cav', marker='<')
ax[0, 1].plot(x, dfD['T_c'] - convert, label='T_c', marker='>')
ax[0, 1].plot(x, dfD['T_h'] - convert, label='T_h', marker='*')
ax[0, 1].legend()
ax[0, 1].set_ylabel('Temp [C]')

# Press
convert = 1E-5
ax[1, 1].plot(x, dfD['p4'] * convert, label='p4', marker='o')
ax[1, 1].plot(x, dfD['p5'] * convert, label='p5', marker='v')
ax[1, 1].plot(x, dfD['p6'] * convert, label='p6', marker='x')
ax[1, 1].plot(x, dfD['p_cav'] * convert, label='p_cav', marker='<')
ax[1, 1].legend()
ax[1, 1].set_ylabel('Pressure [bar]')
# Mass Storage
ax[4, 1].plot(x, dfD['m_cav'], label='m_cav', marker='o')
ax[4, 1].plot(x, dfD['m_h'], label='m_h', marker='x')
ax[4, 1].legend()
ax[4, 1].set_ylabel('Mass Storage [kg]')

# Save
plt.savefig(savename + ".png", DPI=1000)





#================================

#================================

#

# %%=============================================================================#
# Figure Monte Carlo Simulation
results_filename = "results_monte_carlo.csv"
savename = "Poster_Fig_Monte_Carlo.png"
# =============================================================================#
sns.set_style('white')

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
x_vars = ["p_min", "p_max","V"]
x_labels = ["Min Pressure (bar)","Max Pressure (bar)","Cavern Volume (1E3 m3)"]
x_converts = [1,1,1E-3]

y_vars = ["RTE","E_in"]
y_labels = ["Round Trip Efficiency (%)", "Storage Capacity (MWh)"]
y_converts = [1,1]

series_var = 'Goal'
series_vals = ['RTE','Ein','Neither','Design']
series_labels = ['RTE Goal','Storage Goal','Neither','Design']
series_colors = sns.color_palette()
series_markers = ['x', '+','o','*']

DPI = 1200

# Create Plots
nrows = len(y_vars)
ncols = len(x_vars)

f, ax = plt.subplots(nrows, ncols,figsize=(8,5))

# Iterate Rows (Y variables)
for i,y_var,y_label,y_convert in zip(range(nrows),y_vars,y_labels,y_converts):

    # Itereate Columns (X variables)
    for j, x_var, x_label, x_convert in zip(range(ncols), x_vars, x_labels, x_converts):

        # Iterate Series
        for series_val,label,color,marker in zip(series_vals,series_labels,series_colors,series_markers):

            # Select entries of interest
            df2 = df[(df.loc[:,series_var] == series_val)]

            # Plot
            x = df2.loc[:, x_var] * x_convert
            y = df2.loc[:, y_var] * y_convert
            ax[i,j].scatter(x.values, y.values, c=color, marker=marker, label=label)

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
        # ax.set_xlim(left=xlims[0], right=xlims[1])
        # ax.set_ylim(bottom=ylims[0],top=ylims[1])

        # if len(xticks) > 2:
        #     ax.xaxis.set_ticks(xticks)
        # #        ax.set_xticks(xticks)
        # #        ax.set_xticklabels = xtick_labels


# Legend (only for middle bottom)
leg = ax[nrows-1,ncols/2].legend(bbox_to_anchor=(2.0, -0.2), ncol=len(series_labels), prop={'size': 12})

# Adjust layout
plt.tight_layout()

# Save Figure
plt.savefig(savename, dpi=DPI, bbox_inches="tight")
plt.close()