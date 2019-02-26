from CoolProp.CoolProp import PropsSI
from scipy.interpolate import interp1d
from math import pi
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

# Sizing Rules
PR_stg_min = 1.5
PR_stg_max = 3.6

# Specific Speed Chart Inputs
Ns_ideal = np.array([17.53573098, 20.31460093, 23.85633867, 29.94568557, 39.64060977, 60.83324952, 139.5346754])
Ds_ideal = np.array([7.848168406, 6.761801714, 5.905258342, 4.690713434, 3.388928695, 2.288095758, 1.116116401])
eff_ideal = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.8])


def SIZE_AIR_CMP(p_in=1.01325, t_in=20.0, p_out=10.0, m_dot=2.2, RPM_low=10000, RPM_high=50000, RPM_cases = 5, debug=False):
    # Convert Inputs
    p_in = p_in * 1E5  # from bar to Pa
    t_in = t_in + 273.15  # from C to K
    p_out = p_out * 1E5  # from bar to Pa

    # Interpolate Specific Speed Chart Inputs
    f_Ds = interp1d(Ns_ideal, Ds_ideal)
    f_eff = interp1d(Ns_ideal, eff_ideal)

    # Determine range of stages to consider
    PR = p_out / p_in
    Nstg_low = math.ceil(math.log(PR) / math.log(PR_stg_max))
    Nstg_high = math.floor(math.log(PR) / math.log(PR_stg_min))
    Nstgs = np.arange(Nstg_low, Nstg_high, 1)
    if debug == True:
        print 'Nstg_low  :' + str(round(Nstg_low, 0))
        print 'Nstg_high :' + str(round(Nstg_high, 0))
        print str(Nstgs)

    # RPMs to consider
    RPMs = np.linspace(RPM_low, RPM_high, RPM_cases)

    # Constants and Fluid Properties
    g = 9.81  # m/s^2
    fluid = 'Air'
    CP = PropsSI('CPMASS', "T", t_in, "P", p_in, fluid) * 1000.0  # KJ/Kg
    CV = PropsSI('CVMASS', "T", t_in, "P", p_in, fluid) * 1000.0  # KJ/Kg
    kappa = CP / CV
    MW = PropsSI('M', fluid) * 1000.0  # kg/kmol
    R_bar = PropsSI('GAS_CONSTANT', fluid)  # kJ/kmol/K
    R = R_bar / MW * 1000.0  # J/kg-K
    D1 = PropsSI('H', 'T', t_in, 'P', p_in, fluid)  # Density (kg/m3)
    V1 = m_dot * D1 # m3/s

    # DataFrame to hold results
    variables = ['p_in', 't_in', 'p_out', 'm_dot', 'V1', 'Nstg', 'PR_stg', 'RPM', 'Ns', 'Ds', 'D', 'eff']
    df = pd.DataFrame(columns=variables)

    # Perform Runs
    for Nstg in Nstgs:

        PR_stg = PR ** (1.0 / Nstg)

        for RPM in RPMs:

            # Balje Calculations (Ideal gas)
            omega = 2 * pi / 60.0 * RPM  # rad/s
            omega = RPM
            H_ad = kappa / (kappa - 1.0) * R * t_in * ((PR_stg) ** ((kappa - 1.0) / kappa) - 1.0)  # kJ/kg
            Ns = (omega*V1**0.5)/(H_ad)**0.75

            # Print-out values, if debugging
            if debug == True:
                print 'Nstg  :' + str(round(Nstg,0))
                print 'PR_stg:' + str(round(PR_stg,2))
                print 'RPM   :' + str(round(RPM,0))
                print 'Ns    :' + str(round(Ns,2)) + "\n"

            # Check if within the interpolation limits
            if Ns_ideal.min() <= Ns and Ns <= Ns_ideal.max():
                eff = f_eff(Ns)
                Ds =  f_Ds(Ns)
                D = Ds * V1 ** 0.5 / (g * H_ad) ** 0.75

                # Print-out values, if debugging
                if debug == True:
                    print "Successfully sized"
                    print 'Ds    :' + str(round(Ds,2))
                    print 'D     :' + str(round(D,2))
                    print 'eff   :' + str(round(eff,2))
                    print '#================#\n'

                # Save Values
                s = pd.Series(index=['Nstg', 'PR_stg', 'RPM', 'Ns', 'Ds', 'D', 'eff'])
                s['Nstg'] = Nstg
                s['PR_stg'] = PR_stg
                s['RPM'] = RPM
                s['Ns'] = Ns
                s['Ds'] = Ds
                s['D'] = 0.0
                s['eff'] = 0.0
                df = df.append(s, ignore_index=True)

    # Store Inputs
    df.loc[:, 'p_in'] = p_in / 1E5  # from Pa back to bar
    df.loc[:, 't_in'] = t_in - 273.15  # from K back to C
    df.loc[:, 'p_out'] = p_out / 1E5  # from Pa back to bar
    df.loc[:, 'm_dot'] = m_dot  # kg/s
    df.loc[:, 'V1'] = V1  # m3/s

    return df
