from estorage import DESIGN_AIR_CMP
import seaborn as sns
import matplotlib.pyplot as plt


# Test
designs = DESIGN_AIR_CMP(p_in=1.01325, t_in=20.0, p_out=31.132, m_dot=13.82, RPM=8500, Nstgs=6, debug=True)

designs.to_csv('cmp_design.csv')