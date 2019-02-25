import pandas as pd
import time
import numpy as np
import multiprocessing
from joblib import Parallel, delayed, parallel_backend
from estorage import ACAES_0D

#=====================
# Function to enable parameter sweep
#=====================
def parameterSweep(inputs):
    # Record time to solve
    t0 = time.time()

    # Run Simulation
    acaes = ACAES_0D(cmp_eff=inputs['cmp_eff'], trb_eff=inputs['trb_eff'], T_stor=inputs['T_stor'],
                     p_max=inputs['p_max'], pwr=inputs['pwr'], V=inputs['V'])
    results = acaes.run()
        
    # Display Elapsed Time
    t1 = time.time()
    print "Time Elapsed: " + str(round(t1-t0,2)) + " s"
    
    # Combine inputs and results into output and then return
    output = pd.concat([inputs,results],axis=0)
    return output

#=====================
# Main Program
#=====================
if __name__ == '__main__':
    
    #==============
    # User Inputs
    #==============
    studyName = "results_monte_carlo"

    iterations = 3

    # High and low values to evaluate
    T_stor = [150,500] # C
    p_max = [10,35] # bar
    V = [1E4,2E6]# m3

    # Fixed Inputs
    cmp_eff = [0.8,0.8]  # fraction
    trb_eff = [0.88,0.88]  # fraction
    pwr = [50,50]  # MW

    # Number of cores to use
    num_cores = multiprocessing.cpu_count()-1 # Consider saving one for other processes


    # ==============
    # Prepare Monte Carlo Distributions
    # ==============
    inputs = pd.DataFrame(index=range(iterations),columns=['cmp_eff','trb_eff','pwr','T_stor', 'p_max', 'V'])
    inputs.loc[:, 'cmp_eff'] = np.random.uniform(low=cmp_eff[0], high=cmp_eff[1], size=iterations)
    inputs.loc[:, 'trb_eff'] = np.random.uniform(low=trb_eff[0], high=trb_eff[1], size=iterations)
    inputs.loc[:, 'pwr'] = np.random.uniform(low=pwr[0], high=pwr[1], size=iterations)
    inputs.loc[:, 'T_stor'] = np.random.uniform(low=T_stor[0], high=T_stor[1], size=iterations)
    inputs.loc[:, 'p_max'] = np.random.uniform(low=p_max[0], high=p_max[1], size=iterations)
    inputs.loc[:, 'V'] = np.random.uniform(low=V[0], high=V[1], size=iterations)

    # ==============
    # Run Simulations
    # ==============

    # Perform Simulations (Run all plant variations in parallel)
    with parallel_backend('multiprocessing', n_jobs=num_cores):
        output = Parallel(verbose=10)(delayed(parameterSweep)(inputs.loc[index]) for index in range(iterations))

    # Combine outputs into single dataframe and save
    df = pd.concat(output,axis=1)
    df = df.transpose()
    df.to_csv(studyName + '.csv')