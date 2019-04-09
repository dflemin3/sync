"""

@author: David P Fleming, University of Washington, April 2019
@email dflemin3 (at) uw (dot) edu

Determine the age error introduced by assuming that tidally-interacting and
tidally-locked binaries follow the same angular momentum evolution as single
stars, i.e. by applying gyrochronology to binaries.

"""

import numpy as np
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from cmap import MidpointNormalize
from matplotlib.gridspec import GridSpec

#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (9,8)
mpl.rcParams['font.size'] = 20.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

# Plot constants
num = 16 # 1 more than the number of bins
cmap = mpl.cm.RdBu
cmap.set_bad('white')
vmin = -300
vmax = 25
norm = MidpointNormalize(vmin=vmin, vmax=vmax, midpoint=0)

# Load in data
cpl = pd.read_csv("../Data/mcCPLMarch27.csv")
ctl = pd.read_csv("../Data/mcCTLMarch27.csv")
single = pd.read_csv("../Data/mcSingleMarch27.csv")

# Lock times < 0 -> Not locked, set them to 7e9 (last simulation output time)
cpl["Pri_LockTime"][cpl["Pri_LockTime"] < 0] = 7.0e9
cpl["Sec_LockTime"][cpl["Sec_LockTime"] < 0] = 7.0e9
ctl["Pri_LockTime"][ctl["Pri_LockTime"] < 0] = 7.0e9
ctl["Sec_LockTime"][ctl["Sec_LockTime"] < 0] = 7.0e9

# Make flag for binaries who are locked by the age of the system
cpl["Locked"] = pd.Series(cpl["Pri_LockTime"] < cpl["Age"], index=cpl.index)
ctl["Locked"] = pd.Series(ctl["Pri_LockTime"] < ctl["Age"], index=ctl.index)

# Make flag for binaries that are strongly tidally-influence, that is, stars with
# Prot/Peq within [0.9, 1.1] and/or tidally-locked
mask = ((np.fabs(1.0 - (cpl["Pri_ProtAge"]/cpl["Age_Peq"])) <= 0.1).values) | (cpl["Locked"].values)
cpl["Tides"] = pd.Series(mask, index=cpl.index)
mask = ((np.fabs(1.0 - (ctl["Pri_ProtAge"]/ctl["Age_Peq"])) <= 0.1).values) | (ctl["Locked"].values)
ctl["Tides"] = pd.Series(mask, index=ctl.index)

# Construct prot, mass bins based on assumed ranges
protBinEdges = np.linspace(0, 70, num)
massBinEdges = np.linspace(0.1, 1.0, num)

# Array for joint locking time distribution
cplErr = np.zeros((num-1, num-1)) * np.nan
ctlErr = np.zeros((num-1, num-1)) * np.nan

for ii in range(num-1):
    for jj in range(num-1):
        # Isolate bins for CPL, CTL, and single star simulations
        cplMask = (cpl["Pri_ProtAge"][cpl["Tides"]] > protBinEdges[ii])
        cplMask = cplMask & (cpl["Pri_ProtAge"][cpl["Tides"]] < protBinEdges[ii + 1])
        cplMask = cplMask & (cpl["Pri_dMass"][cpl["Tides"]] > massBinEdges[jj])
        cplMask = cplMask & (cpl["Pri_dMass"][cpl["Tides"]] < massBinEdges[jj + 1])

        ctlMask = (ctl["Pri_ProtAge"][ctl["Tides"]] > protBinEdges[ii])
        ctlMask = ctlMask & (ctl["Pri_ProtAge"][ctl["Tides"]] < protBinEdges[ii + 1])
        ctlMask = ctlMask & (ctl["Pri_dMass"][ctl["Tides"]] > massBinEdges[jj])
        ctlMask = ctlMask & (ctl["Pri_dMass"][ctl["Tides"]] < massBinEdges[jj + 1])

        singleMask = (single["Pri_ProtAge"] > protBinEdges[ii])
        singleMask = singleMask & (single["Pri_ProtAge"] < protBinEdges[ii + 1])
        singleMask = singleMask & (single["Pri_dMass"] > massBinEdges[jj])
        singleMask = singleMask & (single["Pri_dMass"] < massBinEdges[jj + 1])

        # Populate it if there's samples, default to NaN otherwise
        if np.sum(cplMask) > 0 and np.sum(singleMask) > 0:
            cplErr[ii, jj] = 100*(np.mean(single["Age"][singleMask]) - np.mean(cpl["Age"][cpl["Tides"]][cplMask]))/np.mean(single["Age"][singleMask])
        if np.sum(ctlMask) > 0 and np.sum(singleMask) > 0:
            ctlErr[ii, jj] = 100*(np.mean(single["Age"][singleMask]) - np.mean(ctl["Age"][ctl["Tides"]][ctlMask]))/np.mean(single["Age"][singleMask])

### Plot! ###

fig = plt.figure(figsize=(13, 6))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)
extent = [0.1, 1, 0, 70]

### CPL ###

ax0 = fig.add_subplot(gs[0])
im = ax0.imshow(cplErr, origin="lower", aspect="auto", extent=extent,
                interpolation='nearest', cmap=cmap, vmin=vmin, vmax=vmax,
                norm=norm)

# Annotate where there are no single stars
ax0.text(0.82, 4, "No Single Stars", ha="center", va="center", size=17,
         color="k")
ax0.text(0.85, 60, "No Single \n Stars", ha="center", va="center", size=17,
         color="k")

# Format plot
ax0.set_xlabel(r"Mass [M$_{\odot}$]", fontsize=22)
ax0.set_xlim(0.1, 1)
ax0.set_ylabel("Rotation Period [d]", fontsize=22)
ax0.set_ylim(0, 70)
ax0.set_title("CPL", fontsize=22)

### CTL ###

ax1 = fig.add_subplot(gs[2])
im = ax1.imshow(ctlErr, origin="lower", aspect="auto", extent=extent,
                interpolation='nearest', cmap=cmap, vmin=vmin, vmax=vmax,
                norm=norm)

# Annotate where there are no single stars
ax1.text(0.82, 4, "No Single Stars", ha="center", va="center", size=17,
         color="k")
ax1.text(0.85, 60, "No Single \n Stars", ha="center", va="center", size=17,
         color="k")

# Format plot
ax1.set_xlabel(r"Mass [M$_{\odot}$]", fontsize=22)
ax1.set_xlim(0.1, 1)
ax1.set_ylim(0, 70)

# Colorbar
cbax = fig.add_subplot(gs[4])
cb = fig.colorbar(im, ticks=[-300, -250, -200, -150, -100, -50, 0, 25], cax=cbax)
cb.ax.set_yticklabels(["-300", "-250", "-200", "-150", "-100", "-50", "0", "25"])
cb.set_label(label="Relative Age Error [\%]", fontsize=20)
ax1.set_title("CTL", fontsize=22)

# Save!
fig.savefig("../Plots/gyro.pdf", bbox_inches="tight", dpi=200)
