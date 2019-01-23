from ambient import Ambient
from compressor import Compressor
from tank import Tank
from turbine import Turbine


class CAES:
    def __init__(self,V=1000.,cmp_eff=80.,trb_eff=90.,p=200000):

        # Air Side
        self.amb = Ambient()
        self.cmp = Compressor(eff=cmp_eff)
        self.tank = Tank(V=V,p=p)
        self.trb = Turbine(eff=trb_eff)
        self.m_dot = 0.0

        # Heat Side

    def charge(self, pwr, dt):
        # Do something
        state1 = self.amb.state
        p_tank = self.tank.state.p
        state2 = self.cmp.compress(state1, p_tank)
        m_dot = pwr/(state2.h-state1.h)
        state3 = state2 # Hxer - to be added
        self.tank.charge(state3,m_dot,dt)
        self.m_dot = m_dot


    def discharge(self, pwr, dt):
        state4 = self.tank.state
        state5 = state4 # Hxer - to be added
        p_amb = self.amb.state.p
        state6 = self.trb.expand(state4, p_amb)
        m_dot = pwr / (state4.h - state5.h)
        self.tank.discharge(state4, m_dot, dt)

