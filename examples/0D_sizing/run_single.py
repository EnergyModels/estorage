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
inputs['trb_eff'] = 0.895  # fraction
inputs['pwr'] = 10.0  # MW

#  Design Variables
inputs['V'] = 2.4E4  # m3
inputs['p_min'] = 2.8  # bar
inputs['p_max'] = 31.1  # ratio

# ==============
# Run Simulation
# ==============
acaes = ACAES_IDEALGAS_0D(cmp_eff=inputs['cmp_eff'], trb_eff=inputs['trb_eff'], pwr=inputs['pwr'],
                          V=inputs['V'], p_min=inputs['p_min'], p_max=inputs['p_max'], debug=True)
results = acaes.run()
print results
acaes.create_plots('single_run')
acaes.create_pretty_plots('single_run2')

results.to_csv('single_run_results.csv')
