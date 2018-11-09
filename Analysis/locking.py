"""

@author: David P Fleming, University of Washington, Nov 2018
@email dflemin3 (at) uw (dot) edu

Plot to show which binaries are tidally locked in mass-Prot space by the age of
the system for both the CPL and CTL models.  We randomly assigned ages to systems
from a uniform distribution over 1-7 Gyr, broadly consistent with stellar ages
in the Kepler field.

Script Output:

CPL locked Prot median: 27.049087
CPL unlocked Prot median: 42.744551
CPL fraction of locked binaries: 0.2518

CTL locked Prot median: 4.683883
CTL unlocked Prot median: 42.3556655
CTL fraction of locked binaries: 0.0202


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

ylims = [0, 100]
bins = "auto"
num = 2500
seed = 42

np.random.seed(seed)

# Load in data
cpl = pd.read_csv("../Data/mcCPLTorque.csv")
ctl = pd.read_csv("../Data/mcCTLTorque.csv")

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

### CPL ###

fig = plt.figure(figsize=(10,9))
gs = GridSpec(4,4, wspace=0.45)

ax = fig.add_subplot(gs[1:4,0:3])
ax_marg_y = fig.add_subplot(gs[1:4,3])

# Plot locked binaries
im = ax.scatter(cpl.iloc[inds]["Pri_dMass"][cpl.iloc[inds]["Locked"]],
                cpl.iloc[inds]["Pri_ProtAge"][cpl.iloc[inds]["Locked"]],
                c=cpl.iloc[inds]["Age"][cpl.iloc[inds]["Locked"]].values/1.0e9,
                cmap="viridis", marker="x", s=50, zorder=1, label="Locked")
# Not tidally locked binaries
im = ax.scatter(cpl.iloc[inds]["Pri_dMass"][~cpl.iloc[inds]["Locked"]],
                cpl.iloc[inds]["Pri_ProtAge"][~cpl.iloc[inds]["Locked"]],
                c=cpl.iloc[inds]["Age"][~cpl.iloc[inds]["Locked"]].values/1.0e9,
                cmap="viridis", marker="o", s=30, zorder=2, label="Not Locked")

# Format plot
ax.set_xlabel("Mass [M$_{\odot}$]", fontsize=28)
ax.set_xlim(np.min(cpl["Pri_dMass"]), np.max(cpl["Pri_dMass"]))
ax.set_ylabel("P$_{rot}$ [d]", fontsize=28)
ax.set_ylim(ylims)
ax.set_rasterization_zorder(0)
leg = ax.legend(loc="upper left", framealpha=0.0, fontsize=15)
for marker in leg.legendHandles:
    marker.set_color('k')

# Plot marginals
ax_marg_y.hist(cpl["Pri_ProtAge"][cpl["Locked"]], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C0",
               label="Locked", density=True)
ax_marg_y.hist(cpl["Pri_ProtAge"][~cpl["Locked"]], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C1",
               label="Not Locked", density=True)

# Format marginals
ax_marg_y.set_ylim(ylims)
ax_marg_y.legend(loc="best", framealpha=0.5, fontsize=12)
plt.setp(ax_marg_y.get_yticklabels(), visible=False);

# Now adding the colorbar
cbaxes = fig.add_axes([0.1, 0.775, 0.8, 0.03])
cb = plt.colorbar(im, cax=cbaxes, label="System Age [Gyr]",
                  orientation="horizontal")

# Save!
fig.savefig("../Plots/lockedCPL.pdf", bbox_inches="tight", dpi=600)

### CTL ###

fig = plt.figure(figsize=(10,9))
gs = GridSpec(4,4, wspace=0.45)

ax = fig.add_subplot(gs[1:4,0:3])
ax_marg_y = fig.add_subplot(gs[1:4,3])

# Plot locked binaries
im = ax.scatter(ctl.iloc[inds]["Pri_dMass"][ctl.iloc[inds]["Locked"]],
                ctl.iloc[inds]["Pri_ProtAge"][ctl.iloc[inds]["Locked"]],
                c=ctl.iloc[inds]["Age"][ctl.iloc[inds]["Locked"]].values/1.0e9,
                cmap="viridis", marker="x", s=50, zorder=1, label="Locked")
# Not tidally locked binaries
im = ax.scatter(ctl.iloc[inds]["Pri_dMass"][~ctl.iloc[inds]["Locked"]],
                ctl.iloc[inds]["Pri_ProtAge"][~ctl.iloc[inds]["Locked"]],
                c=ctl.iloc[inds]["Age"][~ctl.iloc[inds]["Locked"]].values/1.0e9,
                cmap="viridis", marker="o", s=30, zorder=2, label="Not Locked")

# Format plot
ax.set_xlabel("Mass [M$_{\odot}$]", fontsize=28)
ax.set_xlim(np.min(ctl["Pri_dMass"]), np.max(ctl["Pri_dMass"]))
ax.set_ylabel("P$_{rot}$ [d]", fontsize=28)
ax.set_ylim(ylims)
ax.set_rasterization_zorder(0)
leg = ax.legend(loc="upper left", framealpha=0.0, fontsize=15)
for marker in leg.legendHandles:
    marker.set_color('k')

# Plot marginals
ax_marg_y.hist(ctl["Pri_ProtAge"][ctl["Locked"]], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C0",
               label="Locked", density=True)
ax_marg_y.hist(ctl["Pri_ProtAge"][~ctl["Locked"]], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C1",
               label="Not Locked", density=True)

# Format marginals
ax_marg_y.set_ylim(ylims)
ax_marg_y.legend(loc="best", framealpha=0.5, fontsize=11)
plt.setp(ax_marg_y.get_yticklabels(), visible=False);

# Now adding the colorbar
cbaxes = fig.add_axes([0.1, 0.775, 0.8, 0.03])
cb = plt.colorbar(im, cax=cbaxes, label="System Age [Gyr]",
                  orientation="horizontal")

# Save!
fig.savefig("../Plots/lockedCTL.pdf", bbox_inches="tight", dpi=600)

print("CPL locked Prot median:",np.median(cpl["Pri_ProtAge"][cpl["Locked"]]))
print("CPL unlocked Prot median:",np.median(cpl["Pri_ProtAge"][~cpl["Locked"]]))
print("CPL fraction of locked binaries:",np.mean(cpl["Locked"]))
print()
print("CTL locked Prot median:",np.median(ctl["Pri_ProtAge"][ctl["Locked"]]))
print("CTL unlocked Prot median:",np.median(ctl["Pri_ProtAge"][~ctl["Locked"]]))
print("CTL fraction of locked binaries:",np.mean(ctl["Locked"]))

# Done!
