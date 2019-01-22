from CoolProp.CoolProp import PropsSI

class Tank:
    def __init__(self,fluid='Air',V=1000,t=293.15,p=101325.):
        # Provided inputs
        self.V = V  # Volume (m3)
        self.t = t # Temperature (K)
        self.p = p # Pressure (Pa)
        self.fluid = fluid # Fluid Name (-)
        # Calculate to initialize
        self.m = V*PropsSI('D','T',t,'P',p,fluid) # Fluid Mass (kg)
        self.state =


    def getP(self, state,m_dot,dt):

        m_in = m_dot*dt
        m_total = self.m + self.m_in

        return self.p