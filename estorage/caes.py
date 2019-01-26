import pandas as pd
from ambient import Ambient
from compressor import Compressor
from tank import Tank
from turbine import Turbine

variables =     ['dt',
              'pwr_i','pwr_o', # Power
              'T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', # Temperature
              'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', # Pressure
              'm_tank', # Mass stored
              'm0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6',  # Mass flow
              'Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5','Q6'] # Volumetric flow

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
            self.maintain(dt)

        # Store current state
        s = pd.Series(index=variables)
        s['dt'] = dt
        s['pwr'] = pwr

        # -----
        # Store Tank Data
        #-----
            # Temperature
        s['T_TA'] = 0.0
        s['T_TC'] = 0.0
        s['T_TH'] = 0.0
            # Pressure
        s['p_TA'] = 0.0
        s['p_TC'] = 0.0
        s['p_TH'] = 0.0
            # Mass stored
        s['m_TA'] = self.tank.m
        s['m_TC'] = 0.0
        s['m_TH'] = 0.0

        # -----
        # Store Flow Data
        # -----
            # Temperature
        s['T_A1'] = self.cmp.state1['T']
        s['T_A2'] = self.cmp.state2['T']
        s['T_A3'] = 0.0
        s['T_B1'] = 0.0
        s['T_B2'] = 0.0
        s['T_B3'] = 0.0
        s['T_C1'] = 0.0
        s['T_C2'] = 0.0
        s['T_D1'] = 0.0
        s['T_D2'] = 0.0
            # Pressure
        s['p_A1'] = self.cmp.state1['p']
        s['p_A2'] = self.cmp.state2['p']
        s['p_A3'] = self.tank.state['p']
        s['p_B1'] = 0.0
        s['p_B2'] = 0.0
        s['p_B3'] = 0.0
        s['p_C1'] = 0.0
        s['p_C2'] = 0.0
        s['p_D1'] = 0.0
        s['p_D2'] = 0.0
        s['p_E1'] = 0.0
        s['p_E2'] = 0.0
            # Mass flow rate
        s['m_dot_A'] = self.cmp.m_dot
        s['m_dot_B'] = self.cmp.m_dot
        s['m_dot_C'] = self.cmp.m_dot
        s['m_dot_D'] = self.cmp.m_dot
        s['m_dot_E'] = self.cmp.m_dot
            # Volumetric flow rate
        s['Q_A1'] = self.cmp.Q_dot_1
        s['Q2'] = self.cmp.Q_dot_2
        s['Q3'] = self.tank.state['T']
        s['Q4'] = self.trb.Q_dot_1
        s['Q5'] = self.trb.Q_dot_2
        # Add to DataFrame
        self.df.append(s)

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

    def maintain(self, dt):
        # Turn Everything off

