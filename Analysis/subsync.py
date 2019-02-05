"""

@author: David P. Fleming, University of Washington, Nov 2018
@email: dflemin3 (at) uw (dot) edu

Comparison of simulations with Lurie+2017 Porb <= 10 d population, with a focus
on the subsynchronous rotators.

Script output:

CTL:

Median subsync tidal tau: 0.17078373819999998
Median supersync tidal tau: 0.466656378
Median subsync ecc: 0.107152
Median supersync ecc: 0.15391400000000002
Median subsync mass ratio: 0.6416154898583578
Median supersync mass ratio: 0.6614121797592005
Fraction with Porb/Prot in [0.92,1.2] for Porb < 10d: 0.7182910547396528
Fraction with Porb/Prot in [0.84,0.92] for Porb < 10d: 0.09078771695594126

CPL:

Fraction with Porb/Prot in [0.92,1.2] for Porb < 10d: 0.6887052341597796
Fraction with Porb/Prot in [0.84,0.92] for Porb < 10d: 0.01928374655647383

Interpretation:

Although Lurie+2017 attributes differential rotation to the production of the
subsynchronous population, we find that coupled stellar-tidal evolution naturally
produces the population. Compare with Lurie+2017 sample for 2 < Porb < 10 days:
72% in [0.92,1.2] and 15% in [0.84, 0.92].

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
bins = "auto"

# Load data
cpl = pd.read_csv("../Data/mcCPLDec22.csv")
ctl = pd.read_csv("../Data/mcCTLDec22.csv")

# Load in cleaned sample of Prot and Ecc from Lurie+2017
lurie = pd.read_csv("../Data/Lurie2017.csv", comment="#", header=None,
                    names=["Porb", "Prot", "Ecc"])

### 1st Fig modeled after Fig. 7 from Lurie+2017, sub zoomed in on subsync population ###

fig = plt.figure(figsize=(9, 8))
gs = GridSpec(1, 3, width_ratios=[1, 0.01, 0.075], wspace=0.05)

# Plot simulated data
ax0 = fig.add_subplot(gs[0])
im = ax0.scatter(ctl["Age_Porb"], ctl["Age_Porb"]/ctl["Pri_ProtAge"],
                 c=ctl["Age_Ecc"].values, cmap="viridis", zorder=1,
                 s=40, marker="o", vmin=0, vmax=0.3, label="Simulated")

if plotLurie:
    # Plot Lurie+2017 data
    ax0.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"], c=lurie["Ecc"], s=80, zorder=3,
                marker="x", vmin=0, vmax=0.3, label="Lurie et al. (2017)")

# Format
ax0.set_rasterization_zorder(0)
ax0.set_xlim(0,10)
ax0.set_ylim(0.6, 1.25)
ax0.set_xlabel("P$_{orb}$ [d]", fontsize=30)
ax0.set_ylabel("P$_{orb}$ / P$_{rot}$", fontsize=30)
leg = ax0.legend(loc="lower left", framealpha=0.5, fontsize=22)
leg.legendHandles[0]._sizes = [100]
leg.legendHandles[0].set_color('k')
if plotLurie:
    leg.legendHandles[1].set_color('k')
    leg.legendHandles[1]._sizes = [100]

ax0.text(0.5, 1.2, "CTL", ha="left", va="center", size=28,
         color="black", zorder=100)

### Colorbar ###
cbaxes = fig.add_subplot(gs[2])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Eccentricity", fontsize=25)

fig.savefig("../Plots/subsync.pdf", bbox_inches="tight", dpi=200)

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


### Make version of above plot with marginal Porb/Prot histogram with CTL ###

fig = plt.figure(figsize=(9,9))

gs = GridSpec(4,4)

ax = fig.add_subplot(gs[1:4,0:3])
ax_marg_y = fig.add_subplot(gs[1:4,3])

im = ax.scatter(ctl["Age_Porb"], ctl["Age_Porb"]/ctl["Pri_ProtAge"],
                c=ctl["Age_Ecc"].values, cmap="viridis", zorder=1,
                s=40, marker="o", vmin=0, vmax=0.3, label="CTL")

# Line at synchronization
ax.axhline(1, lw=2, color="black", ls="-", zorder=2)

if plotLurie:
    # Plot Lurie+2017 data
    ax.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"], c=lurie["Ecc"], s=75, zorder=3,
               marker="d", vmin=0, vmax=0.3, label="Lurie et al. (2017)")

ax.set_xlabel("P$_{orb}$ [d]", fontsize=30)
ax.set_ylabel("P$_{orb}$ / P$_{rot}$", fontsize=30)
ax.set_xlim(0,10)
ax.set_ylim(0.6, 1.25)
leg = ax.legend(loc="lower left", framealpha=0.0, fontsize=22)
leg.legendHandles[0]._sizes = [100]
leg.legendHandles[0].set_color('k')
if plotLurie:
    leg.legendHandles[1].set_color('k')
    leg.legendHandles[1]._sizes = [100]
ax.set_rasterization_zorder(0)

# Now adding the colorbar
cbaxes = fig.add_axes([0.1, 0.775, 0.8, 0.03])
cb = plt.colorbar(im, cax=cbaxes, label="Eccentricity", orientation="horizontal")

# Marginalized histograms
ax_marg_y.hist(ctl["Age_Porb"]/ctl["Pri_ProtAge"], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C0", label="CTL",
               density=True, range=(0.6, 1.25))

# Histogram for Kepler data
ax_marg_y.hist(lurie["Porb"]/lurie["Prot"], orientation="horizontal", bins=bins,
                histtype="step", lw=3, color="C1", label="Lurie et al. (2017)",
                range=(0.6, 1.25), density=True)

ax_marg_y.legend(loc="best", framealpha=0.0, fontsize=15)

# Turn off tick labels on marginals
ax_marg_y.set_ylim(0.6, 1.25)
plt.setp(ax_marg_y.get_yticklabels(), visible=False);

fig.savefig("../Plots/subsyncMarginalCTL.pdf", bbox_inches="tight", dpi=600)


### Make version of above plot with marginal Porb/Prot histogram with CPL ###

fig = plt.figure(figsize=(9,9))

gs = GridSpec(4,4)

ax = fig.add_subplot(gs[1:4,0:3])
ax_marg_y = fig.add_subplot(gs[1:4,3])

im = ax.scatter(cpl["Age_Porb"], cpl["Age_Porb"]/cpl["Pri_ProtAge"],
                c=cpl["Age_Ecc"].values, cmap="viridis", zorder=1,
                s=40, marker="o", vmin=0, vmax=0.3, label="CPL")

# Line at synchronization
ax.axhline(1, lw=2, color="black", ls="-", zorder=2)

if plotLurie:
    # Plot Lurie+2017 data
    ax.scatter(lurie["Porb"], lurie["Porb"]/lurie["Prot"], c=lurie["Ecc"], s=75, zorder=3,
               marker="d", vmin=0, vmax=0.3, label="Lurie et al. (2017)")

ax.set_xlabel("P$_{orb}$ [d]", fontsize=30)
ax.set_ylabel("P$_{orb}$ / P$_{rot}$", fontsize=30)
ax.set_xlim(0,10)
ax.set_ylim(0.6, 1.25)
leg = ax.legend(loc="lower left", framealpha=0.0, fontsize=22)
leg.legendHandles[0]._sizes = [100]
leg.legendHandles[0].set_color('k')
if plotLurie:
    leg.legendHandles[1].set_color('k')
    leg.legendHandles[1]._sizes = [100]
ax.set_rasterization_zorder(0)

# Now adding the colorbar
cbaxes = fig.add_axes([0.1, 0.775, 0.8, 0.03])
cb = plt.colorbar(im, cax=cbaxes, label="Eccentricity", orientation="horizontal")

# Marginalized histograms
ax_marg_y.hist(cpl["Age_Porb"]/cpl["Pri_ProtAge"], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C0", label="CPL",
               density=True, range=(0.6, 1.25))

# Histogram for Kepler data
ax_marg_y.hist(lurie["Porb"]/lurie["Prot"], orientation="horizontal", bins=bins,
                histtype="step", lw=3, color="C1", label="Lurie et al. (2017)",
                range=(0.6, 1.25), density=True)

ax_marg_y.legend(loc="best", framealpha=0.0, fontsize=15)

# Turn off tick labels on marginals
ax_marg_y.set_ylim(0.6, 1.25)
plt.setp(ax_marg_y.get_yticklabels(), visible=False);

fig.savefig("../Plots/subsyncMarginalCPL.pdf", bbox_inches="tight", dpi=600)

### Plot histogram of log10 tidal taus above and below Prot=Peq=Porb=1 line

subMask = (ctl["Age_Porb"]/ctl["Pri_ProtAge"] < 1.0)

fig, ax = plt.subplots()

ax.hist(np.log10(ctl["Pri_dTidalTau"][subMask].values), lw=3, histtype="step",
        color="C0", label="P$_{orb}$/P$_{rot} < 0.7$", bins="auto", density=True)

ax.hist(np.log10(ctl["Pri_dTidalTau"][~subMask].values), lw=3, histtype="step",
        color="C1", label="P$_{orb}$/P$_{rot} > 0.7$", bins="auto", density=True)

ax.set_ylabel("Normalized Counts")
ax.set_xlabel(r"log$_{10}(\tau \mathrm{[s]})$")
ax.legend(loc="lower center", framealpha=0, fontsize=18)

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

# Print median sub,supersync tidal ecc
print("Median subsync ecc:",np.median(ctl["Age_Ecc"][subMask].values))
print("Median supersync ecc:",np.median(ctl["Age_Ecc"][~subMask].values))

### Plot histogram of mass ratio above and below Prot=Peq=Porb=1 line

subMask = (ctl["Age_Porb"]/ctl["Pri_ProtAge"] < 1)

fig, ax = plt.subplots()

mu = ctl["Sec_dMass"][subMask].values/ctl["Pri_dMass"][subMask].values
ax.hist(mu, lw=3, histtype="step",
        color="C0", label="Subsynchronous", bins="auto", density=True)

mu = ctl["Sec_dMass"][~subMask].values/ctl["Pri_dMass"][~subMask].values
ax.hist(mu, lw=3, histtype="step",
        color="C1", label="Supersynchronous", bins="auto", density=True)

ax.set_ylabel("Normalized Counts")
ax.set_xlabel("Mass Ratio (M$_2$/M$_1$)")
ax.legend(loc="lower center", framealpha=0)

fig.savefig("../Plots/subsyncMuHist.pdf", bbox_inches="tight", dpi=600)

# Print median sub,supersync tidal taus
mu = ctl["Sec_dMass"][subMask].values/ctl["Pri_dMass"][subMask].values
print("Median subsync mass ratio:",np.median(mu))
mu = ctl["Sec_dMass"][~subMask].values/ctl["Pri_dMass"][~subMask].values
print("Median supersync mass ratio:",np.median(mu))

# Done!
