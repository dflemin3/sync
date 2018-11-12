"""

@author: David P. Fleming, University of Washington, Nov 2018
@email: dflemin3 (at) uw (dot) edu

Joint distribution of median tidal locking time over binary ecc and Porb.

"""

import numpy as np
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

#Typical plot parameters that make for pretty plots
mpl.rcParams['font.size'] = 20.0
cmap = "RdBu"

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

# Load data
cpl = pd.read_csv("../Data/mcCPLTorque.csv")
ctl = pd.read_csv("../Data/mcCTLTorque.csv")

# Construct Porb, ecc bins based on assumed ranges
num = 11
porbBinEdges = np.linspace(0, 100, num)
eccBinEdges = np.linspace(0, 0.3, num)

# Array for joint locking time distribution
cplJointPeq = np.zeros((num-1, num-1))
ctlJointPeq = np.zeros_like(cplJointPeq)

# Array for joint Prot/Porb distribution
cplJointRatio = np.zeros_like(cplJointPeq)
ctlJointRatio = np.zeros_like(cplJointPeq)

# Loop over bins, compute median tidal locking time in joing Porb/ecc bins
for ii in range(num-1):
    for jj in range(num-1):
        cplMask = (cpl["Final_Porb"] > porbBinEdges[ii])
        cplMask = cplMask & (cpl["Final_Porb"] < porbBinEdges[ii + 1])
        cplMask = cplMask & (cpl["Final_Ecc"] > eccBinEdges[jj])
        cplMask = cplMask & (cpl["Final_Ecc"] < eccBinEdges[jj + 1])

        ctlMask = (ctl["Final_Porb"] > porbBinEdges[ii])
        ctlMask = ctlMask & (ctl["Final_Porb"] < porbBinEdges[ii + 1])
        ctlMask = ctlMask & (ctl["Final_Ecc"] > eccBinEdges[jj])
        ctlMask = ctlMask & (ctl["Final_Ecc"] < eccBinEdges[jj + 1])

        # Populate array elements ctl["Pri_ProtFinal"][ctlMask]
        cplJointPeq[ii, jj] = np.median(cpl["Final_Peq"][cplMask]/cpl["Pri_ProtFinal"][cplMask])
        ctlJointPeq[ii, jj] = np.median(ctl["Final_Peq"][ctlMask]/ctl["Pri_ProtFinal"][ctlMask])

        cplJointRatio[ii, jj] = np.median(cpl["Final_Porb"][cplMask]/cpl["Pri_ProtFinal"][cplMask])
        ctlJointRatio[ii, jj] = np.median(ctl["Final_Porb"][ctlMask]/ctl["Pri_ProtFinal"][ctlMask])
# end loop

################################################################################
#
#   Joint Tidal Locking Times
#
################################################################################

fig = plt.figure(figsize=(19, 8))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)
extent = [0, 0.3, 0, 100]

### CPL Plot ###
ax1 = fig.add_subplot(gs[0])

ax1.imshow(cplJointPeq, origin="lower", aspect="auto", extent=extent,
          cmap=cmap, vmin=0.5, vmax=1.5)

ax1.set_xlabel("Eccentricity", fontsize=22)
ax1.set_ylabel("Orbital Period [d]", fontsize=22)
ax1.set_title("CPL")

### CTL Plot ###
ax2 = fig.add_subplot(gs[2])

im = ax2.imshow(ctlJointPeq, origin="lower", aspect="auto", extent=extent,
                  cmap=cmap, vmin=0.5, vmax=1.5)

#ax2.axes.get_yaxis().set_visible(False)
ax2.set_xlabel("Eccentricity", fontsize=22)
ax2.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Median P$_{eq}$/P$_{rot}$", labelpad=30, rotation=270)

fig.savefig("../Plots/eccPorbPeq.pdf", bbox_inches="tight", dpi=600)
# Done!

################################################################################
#
#   Joint distribution of Prot/Porb
#
################################################################################

fig = plt.figure(figsize=(19, 8))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)
extent = [0, 0.3, 0, 100]

### CPL Plot ###
ax1 = fig.add_subplot(gs[0])

ax1.imshow(cplJointRatio, origin="lower", aspect="auto", extent=extent,
          cmap=cmap, vmin=0.5, vmax=1.5)

ax1.set_xlabel("Eccentricity", fontsize=22)
ax1.set_ylabel("Orbital Period [d]", fontsize=22)
ax1.set_title("CPL")

### CTL Plot ###
ax2 = fig.add_subplot(gs[2])

im = ax2.imshow(ctlJointRatio, origin="lower", aspect="auto", extent=extent,
                cmap=cmap, vmin=0.5, vmax=1.5)

#ax2.axes.get_yaxis().set_visible(False)
ax2.set_xlabel("Eccentricity", fontsize=22)
ax2.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Mean P$_{orb}$/P$_{rot}$", labelpad=30, rotation=270)

fig.savefig("../Plots/eccPorbRatioHist.pdf", bbox_inches="tight", dpi=600)
# Done!
