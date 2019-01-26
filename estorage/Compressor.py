from CoolProp.CoolProp import PropsSI
from state import def_state_ph, def_state_init


class Compressor:
    def __init__(self, eff=80.):
        self.eff = eff  # Isentropic Efficiency (%)
        fluid = 'Air'
        self.state1 = def_state_init(fluid)
        self.state2 = def_state_init(fluid)
        self.m_dot = 0.0
        self.Q_dot_1 = 0.0
        self.Q_dot_2 = 0.0

    def compress(self, state1, p2,pwr):
        # Inlet
        fluid = state1['fluid']
        h1 = state1['h']
        s1 = state1['s']

        # Outlet
        h2s = PropsSI('H', 'P', p2, 'S', s1, fluid)
        h2 = h1 + (h2s - h1) / self.eff
        state2 = def_state_ph(fluid,p2,h2)

        # Mass Flow Rate
        m_dot = pwr/(state2.h-state1.h)

        # Volumetric Flow Rate
        Q_dot_1 = state1['D']*m_dot
        Q_dot_2 = state2['D']*m_dot

        # Store results
        self.state1 = state1
        self.state2 = state2
        self.m_dot = m_dot
        self.Q_dot_1 = Q_dot_1
        self.Q_dot_2 = Q_dot_2

        return state2
