from estorage import SIZE_AIR_CMP
import seaborn as sns
import matplotlib.pyplot as plt


# Test
designs = SIZE_AIR_CMP(p_in=1.01325, t_in=20.0, p_out=2.2, m_dot=2.2, RPM_low=22000, RPM_high=22000, RPM_cases = 1, debug=True)

# Run Sweep
designs = SIZE_AIR_CMP(p_in=1.01325, t_in=20.0, p_out=31.1, m_dot=13.82, RPM_low=1800, RPM_high=15000, RPM_cases = 20, debug=False)

designs.to_csv("cmp_sizing_results.csv")

# Plot Results
if len(designs)>0:
    sns.set_style('white')

    # Plot 2 - Ns and Ds
    f,a = plt.subplots(2,1,sharex=True)
    sns.lineplot(x='RPM', y='Ns', hue='Nstg', data=designs, ax=a[0])
    sns.lineplot(x='RPM', y='Ds', hue='Nstg', data=designs, ax=a[1])
    f.savefig('cmp_sizing_NsDs.png',dpi=1000)

    # Plot 2 - D and Eff
    # f, a = plt.subplots(2, 1, sharex=True)
    # sns.lineplot(x='RPM', y='D', hue='Nstg', data=designs, ax=a[0])
    # sns.lineplot(x='RPM', y='eff', hue='Nstg', data=designs, ax=a[1])

    sns.PairGrid(designs, x_vars=['RPM'], y_vars=['eff','D'], hue='Nstg')
    # sns.lineplot(x='RPM', y='eff', hue='Nstg', data=designs, ax=a[1])
    f.savefig('cmp_sizing_Deff.png', dpi=1000)

    ind = designs.loc[:,type]=='Radial' or designs.loc[:,'type']=='Mixed'
    designs2 = designs.loc[ind, :]
    sns.PairGrid(designs2, x_vars=['RPM'], y_vars=['eff', 'D'], hue='Nstg')
    # sns.lineplot(x='RPM', y='eff', hue='Nstg', data=designs, ax=a[1])
    plt.savefig('cmp_sizing_Deff_radialMixed.png', dpi=1000)