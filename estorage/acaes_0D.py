import pandas as pd
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
import seaborn as sns

# Performance variables for charging (C) and discharging (D)
variablesC = ['t','pwr','m_dot','p1','T1','p2','T2','p3','T3','p_tnk','T_tnk','Q_clr','E_stor','Q_stor']
variablesD = ['t','pwr','m_dot','p4','T4','p5','T5','p6','T6','p_tnk','T_tnk','Q_htr','E_stor','Q_stor']

class ACAES_0D:

    def __init__(self, cmp_eff=0.80,trb_eff=0.88,T_stor=150,p_max=75.0,pwr=10,V=1E6):

        # ----------
        # Characteristics
        # ----------

        # Ambient Conditions
        self.fluid = 'Air'
        self.T_amb = 20. + 273.15  # K
        self.p_amb = 101325.  # Pa
        # Compressor
        self.cmp_eff = cmp_eff
        # Compressor
        self.trb_eff = trb_eff
        # Cooler
        self.T_stor = T_stor + 273.15  # convert from C to K
        # Tank
        self.V = V  # m3
        self.p_min = 2.0 * self.p_amb # convert from bar to Pa
        self.p_max = p_max * self.p_amb # convert from bar to Pa
        # Simulation
        self.dt = 60.0  # s
        self.pwr = pwr*10E6  # convert from MW to W

        # ----------
        # Performance
        # ----------
        self.dfC = pd.DataFrame(columns=variablesC)
        self.dfD = pd.DataFrame(columns=variablesD)
        self.RTE = -1.0
        self.Heat_Util = -1.0

    def run(self):
        # ----------
        # Pre-processing calculations
        # ----------
        # Ambient
        T1 = self.T_amb
        p1 = self.p_amb
        h1 = PropsSI('H', 'T', T1, 'P', p1, self.fluid)
        s1 = PropsSI('S', 'T', T1, 'P', p1, self.fluid)

        # Air Tank
        T_tnk = self.T_amb
        p_tnk = self.p_min
        m_tnk = self.V*PropsSI('D', 'T', T_tnk, 'P', p_tnk, self.fluid)
        u_tnk = PropsSI('U', 'T', T_tnk, 'P', p_tnk, self.fluid)
        MW = PropsSI('MOLEMASS', self.fluid) # kg/mol
        R = PropsSI('GAS_CONSTANT', self.fluid) # J/mol-K

        # Track energy and heat stored
        E_stor = 0.0
        Q_stor = 0.0

        #-------------------------------------
        # Charge
        #-------------------------------------
        t = 0.
        while p_tnk < self.p_max:
            t = t + self.dt

            # Compressor
            p2 = p_tnk
            h2s = PropsSI('H', 'P', p2, 'S', s1, self.fluid)
            h2 = h1 + (h2s - h1) / self.cmp_eff
            T2 = PropsSI('T', 'P', p2, 'H', h2, self.fluid)
            m_dot = self.pwr / (h2 - h1)

            # Cooler
            p3 = p2
            T3 = min(self.T_stor,T2)
            h3 = PropsSI('H', 'T', T3, 'P', p3, self.fluid)
            Q_clr = m_dot * (h2 - h3)

            # Storage Tank
            # Mass balance
            m_tnk = m_tnk + m_dot*self.dt
            n = m_tnk / MW  # moles
            # Energy balance
            Cv = PropsSI('CVMASS', 'T', T_tnk, 'P', p_tnk, self.fluid)  # Assume small differences in Cv
            u_tnk = ((m_tnk-m_dot*self.dt)*u_tnk + m_dot*self.dt*h3)/(m_tnk)
            T_tnk = u_tnk / Cv
            p_tnk = n * R * T_tnk / self.V

            # Energy/Heat Storage
            Q_stor = Q_stor + Q_clr*self.dt
            E_stor = E_stor + self.pwr*self.dt

            # Store Data
            s = pd.Series(index=variablesC)
            s['t']= t
            s['pwr'] = self.pwr
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
            self.dfC = self.dfC.append(s)

        #-------------------------------------
        # Mid-Analysis
        #-------------------------------------
        E_in = E_stor
        Q_in = Q_stor
        self.E_stor_max = E_stor/1E6/60./60. # convert from Ws to MWh

        #-------------------------------------
        # Discharge
        #-------------------------------------
        t = 0.

        while p_tnk > self.p_min:
            t = t + self.dt

            # Heater
            T4 = T_tnk
            p4 = p_tnk
            h4 = PropsSI('H', 'T', T4, 'P', p4, self.fluid)
            p5 = p_tnk
            if Q_stor>0:
                T5 = max(self.T_stor, T_tnk)
            else:
                T5 = T_tnk
            h5 = PropsSI('H', 'T', T5, 'P', p5, self.fluid)
            s5 = PropsSI('S', 'T', T5, 'P', p5, self.fluid)

            # Turbine
            p6 = self.p_amb
            h6s = PropsSI('H', 'P', p6, 'S', s5, self.fluid)
            h6 = h5 + (h6s - h5) * self.trb_eff
            T6 = PropsSI('T', 'P', p6, 'H', h6, self.fluid)
            m_dot = self.pwr / (h5 - h6)

            # Revisit Heater
            Q_htr = m_dot * (h5 - h4)

            # Storage Tank
                # Mass balance
            m_tnk = m_tnk - m_dot*self.dt
            n = m_tnk / MW  # moles
                # Energy balance
            Cv = PropsSI('CVMASS', 'T', T_tnk, 'P', p_tnk, self.fluid)  # Assume small differences in Cv
            u_tnk = ((m_tnk+m_dot*self.dt)*u_tnk - m_dot*self.dt*h4)/(m_tnk)
            T_tnk = u_tnk / Cv
            p_tnk = n * R * T_tnk / self.V

            # Energy/Heat Storage
            Q_stor = Q_stor - Q_htr*self.dt
            E_stor = E_stor - self.pwr*self.dt

            # Store Data
            s = pd.Series(index=variablesD)
            s['t']= t
            s['pwr'] = self.pwr
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
            self.dfD = self.dfD.append(s)

        #-------------------------------------
        # Final-Analysis
        #-------------------------------------
        Q_out = Q_in- Q_stor
        E_out = E_in- E_stor
        self.RTE = E_out/E_in*100.0
        self.Heat_Util = Q_out/Q_in*100.0
        # print "RTE: " + str(self.RTE)
        # print "Heat_Util: " + str(self.Heat_Util)

        results = pd.Series(index=['RTE','Heat_Util','E_stor_max'])
        results['RTE'] = self.RTE
        results['Heat_Util'] = self.Heat_Util
        results['E_stor_max'] = self.E_stor_max

        return results

    # -------------------------------------
    # Create Plots
    # -------------------------------------
    def create_plots(self,savename='Results'):

        f,ax = plt.subplots(nrows=4,ncols=2)
        #----
        # Charging
        #----
        x = self.dfC['t']
        # Temp
        convert = 273.15
        ax[0,0].plot(x, self.dfC['T1']-convert,label='T1')
        ax[0,0].plot(x, self.dfC['T2']-convert,label='T2')
        ax[0,0].plot(x, self.dfC['T3']-convert,label='T3')
        ax[0,0].plot(x, self.dfC['T_tnk']-convert,label='T_tnk')
        ax[0,0].legend()
        ax[0,0].set_ylabel('Temp [C]')
        # Press
        convert = 1E-6
        ax[1,0].plot(x, self.dfC['p1']*convert,label='p1')
        ax[1,0].plot(x, self.dfC['p2']*convert,label='p2')
        ax[1,0].plot(x, self.dfC['p3']*convert,label='p3')
        ax[1,0].plot(x, self.dfC['p_tnk']*convert,label='p_tnk')
        ax[1,0].legend()
        ax[1,0].set_ylabel('Pressure [MPa]')
        # Power/Heat
        convert = 1E-6
        ax[2,0].plot(x, self.dfC['pwr']*convert,label='pwr')
        ax[2,0].plot(x, self.dfC['Q_clr']*convert,label='Q_clr')
        ax[2,0].legend()
        ax[2,0].set_ylabel('Power/heat Flow [MW]')
        # Energy & Heat Storage
        convert = 1E-6
        ax[3,0].plot(x, self.dfC['E_stor']*convert,label='E_stor')
        ax[3,0].plot(x, self.dfC['Q_stor']*convert,label='Q_stor')
        ax[3,0].legend()
        ax[3,0].set_ylabel('Power/heat Storage [GJ]')

        #----
        # Discharging
        #----
        x = self.dfD['t']
        # Temp
        convert = 273.15
        ax[0,1].plot(x, self.dfD['T4']-convert,label='T4')
        ax[0,1].plot(x, self.dfD['T5']-convert,label='T5')
        ax[0,1].plot(x, self.dfD['T6']-convert,label='T6')
        ax[0,1].plot(x, self.dfD['T_tnk']-convert,label='T_tnk')
        ax[0,1].legend()
        ax[0,1].set_ylabel('Temp [C]')

        # Press
        convert = 1E-6
        ax[1,1].plot(x, self.dfD['p4']*convert,label='p4')
        ax[1,1].plot(x, self.dfD['p5']*convert,label='p5')
        ax[1,1].plot(x, self.dfD['p6']*convert,label='p6')
        ax[1,1].plot(x, self.dfD['p_tnk']*convert,label='p_tnk')
        ax[1,1].legend()
        ax[1,1].set_ylabel('Pressure [MPa]')
        # Power/heat
        convert = 1E-6
        ax[2,1].plot(x, self.dfD['pwr']*convert,label='pwr')
        ax[2,1].plot(x, self.dfD['Q_htr']*convert,label='Q_htr')
        ax[2,1].legend()
        ax[2,1].set_ylabel('Power/heat Flow [MW]')
        # Energy & Heat Storage
        convert = 1E-6
        ax[3,1].plot(x, self.dfD['E_stor']*convert,label='E_stor')
        ax[3,1].plot(x, self.dfD['Q_stor']*convert,label='Q_stor')
        ax[3,1].legend()
        ax[3,1].set_ylabel('Power/heat Storage [GJ]')

        # Save
        plt.savefig(savename+".png",DPI=1000)


# TO ADD
# Cumulative heat stored, energy stored, energy discharged, heat discharged
# Check energy balance