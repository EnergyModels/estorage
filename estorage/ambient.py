

class Ambient:
    def __init__(self,fluid='Air',T=298.15,p=101325.):
        self.fluid = fluid # Fluid Name (-)
        self.T = T
        self.p = p