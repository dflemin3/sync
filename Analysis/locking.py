"""

@author: David P Fleming, University of Washington, Nov 2018
@email dflemin3 (at) uw (dot) edu

Plot to show which binaries are tidally locked in mass-Prot space by the age of
the system for both the CPL and CTL models.  We randomly assigned ages to systems
from a uniform distribution over 1-7 Gyr, broadly consistent with stellar ages
in the Kepler field.

Script Output:

CPL Prot median: 31.550073499999996
CPL locked Prot median: 22.636840499999998
CPL unlocked Prot median: 32.429345
CPL interacting Prot median: 43.517854
CPL fraction of locked binaries: 0.2354
CPL fraction of not locked but interacting binaries: 0.071
CPL fraction of locked binaries with Prot < 20 d: 0.46219201359388273

CTL Prot median: 31.293733500000002
CTL locked Prot median: 8.751350500000001
CTL unlocked Prot median: 32.4363845
CTL interacting Prot median: 36.4195355
CTL fraction of locked binaries: 0.0816
CTL fraction of not locked but interacting binaries: 0.157
CTL fraction of locked binaries with Prot < 20 d: 0.8308823529411765

Age Stats:
CPL locked Age median: 4.445921424688489
CPL unlocked Age median: 3.6702531621032675
CPL interacting Age median: 5.050168624194712

CTL locked Age median: 3.9992385987802774
CTL unlocked Age median: 3.8249306365530074
CTL interacting Age median: 4.683332960365213

Porb Stats:
CPL locked Porb median: 23.502239499999998
CPL unlocked Porb median: 62.8394635
CPL interacting Porb median: 48.727921499999994

CTL locked Porb median: 9.3593115
CTL unlocked Porb median: 60.113932999999996
CTL interacting Porb median: 41.761252999999996

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
xlims = [0.1, 1]
bins = "auto"
num = 2500
seed = 42

np.random.seed(seed)

# Load in data
cpl = pd.read_csv("../Data/mcCPLMarch27.csv")
ctl = pd.read_csv("../Data/mcCTLMarch27.csv")

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

### CPL ###

fig = plt.figure(figsize=(9,8.5))

gs = GridSpec(3, 3, width_ratios=[1, 0.01, 0.25], wspace=0.05,
              height_ratios=[0.25, 0.01, 1], hspace=0.05)

# Main panel
ax = fig.add_subplot(gs[2, 0])

# Not tidally locked binaries: sub and super sync populations
x = cpl.iloc[inds]["Pri_dMass"][cpl.iloc[inds]["Free"]]
y = cpl.iloc[inds]["Pri_ProtAge"][cpl.iloc[inds]["Free"]]
im = ax.scatter(x, y, color="C1", marker="o", s=30, zorder=1, label="Not Locked")

# Not locked, but strongly tidally interacting
x = cpl.iloc[inds]["Pri_dMass"][cpl.iloc[inds]["Interacting"]]
y = cpl.iloc[inds]["Pri_ProtAge"][cpl.iloc[inds]["Interacting"]]
color = (cpl.iloc[inds]["Pri_ProtAge"][cpl.iloc[inds]["Interacting"]]/cpl.iloc[inds]["Age_Peq"][cpl.iloc[inds]["Interacting"]]).values
im = ax.scatter(x, y, color="C2", marker="d", s=50, zorder=2, label="Interacting")

# Plot locked binaries
x = cpl.iloc[inds]["Pri_dMass"][cpl.iloc[inds]["Locked"]]
y = cpl.iloc[inds]["Pri_ProtAge"][cpl.iloc[inds]["Locked"]]
color = (cpl.iloc[inds]["Pri_ProtAge"][cpl.iloc[inds]["Locked"]]/cpl.iloc[inds]["Age_Peq"][cpl.iloc[inds]["Locked"]]).values
im = ax.scatter(x, y, color="C0", marker="x", s=50, zorder=3, label="Locked")

# Format plot
ax.set_xlabel(r"Mass [M$_{\odot}$]", fontsize=30)
ax.set_xlim(np.min(cpl["Pri_dMass"]), np.max(cpl["Pri_dMass"]))
ax.set_ylabel("P$_{rot}$ [d]", fontsize=30)
ax.set_ylim(ylims)
ax.set_rasterization_zorder(0)
leg = ax.legend(loc="upper left", framealpha=0.7, fontsize=18)

# Plot marginals: y for prot
ax_marg_y = fig.add_subplot(gs[2, 2])

ax_marg_y.hist(cpl["Pri_ProtAge"][cpl["Free"]], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C1",
               label="Not Locked", density=False)
ax_marg_y.hist(cpl["Pri_ProtAge"][cpl["Interacting"]], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C2",
               label="Interacting", density=False)
ax_marg_y.hist(cpl["Pri_ProtAge"][cpl["Locked"]], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C0",
               label="Locked", density=False)

# Format marginals
ax_marg_y.set_ylim(ylims)
ax_marg_y.legend(loc="upper center", framealpha=0.5, fontsize=12)
plt.setp(ax_marg_y.get_yticklabels(), visible=False);

# Plot marginals: x for mass
ax_marg_x = fig.add_subplot(gs[0, 0])

ax_marg_x.hist(cpl["Pri_dMass"][cpl["Free"]],
               bins=bins, histtype="step", lw=3, color="C1",
               label="Not Locked", density=False)
ax_marg_x.hist(cpl["Pri_dMass"][cpl["Interacting"]],
               bins=bins, histtype="step", lw=3, color="C2",
               label="Interacting", density=False)
ax_marg_x.hist(cpl["Pri_dMass"][cpl["Locked"]],
               bins=bins, histtype="step", lw=3, color="C0",
               label="Locked", density=False)

# Format marginals
ax_marg_x.set_xlim(xlims)
plt.setp(ax_marg_x.get_xticklabels(), visible=False);

# Annotate with model name
ax.text(1.15, 117, "CPL", ha="center", va="center", size=30, color="k")

# Save!
fig.savefig("../Plots/lockedCPL.pdf", bbox_inches="tight", dpi=200)

### CTL ###

fig = plt.figure(figsize=(9,8.5))

gs = GridSpec(3, 3, width_ratios=[1, 0.01, 0.25], wspace=0.05,
              height_ratios=[0.25, 0.01, 1], hspace=0.05)

# Main panel
ax = fig.add_subplot(gs[2, 0])

# Not tidally locked binaries: sub and super sync populations
x = ctl.iloc[inds]["Pri_dMass"][ctl.iloc[inds]["Free"]]
y = ctl.iloc[inds]["Pri_ProtAge"][ctl.iloc[inds]["Free"]]
im = ax.scatter(x, y, color="C1", marker="o", s=30, zorder=1, label="Not Locked")

# Not locked, but strongly tidally interacting
x = ctl.iloc[inds]["Pri_dMass"][ctl.iloc[inds]["Interacting"]]
y = ctl.iloc[inds]["Pri_ProtAge"][ctl.iloc[inds]["Interacting"]]
color = (ctl.iloc[inds]["Pri_ProtAge"][ctl.iloc[inds]["Interacting"]]/ctl.iloc[inds]["Age_Peq"][ctl.iloc[inds]["Interacting"]]).values
im = ax.scatter(x, y, color="C2", marker="d", s=50, zorder=2, label="Interacting")

# Plot locked binaries
x = ctl.iloc[inds]["Pri_dMass"][ctl.iloc[inds]["Locked"]]
y = ctl.iloc[inds]["Pri_ProtAge"][ctl.iloc[inds]["Locked"]]
color = (ctl.iloc[inds]["Pri_ProtAge"][ctl.iloc[inds]["Locked"]]/ctl.iloc[inds]["Age_Peq"][ctl.iloc[inds]["Locked"]]).values
im = ax.scatter(x, y, color="C0", marker="x", s=50, zorder=3, label="Locked")

# Format plot
ax.set_xlabel(r"Mass [M$_{\odot}$]", fontsize=30)
ax.set_xlim(np.min(ctl["Pri_dMass"]), np.max(ctl["Pri_dMass"]))
ax.set_ylabel("P$_{rot}$ [d]", fontsize=30)
ax.set_ylim(ylims)
ax.set_rasterization_zorder(0)
leg = ax.legend(loc="upper left", framealpha=0.7, fontsize=18)

# Plot marginals: y for prot
ax_marg_y = fig.add_subplot(gs[2, 2])

ax_marg_y.hist(ctl["Pri_ProtAge"][ctl["Free"]], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C1",
               label="Not Locked", density=False)
ax_marg_y.hist(ctl["Pri_ProtAge"][ctl["Interacting"]], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C2",
               label="Interacting", density=False)
ax_marg_y.hist(ctl["Pri_ProtAge"][ctl["Locked"]], orientation="horizontal",
               bins=bins, histtype="step", lw=3, color="C0",
               label="Locked", density=False)

# Format marginals
ax_marg_y.set_ylim(ylims)
ax_marg_y.legend(loc="upper center", framealpha=0.5, fontsize=12)
plt.setp(ax_marg_y.get_yticklabels(), visible=False);

# Plot marginals: x for mass
ax_marg_x = fig.add_subplot(gs[0, 0])

ax_marg_x.hist(ctl["Pri_dMass"][ctl["Free"]],
               bins=bins, histtype="step", lw=3, color="C1",
               label="Not Locked", density=False)
ax_marg_x.hist(ctl["Pri_dMass"][ctl["Interacting"]],
               bins=bins, histtype="step", lw=3, color="C2",
               label="Interacting", density=False)
ax_marg_x.hist(ctl["Pri_dMass"][ctl["Locked"]],
               bins=bins, histtype="step", lw=3, color="C0",
               label="Locked", density=False)

# Format marginals
ax_marg_x.set_xlim(xlims)
plt.setp(ax_marg_x.get_xticklabels(), visible=False);

# Annotate with model name
ax.text(1.15, 117, "CTL", ha="center", va="center", size=30, color="k")

# Save!
fig.savefig("../Plots/lockedCTL.pdf", bbox_inches="tight", dpi=200)

# Output interesting statistics

# Prots in d
print("CPL Prot median:",np.median(cpl["Pri_ProtAge"]))
print("CPL locked Prot median:",np.median(cpl["Pri_ProtAge"][cpl["Locked"]]))
print("CPL unlocked Prot median:",np.median(cpl["Pri_ProtAge"][cpl["Free"]]))
print("CPL interacting Prot median:",np.median(cpl["Pri_ProtAge"][cpl["Interacting"]]))
print("CPL fraction of locked binaries:",np.mean(cpl["Locked"]))
print("CPL fraction of not locked but interacting binaries:",np.mean(cpl["Interacting"]))
val = np.sum(cpl["Locked"][cpl["Pri_ProtAge"] <= 20])/np.sum(cpl["Locked"])
print("CPL fraction of locked binaries with Prot < 20 d:",val)
print()
print("CTL Prot median:",np.median(ctl["Pri_ProtAge"]))
print("CTL locked Prot median:",np.median(ctl["Pri_ProtAge"][ctl["Locked"]]))
print("CTL unlocked Prot median:",np.median(ctl["Pri_ProtAge"][ctl["Free"]]))
print("CTL interacting Prot median:",np.median(ctl["Pri_ProtAge"][ctl["Interacting"]]))
print("CTL fraction of locked binaries:",np.mean(ctl["Locked"]))
print("CTL fraction of not locked but interacting binaries:",np.mean(ctl["Interacting"]))
val = np.sum(ctl["Locked"][ctl["Pri_ProtAge"] <= 20])/np.sum(ctl["Locked"])
print("CTL fraction of locked binaries with Prot < 20 d:",val)
print()

# Ages in Gyr
print("Age Stats:")
print("CPL locked Age median:",np.median(cpl["Age"][cpl["Locked"]]/1.0e9))
print("CPL unlocked Age median:",np.median(cpl["Age"][cpl["Free"]]/1.0e9))
print("CPL interacting Age median:",np.median(cpl["Age"][cpl["Interacting"]]/1.0e9))
print()
print("CTL locked Age median:",np.median(ctl["Age"][ctl["Locked"]]/1.0e9))
print("CTL unlocked Age median:",np.median(ctl["Age"][ctl["Free"]]/1.0e9))
print("CTL interacting Age median:",np.median(ctl["Age"][ctl["Interacting"]]/1.0e9))
print()

# Porbs in d
print("Porb Stats:")
print("CPL locked Porb median:",np.median(cpl["Age_Porb"][cpl["Locked"]]))
print("CPL unlocked Porb median:",np.median(cpl["Age_Porb"][cpl["Free"]]))
print("CPL interacting Porb median:",np.median(cpl["Age_Porb"][cpl["Interacting"]]))
print()
print("CTL locked Porb median:",np.median(ctl["Age_Porb"][ctl["Locked"]]))
print("CTL unlocked Porb median:",np.median(ctl["Age_Porb"][ctl["Free"]]))
print("CTL interacting Porb median:",np.median(ctl["Age_Porb"][ctl["Interacting"]]))

# Make histograms of CPL, CTL Prot and Porb for 3 classifications: Diagnostic version

### CPL ###
fig, axes = plt.subplots(ncols=2, figsize=(17, 8), sharey=True)
ax0 = axes[0]
ax1 = axes[1]

# Prot
ax0.hist(cpl["Pri_ProtAge"][cpl["Free"]],
         bins=bins, histtype="step", lw=3, color="C1",
         label="Not Locked", density=True, ls="-", range=[0,100])
ax0.hist(cpl["Pri_ProtAge"][cpl["Interacting"]],
         bins=bins, histtype="step", lw=3, color="C2",
         label="Interacting", density=True, ls="-", range=[0,100])
ax0.hist(cpl["Pri_ProtAge"][cpl["Locked"]],
         bins=bins, histtype="step", lw=3, color="C0",
         label="Locked", density=True, ls="-", range=[0,100])

# Porb
ax0.hist(cpl["Age_Porb"][cpl["Free"]],
         bins=bins, histtype="step", lw=3, color="C1",
         label="", density=True, ls="--", range=[0,100])
ax0.hist(cpl["Age_Porb"][cpl["Interacting"]],
         bins=bins, histtype="step", lw=3, color="C2",
         label="", density=True, ls="--", range=[0,100])
ax0.hist(cpl["Age_Porb"][cpl["Locked"]],
         bins=bins, histtype="step", lw=3, color="C0",
         label="", density=True, ls="--", range=[0,100])

# Format marginals
ax0.set_xlim(0,100)
ax0.set_ylim(0, 0.0325)
ax0.set_xlabel("Period [d]", fontsize=30)
ax0.set_ylabel("Normalized Counts", fontsize=30)

### CTL ###

# Prot
ax1.hist(ctl["Pri_ProtAge"][ctl["Free"]],
         bins=bins, histtype="step", lw=3, color="C1",
         label="Not Locked", density=True, ls="-", range=[0,100])
ax1.hist(ctl["Pri_ProtAge"][ctl["Interacting"]],
         bins=bins, histtype="step", lw=3, color="C2",
         label="Interacting", density=True, ls="-", range=[0,100])
ax1.hist(ctl["Pri_ProtAge"][ctl["Locked"]],
         bins=bins, histtype="step", lw=3, color="C0",
         label="Locked", density=True, ls="-", range=[0,100])

# Porb
ax1.hist(ctl["Age_Porb"][ctl["Free"]],
         bins=bins, histtype="step", lw=3, color="C1",
         label="", density=True, ls="--", range=[0,100])
ax1.hist(ctl["Age_Porb"][ctl["Interacting"]],
         bins=bins, histtype="step", lw=3, color="C2",
         label="", density=True, ls="--", range=[0,100])
ax1.hist(ctl["Age_Porb"][ctl["Locked"]],
         bins=bins, histtype="step", lw=3, color="C0",
         label="", density=True, ls="--", range=[0,100])

# Dummy lines for legend
ax1.plot([500], [500], lw=3, ls="-", color="grey", label="P$_{rot}$")
ax1.plot([500], [500], lw=3, ls="--", color="grey", label="P$_{orb}$")

# Format marginals
ax1.set_xlim(0,100)
ax1.set_ylim(0, 0.0325)
ax1.set_xlabel("Period [d]", fontsize=30)
ax1.legend(loc="best", framealpha=0.0, fontsize=17)

fig.tight_layout()
fig.savefig("../Plots/lockedProtPorbHist.pdf", bbox_inches="tight", dpi=200)

# Make histograms of CPL, CTL Prot and Porb for 3 classifications: Paper version
fig, ax = plt.subplots()

# CPL
ax.hist(cpl["Pri_ProtAge"][cpl["Interacting"]],
        bins=bins, histtype="step", lw=3, color="C2",
        label="Interacting", density=True, ls="-", range=[0,100])
ax.hist(cpl["Pri_ProtAge"][cpl["Locked"]],
        bins=bins, histtype="step", lw=3, color="C0",
        label="Locked", density=True, ls="-", range=[0,100])

# CTL
ax.hist(ctl["Pri_ProtAge"][ctl["Interacting"]],
        bins=bins, histtype="step", lw=3, color="C2", density=True, ls="--",
        range=[0,100], label="")
ax.hist(ctl["Pri_ProtAge"][ctl["Locked"]],
        bins=bins, histtype="step", lw=3, color="C0", density=True, ls="--",
        range=[0,100], label="")

# Dummy lines for legend
ax.plot([500], [500], lw=3, ls="-", color="grey", label="CPL")
ax.plot([500], [500], lw=3, ls="--", color="grey", label="CTL")

# Format marginals
ax.set_xlim(0,100)
ax.set_ylim(0, 0.0325)
ax.set_xlabel("Rotation Period [d]", fontsize=30)
ax.set_ylabel("Normalized Counts", fontsize=30)
ax.legend(loc="upper right", fontsize=20)

fig.tight_layout()
fig.savefig("../Plots/lockedProtHist.pdf", bbox_inches="tight", dpi=200)

# Done!
