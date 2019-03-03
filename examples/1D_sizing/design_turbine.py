from estorage import DESIGN_AIR_TRB
import seaborn as sns
import matplotlib.pyplot as plt


# Test
designs = DESIGN_AIR_TRB(p_in=31.132, t_in=370.0, p_out=1.01325, m_dot=13.82, RPM=10000, Nstgs=3, debug=True)

designs.to_csv('trb_design.csv')