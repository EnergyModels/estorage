import pandas as pd
from ambient import Ambient
from compressor import Compressor
from tank import Tank
from turbine import Turbine

variables =     ['dt',
              'pwr_i','pwr_o', # Power
              'T1', 'T2', 'T3', 'T4', 'T5', # Temperature
              'p1', 'p2', 'p3', 'p4', 'p5', # Pressure
              'm_tank', # Mass stored
              'm1', 'm2', 'm3', 'm4', 'm5',  # Mass flow
              'Q1', 'Q2','Q3', 'Q4','Q5'] # Volumetric flow

class CAES:
    def __init__(self,V=1000.,cmp_eff=80.,trb_eff=90.,p=200000):

        # Air Side
        self.amb = Ambient()
        self.cmp = Compressor(eff=cmp_eff)
        self.tank = Tank(V=V,p=p)
        self.trb = Turbine(eff=trb_eff)
        self.m_dot_i = 0.0
        self.m_dot_o = 0.0

        # Heat Side

        # Create pandas DataFrame to store results
        self.df = pd.DataFrame(columns=variables)

    def update(self, pwr, dt):
        # Charge
        if pwr>0.0:
            self.charge(pwr, dt)
        # Discharge
        elif pwr > 0.0:
            self.discharge(pwr, dt)
        # Do nothing
        else:

        # Store current state
        s = pd.Series(index=variables)
        s['dt'] = dt
        s['pwr'] = pwr
        s['T1'] = self.amb.state
        s['T2'] = self.cmp.state2
        s['T3'] =
        s['T4'] =
        s['T5'] =
        s['p1'] = self.amb.state
        s['p2'] = self.cmp.state2
        s['p3'] =
        s['p4'] =
        s['p5'] =
        s['m_tank'] =
        s['m1'] = self.cmp.m_dot
        s['m2'] = self.cmp.m_dot
        s['m3'] =
        s['m4'] =
        s['m5'] =
        s['Q1'] = self.cmp.Q_dot_1
        s['Q2'] = self.cmp.Q_dot_2
        s['Q3'] =
        s['Q4'] = 0.0
        s['Q5'] = 0.0

        self.df.append(s)



        state1 = self.amb.state
        p_tank = self.tank.state.p
        state2 = self.cmp.compress(state1, p_tank,pwr)
        m_dot_i = self.cmp.m_dot
        state3 = state2 # Hxer - to be added
        self.tank.charge(state3,m_dot_i,dt)
        self.m_dot_i = m_dot_i

    def charge(self, pwr, dt):
        # Do something
        state1 = self.amb.state
        p_tank = self.tank.state.p
        state2 = self.cmp.compress(state1, p_tank,pwr)
        m_dot_i = self.cmp.m_dot
        state3 = state2 # Hxer - to be added
        self.tank.charge(state3,m_dot_i,dt)
        self.m_dot_i = m_dot_i


    def discharge(self, pwr, dt):
        state4 = self.tank.state
        state5 = state4 # Hxer - to be added
        p_amb = self.amb.state.p
        state6 = self.trb.expand(state4, p_amb)
        m_dot = pwr / (state4.h - state5.h)
        self.tank.discharge(state4, m_dot, dt)

