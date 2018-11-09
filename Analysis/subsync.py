"""

@author: David P. Fleming, University of Washington, Nov 2018
@email: dflemin3 (at) uw (dot) edu

Comparison of simulations with Lurie+2017 Porb <= 10 d population, with a focus
on the subsynchronous rotators.

Script output:

Median subsync tidal tau: 0.024179478659999996
Median supersync tidal tau: 0.0412718247
Median subsync ecc: 0.13616799999999998
Median supersync ecc: 0.1525495
Fraction with Porb/Prot in [0.92,1.2] for Porb < 10d: 0.44291609353507566
Fraction with Porb/Prot in [0.84,0.92] for Porb < 10d: 0.08665749656121045

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
cpl = pd.read_csv("../Data/mcCPLTorque.csv")
ctl = pd.read_csv("../Data/mcCTLTorque.csv")

lurie = pd.read_csv("../Data/Lurie2017.csv", comment="#", header=None,
                    names=["Porb", "Prot", "Ecc"])

# Lock times < 0 -> Not locked, set them to 7e9 (last simulation output time)
cpl["Pri_LockTime"][cpl["Pri_LockTime"] < 0] = 7.0e9
cpl["Sec_LockTime"][cpl["Sec_LockTime"] < 0] = 7.0e9
ctl["Pri_LockTime"][ctl["Pri_LockTime"] < 0] = 7.0e9
ctl["Sec_LockTime"][ctl["Sec_LockTime"] < 0] = 7.0e9

### 1st Fig modeled after Fig. 7 from Lurie+2017, sub zoomed in on subsync population ###

fig = plt.figure(figsize=(9, 8))
gs = GridSpec(1, 3, width_ratios=[1, 0.01, 0.075], wspace=0.05)

# Plot simulated data
ax0 = fig.add_subplot(gs[0])
im = ax0.scatter(ctl["Age_Porb"], ctl["Age_Porb"]/ctl["Pri_ProtAge"],
                 c=ctl["Age_Ecc"].values, cmap="viridis", zorder=1,
                 s=40, marker="o", vmin=0, vmax=0.3, label="Simulated")

ax0.axhline(1, lw=2, color="black", ls="-", zorder=2)

if plotLurie:
    # Plot Lurie+2017 data
    ax0.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"], c=lurie["Ecc"], s=100, zorder=3,
                marker="+", vmin=0, vmax=0.3, label="Lurie et al. (2017)")

# Format
ax0.set_rasterization_zorder(0)
ax0.set_xlim(0,10)
ax0.set_ylim(0.0, 1.3)
ax0.set_xlabel("P$_{orb}$ [d]", fontsize=25)
ax0.set_ylabel("P$_{orb}$ / P$_{rot}$", fontsize=25)
leg = ax0.legend(loc="upper left", framealpha=0.75, fontsize=17)
leg.legendHandles[0]._sizes = [50]
leg.legendHandles[0].set_color('k')
if plotLurie:
    leg.legendHandles[1].set_color('k')
    leg.legendHandles[1]._sizes = [50]

### Colorbar ###
cbaxes = fig.add_subplot(gs[2])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Eccentricity")

fig.savefig("../Plots/subsync.pdf", bbox_inches="tight", dpi=600)

### Plot histogram of log10 tidal taus above and below Prot=Peq=Porb=1 line

subMask = (ctl["Age_Porb"]/ctl["Pri_ProtAge"] < 0.7)

fig, ax = plt.subplots()

ax.hist(np.log10(ctl["Pri_dTidalTau"][subMask].values), lw=3, histtype="step",
        color="C0", label="P$_{orb}$/P$_{rot} < 0.7$", bins="auto", density=True)

ax.hist(np.log10(ctl["Pri_dTidalTau"][~subMask].values), lw=3, histtype="step",
        color="C1", label="P$_{orb}$/P$_{rot} > 0.7$", bins="auto", density=True)

ax.set_ylabel("Normalized Counts")
ax.set_xlabel(r"log$_{10}(\tau \mathrm{[s]})$")
ax.legend(loc="lower center", framealpha=0)

fig.savefig("../Plots/subsyncTauHist.pdf", bbox_inches="tight", dpi=600)

# Print median sub,supersync tidal taus
print("Median subsync tidal tau:",np.median(ctl["Pri_dTidalTau"][subMask].values))
print("Median supersync tidal tau:",np.median(ctl["Pri_dTidalTau"][~subMask].values))

### Plot histogram of ecc above and below Prot=Peq=Porb=1 line

subMask = (ctl["Age_Porb"]/ctl["Pri_ProtAge"] < 1)

fig, ax = plt.subplots()

ax.hist(ctl["Age_Ecc"][subMask].values, lw=3, histtype="step",
        color="C0", label="Subsynchronous", bins="auto", density=True)

ax.hist(ctl["Age_Ecc"][~subMask].values, lw=3, histtype="step",
        color="C1", label="Supersynchronous", bins="auto", density=True)

ax.set_ylabel("Normalized Counts")
ax.set_xlabel("Eccentricity")
ax.legend(loc="lower center", framealpha=0)

fig.savefig("../Plots/subsyncEccHist.pdf", bbox_inches="tight", dpi=600)

# Print median sub,supersync tidal taus
print("Median subsync ecc:",np.median(ctl["Age_Ecc"][subMask].values))
print("Median supersync ecc:",np.median(ctl["Age_Ecc"][~subMask].values))

# Compare with Lurie+2017 sample for 2 < Porb < 10 days
# Lurie+2017: 72% in [0.92,1.2]
# Lurie+2017: 15% in [0.84, 0.92]

porbMask = (ctl["Age_Porb"] < 10) & (ctl["Age_Porb"] > 2)
mask = (ctl["Age_Porb"]/ctl["Pri_ProtAge"] >= 0.92)
mask = mask & (ctl["Age_Porb"]/ctl["Pri_ProtAge"] < 1.2)
mask = mask & porbMask
print("Fraction with Porb/Prot in [0.92,1.2] for Porb < 10d:",np.sum(mask)/np.sum(porbMask))

mask = (ctl["Age_Porb"]/ctl["Pri_ProtAge"] >= 0.84)
mask = mask & (ctl["Age_Porb"]/ctl["Pri_ProtAge"] < 0.92)
mask = mask & porbMask
print("Fraction with Porb/Prot in [0.84,0.92] for Porb < 10d:",np.sum(mask)/np.sum(porbMask))

# Done!
