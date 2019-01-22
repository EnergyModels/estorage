# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:18:11 2019

@author: jab6ft
"""
import pandas as pd
from CoolProp.CoolProp import PropsSI
import numpy as np

# What volume size is required?


# Constant inputs
p_amb = 100.0 # kPa
t_amb = 25.0 # C
#t_grd = 25.0 # C
beta_max = 200.0
comp_eff = 0.85
#trb_eff  = 0.90
#hxer_eff = 0.90

## Variables to change
#V = 1000 # volume (m3)

#p_init = 100 # kPa
#
## Analysis inputs
#dt = 1.0 # min



#----------------
# End Simulation
#----------------
pwr = 1 # MW
fluid = 'Air'

n_cases = 50
betas = np.linspace(1.1,200.,n_cases)

df = pd.DataFrame(index=range(n_cases),columns=['beta','m_dot','t1'])

# Inlet Conditions
p0 = p_amb*1000.0 # Pa
t0 = t_amb + 273.15 # K
h0 = PropsSI('H','T',t0,'P',p0,fluid)
s0 = PropsSI('S','T',t0,'P',p0,fluid)

# Outlet Conditions
for i,beta in enumerate(betas):
    p1 = beta*p0
    h1s = PropsSI('H','P',p1,'S',s0,fluid)
    h1 = h0 + (h1s-h0)/comp_eff
    t1 = PropsSI('T','P',p1,'H',h1,fluid)
    s1 = PropsSI('S','P',p1,'H',h1,fluid)
    
    m_dot = pwr*1E6/(h1-h0)
    
    df.loc[i] = [beta,m_dot,t1]
    
    
df.plot(x='beta',y='m_dot')


    
    