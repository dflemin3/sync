"""

@author: David P. Fleming, University of Washington, Nov 2018
@email: dflemin3 (at) uw (dot) edu

Joint distribution of median tidal locking (for the secondary!) time over binary
mass ratio and Porb where the mass ratio = massSecondary/massPrimary

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

# Lock times < 0 -> Not locked, set them to 7e9 (last simulation output time)
cpl["Pri_LockTime"][cpl["Pri_LockTime"] < 0] = 7.0e9
cpl["Sec_LockTime"][cpl["Sec_LockTime"] < 0] = 7.0e9
ctl["Pri_LockTime"][ctl["Pri_LockTime"] < 0] = 7.0e9
ctl["Sec_LockTime"][ctl["Sec_LockTime"] < 0] = 7.0e9

# Define mass ratio
cpl["MassRatio"] = pd.Series(cpl["Sec_dMass"].values/cpl["Pri_dMass"].values, index=cpl.index)
ctl["MassRatio"] = pd.Series(ctl["Sec_dMass"].values/ctl["Pri_dMass"].values, index=ctl.index)

# Construct Porb, mass ratio bins based on assumed ranges
num = 11
porbBinEdges = np.linspace(0, 100, num)
ratioBinEdges = np.linspace(0.1, 1.0, num)

# Array for joint locking time distribution
cplJointPeq = np.zeros((num-1, num-1))
ctlJointPeq = np.zeros_like(cplJointPeq)

# Array for joint Prot/Porb distribution
cplJointRatio = np.zeros_like(cplJointPeq)
ctlJointRatio = np.zeros_like(cplJointPeq)

# Loop over bins, compute median tidal locking time in joing Porb/mu bins
for ii in range(num-1):
    for jj in range(num-1):
        cplMask = (cpl["Final_Porb"] > porbBinEdges[ii])
        cplMask = cplMask & (cpl["Final_Porb"] < porbBinEdges[ii + 1])
        cplMask = cplMask & (cpl["MassRatio"] > ratioBinEdges[jj])
        cplMask = cplMask & (cpl["MassRatio"] < ratioBinEdges[jj + 1])

        ctlMask = (ctl["Final_Porb"] > porbBinEdges[ii])
        ctlMask = ctlMask & (ctl["Final_Porb"] < porbBinEdges[ii + 1])
        ctlMask = ctlMask & (ctl["MassRatio"] > ratioBinEdges[jj])
        ctlMask = ctlMask & (ctl["MassRatio"] < ratioBinEdges[jj + 1])

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
extent = [0.1, 1.0, 0, 100]

### CPL Plot ###
ax1 = fig.add_subplot(gs[0])

ax1.imshow(cplJointPeq, origin="lower", aspect="auto", extent=extent,
          cmap=cmap, vmin=0.5, vmax=1.5)

ax1.set_xlabel("Mass Ratio", fontsize=22)
ax1.set_ylabel("Orbital Period [d]", fontsize=22)
ax1.set_title("CPL")

### CTL Plot ###
ax2 = fig.add_subplot(gs[2])

im = ax2.imshow(ctlJointPeq, origin="lower", aspect="auto", extent=extent,
                  cmap=cmap, vmin=0.5, vmax=1.5)

ax2.set_xlabel("Mass Ratio", fontsize=22)
ax2.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Median P$_{eq}$/P$_{rot}$", labelpad=30, rotation=270)

fig.savefig("../Plots/ratioPorbPeq.pdf", bbox_inches="tight", dpi=600)
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

ax1.imshow(cplJointRatio, origin="lower", aspect="auto", extent=extent,
          cmap=cmap, vmin=0.5, vmax=1.5)

ax1.set_xlabel("Mass Ratio", fontsize=22)
ax1.set_ylabel("Orbital Period [d]", fontsize=22)
ax1.set_title("CPL")

### CTL Plot ###
ax2 = fig.add_subplot(gs[2])

im = ax2.imshow(ctlJointRatio, origin="lower", aspect="auto", extent=extent,
                cmap=cmap, vmin=0.5, vmax=1.5)

ax2.set_xlabel("Mass Ratio", fontsize=22)
ax2.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Median P$_{orb}$/P$_{rot}$", labelpad=30, rotation=270)

fig.savefig("../Plots/ratioPorbRatioHist.pdf", bbox_inches="tight", dpi=600)
# Done!
