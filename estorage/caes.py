from .ambient import Ambient
from .compressor import Compressor
from .tank import Tank
from .turbine import Turbine


class CAES:
    def __init__(self,V=1000.,cmp_eff=80.,trb_eff=90.):

        # Air Side
        self.amb = Ambient()
        self.cmp = Compressor(eff=cmp_eff)
        self.tank = Tank(V=V)
        self.trb = Turbine(eff=trb_eff)

        # Heat Side

    def charge(self, pwr, dt):
        # Do something

        state1 = self.amb.state
        p_tank = self.tank.getP()
        state2 = self.cmp.compress(state1, p_tank)
        m_dot = pwr/(state2.h-state1.h)
        state3 = state2 # Hxer
        self.tank.input(m_dot,state3)









    def discharge(self, pwr, dt):
        # Do something

