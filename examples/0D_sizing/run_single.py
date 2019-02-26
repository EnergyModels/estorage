import pandas as pd
import time
import numpy as np
import multiprocessing
from joblib import Parallel, delayed, parallel_backend
from estorage import ACAES_IDEALGAS_0D

# ==============
# User Inputs
# ==============

inputs = pd.Series(index=['cmp_eff', 'trb_eff', 'pwr', 'V', 'p_min', 'PR'])

# Fixed Inputs
inputs['cmp_eff'] = 0.8  # fraction
inputs['trb_eff'] = 0.88  # fraction
inputs['pwr'] = 10  # MW

#  Design Variables
inputs['V'] = 1.E4  # m3
inputs['p_min'] = 1.1  # bar
inputs['PR'] = 10.  # ratio

# ==============
# Run Simulation
# ==============
acaes = ACAES_IDEALGAS_0D(cmp_eff=inputs['cmp_eff'], trb_eff=inputs['trb_eff'], pwr=inputs['pwr'],
                          V=inputs['V'], p_min=inputs['p_min'], PR=inputs['PR'], debug=True)
results = acaes.run()
print results
acaes.create_plots('single_run')
