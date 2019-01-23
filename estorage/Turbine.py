from CoolProp.CoolProp import PropsSI
from state import def_state_ph


class Turbine:
    def __init__(self,eff=90.):
        self.eff = eff  # Isentropic Efficiency (%)

    def expand(self,state1, p2):
        # Inlet
        fluid = state1.fluid
        h1 = state1.h
        s1 = state1.s

        # Outlet
        h2s = PropsSI('H', 'P', p2, 'S', s1, fluid)
        h2 = h1 + (h2s - h1) * self.eff
        state2 = def_state_ph(fluid, p2, h2)

        return state2
