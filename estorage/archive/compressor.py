from CoolProp.CoolProp import PropsSI
import pandas as pd

variables = ['fluid','pwr','m_dot','T_in','p_in','Q_dot_in','T_out','p_out','Q_dot_out']


class Compressor:
    def __init__(self, eff=80.):

        # Performance Definition
        self.eff_isen = eff  # Isentropic Efficiency (%)

        # Current Operation

        self.df = pd.DataFrame(index=variables)

        # self.fluid = 'TBD'
        # self.pwr = 0.0
        # self.m_dot = 0.0
        # self.T_in = 0.0
        # self.p_in = 0.0
        # self.Q_dot_in = 0.0
        # self.T_out = 0.0
        # self.p_out = 0.0
        # self.Q_dot_out = 0.0

    def update(self, fluid, T_in, p_in, p_out, pwr):

        # Inlet
        h1 = PropsSI('H', 'T', T_in, 'P', p_in, fluid)
        s1 = PropsSI('S', 'T', T_in, 'P', p_in, fluid)

        # Outlet
        h2s = PropsSI('H', 'P', p_out, 'S', s1, fluid)
        h2 = h1 + (h2s - h1) / self.eff_isen
        T_out = PropsSI('T', 'P', p_out, 'H', h2, fluid)

        # Mass Flow Rate
        m_dot = pwr/(h2-h1)

        # Volumetric Flow Rate
        rho_in = PropsSI('D', 'T', T_in, 'P', p_in, fluid)
        Q_dot_in = m_dot * rho_in
        rho_out = PropsSI('D', 'T', T_out, 'P', p_out, fluid)
        Q_dot_out = m_dot * rho_out

        # Store Results
        s = pd.Series(index=variables)
        s['fluid'] = 'TBD'
        s['pwr'] = pwr
        s['m_dot'] = m_dot
        s['T_in'] = T_in
        s['p_in'] = p_in
        s['Q_dot_in'] = Q_dot_in
        s['T_out'] = T_out
        s['p_out'] = p_out
        s['Q_dot_out'] = Q_dot_out
        self.df.append(s)