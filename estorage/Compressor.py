from CoolProp.CoolProp import PropsSI
from state import def_state_ph, def_state_tp


class Compressor:
    def __init__(self, eff=80.):
        self.eff = eff  # Isentropic Efficiency (%)
        fluid = 'Air'
        T = 293.15
        p = 101325.
        self.state1 = def_state_tp(fluid, T, p)
        self.state2 = def_state_tp(fluid, T, p)

    def compress(self, state1, p2):
        # Inlet
        fluid = state1['fluid']
        h1 = state1['h']
        s1 = state1['s']

        # Outlet
        h2s = PropsSI('H', 'P', p2, 'S', s1, fluid)
        h2 = h1 + (h2s - h1) / self.eff
        state2 = def_state_ph(fluid,p2,h2)

        self.state1 = state1
        self.state2 = state2
        return state2
