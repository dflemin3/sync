"""

@author: David P. Fleming, University of Washington, Nov 2018
@email: dflemin3 (at) uw (dot) edu

Prot distributions as a function of stellar mass and age for the CPL, CTL, and
single star models uniform over ages [1,7] Gyr, roughly field star ages.

"""

import numpy as np
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (9,8)
mpl.rcParams['font.size'] = 25.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

# Constants
cmap = "viridis"
bins = "auto"
seed = 42
num = 2500

# Set RNG Seed
np.random.seed(seed)

# Load data
cpl = pd.read_csv("../Data/mcCPLDec22.csv")
ctl = pd.read_csv("../Data/mcCTLDec22.csv")
single = pd.read_csv("../Data/mcSingle.csv")
lurie = pd.read_csv("../Data/Lurie2017.csv", comment="#", header=None,
                    names=["Porb", "Prot", "Ecc"])

### Age histogram of rapid rotators (Prot <= 20 d) ###
fig, ax = plt.subplots()

ax.hist(cpl["Age"][cpl["Pri_ProtAge"] <= 20]/1.0e9, bins="auto",
        histtype="step", lw=3, label="Binary, CPL", color="C0", density=False)
ax.hist(ctl["Age"][ctl["Pri_ProtAge"] <= 20]/1.0e9, bins="auto",
        histtype="step", lw=3, label="Binary, CTL", color="C1", density=False)
ax.hist(single["Age"][single["Pri_ProtAge"] <= 20]/1.0e9, bins="auto",
        histtype="step", lw=3, label="Single", color="C2", density=False)

# Annotate young stars
ax.annotate(s="", xy=(2.5, 430), xytext=(0.8, 430),
            arrowprops={"arrowstyle" : "<->", "color" : "black"})
ax.text(1.65, 460, "Young \n Rapid Rotators", ha="center", va="center", size=21, color="k")

# Annotate locked population
ax.annotate(s="", xy=(7, 180), xytext=(2.75, 180),
            arrowprops={"arrowstyle" : "<->", "color" : "black"})
ax.text(4.85, 200, "Tidally-Locked Binaries", ha="center", va="center", size=21,
        color="k")

ax.set_xlabel("Age [Gyr]", fontsize=30)
ax.set_ylabel("Counts", fontsize=30)
ax.set_xlim(0.8,7.2)
ax.set_ylim(0, 490)
ax.legend(loc="best", framealpha=0.0, fontsize=22)

fig.savefig("../Plots/protAgeHist.pdf", dpi=200, bbox_inches="tight")

### Age histogram of rapid rotators (Prot <= 20 d) highlighting single stars ###
fig, ax = plt.subplots()

ax.hist(cpl["Age"][cpl["Pri_ProtAge"] <= 20]/1.0e9, bins="auto",
        histtype="step", lw=3, label="Binary, CPL", color="C0")
ax.hist(ctl["Age"][ctl["Pri_ProtAge"] <= 20]/1.0e9, bins="auto",
        histtype="step", lw=3, label="Binary, CTL", color="C1")
ax.hist(single["Age"][single["Pri_ProtAge"] <= 20]/1.0e9, bins="auto",
        lw=3, label="Single", color="C2", zorder=10)

ax.set_xlabel("Age [Gyr]", fontsize=30)
ax.set_ylabel("Counts", fontsize=30)
ax.set_title("Age distribution for stars with P$_{rot} < 20$ d", fontsize=30)
ax.set_xlim(0.8,7.2)
ax.legend(loc="best", framealpha=0.0)

fig.savefig("../Plots/protAgeHistSingle.png", dpi=200, bbox_inches="tight")

### Age histogram of rapid rotators (Prot <= 20 d) highlighting binary stars ###
fig, ax = plt.subplots()

ax.hist(cpl["Age"][cpl["Pri_ProtAge"] <= 20]/1.0e9, bins="auto",
        zorder=8, lw=3, label="Binary, CPL", color="C0", alpha=0.75)
ax.hist(ctl["Age"][ctl["Pri_ProtAge"] <= 20]/1.0e9, bins="auto",
        zorder=9, lw=3, label="Binary, CTL", color="C1", alpha=0.75)
ax.hist(single["Age"][single["Pri_ProtAge"] <= 20]/1.0e9, bins="auto",
        histtype="step", lw=3, label="Single", color="C2", zorder=10)

ax.set_xlabel("Age [Gyr]", fontsize=30)
ax.set_ylabel("Counts", fontsize=30)
ax.set_title("Age distribution for stars with P$_{rot} < 20$ d", fontsize=30)
ax.set_xlim(0.8,7.2)
ax.legend(loc="best", framealpha=0.0)

fig.savefig("../Plots/protAgeHistBinary.png", dpi=200, bbox_inches="tight")

### Single, Binary Plots ###

# Create indices for a random sample of num points to make scatterplot legible
inds = np.random.choice(np.arange(len(cpl)), size=num, replace=False)

# Binary
fig , ax = plt.subplots()

cax = ax.scatter(ctl.iloc[inds]["Pri_dMass"], ctl.iloc[inds]["Pri_ProtAge"], s=50,
                 c=ctl.iloc[inds]["Age"].values/1.0e9, vmin=1, vmax=7, cmap=cmap)
ax.set_rasterization_zorder(0)
ax.set_ylabel("Rotation Period [d]", fontsize=30)
ax.set_xlabel("Mass [M$_{\odot}$]", fontsize=30)
ax.set_title("Binary Star Only", fontsize=30)
ax.set_xlim(0.1, 1)
ax.set_ylim(0.0, 85)

cbar = fig.colorbar(cax)
cbar.set_label("Age [Gyr]", fontsize=30, labelpad=20)

fig.savefig("../Plots/ProtDistPresentationBinary.png", dpi=200, bbox_inches="tight")

# Single
fig , ax = plt.subplots()

cax = ax.scatter(single.iloc[inds]["Pri_dMass"], single.iloc[inds]["Pri_ProtAge"], s=50,
                 c=single.iloc[inds]["Age"].values/1.0e9, vmin=1, vmax=7, cmap=cmap)
ax.set_rasterization_zorder(0)
ax.set_ylabel("Rotation Period [d]", fontsize=30)
ax.set_xlabel("Mass [M$_{\odot}$]", fontsize=30)
ax.set_title("Single Star Only", fontsize=30)
ax.set_xlim(0.1, 1)
ax.set_ylim(0.0, 85)

cbar = fig.colorbar(cax)
cbar.set_label("Age [Gyr]", fontsize=30, labelpad=20)

fig.savefig("../Plots/ProtDistPresentationSingle.png", dpi=200, bbox_inches="tight")

# Done!
