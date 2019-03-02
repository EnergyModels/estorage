from CoolProp.CoolProp import PropsSI
from scipy.interpolate import interp1d
from math import pi
import pandas as pd
import numpy as np
import math


def DESIGN_AIR_CMP(p_in=1.01325, t_in=20.0, p_out=10.0, m_dot=2.2, RPM=10000, Nstgs=6, debug=False):
    # Convert Inputs
    p_in = p_in * 1E5  # from bar to Pa
    t_in = t_in + 273.15  # from C to K
    p_out = p_out * 1E5  # from bar to Pa

    # Constants and Fluid Properties
    g = 9.81  # m/s^2
    fluid = 'Air'
    CP = PropsSI('CPMASS', "T", t_in, "P", p_in, fluid) / 1000.0  # KJ/Kg-K
    CV = PropsSI('CVMASS', "T", t_in, "P", p_in, fluid) / 1000.0  # KJ/Kg-K
    kappa = CP / CV
    MW = PropsSI('M', fluid) * 1000.0  # kg/kmol
    R_bar = PropsSI('GAS_CONSTANT', fluid)  # kJ/kmol/K
    R = R_bar / MW * 1000.0  # J/kg-K

    # Balje Calculations
    omega = 2 * pi / 60.0 * RPM  # rad/s
    PR = p_out/p_in
    H_ad = kappa / (kappa - 1.0) * R * t_in * ((PR) ** ((kappa - 1.0) / kappa) - 1.0)/Nstgs  # kJ/kg
    H = H_ad * m_dot

    # Print-out values, if debugging
    if debug == True:
        print 'Constants and Fluid Properties:'
        print 'g     :' + str(round(g, 3)) + ' (m/s^2)'
        print 'CP    :' + str(round(CP, 3)) + ' (kJ/kg-K)'
        print 'CV    :' + str(round(CV, 3)) + ' (kJ/kg-K)'
        print 'kappa :' + str(round(kappa, 3)) + ' (-)'
        print 'MW    :' + str(round(MW, 3)) + ' (kg/kmol)'
        print 'R_bar :' + str(round(R_bar, 3)) + ' (kJ/kmol-K)'
        print 'R     :' + str(round(R, 3)) + ' (J/kg-K)\n'

    # DataFrame to hold results
    variables = ['Nstg', 'RPM', 'H_ad','m_dot','V_in','p_in', 't_in', 'p_out','t_out','PR_stg']
    df = pd.DataFrame(columns=variables)

    # Perform Runs
    for Nstg in range(Nstgs):

        PR_stg = (1.0+(H_ad/(t_in*R*(kappa/(kappa-1.0)))))**(kappa/(kappa-1.0))
        p_out = p_in * PR_stg
        t_out = t_in+t_in*(PR_stg**((kappa-1.0)/kappa)-1.0)

        # Volumetric flow Rate
        D_in = PropsSI('D', 'T', t_in, 'P', p_in, fluid)  # Density (kg/m3)
        V_in = m_dot * D_in  # m3/s

        # Print-out values, if debugging
        if debug == True:
            print 'Nstg     :' + str(round(Nstg+1,3))
            print 'PR_stg   :' + str(round(PR_stg,3))
            print 'p_in     :' + str(round(p_in,3))
            print 'p_in     :' + str(round(p_out,3))
            print 't_in     :' + str(round(t_in,3))
            print 't_out    :' + str(round(t_out,3))
            print '#================#'

        # Save Values
        s = pd.Series(index=variables)
        s['Nstg'] = Nstg+1
        s['RPM'] = RPM
        s['H_ad'] = H_ad
        s['H'] = H / 1E6
        s['m_dot'] = m_dot
        s['V_in'] = V_in
        s['p_in'] = p_in / 1E5
        s['t_in'] = t_in - 273.15
        s['p_out'] = p_out / 1E5
        s['t_out'] = t_out - 273.15
        s['PR_stg'] = PR_stg
        df = df.append(s, ignore_index=True)

        # Update for next stage
        p_in = p_out
        t_in = t_out

    return df
