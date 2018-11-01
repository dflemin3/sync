"""

@author: David P. Fleming, University of Washington, Oct 2018
@email: dflemin3 (at) uw (dot) edu

TODO:
- Write description
- Annotate multipanel figure

Script output:

CPL Primary Locked Fraction: 0.7959
CTL Primary Locked Fraction: 0.7892
CPL Secondary Locked Fraction: 0.8074
CTL Secondary Locked Fraction: 0.8199

"""

import numpy as np
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

#Typical plot parameters that make for pretty plots
mpl.rcParams['font.size'] = 18.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif','serif':['Computer Modern']})
mpl.rc('text', usetex=True)

# Constants
EPS = 1.0e-10 # Small-enough number

# Load data
cpl = pd.read_csv("../Data/mcCPL.csv")
ctl = pd.read_csv("../Data/mcCTL.csv")

# Lock times < 0 -> Not locked, set them to 7e9 (last simulation output time)
cpl["Pri_LockTime"][cpl["Pri_LockTime"] < 0] = 7.0e9
cpl["Sec_LockTime"][cpl["Sec_LockTime"] < 0] = 7.0e9
ctl["Pri_LockTime"][ctl["Pri_LockTime"] < 0] = 7.0e9
ctl["Sec_LockTime"][ctl["Sec_LockTime"] < 0] = 7.0e9

# Output how many systems are actually locked
print("CPL Primary Locked Fraction:",np.sum(cpl["Pri_LockTime"] < 7.0e9)/len(cpl))
print("CTL Primary Locked Fraction:",np.sum(ctl["Pri_LockTime"] < 7.0e9)/len(ctl))

print("CPL Secondary Locked Fraction:",np.sum(cpl["Sec_LockTime"] < 7.0e9)/len(cpl))
print("CTL Secondary Locked Fraction:",np.sum(ctl["Sec_LockTime"] < 7.0e9)/len(ctl))

### Total marginal histogram of tidal locking times ###

fig, ax = plt.subplots()

ax.hist(cpl["Pri_LockTime"].values/1.0e9, bins="auto", color="C0", label="CPL",
        histtype="step", normed=True, lw=3)
ax.hist(ctl["Pri_LockTime"].values/1.0e9, bins="auto", color="C1", label="CTL",
        histtype="step", normed=True, lw=3)

ax.set_xlabel("Tidal Locking Time [Gyr]")
ax.set_ylabel("Normalized Counts [Arbitrary Units]")
ax.legend(loc="upper left", fontsize=15, framealpha=0)

fig.savefig("../Plots/lockTimeMarginalHistTot.pdf", bbox_inches="tight")

### Marginal tidal locking time histograms by final binary orbital period

porbBinEdges = [0, 20, 40, 60, 80, 100]

fig = plt.figure(figsize=(5, 15))

gs = GridSpec(9, 1, height_ratios=[1, 0.001,
                                   1, 0.001,
                                   1, 0.001,
                                   1, 0.001, 1])

# Loop over gridspec
for ii in range(9):

    # Only add axes on even gridspecs (odd ones are small spaces)
    if ii % 2 == 0:

        ax = fig.add_subplot(gs[ii])

        # Make mask to select systems in correct period range
        cplMask = (cpl["Final_Porb"] > porbBinEdges[ii//2])
        cplMask = cplMask & (cpl["Final_Porb"] < porbBinEdges[ii//2 + 1])

        ctlMask = (ctl["Final_Porb"] > porbBinEdges[ii//2])
        ctlMask = ctlMask & (ctl["Final_Porb"] < porbBinEdges[ii//2 + 1])

        ax.hist(cpl["Pri_LockTime"][cplMask].values/1.0e9, bins="auto", color="C0", label="CPL",
                histtype="step", normed=True, lw=3)
        ax.hist(ctl["Pri_LockTime"][ctlMask].values/1.0e9, bins="auto", color="C1", label="CTL",
                histtype="step", normed=True, lw=3)

        # Uniform x axis limits
        ax.set_xlim(0, 7)

        if ii == 4:
            ax.set_ylabel("Normalized Counts [Arbitrary Units]", fontsize=23, labelpad=10)

# Format last axis
ax.set_xlabel("Tidal Locking Time [Gyr]", fontsize=23)

fig.savefig("../Plots/lockTimePorbHist.pdf", bbox_inches="tight", dpi=600)
