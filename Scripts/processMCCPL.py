# -*- coding: utf-8 -*-
"""

@author: David P. Fleming, University of Washington, Seattle
@email: dflemin3 (at) uw (dot) edu
Oct 2018

This script parses data from an ensemble of VPLanet CPL/CTL coupled stellar-tidal
simulations.

"""

import os
import re
import numpy as np
import pandas as pd

# Constants and names
primary_name = "primary.in"
secondary_name = "secondary.in"
logfile_name = "bintides.log"
primary_out_name = "bintides.primary.forward"
secondary_out_name = "bintides.secondary.forward"
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

    # Read in mass, tidal Q from primary input file
    with open(os.path.join(directory, primary_name), 'r') as f:
        primary_in = f.read()

        # Find the line where dMass lives, remove whitespace, make it a float
        dMass = re.findall('%s(.*?)#' % 'dMass', primary_in)[0]
        dMass = float("".join(dMass.split()))
        tmp.append(dMass)

        # Find the line where dTidalQ lives, remove whitespace, make it a float
        dTidalQ = re.findall('%s(.*?)#' % 'dTidalQ', primary_in)[0]
        dTidalQ = float("".join(dTidalQ.split()))
        tmp.append(dTidalQ)

    # Read in mass from secondary input file
    with open(os.path.join(directory, secondary_name), 'r') as f:
        secondary_in = f.read()

        # Find the line where dMass lives, remove whitespace, make it a float
        dMass2 = re.findall('%s(.*?)#' % 'dMass', secondary_in)[0]
        dMass2 = float("".join(dMass2.split()))
        tmp.append(dMass2)

        # Find the line where dTidalQ lives, remove whitespace, make it a float
        dTidalQ2 = re.findall('%s(.*?)#' % 'dTidalQ', secondary_in)[0]
        dTidalQ2 = float("".join(dTidalQ2.split()))
        tmp.append(dTidalQ2)

    # Pull LockTimes out of logfile
    with open(os.path.join(os.path.join(directory, logfile_name)), 'r') as f:
        logfile_in = f.read()

    matches = []
    for line in logfile_in.split("\n"):
        if line.startswith("(LockTime)"):
            matches.append((line.split()[-1]))

    # Convert lock times to years
    if len(matches) > 2:
        dLockTime1 = float(matches[2])/YEARSEC
        dLockTime2 = float(matches[3])/YEARSEC
    else:
        dLockTime1 = -1
        dLockTime2 = -1

    tmp.append(dLockTime1)
    tmp.append(dLockTime2)

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

    # Read in simulation data for secondary star
    # saOutputOrder	Time Semim Ecce -RotPer -Radius RadGyra -OrbPeriod -TotEn
    # -TotAngMom -EqRotPer #Output order
    data = np.genfromtxt(os.path.join(directory,secondary_out_name), delimiter=" ")

    # Save initial rotation period
    tmp.append(data[0,3])

    # Extract rotation period at age [units == days]
    tmp.append(data[ind,3])

    # Save final rotation period at end of simulation
    tmp.append(data[-1,3])

    # Save initial, final ecc, ecc at age
    tmp.append(data[0,2])
    tmp.append(data[-1,2])
    tmp.append(data[ind,2])

    # Save initial, final Porb, Porb at age
    tmp.append(data[0,6])
    tmp.append(data[-1,6])
    tmp.append(data[ind,6])

    # Save initial, final Peq, Peq at age
    tmp.append(data[0,9])
    tmp.append(data[-1,9])
    tmp.append(data[ind,9])

    # Save row
    table.append(tmp)

# Make df with the following columns:
headers = ["Pri_dMass", "Pri_dTidaLQ", "Sec_dMass", "Sec_dTidalQ", "Pri_LockTime", "Sec_LockTime", "Age"]
headers = headers + ["Pri_ProtInitial", "Pri_ProtAge", "Pri_ProtFinal"]
headers = headers + ["Sec_ProtInitial", "Sec_ProtAge", "Sec_ProtFinal"]
headers = headers + ["Initial_Ecc", "Final_Ecc", "Age_Ecc"]
headers = headers + ["Initial_Porb", "Final_Porb", "Age_Porb"]
headers = headers + ["Initial_Peq", "Final_Peq", "Age_Peq"]
df = pd.DataFrame(table, columns=headers)

# Examine dataframe
print(df.head(5))

# Save it!
df.to_csv("mcCPLMarch27.csv", header=True, index=False)

# Finished!
print("Done!")
