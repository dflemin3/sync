"""

@author: David P. Fleming, University of Washington, Nov 2018
@email: dflemin3 (at) uw (dot) edu

Joint distribution of median tidal locking time over stellar tidal Q/tau and Porb.

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
midpoint = 1 - 1.2614218627451428 / (1.2614218627451428 + 0.2518443643281677)
cmap = shiftedColorMap(mpl.cm.RdBu, midpoint=midpoint)

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

# Load data
cpl = pd.read_csv("../Data/mcCPLTorqueNov9.csv")
ctl = pd.read_csv("../Data/mcCTLTorqueNov9.csv")

# Lock times < 0 -> Not locked, set them to 7e9 (last simulation output time)
cpl["Pri_LockTime"][cpl["Pri_LockTime"] < 0] = 7.0e9
cpl["Sec_LockTime"][cpl["Sec_LockTime"] < 0] = 7.0e9
ctl["Pri_LockTime"][ctl["Pri_LockTime"] < 0] = 7.0e9
ctl["Sec_LockTime"][ctl["Sec_LockTime"] < 0] = 7.0e9
cpl["Pri_dTidalQ"] = pd.Series(cpl["Pri_dTidaLQ"].values, index=cpl.index)

# Construct Porb, ecc bins based on assumed ranges
num = 11
porbBinEdges = np.linspace(0, 100, num)
qBinEdges = np.logspace(4, 7, num)
tauBinEdges = np.logspace(-2, 0, num)[::-1]

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
        cplMask = cplMask & (cpl["Pri_dTidalQ"] > qBinEdges[jj])
        cplMask = cplMask & (cpl["Pri_dTidalQ"] < qBinEdges[jj + 1])

        ctlMask = (ctl["Age_Porb"] > porbBinEdges[ii])
        ctlMask = ctlMask & (ctl["Age_Porb"] < porbBinEdges[ii + 1])
        ctlMask = ctlMask & (ctl["Pri_dTidalTau"] < tauBinEdges[jj])
        ctlMask = ctlMask & (ctl["Pri_dTidalTau"] > tauBinEdges[jj + 1])

        # Populate array elements ctl["Pri_ProtAge"][ctlMask]
        cplJointPeq[ii, jj] = np.median(cpl["Age_Peq"][cplMask]/cpl["Pri_ProtAge"][cplMask])
        ctlJointPeq[ii, jj] = np.median(ctl["Age_Peq"][ctlMask]/ctl["Pri_ProtAge"][ctlMask])

        cplJointRatio[ii, jj] = np.median(cpl["Age_Porb"][cplMask]/cpl["Pri_ProtAge"][cplMask])
        ctlJointRatio[ii, jj] = np.median(ctl["Age_Porb"][ctlMask]/ctl["Pri_ProtAge"][ctlMask])

# end loop

################################################################################
#
#   Peq/Prot joint histogram
#
################################################################################

fig = plt.figure(figsize=(19, 8))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)
qExtent = [4, 7, 0, 100]
tauExtent = [0, -2, 0, 100] # Reverse tau

### CPL Plot ###
ax1 = fig.add_subplot(gs[0])

ax1.imshow(cplJointPeq, origin="lower", aspect="auto", extent=qExtent,
          cmap=cmap)

ax1.set_xlabel(r"log$_{10}(Q)$", fontsize=30)
ax1.set_ylabel("Orbital Period [d]", fontsize=30)
ax1.set_title("CPL")

### CTL Plot ###
ax2 = fig.add_subplot(gs[2])

im = ax2.imshow(ctlJointPeq, origin="lower", aspect="auto", extent=tauExtent,
                  cmap=cmap)

#ax2.axes.get_yaxis().set_visible(False)
ax2.set_xlabel(r"log$_{10}(\tau \mathrm{[s]})$", fontsize=22)
ax2.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Median P$_{eq}$/P$_{rot}$", labelpad=30, rotation=270)

fig.savefig("../Plots/qTauPorbPeqAge.pdf", bbox_inches="tight", dpi=600)
# Done!

################################################################################
#
#   Joint distribution of Porb/Prot
#
################################################################################

fig = plt.figure(figsize=(19, 8))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)

### CPL Plot ###
ax1 = fig.add_subplot(gs[0])

ax1.imshow(cplJointRatio, origin="lower", aspect="auto", extent=qExtent,
          cmap="RdBu", vmin=0.5, vmax=1.5)

ax1.set_xlabel(r"log$_{10}(Q)$", fontsize=30)
ax1.set_ylabel("Orbital Period [d]", fontsize=30)
ax1.set_title("CPL")

### CTL Plot ###
ax2 = fig.add_subplot(gs[2])

im = ax2.imshow(ctlJointRatio, origin="lower", aspect="auto", extent=tauExtent,
                cmap="RdBu", vmin=0.5, vmax=1.5)

#ax2.axes.get_yaxis().set_visible(False)
ax2.set_xlabel(r"log$_{10}(\tau \mathrm{[s]})$", fontsize=30)
ax2.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Median P$_{orb}$/P$_{rot}$", labelpad=30, rotation=270, fontsize=25)

fig.savefig("../Plots/qTauPorbRatioHistAge.pdf", bbox_inches="tight", dpi=600)
# Done!
