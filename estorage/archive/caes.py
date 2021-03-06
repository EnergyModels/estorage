import pandas as pd
from estorage.archive.ambient import Ambient
from estorage.archive.compressor import Compressor
from estorage.archive.tank import Tank
from estorage.archive.turbine import Turbine

variables =     ['dt',
              'pwr_i','pwr_o', # Power
              
              'm_tank', # Mass stored
              'm0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6',  # Mass flow
              'T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', # Temperature
              'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', # Pressure
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

        

    def charge(self, pwr, dt):
        # Do something

        #
        T_amb = 25.+273.15
        P_amb = 101325.
        fluid = 'Air'

        p2 = tank_pressure


        # ----------
        # Compressor
        #-----------
        # Inlet
        h1 = PropsSI('H', 'T', T_amb, 'P', p_amb, fluid)
        s1 = PropsSI('S', 'T', T_amb, 'P', p_amb, fluid)

        # Outlet
        h2s = PropsSI('H', 'P', p_out, 'S', s1, fluid)
        h2 = h1 + (h2s - h1) / self.eff_isen
        T_out = PropsSI('T', 'P', p_out, 'H', h2, fluid)

        # Mass Flow Rate
        m_dot = pwr / (h2 - h1)

        # Cooler













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

	def saveState(self, pwr, dt):
        
		#-----
		# Prepare series to store current state
		#-----
        s = pd.Series(index=variables)
        
		#-----
		# System Level
		#-----
		s['dt'] = dt
		s['pwr'] = pwr

		#-----
		# Fluid
		#-----
			# Tanks
		s['fluid_TA'] = 0.0
        s['fluid_TC'] = 0.0
        s['fluid_TH'] = 0.0
			# Flow paths
		s['fluid_A'] = self.cmp.m_dot
        s['fluid_B'] = 0.0
        s['fluid_C'] = 0.0
        s['fluid_D'] = 0.0
        s['fluid_E'] = 0.0	
		#-----
		# Mass stored (Tanks only)
		#-----
        s['m_TA'] = self.tank.m
        s['m_TC'] = 0.0
        s['m_TH'] = 0.0
		#-----
		# Mass flow rate (Flow paths only)
		#-----
        s['m_dot_A'] = self.cmp.m_dot
        s['m_dot_B'] = 0.0
        s['m_dot_C'] = 0.0
        s['m_dot_D'] = 0.0
        s['m_dot_E'] = 0.0
		#-----
		# Temperature
		#-----
			# Tanks
		s['T_TA'] = 0.0
        s['T_TC'] = 0.0
        s['T_TH'] = 0.0
			# Flow paths
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
		#-----
		# Pressure
		#-----
			# Tanks
		s['p_TA'] = self.tank.state['p']
        s['p_TC'] = 0.0
        s['p_TH'] = 0.0
			# Flow paths
        s['p_A1'] = self.cmp.state1['p']
        s['p_A2'] = self.cmp.state2['p']
        s['p_A3'] = 0.0
        s['p_B1'] = 0.0
        s['p_B2'] = 0.0
        s['p_B3'] = 0.0
        s['p_C1'] = 0.0
        s['p_C2'] = 0.0
        s['p_D1'] = 0.0
        s['p_D2'] = 0.0
        s['p_E1'] = 0.0
        s['p_E2'] = 0.0
        #-----
		# Turbomachienry Volumetric flow rates
        #-----
		s['Q_A1'] = self.cmp.Q_dot_1
        s['Q_A2'] = self.cmp.Q_dot_2
		s['Q_B2'] = 0.0
        s['Q_B3'] = 0.0
        #-----
		# Add to DataFrame
		#-----
        self.df.append(s)