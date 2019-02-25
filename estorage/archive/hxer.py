from CoolProp.CoolProp import PropsSI


class Hxer:
    def __init__(self, effect=95.,dp_pct1=5.,dp_pct2=5.):
        # Performance Definition
        self.effect = effect  # Effectiveness (%)
        self.dp_pct1 = dp_pct1  # Pressure drop (%)
        self.dp_pct2 = dp_pct2  # Pressuure drop (%)

        # Current Operation
        self.duty = 0.0

        self.fluid1 = 'TBD'
        self.m_dot1 = 0.0
        self.T_in1 = 0.0
        self.p_in1 = 0.0
        self.T_out1 = 0.0
        self.p_out1 = 0.0

        self.fluid2 = 'TBD'
        self.m_dot2 = 0.0
        self.T_in2 = 0.0
        self.p_in2 = 0.0
        self.T_out2 = 0.0
        self.p_out2 = 0.0

    def update(self, fluid1, m_dot1, T_in1, p_in1, fluid2, m_dot2, T_in2, p_in2):

        # Given
        self.fluid1 = fluid1
        self.m_dot1 = m_dot1
        self.T_in1 = T_in1
        self.p_in1 = p_in1
        self.fluid2 = fluid2
        self.m_dot2 = m_dot2
        self.T_in2 = T_in2
        self.p_in2 = p_in2

        # Calculate outlet pressures
        self.p_out1 = self.p_in1*(1.-self.dp_pct1/100.)
        self.p_out2 = self.p_in2*(1.-self.dp_pct2/100.)

        # Inlet enthalpy conditions
        h_in1 = PropsSI('H', 'T', self.T_in1, 'P', self.p_in1, self.fluid1)
        h_in2 = PropsSI('H', 'T', self.T_in2, 'P', self.p_in2, self.fluid2)

        # Max theoretical outlet enthalpies - fluid
        h_out1_max = PropsSI('H', 'T', self.T_in2, 'P', self.p_out1, self.fluid1)
        h_out2_max = PropsSI('H', 'T', self.T_in1, 'P', self.p_out2, self.fluid2)

        # Calculate Max and Actual Duty
        dh1_max = abs(h1-h_out1_max)
        dh2_max = abs(h2-h_out2_max)
        duty1_max = self.m_dot1*dh1_max*self.effect
        duty2_max = self.m_dot2*dh2_max*self.effect

        self.duty = min(duty1_max,duty2_max)

        # Calculate Outlet Temps
        if T_in1 > T_in2:
            h_out1 = h_in1 - self.duty/self.m_dot1
            h_out2 = h_in2 + self.duty/self.m_dot1
        else:
            h_out1 = h_in1 + self.duty / self.m_dot1
            h_out2 = h_in2 - self.duty / self.m_dot1
        self.T_out1 = PropsSI('T', 'P', self.P_out1, 'H', h_out1, self.fluid1)
        self.T_out2 = PropsSI('T', 'P', self.P_out2, 'H', h_out2, self.fluid2)