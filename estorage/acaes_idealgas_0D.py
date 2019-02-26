import pandas as pd
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
import seaborn as sns

# Performance variables for charging (C) and discharging (D)
variablesC = ['t', 'pwr', 'm_cav', 'm_hw', 'm_dot', 'm_dot_w', 'p1', 'T1', 'p2', 'T2', 'p3', 'T3', 'p_cav', 'T_cav',
              'T_c', 'T_h', 'Q_clr', 'E_stor', 'Q_stor']
variablesD = ['t', 'pwr', 'm_cav', 'm_hw', 'm_dot', 'm_dot_w', 'p4', 'T4', 'p5', 'T5', 'p6', 'T6', 'p_cav', 'T_cav',
              'T_c', 'T_h', 'Q_htr', 'E_stor', 'Q_stor']


class ACAES_IDEALGAS_0D:

    def __init__(self, cmp_eff=0.80, trb_eff=0.88, pwr=10, V=1E6, p_min=1.01325, PR=10.0, p_max=10.0, switch="p_max",
                 debug=False):

        # ----------
        # Characteristics
        # ----------

        # Ambient Conditions
        self.T_amb = 25. + 273.15  # K
        self.p_amb = 101325.  # Pa

        # Air Properties
        self.gamma = 1.4
        # Water Properties
        self.hxer_approach = 10.0  # K
        self.T_c = 25. + 273.15  # K

        # Machinery
        self.cmp_eff = cmp_eff
        self.trb_eff = trb_eff

        # Cavern
        self.V = V  # m3
        self.p_min = p_min * 1E5  # convert from bar to Pa
        self.T_cav = self.T_amb
        if switch == "p_max":
            self.p_max = p_max * 1E5  # convert from bar to Pa
        elif switch == 'PR':
            self.p_max = PR * self.p_min

        # Simulation
        self.dt = 60.0  # s
        self.pwr = pwr * 1E6  # convert from MW to KW

        self.debug = debug

        # ----------
        # Performance
        # ----------
        self.dfC = pd.DataFrame(columns=variablesC)
        self.dfD = pd.DataFrame(columns=variablesD)
        self.RTE = -1.0
        self.Heat_Util = -1.0
        self.E_in = -1.0
        self.E_out = -1.0
        self.Q_in = -1.0
        self.Q_out = -1.0
        self.T_out_min = -1.0
        self.m_dot_des = -1.0

    def run(self):
        # ----------
        # Pre-processing calculations
        # ----------
        # Air Properties
        CP = PropsSI('CPMASS', "T", self.T_amb, "P", self.p_amb, 'Air')  # J/Kg/K
        CV = PropsSI('CVMASS', "T", self.T_amb, "P", self.p_amb, 'Air')  # J/Kg/K
        gamma = CP / CV
        MW = PropsSI('MOLEMASS', 'Air')  # kg/mol
        R = PropsSI('GAS_CONSTANT', 'Air')  # J/mol-K

        # Heat Transfer Fluid Properties
        T_ht_max = 398.00 + 273.15
        CP_ht_low = PropsSI('CPMASS', "T", self.T_amb, "P", self.p_amb, 'INCOMP::S800')  # J/Kg
        CP_ht_high = PropsSI('CPMASS', "T", T_ht_max, "P", self.p_amb, 'INCOMP::S800')  # J/Kg
        CP_ht = 0.5 * (CP_ht_low + CP_ht_high)

        # Ambient
        T1 = self.T_amb
        p1 = self.p_amb

        # Cavern
        p_cav = self.p_min
        m_cav = self.V * PropsSI('D', 'T', self.T_cav, 'P', p_cav, 'Air')

        # Track energy and heat stored
        E_stor = 0.0
        Q_stor = 0.0

        # Water Reservoirs
        self.T_c = self.T_amb
        T_h = self.T_amb
        m_h = 0.001

        # -------------------------------------
        # Charge
        # -------------------------------------
        t = 0.
        while p_cav < self.p_max:
            t = t + self.dt

            # Compressor
            p2 = p_cav
            T2 = T1 * (p2 / p1) ** ((gamma - 1) / (self.cmp_eff * gamma))
            m_dot = self.pwr / (CP * T1 * ((p2 / p1) ** ((gamma - 1) / (self.cmp_eff * gamma)) - 1))

            # Cooler - Air Side
            p3 = p2
            if T2 - self.T_c > self.hxer_approach:
                T3 = self.T_c + self.hxer_approach
                Q_clr = m_dot * CP * (T2 - T3)
            else:
                T3 = T2
                Q_clr = 0.0

            # Cooler - Heat Transfer Fluid Side
            if T2 > T_ht_max:
                T_h_in = T_ht_max - self.hxer_approach
                m_dot_ht = Q_clr / (CP_ht * (T_h_in - self.T_c))
            elif T2 > T3:
                T_h_in = T2 - self.hxer_approach
                m_dot_ht = Q_clr / (CP_ht * (T_h_in - self.T_c))
            else:
                T_h_in = 0.0
                m_dot_ht = 0.0

            # Hot Storage
            m_h_in = m_dot_ht * self.dt
            T_h = (m_h * T_h + m_h_in * T_h_in) / (m_h + m_h_in)
            m_h = m_h + m_h_in

            # Cavern
            m_cav = m_cav + m_dot * self.dt
            p_cav = m_cav / MW * R * self.T_cav / self.V

            # Energy/Heat Storage
            Q_stor = Q_stor + Q_clr * self.dt
            E_stor = E_stor + self.pwr * self.dt

            # Store Data
            s = pd.Series(index=variablesC)
            s['t'] = t
            s['pwr'] = self.pwr
            s['m_cav'] = m_cav
            s['m_h'] = m_h
            s['m_dot'] = m_dot
            s['m_dot_ht'] = m_dot_ht
            s['p1'] = p1
            s['T1'] = T1
            s['p2'] = p2
            s['T2'] = T2
            s['p3'] = p3
            s['T3'] = T3
            s['p_cav'] = p_cav
            s['T_cav'] = self.T_cav
            s['T_c'] = self.T_c
            s['T_h'] = T_h
            s['Q_clr'] = Q_clr
            s['Q_stor'] = Q_stor
            s['E_stor'] = E_stor
            s.name = t
            self.dfC = self.dfC.append(s)

            if self.debug == True:
                print "Charging - p_cav: " + str(round(p_cav / 1E5, 2)) + " m_dot: " + str(round(m_dot, 2))

        # -------------------------------------
        # Mid-Analysis
        # -------------------------------------
        E_in = E_stor
        Q_in = Q_stor
        self.m_dot_des = m_dot

        # -------------------------------------
        # Discharge
        # -------------------------------------
        t = 0.

        while p_cav > self.p_min and m_h > 0.0:
            t = t + self.dt

            # Heater - Air Side
            T4 = self.T_cav
            p4 = p_cav
            p5 = p_cav
            if T_h - self.T_cav > self.hxer_approach:
                T5 = T_h - self.hxer_approach
            else:
                T5 = T4

            # Turbine
            p6 = self.p_amb
            T6 = T5 * (p6 / p5) ** ((gamma - 1) / (self.cmp_eff * gamma))
            m_dot = -1.0 * self.pwr / (CP * T5 * ((p6 / p5) ** (self.trb_eff * (gamma - 1) / (gamma)) - 1))

            # Revisit Heater - Air Side
            Q_htr = m_dot * CP * (T5 - T4)

            # Heater - Water Side & How Water Storage
            if T4 < T5:
                T_c_in = T4 + self.hxer_approach
                m_dot_ht = Q_htr / (CP_ht * (T5 - T_c_in))
            else:
                T_c_in = 0.0
                m_dot_ht = 0.0
            m_h = m_h - m_dot_ht * self.dt

            # Cavern
            m_cav = m_cav - m_dot * self.dt
            p_cav = m_cav / MW * R * self.T_cav / self.V  # Ideal Gas Law

            # Energy/Heat Storage
            Q_stor = Q_stor - Q_htr * self.dt
            E_stor = E_stor - self.pwr * self.dt

            # Check outlet temp
            if self.T_out_min == -1.0:
                self.T_out_min = T6
            else:
                self.T_out_min = min(self.T_out_min, T6)

            # Store Data
            s = pd.Series(index=variablesD)
            s['t'] = t
            s['pwr'] = self.pwr
            s['m_cav'] = m_cav
            s['m_h'] = m_h
            s['m_dot'] = m_dot
            s['m_dot_ht'] = m_dot_ht
            s['p4'] = p4
            s['T4'] = T4
            s['p5'] = p5
            s['T5'] = T5
            s['p6'] = p6
            s['T6'] = T6
            s['p_cav'] = p_cav
            s['T_cav'] = self.T_cav
            s['T_c'] = self.T_c
            s['T_h'] = T_h
            s['Q_htr'] = Q_htr
            s['Q_stor'] = Q_stor
            s['E_stor'] = E_stor
            s.name = t
            self.dfD = self.dfD.append(s)

            if self.debug == True:
                print "Discharging - p_cav: " + str(round(p_cav / 1E5, 2)) + " m_dot: " + str(round(m_dot, 2))

        # -------------------------------------
        # Final-Analysis
        # -------------------------------------
        Q_out = Q_in - Q_stor
        E_out = E_in - E_stor

        self.RTE = E_out / E_in * 100.0
        self.Heat_Util = Q_out / Q_in * 100.0

        # Store and Convert from Ws to MWh
        convert = 1.0 / 1E6 / 60. / 60.
        self.E_in = E_in * convert
        self.E_out = E_out * convert
        self.Q_in = Q_in * convert
        self.Q_out = Q_out * convert

        # Convert to C
        self.T_out_min = self.T_out_min - 273.15

        results = pd.Series(
            index=['RTE', 'Heat_Util', 'E_in', 'E_out', 'Q_in', 'Q_out', 'T_out_min', 'Ebal', 'Qbal', 'T_h'])
        results['RTE'] = self.RTE
        results['Heat_Util'] = self.Heat_Util
        results['E_in'] = self.E_in
        results['E_out'] = self.E_out
        results['Q_in'] = self.Q_in
        results['Q_out'] = self.Q_out
        results['T_out_min'] = self.T_out_min
        results['Ebal'] = self.E_in - self.E_out
        results['Qbal'] = self.Q_in - self.Q_out
        results['T_h'] = T_h - 273.15
        results['m_dot_des'] = self.m_dot_des

        return results

    # -------------------------------------
    # Create Plots
    # -------------------------------------
    def create_plots(self, savename='Results'):

        f, ax = plt.subplots(nrows=5, ncols=2, figsize=(20, 20))
        # ----
        # Charging
        # ----
        x = self.dfC['t']
        # Temp
        convert = 273.15
        ax[0, 0].plot(x, self.dfC['T1'] - convert, label='T1', marker='o')
        ax[0, 0].plot(x, self.dfC['T2'] - convert, label='T2', marker='v')
        ax[0, 0].plot(x, self.dfC['T3'] - convert, label='T3', marker='x')
        ax[0, 0].plot(x, self.dfC['T_cav'] - convert, label='T_cav', marker='<')
        ax[0, 0].plot(x, self.dfC['T_c'] - convert, label='T_c', marker='>')
        ax[0, 0].plot(x, self.dfC['T_h'] - convert, label='T_h', marker='*')
        ax[0, 0].legend()
        ax[0, 0].set_ylabel('Temp [C]')
        # Press
        convert = 1E-5
        ax[1, 0].plot(x, self.dfC['p1'] * convert, label='p1', marker='o')
        ax[1, 0].plot(x, self.dfC['p2'] * convert, label='p2', marker='v')
        ax[1, 0].plot(x, self.dfC['p3'] * convert, label='p3', marker='x')
        ax[1, 0].plot(x, self.dfC['p_cav'] * convert, label='p_cav', marker='<')
        ax[1, 0].legend()
        ax[1, 0].set_ylabel('Pressure [bar]')
        # Power/Heat
        convert = 1E-6
        ax[2, 0].plot(x, self.dfC['pwr'] * convert, label='pwr', marker='o')
        ax[2, 0].plot(x, self.dfC['Q_clr'] * convert, label='Q_clr', marker='x')
        ax[2, 0].legend()
        ax[2, 0].set_ylabel('Power/heat Flow [MW]')
        # Energy & Heat Storage
        convert = 1E-3
        ax[3, 0].plot(x, self.dfC['E_stor'] * convert, label='E_stor', marker='o')
        ax[3, 0].plot(x, self.dfC['Q_stor'] * convert, label='Q_stor', marker='x')
        ax[3, 0].legend()
        ax[3, 0].set_ylabel('Power/heat Storage [GJ]')
        # Mass Storage
        ax[4, 0].plot(x, self.dfC['m_cav'], label='m_cav', marker='o')
        ax[4, 0].plot(x, self.dfC['m_h'], label='m_h', marker='x')
        ax[4, 0].legend()
        ax[4, 0].set_ylabel('Mass Storage [kg]')

        # ----
        # Discharging
        # ----
        x = self.dfD['t']
        # Temp
        convert = 273.15
        ax[0, 1].plot(x, self.dfD['T4'] - convert, label='T4', marker='o')
        ax[0, 1].plot(x, self.dfD['T5'] - convert, label='T5', marker='v')
        ax[0, 1].plot(x, self.dfD['T6'] - convert, label='T6', marker='x')
        ax[0, 1].plot(x, self.dfD['T_cav'] - convert, label='T_cav', marker='<')
        ax[0, 1].plot(x, self.dfD['T_c'] - convert, label='T_c', marker='>')
        ax[0, 1].plot(x, self.dfD['T_h'] - convert, label='T_h', marker='*')
        ax[0, 1].legend()
        ax[0, 1].set_ylabel('Temp [C]')

        # Press
        convert = 1E-5
        ax[1, 1].plot(x, self.dfD['p4'] * convert, label='p4', marker='o')
        ax[1, 1].plot(x, self.dfD['p5'] * convert, label='p5', marker='v')
        ax[1, 1].plot(x, self.dfD['p6'] * convert, label='p6', marker='x')
        ax[1, 1].plot(x, self.dfD['p_cav'] * convert, label='p_cav', marker='<')
        ax[1, 1].legend()
        ax[1, 1].set_ylabel('Pressure [bar]')
        # Power/heat
        convert = 1E-6
        ax[2, 1].plot(x, self.dfD['pwr'] * convert, label='pwr', marker='o')
        ax[2, 1].plot(x, self.dfD['Q_htr'] * convert, label='Q_htr', marker='x')
        ax[2, 1].legend()
        ax[2, 1].set_ylabel('Power/heat Flow [MW]')
        # Energy & Heat Storage
        convert = 1E-3
        ax[3, 1].plot(x, self.dfD['E_stor'] * convert, label='E_stor', marker='o')
        ax[3, 1].plot(x, self.dfD['Q_stor'] * convert, label='Q_stor', marker='x')
        ax[3, 1].legend()
        ax[3, 1].set_ylabel('Power/heat Storage [GJ]')
        # Mass Storage
        ax[4, 1].plot(x, self.dfD['m_cav'], label='m_cav', marker='o')
        ax[4, 1].plot(x, self.dfD['m_h'], label='m_h', marker='x')
        ax[4, 1].legend()
        ax[4, 1].set_ylabel('Mass Storage [kg]')

        # Save
        plt.savefig(savename + ".png", DPI=1000)

# TO ADD
# Check energy balance
