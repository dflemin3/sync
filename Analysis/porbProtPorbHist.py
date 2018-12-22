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
from cmap import shiftedColorMap

#Typical plot parameters that make for pretty plots
mpl.rcParams['font.size'] = 20.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

# Load data
cpl = pd.read_csv("../Data/mcCPLDec22.csv")
cpl["Pri_dTidalQ"] = pd.Series(cpl["Pri_dTidaLQ"].values, index=cpl.index)
ctl = pd.read_csv("../Data/mcCTLDec22.csv")

# Read in lurie data
lurie = pd.read_csv("../Data/Lurie2017Full.csv", header=0)
lurie["Prot"] = lurie["p_1_min"].copy() # As recommended by Lurie+2017 for equitorial Prot
lurie["Porb"] = lurie["p_orb"].copy()

# Construct Porb, ecc bins based on assumed ranges
num = 11
bins = 20
porbBinEdges = np.linspace(0, 100, num)
porbProtBinEdges = np.linspace(0.4, 2.0, num)
estQTau = False

# Array for joint locking time distribution
cplTidalQ = np.zeros((num-1, num-1))
ctlTidalTau = np.zeros_like(cplTidalQ)
cplTidalQUp = np.zeros((num-1, num-1))
ctlTidalTauUp = np.zeros_like(cplTidalQ)
cplTidalQDown = np.zeros((num-1, num-1))
ctlTidalTauDown = np.zeros_like(cplTidalQ)

# Loop over bins, compute median tidal locking time in joing Porb/ecc bins
for ii in range(num-1):
    for jj in range(num-1):
        cplMask = (cpl["Final_Porb"] > porbBinEdges[ii])
        cplMask = cplMask & (cpl["Final_Porb"] < porbBinEdges[ii + 1])
        cplMask = cplMask & (cpl["Final_Porb"]/cpl["Pri_ProtFinal"] > porbProtBinEdges[jj])
        cplMask = cplMask & (cpl["Final_Porb"]/cpl["Pri_ProtFinal"] < porbProtBinEdges[jj + 1])

        ctlMask = (ctl["Final_Porb"] > porbBinEdges[ii])
        ctlMask = ctlMask & (ctl["Final_Porb"] < porbBinEdges[ii + 1])
        ctlMask = ctlMask & (ctl["Final_Porb"]/ctl["Pri_ProtFinal"] > porbProtBinEdges[jj])
        ctlMask = ctlMask & (ctl["Final_Porb"]/ctl["Pri_ProtFinal"] < porbProtBinEdges[jj + 1])

        # Populate array elements ctl["Pri_ProtFinal"][ctlMask]
        if np.sum(cplMask) == 0:
            cplTidalQ[ii, jj] = np.nan
            cplTidalQUp[ii, jj] = np.nan
            cplTidalQDown[ii, jj] = np.nan
        else:
            cplTidalQ[ii, jj] = np.median(np.log10(cpl["Pri_dTidalQ"][cplMask]))
            cplTidalQUp[ii, jj] = np.percentile(np.log10(cpl["Pri_dTidalQ"][cplMask]), 84) - cplTidalQ[ii, jj]
            cplTidalQDown[ii, jj] = cplTidalQ[ii, jj] - np.percentile(np.log10(cpl["Pri_dTidalQ"][cplMask]), 16)

        # Populate array elements ctl["Pri_ProtFinal"][ctlMask]
        if np.sum(ctlMask) == 0:
            ctlTidalTau[ii, jj] = np.nan
            ctlTidalTauUp[ii, jj] = np.nan
            ctlTidalTauDown[ii, jj] = np.nan
        else:
            ctlTidalTau[ii, jj] = np.median(np.log10(ctl["Pri_dTidalTau"][ctlMask]))
            ctlTidalTauUp[ii, jj] = np.percentile(np.log10(ctl["Pri_dTidalTau"][ctlMask]), 84) - ctlTidalTau[ii, jj]
            ctlTidalTauDown[ii, jj] = ctlTidalTau[ii, jj] - np.percentile(np.log10(ctl["Pri_dTidalTau"][ctlMask]), 16)
# end loop

################################################################################
#
#   Peq/Prot joint histogram
#
################################################################################

fig = plt.figure(figsize=(9, 8))
gs = GridSpec(1, 3, width_ratios=[1, 0.01, 0.075], wspace=0.05)
extent = [0.4, 2.0, 0, 100]

### CPL Plot ###
ax1 = fig.add_subplot(gs[0])

im = ax1.imshow(cplTidalQ, origin="lower", aspect="auto", extent=extent,
                cmap="viridis_r", vmin=4, vmax=8)

# Annotate with med + errors
porbBinEdges = np.linspace(0, 100, num)
porbProtBinEdges = np.linspace(0.4, 2.0, num)
for ii in range(len(porbBinEdges)-1):
    y = 0.5*(porbBinEdges[ii] + porbBinEdges[ii+1])
    for jj in range(len(porbProtBinEdges)-1):
        x = 0.5*(porbProtBinEdges[jj] + porbProtBinEdges[jj+1])
        if not np.isnan(cplTidalQ[ii,jj]):
            ax1.text(x, y, ("$%.1lf^{+%0.1lf}_{-%0.1lf}$" % (cplTidalQ[ii,jj], cplTidalQUp[ii,jj], cplTidalQDown[ii,jj])),
                     ha="center", va="center", size=14, color="white", zorder=100)

ax1.set_xlim(0.4, 2.0)
ax1.set_ylim(0, 100)
ax1.set_xlabel(r"P$_{orb}$/P$_{rot}$", fontsize=30)
ax1.set_ylabel("Orbital Period [d]", fontsize=30)

### Colorbar ###
cbaxes = fig.add_subplot(gs[2])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label="Median log$_{10}(Q)$", labelpad=30, fontsize=25)

fig.savefig("../Plots/porbProtPorbQHist.pdf", bbox_inches="tight", dpi=600)

### CTL Plot ###
fig = plt.figure(figsize=(9, 8))
gs = GridSpec(1, 3, width_ratios=[1, 0.01, 0.075], wspace=0.05)
ax2 = fig.add_subplot(gs[0])

im = ax2.imshow(ctlTidalTau, origin="lower", aspect="auto", extent=extent,
                  cmap="viridis", vmin=-2, vmax=1)

# Annotate with med + errors
porbBinEdges = np.linspace(0, 100, num)
porbProtBinEdges = np.linspace(0.4, 2.0, num)
for ii in range(len(porbBinEdges)-1):
    y = 0.5*(porbBinEdges[ii] + porbBinEdges[ii+1])
    for jj in range(len(porbProtBinEdges)-1):
        x = 0.5*(porbProtBinEdges[jj] + porbProtBinEdges[jj+1])
        if not np.isnan(ctlTidalTau[ii,jj]):
            ax2.text(x, y, ("$%.1lf^{+%0.1lf}_{-%0.1lf}$" % (ctlTidalTau[ii,jj], ctlTidalTauUp[ii,jj], ctlTidalTauDown[ii,jj])),
                     ha="center", va="center", size=12, color="white", zorder=100)

ax2.set_xlim(0.4, 2.0)
ax2.set_ylim(0, 100)
ax2.set_ylabel("Orbital Period [d]", fontsize=30)
ax2.set_xlabel(r"P$_{orb}$/P$_{rot}$", fontsize=30)

### Colorbar ###
cbaxes = fig.add_subplot(gs[2])
cb = plt.colorbar(im, cax=cbaxes)
cb.set_label(label=r"Median log$_{10}(\tau[\mathrm{s}])$", labelpad=30, fontsize=25)

fig.savefig("../Plots/porbProtPorbTauHist.pdf", bbox_inches="tight", dpi=600)

################################################################################
#
#   Estimate tidal Q, tau for Lurie+2017 sample
#
################################################################################

if estQTau:

    nsamp = 100
    qs = []
    taus = []


    # Loop over Lurie+2017 data, assign points to bin, estimate tidal parameters
    for kk in range(len(lurie)):
        for ii in range(num-1):
            for jj in range(num-1):
                cplMask = (cpl["Final_Porb"] > porbBinEdges[ii])
                cplMask = cplMask & (cpl["Final_Porb"] < porbBinEdges[ii + 1])
                cplMask = cplMask & (cpl["Final_Porb"]/cpl["Pri_ProtFinal"] > porbProtBinEdges[jj])
                cplMask = cplMask & (cpl["Final_Porb"]/cpl["Pri_ProtFinal"] < porbProtBinEdges[jj + 1])

                ctlMask = (ctl["Final_Porb"] > porbBinEdges[ii])
                ctlMask = ctlMask & (ctl["Final_Porb"] < porbBinEdges[ii + 1])
                ctlMask = ctlMask & (ctl["Final_Porb"]/ctl["Pri_ProtFinal"] > porbProtBinEdges[jj])
                ctlMask = ctlMask & (ctl["Final_Porb"]/ctl["Pri_ProtFinal"] < porbProtBinEdges[jj + 1])

                if np.sum(cplMask) == 0:
                    continue
                else:
                    porbProt = lurie["Porb"][kk]/lurie["Prot"][kk]
                    porb = lurie["Porb"][kk]
                    if(porb > porbBinEdges[ii]) and (porb < porbBinEdges[ii+1]):
                        if (porbProt > porbProtBinEdges[jj]) and (porbProt < porbProtBinEdges[jj+1]):
                            # Found correct bin, sample tidal Qs, taus with replacement
                            qs = qs + list(np.random.choice(np.log10(cpl["Pri_dTidalQ"][cplMask]),
                                           size=nsamp, replace=True))
                if np.sum(ctlMask) == 0:
                    continue
                else:
                    porbProt = lurie["Porb"][kk]/lurie["Prot"][kk]
                    porb = lurie["Porb"][kk]
                    if(porb > porbBinEdges[ii]) and (porb < porbBinEdges[ii+1]):
                        if (porbProt > porbProtBinEdges[jj]) and (porbProt < porbProtBinEdges[jj+1]):
                            # Found correct bin, sample tidal Qs, taus with replacement
                            taus = taus + list(np.random.choice(np.log10(ctl["Pri_dTidalTau"][ctlMask]),
                                               size=nsamp, replace=True))

    # Tidal Q figure
    fig, ax = plt.subplots()

    ax.hist(qs, bins=bins, range=[4, 7], histtype="step", lw=3, density=True)
    ax.set_xlabel("log$_{10}(Q)$")
    ax.set_ylabel("Normalized Counts")

    # Plot
    med = np.median(qs)
    up = np.percentile(qs, 84)
    down = np.percentile(qs, 16)
    ax.axvline(med, ls="--", color="black", lw=2)
    ax.axvline(down, ls="--", color="black", lw=2)
    ax.axvline(up, ls="--", color="black", lw=2)

    # Annotate
    ax.text(5.2, 0.425, (r"log$_{10}(Q) = %.2lf^{+%0.2lf}_{-%0.2lf}$" % (med, up-med, med-down)),
            ha="center", va="center", size=16, color="black", zorder=100,
            bbox=dict(boxstyle="square", fc="white", ec="white", alpha=0.9))

    fig.savefig("../Plots/qLurie.pdf", bbox_inches="tight", dpi=600)

    # Tidal tau figure
    fig, ax = plt.subplots()

    ax.hist(taus, bins=bins, range=[-2, 0], histtype="step", lw=3, density=True)
    ax.set_xlabel(r"log$_{10}(\tau[\mathrm{s}])$")
    ax.set_ylabel("Normalized Counts")

    # Plot
    med = np.median(taus)
    up = np.percentile(taus, 84)
    down = np.percentile(taus, 16)
    ax.axvline(med, ls="--", color="black", lw=2)
    ax.axvline(down, ls="--", color="black", lw=2)
    ax.axvline(up, ls="--", color="black", lw=2)

    # Annotate
    ax.text(-1.5, 0.8, (r"log$_{10}(\tau) = %.2lf^{+%0.2lf}_{-%0.2lf}$" % (med, up-med, med-down)),
            ha="center", va="center", size=16, color="black", zorder=100,
            bbox=dict(boxstyle="square", fc="white", ec="white", alpha=0.9))

    fig.savefig("../Plots/tauLurie.pdf", bbox_inches="tight", dpi=600)
