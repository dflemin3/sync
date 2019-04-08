"""

@author: David P. Fleming, University of Washington, Nov 2018
@email: dflemin3 (at) uw (dot) edu

Prot distributions as a function of stellar mass and Porb for the CPL, CTL, and
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
cpl = pd.read_csv("../Data/mcCPLMarch27.csv")
ctl = pd.read_csv("../Data/mcCTLMarch27.csv")
single = pd.read_csv("../Data/mcSingleMarch27.csv")

# Create indices for a random sample of num points to make scatterplot legible
inds = np.random.choice(np.arange(len(cpl)), size=num, replace=False)

# Plot!
fig = plt.figure(figsize=(30, 10))
gs = GridSpec(3, 7,
              height_ratios=[0.05, 0.015, 1],
              width_ratios=[1, 0.001, 1, 0.001, 1, 0.001, 0.25],
              wspace=0.1)

### CPL Plot ###
ax0 = fig.add_subplot(gs[14])

im = ax0.scatter(cpl.iloc[inds]["Pri_dMass"], cpl.iloc[inds]["Pri_ProtAge"], s=50,
                 c=cpl.iloc[inds]["Age_Porb"].values, vmin=0, vmax=100, cmap=cmap)
ax0.set_rasterization_zorder(0)
ax0.set_xlabel("Mass [M$_{\odot}$]", fontsize=30)
ax0.set_ylabel("Rotation Period [d]", fontsize=30)
ax0.set_xlim(0.1, 1)
ax0.set_ylim(0.0, 100)
ax0.text(0.15, 90, "CPL", ha="left", va="center", size=30, color="black",
         zorder=100)

ax0.text(0.13, 112, "Matt et al. (2015)", ha="left", va="center", size=30,
         color="black", zorder=100)

### CTL Plot ###
ax1 = fig.add_subplot(gs[16])

ax1.scatter(ctl.iloc[inds]["Pri_dMass"], ctl.iloc[inds]["Pri_ProtAge"], s=50,
            c=ctl.iloc[inds]["Age_Porb"].values, vmin=0, vmax=100, cmap=cmap)
ax1.set_rasterization_zorder(0)
ax1.set_xlabel("Mass [M$_{\odot}$]", fontsize=30)
ax1.set_xlim(0.1, 1)
ax1.set_ylim(0.0, 100)
ax1.text(0.15, 90, "CTL", ha="left", va="center", size=30, color="black",
         zorder=100)

### Single Plot ###
ax2 = fig.add_subplot(gs[18])

ax2.scatter(single.iloc[inds]["Pri_dMass"], single.iloc[inds]["Pri_ProtAge"], s=50,
            color="k")
ax2.set_rasterization_zorder(0)
ax2.set_xlabel("Mass [M$_{\odot}$]", fontsize=30)
ax2.set_xlim(0.1, 1)
ax2.set_ylim(0.0, 100)
ax2.text(0.15, 90, "Single Star", ha="left", va="center", size=30, color="black",
         zorder=100)

### Colorbar for scatter plots ###
cbaxes = fig.add_subplot(gs[2])
cb = plt.colorbar(im, cax=cbaxes, orientation="horizontal")
cb.set_label(label="Age [Gyr]")

### Marginal Prot Hist ###
ax3 = fig.add_subplot(gs[20])

ax3.hist(cpl["Pri_ProtAge"], orientation="horizontal", bins=bins,
         histtype="step", lw=3, color="C0", label="CPL", density=True)
ax3.hist(ctl["Pri_ProtAge"], orientation="horizontal", bins=bins,
         histtype="step", lw=3, color="C1", label="CTL", density=True)
ax3.hist(single["Pri_ProtAge"], orientation="horizontal", bins=bins,
         histtype="step", lw=3, color="C2", label="Single", density=True)

# Format marginals
ax3.legend(loc="best", framealpha=0.0, fontsize=17)
plt.setp(ax3.get_yticklabels(), visible=False);
ax3.set_ylim(0.0, 100)

fig.savefig("../Plots/porbDist.pdf", dpi=200, bbox_inches="tight")
