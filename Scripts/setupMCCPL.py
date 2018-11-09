"""

@author: David P. Fleming, University of Washington, Seattle
@email: dflemin3 (at) uw (dot) edu
Nov. 2018

This script produces a population of tidally-interacting binaries stars.

Assumptions:
- Template files live directory where this script exists.

"""

import numpy as np
import pandas as pd
import re
import os
from datetime import datetime
import stat
import sys

# Constants/Control Flags
num = 10000 # Number of sets of initial conditions to generate
PATH = os.path.dirname(os.path.realpath(__file__))
save_dist = True # Save initial condition distributions?
show_plots = True # visualize initial condition distributions?
write_infiles = True # Write the vplanet input files, or just sample from distributions if False
seed = int(os.getpid()*datetime.now().microsecond/100) # Random seed

# Set RNG seed
np.random.seed(seed)

# File names
sys_name = "vpl.in"
primary_name = "primary.in"
secondary_name = "secondary.in"

# Lists to hold stuff
pri_rot = []
pri_q = []
pri_mass = []

sec_rot = []
sec_q = []
sec_mass = []
sec_e = []
sec_orb = []

runfile_names = []

### Helper functions ###
def lognuniform(low=0, high=1, size=None, base=10.0):
    return np.power(base, np.random.uniform(low, high, size))
# end function


### Make the simulation initial conditions! ###
for ii in range(num):

    # Create a directory for the simulation to live in
    if write_infiles:
        directory = "simulation_" + str(ii)
        if not os.path.exists(os.path.join(PATH,directory)):
            os.makedirs(os.path.join(PATH,directory))

    ### Populate the primary input file ###

    # Read template input file
    with open(os.path.join(PATH, 'primary.in'), 'r') as f:
        primary_in = f.read()

    # Sample from priors for initial conditions

    # Loguniform initial rotation period prior over [0.8, 15] days (Matt+2015)
    dRotPeriod = -lognuniform(low=np.log10(0.8), high=np.log10(15.0)) # negative -> days

    # Log uniform prior for 10^4 - 10^7 for tidal Q
    dTidalQ = lognuniform(low=4, high=7)

    # Mass is uniformly sampled over [0.1, 1.0]
    dMass = np.random.uniform(low=0.1, high=1.0)

    # Write initial conditions to file
    primary_in = re.sub('%s(.*?)#' % 'dRotPeriod', '%s %.5e #' % ('dRotPeriod', dRotPeriod), primary_in)
    primary_in = re.sub('%s(.*?)#' % 'dTidalQ', '%s %.5e #' % ('dTidalQ', dTidalQ), primary_in)
    primary_in = re.sub('%s(.*?)#' % 'dMass', '%s %.5e #' % ('dMass', dMass), primary_in)

    if write_infiles:
        with open(os.path.join(PATH, directory, primary_name), 'w') as f:
            print(primary_in, file = f)

    # Save em for later...
    pri_rot.append(-dRotPeriod)
    pri_q.append(dTidalQ)
    pri_mass.append(dMass)

    # Read template input file
    with open(os.path.join(PATH, 'secondary.in'), 'r') as f:
        secondary_in = f.read()

    # Sample from priors for initial conditions

    # Loguniform initial rotation period prior over [0.8, 15] days (Matt+2015)
    dRotPeriod = -lognuniform(low=np.log10(0.8), high=np.log10(15.0)) # negative -> days

    # Log uniform prior for 10^4 - 10^7 for tidal Q
    dTidalQ = lognuniform(low=4, high=7)

    # Pick secondary mass using uniform mass ratio distribution over [0.1,1.0]
    # following Moe & Kratter (2018) assumption.  Make sure minimum mass is 0.1.
    dMass2 = -1
    while dMass2 < 0.1:
        q = np.random.uniform(low=0.1, high=1.0)
        dMass2 = dMass*q

    # Uniform eccentricity prior for [0.0,0.3)
    dEcc = np.random.uniform(low=0.0, high=0.3)

    # Uniform orbital period prior from [3.0,100.0)
    dOrbPeriod = -np.random.uniform(low=3.0, high=100.0) # negative -> days

    # Write initial conditions to file
    secondary_in = re.sub('%s(.*?)#' % 'dRotPeriod', '%s %.5e #' % ('dRotPeriod', dRotPeriod), secondary_in)
    secondary_in = re.sub('%s(.*?)#' % 'dTidalQ', '%s %.5e #' % ('dTidalQ', dTidalQ), secondary_in)
    secondary_in = re.sub('%s(.*?)#' % 'dMass', '%s %.5e #' % ('dMass', dMass2), secondary_in)
    secondary_in = re.sub('%s(.*?)#' % 'dEcc', '%s %.5e #' % ('dEcc', dEcc), secondary_in)
    secondary_in = re.sub('%s(.*?)#' % 'dOrbPeriod', '%s %.5e #' % ('dOrbPeriod', dOrbPeriod), secondary_in)

    if write_infiles:
        with open(os.path.join(PATH, directory, secondary_name), 'w') as f:
            print(secondary_in, file = f)

    # Save em for later... and remove -'s
    sec_rot.append(-dRotPeriod)
    sec_q.append(dTidalQ)
    sec_mass.append(dMass2)
    sec_e.append(dEcc)
    sec_orb.append(-dOrbPeriod)

    # Write vpl file

    # Read template input file
    with open(os.path.join(PATH, sys_name), 'r') as f:
        sys_in = f.read()

    # Age = 7 Gyr
    dAge = 7.0e9

    # Tell vpl.in file how many bodies are in simulation
    saBodyFiles = "primary.in"
    saBodyFiles += " secondary.in"

    # Write vpl file
    sys_in = re.sub('%s(.*?)#' % 'dStopTime', '%s %.5e #' % ('dStopTime', dAge), sys_in)
    sys_in = re.sub('%s(.*?)#' % 'saBodyFiles', '%s %s #' % ('saBodyFiles', saBodyFiles), sys_in)

    if write_infiles:
        with open(os.path.join(PATH, directory, sys_name), 'w') as f:
            print(sys_in, file = f)

    # Generate *.sh file needed for cluster to run sims
    if write_infiles:
        command = os.path.join(PATH, directory + ".sh")
        with open(command,"w") as g:
            g.write("#!/bin/bash\n")
            g.write("cd " + os.path.join(PATH, directory) + "\n") # Change dir to where sim is
            g.write("vplanet vpl.in\n") # Run sim command!

        # Now give that .sh file execute permissions
        st = os.stat(command)
        os.chmod(command, st.st_mode | stat.S_IEXEC)

        # Save file name for later...
        runfile_names.append(command)
# end for loop

# Write all runfile names to file needed for cluster
if write_infiles:
    with open(os.path.join(PATH, "vplArgs.txt"), 'w') as f:
        for line in runfile_names:
            f.write(line + "\n")

# Save the distributions?
cols = ["primary_rot", "log(primary_Q)","primary_mass",
        "secondary_rot","log(secondary_Q)","secondary_mass",
        "secondary_e","secondary_orb"]

# Put data into a pandas dataframe
df = percentile_list = pd.DataFrame(np.column_stack([pri_rot,
                                                     np.log10(pri_q),
                                                     pri_mass,
                                                     sec_rot,
                                                     np.log10(sec_q),
                                                     sec_mass,
                                                     sec_e,
                                                     sec_orb]),
                                                     columns=cols)

# Dump it into a CSV since we'll use < 50,000 samples and this is good enough
if save_dist:
    df.to_csv(os.path.join(PATH,"mcCPL_distributions.csv"))

# Visualize the distributions?
if show_plots:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(18,16))

    df.hist(ax=ax, bins="auto")
    fig.tight_layout()
    fig.savefig(os.path.join(PATH,"dist_hist.pdf"), bbox_inches="tight")
# Done!
