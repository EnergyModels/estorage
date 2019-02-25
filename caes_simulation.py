import pandas as pd
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
import seaborn as sns
# ----------
# Inputs
# ----------
    # Ambient Conditions
fluid = 'Air'
T_amb = 0.+273.15  # K
p_amb = 101325.  # Pa
    # Compressor
cmp_eff = 0.80
    # Compressor
trb_eff = 0.88
    # Cooler
T_clr = 150+273.15  # K
    # Tank
V = 1E6  # m3
p_min = 2.0*p_amb
p_max = 10.0*p_amb
    # Simulation
dt = 60.0 # s
pwr = 10E6 # W = 1 MW

# ----------
# Pre-processing calculations
# ----------
    # Ambient
T1 = T_amb
p1 = p_amb
h1 = PropsSI('H', 'T', T1, 'P', p1, fluid)
s1 = PropsSI('S', 'T', T1, 'P', p1, fluid)
    # Air Tank
T_tnk = T_amb
p_tnk = p_min
m_tnk = V*PropsSI('D', 'T', T_tnk, 'P', p_tnk, fluid)
u_tnk = PropsSI('U', 'T', T_tnk, 'P', p_tnk, fluid)
MW = PropsSI('MOLEMASS', fluid) # kg/mol
R = PropsSI('GAS_CONSTANT', fluid) # J/mol-K
    # Track energy and heat stored
E_stor = 0.0
Q_stor = 0.0

#-------------------------------------
# Charge
#-------------------------------------
t = 0.
variables = ['t','pwr','m_dot','p1','T1','p2','T2','p3','T3','p_tnk','T_tnk','Q_clr','E_stor','Q_stor']
df1 = pd.DataFrame(columns=variables)
while p_tnk < p_max:
    t = t + dt

    # Compressor
    p2 = p_tnk
    delta_h = kappa/(kappa - 1.0)*R*T1*((p2/p1)**((kappa-1.0)/kappa) - 1.0)
    h2s = PropsSI('H', 'P', p2, 'S', s1, fluid)
    h2 = h1 + (h2s - h1) / cmp_eff
    T2 = PropsSI('T', 'P', p2, 'H', h2, fluid)
    m_dot = pwr / (h2 - h1)

    # Cooler
    p3 = p2
    T3 = min(T_clr,T2)
    h3 = PropsSI('H', 'T', T3, 'P', p3, fluid)
    Q_clr = m_dot * (h2 - h3)

    # Storage Tank
        # Mass balance
    m_tnk = m_tnk + m_dot*dt
    n = m_tnk / MW  # moles
        # Energy balance
    Cv = PropsSI('CVMASS', 'T', T_tnk, 'P', p_tnk, fluid)  # Assume small differences in Cv
    u_tnk = ((m_tnk-m_dot*dt)*u_tnk + m_dot*dt*h3)/(m_tnk)
    T_tnk = u_tnk / Cv
    p_tnk = n * R * T_tnk / V
    
        # Energy/Heat Storage
    Q_stor = Q_stor + Q_clr*dt
    E_stor = E_stor + pwr*dt

    # Store Data
    s = pd.Series(index=variables)
    s['t']= t
    s['pwr'] = pwr
    s['m_dot'] = m_dot
    s['p1'] = p1
    s['T1'] = T1
    s['p2'] = p2
    s['T2'] = T2
    s['p3'] = p3
    s['T3'] = T3
    s['p_tnk'] = p_tnk
    s['T_tnk'] = T_tnk
    s['Q_clr'] = Q_clr
    s['Q_stor'] = Q_stor
    s['E_stor'] = E_stor
    s.name=t
    df1 =df1.append(s)


#-------------------------------------
# Mid-Analysis
#-------------------------------------
E_in = E_stor
Q_in = Q_stor

#-------------------------------------
# Discharge
#-------------------------------------
t = 0.
variables = ['t','pwr','m_dot','p4','T4','p5','T5','p6','T6','p_tnk','T_tnk','Q_htr','E_stor','Q_stor']
df2 = pd.DataFrame(columns=variables)
while p_tnk > p_min:
    t = t + dt

    # Heater
    T4 = T_tnk
    p4 = p_tnk
    h4 = PropsSI('H', 'T', T4, 'P', p4, fluid)
    p5 = p_tnk
    T5 = max(T_clr, T_tnk)
    h5 = PropsSI('H', 'T', T5, 'P', p5, fluid)
    s5 = PropsSI('S', 'T', T5, 'P', p5, fluid)

    # Turbine
    p6 = p_amb
    h6s = PropsSI('H', 'P', p6, 'S', s5, fluid)
    h6 = h5 + (h6s - h5) * trb_eff
    T6 = PropsSI('T', 'P', p6, 'H', h6, fluid)
    m_dot = pwr / (h5 - h6)

    # Revisit Heater
    Q_htr = m_dot * (h5 - h4)

    # Storage Tank
        # Mass balance
    m_tnk = m_tnk - m_dot*dt
    n = m_tnk / MW  # moles
        # Energy balance
    Cv = PropsSI('CVMASS', 'T', T_tnk, 'P', p_tnk, fluid)  # Assume small differences in Cv
    u_tnk = ((m_tnk+m_dot*dt)*u_tnk - m_dot*dt*h4)/(m_tnk)
    T_tnk = u_tnk / Cv
    p_tnk = n * R * T_tnk / V

    # Energy/Heat Storage
    Q_stor = Q_stor - Q_htr*dt
    E_stor = E_stor - pwr*dt

    # Store Data
    s = pd.Series(index=variables)
    s['t']= t
    s['pwr'] = pwr
    s['m_dot'] = m_dot
    s['p4'] = p4
    s['T4'] = T4
    s['p5'] = p5
    s['T5'] = T5
    s['p6'] = p6
    s['T6'] = T6
    s['p_tnk'] = p_tnk
    s['T_tnk'] = T_tnk
    s['Q_htr'] = Q_htr
    s['Q_stor'] = Q_stor
    s['E_stor'] = E_stor
    s.name=t
    df2 =df2.append(s)

#-------------------------------------
# Final-Analysis
#-------------------------------------
Q_out = Q_in- Q_stor
E_out = E_in- E_stor
RTE = E_out/E_in*100.0
Heat_Util = Q_out/Q_in*100.0
print "RTE: " + str(RTE)
print "Heat_Util: " + str(Heat_Util)


#-------------------------------------
# Create Plots
#-------------------------------------

#f, ax = plt.subplots(4, sharex=True)
f,ax =plt.subplots(nrows=4,ncols=2)
#----
# Charging
#----
x = df1['t']
# Temp
convert = 273.15
ax[0,0].plot(x, df1['T1']-convert,label='T1')
ax[0,0].plot(x, df1['T2']-convert,label='T2')
ax[0,0].plot(x, df1['T3']-convert,label='T3')
ax[0,0].plot(x, df1['T_tnk']-convert,label='T_tnk')
ax[0,0].legend()
ax[0,0].set_ylabel('Temp [C]')
# Press
convert = 1E-6
ax[1,0].plot(x, df1['p1']*convert,label='p1')
ax[1,0].plot(x, df1['p2']*convert,label='p2')
ax[1,0].plot(x, df1['p3']*convert,label='p3')
ax[1,0].plot(x, df1['p_tnk']*convert,label='p_tnk')
ax[1,0].legend()
ax[1,0].set_ylabel('Pressure [MPa]')
# Power/Heat
convert = 1E-6
ax[2,0].plot(x, df1['pwr']*convert,label='pwr')
ax[2,0].plot(x, df1['Q_clr']*convert,label='Q_clr')
ax[2,0].legend()
ax[2,0].set_ylabel('Power/heat Flow [MW]')
# Energy & Heat Storage
convert = 1E-6
ax[3,0].plot(x, df1['E_stor']*convert,label='E_stor')
ax[3,0].plot(x, df1['Q_stor']*convert,label='Q_stor')
ax[3,0].legend()
ax[3,0].set_ylabel('Power/heat Storage [GJ]')

#----
# Discharging
#----
x = df2['t']
# Temp
convert = 273.15
ax[0,1].plot(x, df2['T4']-convert,label='T4')
ax[0,1].plot(x, df2['T5']-convert,label='T5')
ax[0,1].plot(x, df2['T6']-convert,label='T6')
ax[0,1].plot(x, df2['T_tnk']-convert,label='T_tnk')
ax[0,1].legend()
ax[0,1].set_ylabel('Temp [C]')

# Press
convert = 1E-6
ax[1,1].plot(x, df2['p4']*convert,label='p4')
ax[1,1].plot(x, df2['p5']*convert,label='p5')
ax[1,1].plot(x, df2['p6']*convert,label='p6')
ax[1,1].plot(x, df2['p_tnk']*convert,label='p_tnk')
ax[1,1].legend()
ax[1,1].set_ylabel('Pressure [MPa]')
# Power/heat
convert = 1E-6
ax[2,1].plot(x, df2['pwr']*convert,label='pwr')
ax[2,1].plot(x, df2['Q_htr']*convert,label='Q_htr')
ax[2,1].legend()
ax[2,1].set_ylabel('Power/heat Flow [MW]')
# Energy & Heat Storage
convert = 1E-6
ax[3,1].plot(x, df2['E_stor']*convert,label='E_stor')
ax[3,1].plot(x, df2['Q_stor']*convert,label='Q_stor')
ax[3,1].legend()
ax[3,1].set_ylabel('Power/heat Storage [GJ]')


# TO ADD
# Cumulative heat stored, energy stored, energy discharged, heat discharged
# Check energy balance