from CoolProp.CoolProp import PropsSI


class Compressor:
    def __init__(self, eff=80.):

        # Performance Definition
        self.eff_isen = eff  # Isentropic Efficiency (%)

        # Current Operation
        self.fluid = 'TBD'
        self.pwr = 0.0
        self.m_dot = 0.0
        self.T_in = 0.0
        self.p_in = 0.0
        self.Q_dot_in = 0.0
        self.T_out = 0.0
        self.p_out = 0.0
        self.Q_dot_out = 0.0

    def update(self, fluid, T_in, p_in, p_out, pwr):

        # Given
        self.fluid = fluid
        self.pwr = pwr
        self.T_in = T_in
        self.p_in = p_in
        self.p_out = p_out

        # Inlet
        h1 = PropsSI('H', 'T', self.T_in, 'P', self.p_in, self.fluid)
        s1 = PropsSI('S', 'T', self.T_in, 'P', self.p_in, self.fluid)

        # Outlet
        h2s = PropsSI('H', 'P', self.p_out, 'S', s1, self.fluid)
        h2 = h1 + (h2s - h1) / self.eff_isen
        self.T_out = PropsSI('T', 'P', self.p_out, 'H', h2, self.fluid)

        # Mass Flow Rate
        self.m_dot = pwr/(h2-h1)

        # Volumetric Flow Rate
        rho_in = PropsSI('D', 'T', self.T_in, 'P', self.p_in, self.fluid)
        self.Q_dot_in = self.m_dot*rho_in
        rho_out = PropsSI('D', 'T', self.T_out, 'P', self.p_out, self.fluid)
        self.Q_dot_out = self.m_dot * rho_out