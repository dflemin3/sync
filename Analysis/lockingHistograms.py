"""

@author: David P Fleming, University of Washington, Nov 2018
@email dflemin3 (at) uw (dot) edu

"""

import numpy as np
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (9,8)
mpl.rcParams['font.size'] = 24.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

ylims = [0, 100]
bins = "auto"
num = 2500
seed = 42

np.random.seed(seed)

# Load in data
cpl = pd.read_csv("../Data/mcCPLDec22.csv")
ctl = pd.read_csv("../Data/mcCTLDec22.csv")

# Create indices for a random sample of num points to make scatterplot legible
inds = np.random.choice(np.arange(len(cpl)), size=num, replace=False)

# Lock times < 0 -> Not locked, set them to 7e9 (last simulation output time)
cpl["Pri_LockTime"][cpl["Pri_LockTime"] < 0] = 7.0e9
cpl["Sec_LockTime"][cpl["Sec_LockTime"] < 0] = 7.0e9
ctl["Pri_LockTime"][ctl["Pri_LockTime"] < 0] = 7.0e9
ctl["Sec_LockTime"][ctl["Sec_LockTime"] < 0] = 7.0e9

# Make flag for binaries who are locked by the age of the system
cpl["Locked"] = pd.Series(cpl["Pri_LockTime"] < cpl["Age"], index=cpl.index)
ctl["Locked"] = pd.Series(ctl["Pri_LockTime"] < ctl["Age"], index=ctl.index)

# Make flag for binaries that are strongly tidally-influence, that is, stars with
# Prot/Peq within [0.9, 1.1] but not locked
mask = ((np.fabs(1.0 - (cpl["Pri_ProtAge"]/cpl["Age_Peq"])) <= 0.1).values) & (~cpl["Locked"].values)
cpl["Interacting"] = pd.Series(mask, index=cpl.index)
mask = ((np.fabs(1.0 - (ctl["Pri_ProtAge"]/ctl["Age_Peq"])) <= 0.1).values) & (~ctl["Locked"].values)
ctl["Interacting"] = pd.Series(mask, index=ctl.index)

# Make flag for "freely rotating binaries", i.e. not locked and not strongly interacting
mask = (~cpl["Interacting"].values) & (~cpl["Locked"].values)
cpl["Free"] = pd.Series(mask, index=cpl.index)
mask = (~ctl["Interacting"].values) & (~ctl["Locked"].values)
ctl["Free"] = pd.Series(mask, index=ctl.index)

fig, ax = plt.subplots(figsize=(9, 8))

# Porb
ax.hist(cpl["Age_Porb"][cpl["Locked"]], label="CPL Tidal Model",
        bins=bins, histtype="step", lw=4, color="C1",
        density=True, ls="-", range=[0,100])

ax.hist(ctl["Age_Porb"][ctl["Locked"]], label="CTL Tidal Model",
        bins=bins, histtype="step", lw=4, color="C0",
        density=True, ls="-", range=[0,100])

# Format marginals
ax.set_xlim(0,100)
ax.set_ylim(0, 0.0325)
ax.set_ylabel("Normalized Counts", fontsize=30)
ax.set_xlabel("Orbital Period [d]", fontsize=30)
ax.set_title("Tidally-Locked Binary Stars", fontsize=30)
ax.legend(loc="best", framealpha=0.0, fontsize=23)

fig.tight_layout()
fig.savefig("../Plots/lockedPorbHistPresentation.pdf", bbox_inches="tight",
            dpi=600)
