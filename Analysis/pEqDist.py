"""

@author: David P. Fleming, University of Washington, Oct 2018
@email: dflemin3 (at) uw (dot) edu

Construct marginalize histograms of tidal locking times in multiple orbital
period bins.

"""

import numpy as np
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

#Typical plot parameters that make for pretty plots
mpl.rcParams['font.size'] = 16.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif','serif':['Computer Modern']})
mpl.rc('text', usetex=True)

bins = 20

# Load data
cpl = pd.read_csv("../Data/mcCPLDec22.csv")
ctl = pd.read_csv("../Data/mcCTLDec22.csv")

### Total marginal histogram of Peq/Prot ###

fig, ax = plt.subplots()

ax.hist(cpl["Final_Peq"]/cpl["Pri_ProtFinal"].values, bins=bins, color="C0", label="CPL",
        histtype="step", density=True, lw=3)
ax.hist(ctl["Final_Peq"]/ctl["Pri_ProtFinal"].values, bins=bins, color="C1", label="CTL",
        histtype="step", density=True, lw=3)

ax.set_xlabel("P$_{eq}$/P$_{rot}$")
ax.set_ylabel("Normalized Counts [Arbitrary Units]")
ax.legend(loc="upper left", fontsize=15, framealpha=0)

fig.savefig("../Plots/pEqMarginalHist.pdf", bbox_inches="tight")

### Marginal tidal locking time histograms by final binary orbital period

porbBinEdges = [0, 20, 40, 60, 80, 100]

fig = plt.figure(figsize=(5, 15))

gs = GridSpec(9, 1, height_ratios=[1, 0.1,
                                   1, 0.1,
                                   1, 0.1,
                                   1, 0.1, 1])

# Loop over gridspec
for ii in range(9):

    # Only add axes on even gridspecs (odd ones are small spaces)
    if ii % 2 == 0:

        ax = fig.add_subplot(gs[ii])

        # Make mask to select systems in correct period range
        cplMask = (cpl["Final_Porb"] > porbBinEdges[ii//2])
        cplMask = cplMask & (cpl["Final_Porb"] < porbBinEdges[ii//2 + 1])

        ctlMask = (ctl["Final_Porb"] > porbBinEdges[ii//2])
        ctlMask = ctlMask & (ctl["Final_Porb"] < porbBinEdges[ii//2 + 1])

        ax.hist(cpl["Final_Peq"][cplMask]/cpl["Pri_ProtFinal"][cplMask].values,
                bins=bins, color="C0", label="CPL", histtype="step",
                density=True, lw=3)
        ax.hist(ctl["Final_Peq"][cplMask]/ctl["Pri_ProtFinal"][cplMask].values,
                bins=bins, color="C1", label="CTL", histtype="step",
                density=True, lw=3)

        # Annotate with medians, 25,75 percentiles
        med = np.median(cpl["Final_Peq"][cplMask]/cpl["Pri_ProtFinal"][cplMask].values)
        up = np.percentile(cpl["Final_Peq"][cplMask]/cpl["Pri_ProtFinal"][cplMask].values, 75) - med
        down = med - np.percentile(cpl["Final_Peq"][cplMask]/cpl["Pri_ProtFinal"][cplMask].values, 25)
        ax.text(0.75, 0.9, ("CPL: $%.2lf^{+%0.2lf}_{-%0.2lf}$" % (med, up, down)),
                ha="center", va="center", size=15, color="C0", zorder=100,
                bbox=dict(boxstyle="square", fc="white", ec="white", alpha=0.0),
                transform=ax.transAxes)

        med = np.median(ctl["Final_Peq"][ctlMask]/ctl["Pri_ProtFinal"][ctlMask].values)
        up = np.percentile(ctl["Final_Peq"][ctlMask]/ctl["Pri_ProtFinal"][ctlMask].values, 75) - med
        down = med - np.percentile(ctl["Final_Peq"][ctlMask]/ctl["Pri_ProtFinal"][ctlMask].values, 25)
        ax.text(0.75, 0.75, ("CTL: $%.2lf^{+%0.2lf}_{-%0.2lf}$" % (med, up, down)),
                ha="center", va="center", size=15, color="C1", zorder=100,
                bbox=dict(boxstyle="square", fc="white", ec="white", alpha=0.0),
                transform=ax.transAxes)

        # Uniform x axis limits
        ax.set_xlim(0.25, 2.1)

        # Annotate with period range
        up = porbBinEdges[ii//2]
        down = porbBinEdges[ii//2 + 1]
        ax.set_title("$%.0lf$ $<$ P$_{orb}$ $<$ $%.0lf$ [d]" % (up, down),
                     fontsize=15, weight="bold")

        if ii == 4:
            ax.set_ylabel("Normalized Counts [Arbitrary Units]", fontsize=20,
                          labelpad=10)

# Format last axis
ax.set_xlabel("P$_{eq}$/P$_{rot}$", fontsize=20)

fig.savefig("../Plots/pEqPorbHist.pdf", bbox_inches="tight", dpi=600)
