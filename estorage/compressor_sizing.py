from CoolProp.CoolProp import PropsSI
from scipy.interpolate import interp1d
from math import pi
import pandas as pd
import numpy as np
import math

# Sizing Rules
PR_stg_min = 1.5
PR_stg_max = 3.6

# Specific Speed Chart Inputs

Ns_ideal = np.array([0.156592415,0.213784951,0.314421351,0.374907082,0.462458607,0.627128919,1.063672257,2.33449929,6.27822242,8.458415169,11.24347938,16.65613494,26.4048703])
Ds_ideal = np.array([17.82794648,12.62762237,8.191486162,6.642324943,5.533819167,4.054427281,3.03140973,2.491585363,1.850350655,1.616281072,1.520845751,1.337472543,1.168282103])
eff_ideal = np.array([0.5,0.6,0.7,0.75,0.8,0.85,0.85,0.85,0.8,0.75,0.7,0.6,0.5])
Ns_radial = [0.156, 0.627]
Ns_axial = [2.334, 26.405]


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
    if len(Nstgs)==0:
            Nstgs = [Nstg_low]
    if debug == True:
        print 'Range of Stages Considered'
        print 'Nstg_low  :' + str(round(Nstg_low, 0))
        print 'Nstg_high :' + str(round(Nstg_high, 0))
        print 'Nstgs     :' + str(Nstgs) + '\n'

    # RPMs to consider
    RPMs = np.linspace(RPM_low, RPM_high, RPM_cases)

    # Constants and Fluid Properties
    g = 9.81  # m/s^2
    fluid = 'Air'
    CP = PropsSI('CPMASS', "T", t_in, "P", p_in, fluid) / 1000.0  # KJ/Kg-K
    CV = PropsSI('CVMASS', "T", t_in, "P", p_in, fluid) / 1000.0  # KJ/Kg-K
    kappa = CP / CV
    MW = PropsSI('M', fluid) * 1000.0  # kg/kmol
    R_bar = PropsSI('GAS_CONSTANT', fluid)  # kJ/kmol/K
    R = R_bar / MW * 1000.0  # J/kg-K
    D1 = PropsSI('D', 'T', t_in, 'P', p_in, fluid)  # Density (kg/m3)
    V1 = m_dot * D1 # m3/s

    # Print-out values, if debugging
    if debug == True:
        print 'Constants and Fluid Properties:'
        print 'g     :' + str(round(g, 3)) + ' (m/s^2)'
        print 'CP    :' + str(round(CP, 3)) + ' (kJ/kg-K)'
        print 'CV    :' + str(round(CV, 3)) + ' (kJ/kg-K)'
        print 'kappa :' + str(round(kappa, 3)) + ' (-)'
        print 'MW    :' + str(round(MW, 3)) + ' (kg/kmol)'
        print 'R_bar :' + str(round(R_bar, 3)) + ' (kJ/kmol-K)'
        print 'R     :' + str(round(R, 3)) + ' (J/kg-K)'
        print 'D1    :' + str(round(D1, 3)) + ' (kg/m^3)'
        print 'V1    :' + str(round(V1, 3)) + ' (m^3/s)\n'
        print 'Begin Cases'

    # DataFrame to hold results
    variables = ['p_in', 't_in', 'p_out', 'm_dot', 'V1', 'Nstg', 'PR_stg', 'RPM', 'H_ad',
                 'g', 'Ns', 'Ds', 'D', 'eff', 'type','r1','r2','U2','psi','I','mu']
    df = pd.DataFrame(columns=variables)

    # Perform Runs
    for Nstg in Nstgs:

        PR_stg = PR ** (1.0 / Nstg)

        for RPM in RPMs:

            # Balje Calculations (Ideal gas)
            omega = 2 * pi / 60.0 * RPM  # rad/s
            # omega = RPM
            H_ad = kappa / (kappa - 1.0) * R * t_in * ((PR) ** ((kappa - 1.0) / kappa) - 1.0)/Nstg  # kJ/kg
            Ns = (omega*V1**0.5)/(H_ad)**0.75


            # Print-out values, if debugging
            if debug == True:
                print 'Nstg  :' + str(round(Nstg,0)) + ' (-)'
                print 'PR_stg:' + str(round(PR_stg,2)) + ' (-)'
                print 'RPM   :' + str(round(RPM,0)) + ' (rev/min)'
                print 'omega :' + str(round(omega,2)) +' (rad/s)'
                print 'H_ad  :' + str(round(H_ad,2)) + ' (kJ/kg)'
                print 'Ns    :' + str(round(Ns,3)) + " (-)\n"

            # Check if within the interpolation limits
            if Ns_ideal.min() <= Ns and Ns <= Ns_ideal.max():
                eff = f_eff(Ns)
                Ds =  f_Ds(Ns)
                D = (Ds * (V1) ** 0.5) / (g * H_ad) ** 0.25

                r2 = D/2.0 # Tip radius (m)
                r1 = r2/2.0 # Hub radius (m)
                U2 = omega*r2 # Tip speed (m/s)
                psi = V1/(math.pi*(r2)**2.0*U2) # Flow coefficient (-)
                I = H_ad / (U2) ** 2.0  # Work input coefficient (-)
                mu = eff*I # Work coefficient (-)

                # Classify Machine Type
                if Ns < Ns_radial[1]:
                    machine_type = 'Radial'
                elif Ns_axial[0] < Ns:
                    machine_type = 'Axial'
                else:
                    machine_type = 'Mixed'

                # Print-out values, if debugging
                if debug == True:
                    print "Successfully sized"
                    print 'Ds    :' + str(round(Ds,3))
                    print 'D     :' + str(round(D,3))
                    print 'eff   :' + str(round(eff,3))
                    print '#================#\n'

                # Save Values
                s = pd.Series(index=['Nstg', 'PR_stg', 'RPM', 'H_ad', 'g', 'Ns', 'Ds', 'D', 'eff', 'type',
                                     'r1','r2','U2','psi','I','mu'])
                s['Nstg'] = Nstg
                s['PR_stg'] = PR_stg
                s['RPM'] = RPM
                s['H_ad'] = H_ad
                s['g'] = g
                s['Ns'] = Ns
                s['Ds'] = Ds
                s['D'] = D
                s['eff'] = eff
                s['type'] = machine_type
                s['r1'] = r1
                s['r2'] = r2
                s['U2'] = U2
                s['psi'] = psi
                s['I'] = I
                s['mu'] = mu
                df = df.append(s, ignore_index=True)

    # Store Inputs
    df.loc[:, 'p_in'] = p_in / 1E5  # from Pa back to bar
    df.loc[:, 't_in'] = t_in - 273.15  # from K back to C
    df.loc[:, 'p_out'] = p_out / 1E5  # from Pa back to bar
    df.loc[:, 'm_dot'] = m_dot  # kg/s
    df.loc[:, 'V1'] = V1  # m3/s

    return df
