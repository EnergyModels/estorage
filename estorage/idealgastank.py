from CoolProp.CoolProp import PropsSI

class IdealGasTank:

    def __init__(self,fluid='Air',V=1000.,T=293.15,p=101325.):

        # Performance Definition
        self.fluid = fluid
        self.V = V

        # Current State
        self.T = T
        self.p = p
        self.m = V**PropsSI('D', 'T', self.T, 'P', self.p, self.fluid)

    def charge(self, m_dot_in,fluid_in,T_in,p_in,m_dot_out,dt):

        # Subscripts
        # i - inlet
        # 0 - previous time step, time 0
        # 1 - current time step, time 1

        # Tank current state
        T0 = self.T
        p0 = self.p
        Cv0 = PropsSI('CVMASS', 'T', T0, 'P', p0, fluid) # Assume small differences in Cv
        MW = PropsSI('MOLEMASS', fluid) # kg/mol
        R = PropsSI('GAS_CONSTANT', fluid) # J/mol-K

        # Inlet state
        Ti = state_i['T']
        pi = state_i['p']

        # Mass Balance
        mi = m_dot*dt  # mass inflow
        m0 = self.m  # tank mass at t-1 (t0)
        m1 = mi + m0  # tank mass at t (t1)

        # Energy Balance
        ui = PropsSI('U', 'T', Ti, 'P', pi, fluid)
        u0 = PropsSI('U', 'T', T0, 'P', p0, fluid)
        u1 = (mi * ui + m0 * u0) / m1

        # Ideal Gas Law
        T1 = u1 / Cv
        n = m1/MW # moles
        p1=n*R*T1/V

        # Store results
        self.m = m1
        self.state = def_state_tp(fluid, T1, p1)