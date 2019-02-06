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
mpl.rcParams['font.size'] = 22.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

plotLurie = True

# Load data
cpl = pd.read_csv("../Data/mcCPLDec22.csv")
ctl = pd.read_csv("../Data/mcCTLDec22.csv")

#lurie = pd.read_csv("../Data/Lurie2017Full.csv", header=0)
#lurie["Prot"] = lurie["p_1_min"].copy() # As recommended by Lurie+2017 for equitorial Prot
#lurie["Porb"] = lurie["p_orb"].copy()

# Load in cleaned sample of Prot and Ecc from Lurie+2017
lurie = pd.read_csv("../Data/Lurie2017.csv", comment="#", header=None,
                    names=["Porb", "Prot", "Ecc"])

# 1st Fig modeled after Fig. 6, upper panel from Lurie+2017

fig = plt.figure(figsize=(19, 8))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)

### CPL Plot ###

# Plot simulated data
ax0 = fig.add_subplot(gs[0])
im = ax0.scatter(cpl["Age_Porb"], cpl["Age_Porb"]/cpl["Pri_ProtAge"],
                 c=cpl["Age_Ecc"].values, cmap="viridis", zorder=1,
                 s=40, marker="o", vmin=0, vmax=0.3, label="Simulated")

ax0.axhline(1, lw=3, color="black", ls="--", zorder=100)

if plotLurie:
    # Plot Lurie+2017 data
    ax0.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"], color="red", s=100, zorder=2,
                marker="+", vmin=0, vmax=0.3, label="Lurie et al. (2017)")

# Format
ax0.set_rasterization_zorder(0)
ax0.set_xlim(1,100)
ax0.set_ylim(0.9, 30)
ax0.set_xscale("log")
ax0.set_yscale("log")
ax0.set_xlabel("P$_{orb}$ [d]", fontsize=30)
ax0.set_ylabel("P$_{orb}$ / P$_{rot}$", fontsize=30)
ax0.set_title("CPL")
leg = ax0.legend(loc="upper left", framealpha=0.75, fontsize=25)
leg.legendHandles[0]._sizes = [100]
leg.legendHandles[0].set_color('k')
if plotLurie:
    leg.legendHandles[1]._sizes = [100]

### CTL Plots ###
# Plot simulated data
ax1 = fig.add_subplot(gs[2])
im = ax1.scatter(ctl["Age_Porb"], ctl["Age_Porb"]/ctl["Pri_ProtAge"],
                 c=ctl["Age_Ecc"].values, cmap="viridis", zorder=1,
                 s=40, marker="o", vmin=0, vmax=0.3, label="Simulated")

ax1.axhline(1, lw=3, color="black", ls="--", zorder=100)

if plotLurie:
    # Plot Lurie+2017 data
    ax1.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"], color="red", s=100, zorder=2,
               marker="+", vmin=0, vmax=0.3, label="Lurie et al. (2017)")

# Format
ax1.set_rasterization_zorder(0)
ax1.set_xlim(1,100)
ax1.set_ylim(0.9, 30)
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlabel("P$_{orb}$ [d]", fontsize=30)
ax1.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Eccentricity")

fig.savefig("../Plots/lurieFig6.pdf", bbox_inches="tight", dpi=200)

### 2nd Fig modeled after Fig. 7 from Lurie+2017 ###

fig = plt.figure(figsize=(24, 7))
gs = GridSpec(1, 7, width_ratios=[1, 0.05, 1, 0.05, 1, 0.01, 0.075], wspace=0.05)

### CPL Plot ###

# Plot simulated data
ax0 = fig.add_subplot(gs[0])
im = ax0.scatter(cpl["Age_Porb"], cpl["Age_Porb"]/cpl["Pri_ProtAge"],
                 c=cpl["Age_Ecc"].values, cmap="viridis", zorder=3,
                 s=40, marker="o", vmin=0, vmax=0.3)
ax0.axhline(1, lw=3, color="black", ls="--", zorder=100)

# Format
ax0.set_rasterization_zorder(0)
ax0.set_xlim(0, 25)
ax0.set_ylim(0.25, 1.8)
ax0.set_xlabel("P$_{orb}$ [d]", fontsize=30)
ax0.set_ylabel("P$_{orb}$ / P$_{rot}$", fontsize=30)
ax0.set_title("CPL")

### CTL Plots ###
# Plot simulated data
ax1 = fig.add_subplot(gs[2])
im = ax1.scatter(ctl["Age_Porb"], ctl["Age_Porb"]/ctl["Pri_ProtAge"],
                 c=ctl["Age_Ecc"].values, cmap="viridis", zorder=3,
                 s=40, marker="o", vmin=0, vmax=0.3)
ax1.axhline(1, lw=3, color="black", ls="--", zorder=100)

# Format
ax1.set_rasterization_zorder(0)
ax1.set_xlim(0, 25)
ax1.set_ylim(0.25, 1.8)
ax1.set_xlabel("P$_{orb}$ [d]", fontsize=30)
ax1.set_title("CTL")

### Lurie+2017 Plots ###
# Plot simulated data
ax2 = fig.add_subplot(gs[4])
im = ax2.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"],
                 c=lurie["Ecc"].values, cmap="viridis", zorder=3,
                 s=40, marker="o", vmin=0, vmax=0.3)
ax2.axhline(1, lw=3, color="black", ls="--", zorder=100)

# Format
ax2.set_rasterization_zorder(0)
ax2.set_xlim(0, 25)
ax2.set_ylim(0.25, 1.8)
ax2.set_xlabel("P$_{orb}$ [d]", fontsize=30)
ax2.set_title("Lurie et al. (2017)")

### Colorbar ###
cbaxes = fig.add_subplot(gs[-1])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Eccentricity")

fig.savefig("../Plots/lurieFig7.pdf", bbox_inches="tight", dpi=200)

# Done!
