"""

@author: David P. Fleming, University of Washington, Nov 2018
@email: dflemin3 (at) uw (dot) edu

Joint distribution of median tidal locking time over age and Porb.

"""

import numpy as np
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from cmap import shiftedColorMap

#Typical plot parameters that make for pretty plots
mpl.rcParams['font.size'] = 20.0

# Define a shifted colormap so 1 is at the center
cmap = "RdYlBu"

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

# Load data
cpl = pd.read_csv("../Data/mcCPLTorqueNov9.csv")
ctl = pd.read_csv("../Data/mcCTLTorqueNov9.csv")
cpl["Age"] = cpl["Age"].copy()/1.0e9
ctl["Age"] = ctl["Age"].copy()/1.0e9

# Construct Porb, ecc bins based on assumed ranges
num = 11
porbBinEdges = np.linspace(0, 100, num)
ageBinEdges = np.linspace(1, 7, num)

# Array for joint locking time distribution
cplJointPeq = np.zeros((num-1, num-1))
ctlJointPeq = np.zeros_like(cplJointPeq)

# Array for joint Prot/Porb distribution
cplJointRatio = np.zeros_like(cplJointPeq)
ctlJointRatio = np.zeros_like(cplJointPeq)

# Loop over bins, compute median tidal locking time in joing Porb/ecc bins
for ii in range(num-1):
    for jj in range(num-1):
        cplMask = (cpl["Age_Porb"] > porbBinEdges[ii])
        cplMask = cplMask & (cpl["Age_Porb"] < porbBinEdges[ii + 1])
        cplMask = cplMask & (cpl["Age"] > ageBinEdges[jj])
        cplMask = cplMask & (cpl["Age"] < ageBinEdges[jj + 1])

        ctlMask = (ctl["Age_Porb"] > porbBinEdges[ii])
        ctlMask = ctlMask & (ctl["Age_Porb"] < porbBinEdges[ii + 1])
        ctlMask = ctlMask & (ctl["Age"] > ageBinEdges[jj])
        ctlMask = ctlMask & (ctl["Age"] < ageBinEdges[jj + 1])

        # Populate array elements ctl["Pri_ProtFinal"][ctlMask]
        cplJointPeq[ii, jj] = np.median(cpl["Age_Peq"][cplMask]/cpl["Pri_ProtAge"][cplMask])
        ctlJointPeq[ii, jj] = np.median(ctl["Age_Peq"][ctlMask]/ctl["Pri_ProtAge"][ctlMask])

        cplJointRatio[ii, jj] = np.median(cpl["Age_Porb"][cplMask]/cpl["Pri_ProtAge"][cplMask])
        ctlJointRatio[ii, jj] = np.median(ctl["Age_Porb"][ctlMask]/ctl["Pri_ProtAge"][ctlMask])

# end loop

################################################################################
#
#   Joint distribution of Porb/Prot
#
################################################################################

fig = plt.figure(figsize=(19, 8))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)
extent = [1.0, 7.0, 0, 100]

### CPL Plot ###
ax1 = fig.add_subplot(gs[0])

ax1.imshow(cplJointRatio, origin="lower", aspect="auto", extent=extent,
          cmap=cmap, vmin=0.5, vmax=1.5)

ax1.set_xlabel(r"Age [Gyr]", fontsize=22)
ax1.set_ylabel("Orbital Period [d]", fontsize=22)
ax1.set_title("CPL")

### CTL Plot ###
ax2 = fig.add_subplot(gs[2])

im = ax2.imshow(ctlJointRatio, origin="lower", aspect="auto", extent=extent,
                cmap=cmap, vmin=0.5, vmax=1.5)

#ax2.axes.get_yaxis().set_visible(False)
ax2.set_xlabel(r"Age [Gyr]", fontsize=22)
ax2.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Median P$_{orb}$/P$_{rot}$", labelpad=30, rotation=270)

fig.savefig("../Plots/agePorbRatioHist.pdf", bbox_inches="tight", dpi=600)
# Done!
