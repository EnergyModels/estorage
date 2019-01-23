import pandas as pd
import matplotlib.pyplot as plt
from caes import CAES
from state import def_state_tp


state = def_state_tp('Air',293.,2E6)

# Create CAES system
sys = CAES()

# Create run-time parameters
t_steps = range(100)
dt = 1.0 # s
pwr = 1E6 # 1 MW

# Define way to store results
df = pd.DataFrame(index=t_steps,columns=['dt','pwr','T_tank','p_tank','m_tank','T_cmp','p_cmp','m_dot_i','m_dot_o'])

for t_step in t_steps:
    
    if t_step > 0:
        # Charge
        state = sys.charge(pwr, dt)

    # Store results
    df.loc[t_step,'dt'] = dt
    df.loc[t_step, 'pwr'] = pwr

    df.loc[t_step, 'T_tank'] = sys.tank.state['T']
    df.loc[t_step, 'p_tank'] = sys.tank.state['p']
    df.loc[t_step, 'm_tank'] = sys.tank.m

    df.loc[t_step, 'T_cmp'] = sys.cmp.state2['T']
    df.loc[t_step, 'p_cmp'] = sys.cmp.state2['p']
    df.loc[t_step, 'm_dot_i'] = sys.m_dot_i
    df.loc[t_step, 'm_dot_o'] = sys.m_dot_o

#
#df.plot(y=['T_tank'])
#df.plot(y=['p_tank'])
#df.plot(y=['m_tank'])
#df.plot(y=['T_cmp'])
#df.plot(y=['p_cmp'])
#df.plot(y=['m_dot_cmp'])

f, ax = plt.subplots(4, sharex=True)
x = df.index
# Temp
convert = 273.15
ax[0].plot(x, df['T_tank']-convert,label='T_tank')
ax[0].plot(x, df['T_cmp']-convert,label='T_cmp')
ax[0].legend()
ax[0].set_ylabel('Temp [C]')
# Press
convert = 1E-6
ax[1].plot(x, df['p_tank']*convert,label='p_tank')
ax[1].plot(x, df['p_cmp']*convert,label='p_cmp')
ax[1].legend()
ax[1].set_ylabel('Pressure [MPa]')
# Mass Flow
ax[2].plot(x, df['m_dot_i'],label='inflowm')
ax[2].plot(x, df['m_dot_o'],label='outflow')
ax[2].legend()
ax[2].set_ylabel('Mass Flow [kg/s]')
# Mass
ax[3].plot(x, df['m_tank'],label='m_tank')
ax[3].legend()
ax[3].set_ylabel('Tank Mass [kg]')




