"""

@author: David P. Fleming, University of Washington, Nov 2018
@email: dflemin3 (at) uw (dot) edu

Prot distributions as a function of stellar mass and age for the CPL, CTL, and
single star models uniform over ages [1,7] Gyr, roughly field star ages.

Script Output:

CPL median Prot: 38.995495000000005
CTL median Prot: 40.5107835
Single median Prot: 46.4415785

CPL Fraction of Stars with Prot < 7.5 d: 0.0678
CTL Fraction of Stars with Prot < 7.5 d: 0.056
Single Fraction of Stars with Prot < 7.5 d: 0.0172

CPL Fraction of Stars with Prot < 20 d: 0.1947
CTL Fraction of Stars with Prot < 20 d: 0.1702
Single Fraction of Stars with Prot < 20 d: 0.0523

CPL Median Age of Stars with Prot < 20 d: 3.094056856848848
CTL Median Age of Stars with Prot < 20 d: 2.7658880946291395
Single Mediage Age of Stars with Prot < 20 d: 1.346166303555715

CPL + Age of Stars with Prot < 20 d: 5.8487757586979665
CTL + Age of Stars with Prot < 20 d: 5.563816566899135
Single + Age of Stars with Prot < 20 d: 1.8214255111813729

CPL - Age of Stars with Prot < 20 d: 1.3467068622724916
CTL - Age of Stars with Prot < 20 d: 1.2988697413400274
Single - Age of Stars with Prot < 20 d: 1.0843035833816197


Interpretation:

Binary models, regardless of tidal model, systematic rotate more quickly than
single-star only models due to tidal torques.  Both tidal models predict a large
population of rapid rotators (Prot < 7.5 d, < 20 d) than single star models fail
to do, regardless of age, for stars with M > 0.5 Msun, aka GK stars which Kepler
is most sensitive to. Therefore, fast rotators in Kepler field can be explained
by tidally-interacting binaries. Furthermore, note that the binary Prot distribution
does not always follow the expected result of single star gyrochronology that
predicts that, in the long run, stars rotate more slowly with age.  Ages of
binaries, especially short Prot tidally-influenced systems, do not always
correlate with age as tides can fix Prot = Peq, or at least keep it near Peq,
decoupling Prot from age, causing gyrochronlogy methods to fail in this instance.

"""

import numpy as np
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (9,8)
mpl.rcParams['font.size'] = 22.0

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
cpl = pd.read_csv("../Data/mcCPLTorqueNov9.csv")
ctl = pd.read_csv("../Data/mcCTLTorqueNov9.csv")
single = pd.read_csv("../Data/mcSingle.csv")
lurie = pd.read_csv("../Data/Lurie2017.csv", comment="#", header=None,
                    names=["Porb", "Prot", "Ecc"])

# Create indices for a random sample of num points to make scatterplot legible
inds = np.random.choice(np.arange(len(cpl)), size=num, replace=False)

# Plot!
fig = plt.figure(figsize=(30, 8))
gs = GridSpec(3, 7,
              height_ratios=[0.05, 0.015, 1],
              width_ratios=[1, 0.001, 1, 0.001, 1, 0.001, 0.25],
              wspace=0.1)

### CPL Plot ###
ax0 = fig.add_subplot(gs[14])

im = ax0.scatter(cpl.iloc[inds]["Pri_dMass"], cpl.iloc[inds]["Pri_ProtAge"], s=50,
                 c=cpl.iloc[inds]["Age"].values/1.0e9, vmin=1, vmax=7, cmap=cmap)
ax0.set_rasterization_zorder(0)
ax0.set_xlabel("Mass [M$_{\odot}$]", fontsize=30)
ax0.set_ylabel("Rotation Period [d]", fontsize=30)
ax0.set_xlim(0.1, 1)
ax0.set_ylim(0.0, 100)
ax0.text(0.15, 90, "CPL", ha="left", va="center", size=30, color="black",
         zorder=100)

### CTL Plot ###
ax1 = fig.add_subplot(gs[16])

ax1.scatter(ctl.iloc[inds]["Pri_dMass"], ctl.iloc[inds]["Pri_ProtAge"], s=50,
            c=ctl.iloc[inds]["Age"].values/1.0e9, vmin=1, vmax=7, cmap=cmap)
ax1.set_rasterization_zorder(0)
ax1.set_xlabel("Mass [M$_{\odot}$]", fontsize=30)
ax1.set_xlim(0.1, 1)
ax1.set_ylim(0.0, 100)
ax1.text(0.15, 90, "CTL", ha="left", va="center", size=30, color="black",
         zorder=100)

### Single Plot ###
ax2 = fig.add_subplot(gs[18])

ax2.scatter(single.iloc[inds]["Pri_dMass"], single.iloc[inds]["Pri_ProtAge"], s=50,
            c=single.iloc[inds]["Age"].values/1.0e9, vmin=1, vmax=7, cmap=cmap)
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

# Print out interesting statistics
print("CPL median Prot:",np.median(cpl["Pri_ProtAge"]))
print("CTL median Prot:",np.median(ctl["Pri_ProtAge"]))
print("Single median Prot:",np.median(single["Pri_ProtAge"]))
print()
print("CPL Fraction of Stars with Prot < 7.5 d:",np.sum(cpl["Pri_ProtAge"] < 7.5)/len(cpl))
print("CTL Fraction of Stars with Prot < 7.5 d:",np.sum(ctl["Pri_ProtAge"] < 7.5)/len(ctl))
print("Single Fraction of Stars with Prot < 7.5 d:",np.sum(single["Pri_ProtAge"] < 7.5)/len(single))
print()
print("CPL Fraction of Stars with Prot < 20 d:",np.sum(cpl["Pri_ProtAge"] < 20)/len(cpl))
print("CTL Fraction of Stars with Prot < 20 d:",np.sum(ctl["Pri_ProtAge"] < 20)/len(ctl))
print("Single Fraction of Stars with Prot < 20 d:",np.sum(single["Pri_ProtAge"] < 20)/len(single))
print()
print("CPL Median Age of Stars with Prot < 20 d:",np.median(cpl["Age"][cpl["Pri_ProtAge"] < 20]/1.0e9))
print("CTL Median Age of Stars with Prot < 20 d:",np.median(ctl["Age"][ctl["Pri_ProtAge"] < 20]/1.0e9))
print("Single Mediage Age of Stars with Prot < 20 d:",np.median(single["Age"][single["Pri_ProtAge"] < 20]/1.0e9))
print()
print("CPL + Age of Stars with Prot < 20 d:",np.percentile(cpl["Age"][cpl["Pri_ProtAge"] < 20]/1.0e9, 84))
print("CTL + Age of Stars with Prot < 20 d:",np.percentile(ctl["Age"][ctl["Pri_ProtAge"] < 20]/1.0e9, 84))
print("Single + Age of Stars with Prot < 20 d:",np.percentile(single["Age"][single["Pri_ProtAge"] < 20]/1.0e9, 84))
print()
print("CPL - Age of Stars with Prot < 20 d:",np.percentile(cpl["Age"][cpl["Pri_ProtAge"] < 20]/1.0e9, 16))
print("CTL - Age of Stars with Prot < 20 d:",np.percentile(ctl["Age"][ctl["Pri_ProtAge"] < 20]/1.0e9, 16))
print("Single - Age of Stars with Prot < 20 d:",np.percentile(single["Age"][single["Pri_ProtAge"] < 20]/1.0e9, 16))

fig.savefig("../Plots/protDist.pdf", bbox_inches="tight", dpi=600)
