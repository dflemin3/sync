"""

@author: David P. Fleming, University of Washington, Seattle
@email: dflemin3 (at) uw (dot) edu
Nov. 2018

This script produces a population of single stars.

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

# Lists to hold stuff
pri_rot = []
pri_mass = []

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

    # Mass is uniformly sampled over [0.1, 1.0]
    dMass = np.random.uniform(low=0.1, high=1.0)

    # Write initial conditions to file
    primary_in = re.sub('%s(.*?)#' % 'dRotPeriod', '%s %.5e #' % ('dRotPeriod', dRotPeriod), primary_in)
    primary_in = re.sub('%s(.*?)#' % 'dMass', '%s %.5e #' % ('dMass', dMass), primary_in)

    if write_infiles:
        with open(os.path.join(PATH, directory, primary_name), 'w') as f:
            print(primary_in, file = f)

    # Save em for later...
    pri_rot.append(-dRotPeriod)
    pri_mass.append(dMass)

    # Write vpl file

    # Read template input file
    with open(os.path.join(PATH, sys_name), 'r') as f:
        sys_in = f.read()

    # Age = 7 Gyr
    dAge = 7.0e9

    # Tell vpl.in file how many bodies are in simulation
    saBodyFiles = "primary.in"

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
cols = ["primary_rot","primary_mass"]

# Put data into a pandas dataframe
df = percentile_list = pd.DataFrame(np.column_stack([pri_rot,pri_mass]), columns=cols)

# Dump it into a CSV since we'll use < 50,000 samples and this is good enough
if save_dist:
    df.to_csv(os.path.join(PATH,"mcSingle_distributions.csv"))

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
