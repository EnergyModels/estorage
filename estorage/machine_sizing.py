from CoolProp.CoolProp import PropsSI
from scipy.interpolate import interp1d


# Machine Inputs
N = 3600 # RPM
pwr = 10E6 # W, (1E6 W = 1 MW)
cmp_eff = 0.8 # fraction
PR = 6.0

# Inlet Conditions
fluid = 'Air'
T1 = 20.+273.15  # K
p1 = 101325.  # Pa

# Specific Speed Chart Inputs
Ns_ideal = [17.53573098,20.31460093,23.85633867,29.94568557,39.64060977,60.83324952,139.5346754]
Ds_ideal = [7.848168406,6.761801714,5.905258342,4.690713434,3.388928695,2.288095758,1.116116401]
eff_ideal = [0.3,0.4,0.5,0.6,0.7,0.8,0.8]
f_Ds = interp1d(Ns_ideal,Ds_ideal)
f_eff = interp1d(Ns_ideal,eff_ideal)

# Compressor Calculations
p2 = p1 * PR
h1 = PropsSI('H', 'T', T1, 'P', p1, fluid)
s1 = PropsSI('S', 'T', T1, 'P', p1, fluid)
h2s = PropsSI('H', 'P', p2, 'S', s1, fluid)
h2 = h1 + (h2s - h1) / cmp_eff
T2 = PropsSI('T', 'P', p2, 'H', h2, fluid)
m_dot = pwr / (h2 - h1)
Q = m_dot * PropsSI('D', 'T', T2, 'P', p2, fluid)

# Specific Speed
V1 = Q * 35.3147 # ft^3/sec ( 1 m^3 = 35.3147 ft^3)
H_ad = (h2-h1)*0.737/0.453596 # ft-lb/lbm (1 lbm = 0.453596 kg, 1 Nm = 0.737 ft-lb)
Ns = N * (V1)**0.5 / (H_ad)**(3./4.)
print "Ns: " + str(Ns)

# Specifid Diameter
Ds = f_Ds(Ns)
eff = f_eff(Ns)
print "Ds: " + str(Ds)
print "Eff:" + str(eff)
D = Ds * V1**0.5 / H_ad**(1./4.) # ft
D = D * 0.3048
print "D(m):" + str(D)







