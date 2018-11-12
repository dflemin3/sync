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
cpl = pd.read_csv("../Data/mcCPLTorqueNov9.csv")
ctl = pd.read_csv("../Data/mcCTLTorqueNov9.csv")

lurie = pd.read_csv("../Data/Lurie2017Full.csv", header=0)
lurie["Prot"] = lurie["p_acf"].copy()
lurie["Porb"] = lurie["p_orb"].copy()

# 1st Fig modeled after Fig. 6, upper panel from Lurie+2017

fig = plt.figure(figsize=(19, 8))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)

### CPL Plot ###

# Plot simulated data
ax0 = fig.add_subplot(gs[0])
im = ax0.scatter(cpl["Age_Porb"], cpl["Age_Porb"]/cpl["Pri_ProtAge"],
                 c=cpl["Age_Ecc"].values, cmap="viridis", zorder=1,
                 s=40, marker="o", vmin=0, vmax=0.3, label="Simulated")

if plotLurie:
    # Plot Lurie+2017 data
    ax0.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"], color="red", s=100, zorder=2,
                marker="+", vmin=0, vmax=0.3, label="Lurie et al. (2017)", alpha=0.7)

    # Plot Lurie+2017 detection limit of 45 d
    ax0.plot([1.0, 100.0], [1.0/45.0, 100.0/45.0], ls="-", lw="5", color="k", zorder=3)

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

if plotLurie:
    # Plot Lurie+2017 data
    ax1.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"], color="red", s=100, zorder=2,
               marker="+", vmin=0, vmax=0.3, label="Lurie et al. (2017)", alpha=0.7)

    # Plot Lurie+2017 detection limit of 45 d
    ax1.plot([1.0, 100.0], [1.0/45.0, 100.0/45.0], ls="-", lw="5", color="k", zorder=3)

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

fig.savefig("../Plots/lurieFig6.pdf", bbox_inches="tight", dpi=600)

### 2nd Fig modeled after Fig. 7 from Lurie+2017 ###

fig = plt.figure(figsize=(19, 8))
gs = GridSpec(1, 5, width_ratios=[1, 0.05, 1, 0.01, 0.075], wspace=0.05)

### CPL Plot ###

# Plot simulated data
ax0 = fig.add_subplot(gs[0])
im = ax0.scatter(cpl["Age_Porb"], cpl["Age_Porb"]/cpl["Pri_ProtAge"],
                 c=cpl["Age_Ecc"].values, cmap="viridis", zorder=1,
                 s=40, marker="o", vmin=0, vmax=0.3, label="Simulated")

ax0.axhline(1, lw=2, color="black", ls="-", zorder=2)

if plotLurie:
    # Plot Lurie+2017 data
    ax0.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"], color="red", s=100, zorder=3,
                marker="+", vmin=0, vmax=0.3, label="Lurie et al. (2017)", alpha=0.7)

    # Plot Lurie+2017 detection limit of 45 d
    ax0.plot([1.0, 100.0], [1.0/45.0, 100.0/45.0], ls="-", lw="5", color="k", zorder=3)

# Format
ax0.set_rasterization_zorder(0)
ax0.set_xlim(0,50)
ax0.set_ylim(0.0, 3)
ax0.set_xlabel("P$_{orb}$ [d]", fontsize=30)
ax0.set_ylabel("P$_{orb}$ / P$_{rot}$", fontsize=30)
ax0.set_title("CPL")
leg = ax0.legend(loc="lower right", framealpha=0.75, fontsize=18)
leg.legendHandles[0]._sizes = [50]
leg.legendHandles[0].set_color('k')
if plotLurie:
    leg.legendHandles[1]._sizes = [50]

### CTL Plots ###
# Plot simulated data
ax1 = fig.add_subplot(gs[2])
im = ax1.scatter(ctl["Age_Porb"], ctl["Age_Porb"]/ctl["Pri_ProtAge"],
                 c=ctl["Age_Ecc"].values, cmap="viridis", zorder=1,
                 s=40, marker="o", vmin=0, vmax=0.3, label="Simulated")

ax1.axhline(1, lw=2, color="black", ls="-", zorder=2)

if plotLurie:
    # Plot Lurie+2017 data
    ax1.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"], color="red", s=100, zorder=3,
               marker="+", vmin=0, vmax=0.3, label="Lurie et al. (2017)", alpha=0.7)

    # Plot Lurie+2017 detection limit of 45 d
    ax1.plot([1.0, 100.0], [1.0/45.0, 100.0/45.0], ls="-", lw="5", color="k", zorder=2)

# Format
ax1.set_rasterization_zorder(0)
ax1.set_xlim(0,50)
ax1.set_ylim(0.0, 3)
ax1.set_xlabel("P$_{orb}$ [d]", fontsize=30)
ax1.set_title("CTL")

### Colorbar ###
cbaxes = fig.add_subplot(gs[4])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Eccentricity")

fig.savefig("../Plots/lurieFig7.pdf", bbox_inches="tight", dpi=600)

# Done!
