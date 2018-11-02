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

#Typical plot parameters that make for pretty plots
mpl.rcParams['font.size'] = 20.0
cmap = "inferno_r"

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

# Load data
cpl = pd.read_csv("../Data/mcCPL.csv")
ctl = pd.read_csv("../Data/mcCTL.csv")

# Lock times < 0 -> Not locked, set them to 7e9 (last simulation output time)
cpl["Pri_LockTime"][cpl["Pri_LockTime"] < 0] = 7.0e9
cpl["Sec_LockTime"][cpl["Sec_LockTime"] < 0] = 7.0e9
ctl["Pri_LockTime"][ctl["Pri_LockTime"] < 0] = 7.0e9
ctl["Sec_LockTime"][ctl["Sec_LockTime"] < 0] = 7.0e9
cpl["Pri_dTidalQ"] = pd.Series(cpl["Pri_dTidaLQ"].values, index=cpl.index)

# Construct Porb, ecc bins based on assumed ranges
num = 11
porbBinEdges = np.linspace(0, 100, num)
qBinEdges = np.logspace(4, 8, num)
tauBinEdges = np.logspace(-3, 0, num)

# Array for joint locking time distribution
cplJoint = np.zeros((num-1, num-1))
ctlJoint = np.zeros_like(cplJoint)

# Array for joint Prot/Porb distribution
cplJointPeq = np.zeros_like(cplJoint)
ctlJointPeq = np.zeros_like(cplJoint)

# Loop over bins, compute median tidal locking time in joing Porb/ecc bins
for ii in range(num-1):
    for jj in range(num-1):
        cplMask = (cpl["Final_Porb"] > porbBinEdges[ii])
        cplMask = cplMask & (cpl["Final_Porb"] < porbBinEdges[ii + 1])
        cplMask = cplMask & (cpl["Pri_dTidalQ"] > qBinEdges[jj])
        cplMask = cplMask & (cpl["Pri_dTidalQ"] < qBinEdges[jj + 1])

        ctlMask = (ctl["Final_Porb"] > porbBinEdges[ii])
        ctlMask = ctlMask & (ctl["Final_Porb"] < porbBinEdges[ii + 1])
        ctlMask = ctlMask & (ctl["Pri_dTidalTau"] > tauBinEdges[jj])
        ctlMask = ctlMask & (ctl["Pri_dTidalTau"] < tauBinEdges[jj + 1])

        # Populate array elements
        cplJoint[ii, jj] = np.median(cpl["Pri_LockTime"][cplMask].values/1.0e9)
        ctlJoint[ii, jj] = np.median(ctl["Pri_LockTime"][ctlMask].values/1.0e9)

        cplJointPeq[ii, jj] = np.median(cpl["Pri_ProtFinal"][cplMask]/cpl["Final_Porb"][cplMask])
        ctlJointPeq[ii, jj] = np.median(ctl["Pri_ProtFinal"][ctlMask]/ctl["Final_Porb"][ctlMask])
# end loop

################################################################################
#
#   Joint Tidal Locking Times
#
################################################################################

fig = plt.figure(figsize=(19, 8))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)
qExtent = [4, 8, 0, 100]
tauExtent = [0, -3, 0, 100] # Reverse tau

### CPL Plot ###
ax1 = fig.add_subplot(gs[0])

ax1.imshow(cplJoint, origin="lower", aspect="auto", extent=qExtent,
          cmap=cmap, vmin=0.0, vmax=7.0)

ax1.set_xlabel(r"log$_{10}(Q)$", fontsize=22)
ax1.set_ylabel("Orbital Period [d]", fontsize=22)
ax1.set_title("CPL")

### CTL Plot ###
ax2 = fig.add_subplot(gs[2])

im = ax2.imshow(ctlJoint, origin="lower", aspect="auto", extent=tauExtent,
                  cmap=cmap, vmin=0.0, vmax=7.0)

#ax2.axes.get_yaxis().set_visible(False)
ax2.set_xlabel(r"log$_{10}(\tau \mathrm{[s]})$", fontsize=22)
ax2.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Median Tidal Locking Time [Gyr]", labelpad=30, rotation=270)

fig.savefig("../Plots/qTauPorbLockHist.pdf", bbox_inches="tight", dpi=600)
# Done!

################################################################################
#
#   Joint distribution of Prot/Porb
#
################################################################################

fig = plt.figure(figsize=(19, 8))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)

### CPL Plot ###
ax1 = fig.add_subplot(gs[0])

ax1.imshow(cplJointPeq, origin="lower", aspect="auto", extent=qExtent,
          cmap=cmap, vmin=0.6, vmax=1)

ax1.set_xlabel(r"log$_{10}(Q)$", fontsize=22)
ax1.set_ylabel("Orbital Period [d]", fontsize=22)
ax1.set_title("CPL")

### CTL Plot ###
ax2 = fig.add_subplot(gs[2])

im = ax2.imshow(ctlJointPeq, origin="lower", aspect="auto", extent=tauExtent,
                cmap=cmap, vmin=0.6, vmax=1)

#ax2.axes.get_yaxis().set_visible(False)
ax2.set_xlabel(r"log$_{10}(\tau \mathrm{[s]})$", fontsize=22)
ax2.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Median P$_{rot}$/P$_{orb}$", labelpad=30, rotation=270)

fig.savefig("../Plots/qTauPorbRatioHist.pdf", bbox_inches="tight", dpi=600)
# Done!
