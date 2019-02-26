from estorage import SIZE_AIR_CMP


# Test
designs = SIZE_AIR_CMP(p_in=1.01325, t_in=20.0, p_out=2.2, m_dot=2.2, RPM_low=22000, RPM_high=22000, RPM_cases = 1, debug=True)

# Run Sweep
designs = SIZE_AIR_CMP(p_in=1.01325, t_in=20.0, p_out=31.1, m_dot=13.82, RPM_low=3600, RPM_high=50000, RPM_cases = 5, debug=False)

# Plot Results
if len(designs)>0:
    sns.set_style('white')
    f,a = plt.subplots(2,1,sharex=True)
    sns.lineplot(x='RPM',y='eff',hue='Nstg',data=designs,ax=a[0])
    sns.lineplot(x='RPM',y='D',hue='Nstg',data=designs,ax=a[1])
    f.savefig('cmp_sizing.png',dpi=1000)