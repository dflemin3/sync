"""

@author: David P. Fleming, University of Washington, Oct 2018
@email: dflemin3 (at) uw (dot) edu

This script plots stellar-tidal evolution

"""

import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (9,8)
mpl.rcParams['font.size'] = 23.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

# Path to sim results
cplDir = "../Sims/CPLTestReiners"
ctlDir = "../Sims/CTLTestReiners"
logfile_name = "bintides.log"
dirs = ["5", "10", "20", "30", "40", "50", "60"]
colors = ["C0", "C1", "C2", "C3", "C4", "C5", "C6"]
YEARSEC = 3.154e+7 # Seconds per year
DAYSEC = 24.0*3600.0 # Seconds per day

### Two Panel Plot ###

fig, axes = plt.subplots(ncols=2, figsize=(14, 6))

for ii, dir in enumerate(dirs):
    # Load data
    # saOutputOrder	Time -TotEn -TotAngMom -Radius -RotPer -EqRotPer DRotPerDtEqtide DRotPerDtStellar Ecce -OrbPer RadGyra -SurfEnFluxTotal
    cpl = np.genfromtxt(os.path.join(cplDir, dir, "bintides.secondary.forward"))
    ctl = np.genfromtxt(os.path.join(ctlDir, dir, "bintides.secondary.forward"))

    # Pull LockTimes out of logfile
    with open(os.path.join(os.path.join(cplDir, dir, logfile_name)), 'r') as f:
        logfile_in = f.read()

    matches = []
    for line in logfile_in.split("\n"):
        if line.startswith("(LockTime)"):
            matches.append((line.split()[-1]))

    # Convert lock times to years
    dLockTimeCPL = float(matches[3])/YEARSEC

    # Pull LockTimes out of logfile
    with open(os.path.join(os.path.join(ctlDir, dir, logfile_name)), 'r') as f:
        logfile_in = f.read()

    matches = []
    for line in logfile_in.split("\n"):
        if line.startswith("(LockTime)"):
            matches.append((line.split()[-1]))

    # Convert lock times to years
    dLockTimeCTL = float(matches[3])/YEARSEC

    # Find index in time array that corresponds to when simulation tidally locks
    if dLockTimeCPL < 0:
        iLockIndCPL = -1
    else:
        iLockIndCPL = np.argmin(np.fabs(cpl[:,0]-dLockTimeCPL))
    if dLockTimeCTL < 0:
        iLockIndCTL = -1
    else:
        iLockIndCTL = np.argmin(np.fabs(ctl[:,0]-dLockTimeCTL))

    # Left: Prot/Peq
    axes[0].plot(cpl[:,0], cpl[:,4]/cpl[:,5], lw=2.5, ls="-", color=colors[ii])
    axes[0].plot(ctl[:,0], ctl[:,4]/ctl[:,5], lw=2.5, ls="--", color=colors[ii])

    # Right: dProt/dt
    cplDeriv = (cpl[:,6] + cpl[:,7])*YEARSEC/DAYSEC*1.0e9
    ctlDeriv = (ctl[:,6] + ctl[:,7])*YEARSEC/DAYSEC*1.0e9
    axes[1].plot(cpl[:iLockIndCPL,0], cplDeriv[:iLockIndCPL], lw=2, ls="-",
                 color=colors[ii], label="P$_{orb}$ = %s d" % dir)
    axes[1].plot(ctl[:iLockIndCTL,0], ctlDeriv[:iLockIndCTL], lw=2, ls="--",
                 color=colors[ii])

axes[1].plot([100], [100], lw=3, ls="-", color="grey", label="CPL")
axes[1].plot([100], [100], lw=3, ls="--", color="grey", label="CTL")

# Format left axis
axes[0].set_ylabel("P$_{rot}$/P$_{eq}$", fontsize=25)
axes[0].set_xlabel("Time [yr]", fontsize=25)
axes[0].set_xscale("log")
axes[0].axhline(1, lw=2.5, ls=":", color="k")
axes[0].set_xlim(1.0e6, cpl[-1,0])
axes[0].set_ylim(0, 1.2)

axes[0].text(1.05e6, 1.14, "Reiners \& Mohanty (2012)",
         ha="left", va="center", size=17, color="black", zorder=100)

# Format right axis
axes[1].set_ylabel("$d$P$_{rot}$/$dt$ [d/Gyr]", fontsize=25)
axes[1].set_xlabel("Time [yr]", fontsize=25)
axes[1].set_xlim(1.0e6, cpl[-1,0])
axes[1].legend(loc="lower center", framealpha=0.75, fontsize=13.5, ncol=3)
axes[1].set_xscale("log")
axes[1].set_yscale("symlog")
axes[1].axhline(0, lw=2.5, ls=":", color="k")

# Save!
fig.tight_layout()
fig.savefig("../Plots/eqPerTwoPanelReiners.pdf",bbox_inches="tight", dpi=600)

### One Panel Plot ###

fig, ax = plt.subplots(figsize=(9,8))

for ii, dir in enumerate(dirs):
    # Load data
    # saOutputOrder	Time -TotEn -TotAngMom -Radius -RotPer -EqRotPer
    # DRotPerDtEqtide DRotPerDtStellar Ecce -OrbPer RadGyra -SurfEnFluxTotal
    cpl = np.genfromtxt(os.path.join(cplDir, dir, "bintides.secondary.forward"))
    ctl = np.genfromtxt(os.path.join(ctlDir, dir, "bintides.secondary.forward"))

    # Left: Prot/Peq
    ax.plot(cpl[:,0], cpl[:,4]/cpl[:,5], lw=3, ls="-", color=colors[ii],
            label="P$_{orb}$ = %s d" % dir)
    ax.plot(ctl[:,0], ctl[:,4]/ctl[:,5], lw=3, ls="--", color=colors[ii])

# Format left axis
ax.plot([100], [100], lw=3, ls="-", color="grey", label="CPL")
ax.plot([100], [100], lw=3, ls="--", color="grey", label="CTL")

ax.legend(loc="best", framealpha=0, fontsize=18, bbox_to_anchor=[1,1])
ax.set_ylabel("P$_{rot}$/P$_{eq}$", fontsize=30)
ax.set_xlabel("Time [yr]", fontsize=30)
ax.set_xscale("log")
ax.axhline(1, lw=2.5, ls=":", color="k")
ax.set_xlim(1.0e6, cpl[-1,0])
ax.set_ylim(0, 1.3)

# Save!
fig.savefig("../Plots/eqPerReiners.pdf", bbox_inches="tight", dpi=600)

### Short Porb Plot ###

ctlDir = "../Sims/PeqReiners"
cplDir = "../Sims/PeqReiners"
ctlDirs = ["0.1", "0.01", "0.001"]
cplDirs = ["6", "7", "8"]
labels = [r"$Q= 10^6$, $\tau = 10^{-1}$ s", r"$Q=10^7$, $\tau = 10^{-2}$ s",
          r"$Q=10^8$, $\tau = 10^{-3}$ s"]

fig, ax = plt.subplots(figsize=(9,8))

for ii in range(len(ctlDirs)):
    # Load data
    # saOutputOrder	Time -TotEn -TotAngMom -Radius -RotPer -EqRotPer
    # DRotPerDtEqtide DRotPerDtStellar Ecce -OrbPer RadGyra -SurfEnFluxTotal
    ctl = np.genfromtxt(os.path.join(ctlDir, ctlDirs[ii], "bintides.secondary.forward"))
    cpl = np.genfromtxt(os.path.join(cplDir, cplDirs[ii], "bintides.secondary.forward"))

    # Prot/Peq
    ax.plot(cpl[:,0], cpl[:,4]/cpl[:,5], lw=3, ls="-", color="C%d" % ii,
            label=labels[ii])
    ax.plot(ctl[:,0], ctl[:,4]/ctl[:,5], lw=3, ls="--", color="C%d" % ii)

ax.plot([100], [100], ls="-", lw=3, color="grey", label="CPL")
ax.plot([100], [100], ls="--", lw=3, color="grey", label="CTL")

ax.legend(loc="lower right", framealpha=0, fontsize=15)
ax.set_ylabel("P$_{rot}$/P$_{eq}$", fontsize=30)
ax.set_xlabel("Time [yr]", fontsize=30)
ax.set_xscale("log")
ax.axhline(1, lw=2.5, ls=":", color="k")
ax.set_xlim(1.0e6, cpl[-1,0])
ax.set_ylim(0, 2.5)

# Save!
fig.savefig("../Plots/eqPerShortPorbReiners.pdf", bbox_inches="tight", dpi=600)
