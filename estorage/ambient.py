from CoolProp.CoolProp import PropsSI
from state import def_state_tp


class Ambient:
    def __init__(self,fluid='Air',t=298.15,p=101325.):
        # Provided inputs
        self.t = t # Temperature (K)
        self.p = p # Pressure (Pa)
        self.fluid = fluid # Fluid Name (-)
        self.state = def_state_tp(fluid,t,p)