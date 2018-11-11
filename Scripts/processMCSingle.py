# -*- coding: utf-8 -*-
"""

@author: David P. Fleming, University of Washington, Seattle
@email: dflemin3 (at) uw (dot) edu
Oct 2018

This script parses data from an ensemble of VPLanet single star simulations.

"""

import os
import re
import numpy as np
import pandas as pd

# Constants and names
primary_name = "primary.in"
primary_out_name = "bintides.primary.forward"
YEARSEC = 3.154e+7 # Seconds in a year
dLowAge = 1.0e9 # Low age limit of 1 Gyr
dHighAge = 7.0e9 # High limit of 7 Gyr
PATH = os.path.dirname(os.path.realpath(__file__)) # Run in directory where sim dirs live
dirs = [] # Container to hold directory names
ind = None

# Find all simulation directories
with os.scandir(PATH) as it:
    print("Finding all simulation directories...")
    for entry in it:
        # Only consider simulation directories, ignoring hidden directories
        if not entry.name.startswith(".") and os.path.isdir(entry.name):
            dirs.append(entry.name)

# List to store data rows
table = []

# Extract data in directory
for ii, directory in enumerate(dirs):
    print("Parsing directory %d..." % ii)

    # List to hold this sim's data (row in df)
    tmp = []

    # Read in mass, tidal tau from primary input file
    with open(os.path.join(directory, primary_name), 'r') as f:
        primary_in = f.read()

        # Find the line where dMass lives, remove whitespace, make it a float
        dMass = re.findall('%s(.*?)#' % 'dMass', primary_in)[0]
        dMass = float("".join(dMass.split()))
        tmp.append(dMass)

    # Select a random age for this system
    dAge = np.random.uniform(low=dLowAge, high=dHighAge)

    # Save age
    tmp.append(dAge)

    # Read in simulation data
    # saOutputOrder Time -Radius -RotPer RadGyra # Output order
    data = np.genfromtxt(os.path.join(directory,primary_out_name), delimiter=" ")

    # Find row close enough to age
    ind = np.argmin(np.fabs(dAge-data[:,0]))

    # Save initial rotation period
    tmp.append(data[0,2])

    # Extract rotation period at Age [units == days]
    tmp.append(data[ind,2])

    # Save final rotation period at end of simulation, 7 Gyr
    tmp.append(data[-1,2])

    # Save row
    table.append(tmp)

# Make df with the following columns:
headers = ["Pri_dMass", "Age", "Pri_ProtInitial", "Pri_ProtAge", "Pri_ProtFinal"]
df = pd.DataFrame(table, columns=headers)

# Examine dataframe
print(df.head(5))

# Save it!
df.to_csv("mcSingle.csv", header=True, index=False)

# Finished!
print("Done!")
