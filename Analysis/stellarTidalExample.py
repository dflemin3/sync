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
mpl.rcParams['font.size'] = 22.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

# Path to sim results
cplDir = "../Sims/StellarTidalExample/CPL"
ctlDir = "../Sims/StellarTidalExample/CTL"

# When each system tidally locked in yr
cplLock = 2.855941e+07
ctlLock = 3.126642e+07

# Load data
# saOutputOrder	Time -TotEn -TotAngMom -Semim -Radius -RotPer Ecce -RotRate -MeanMotion -OrbPer RadGyra -SurfEnFluxTotal
cpl = np.genfromtxt(os.path.join(cplDir,"bintide.secondary.forward"))
ctl = np.genfromtxt(os.path.join(ctlDir,"bintide.secondary.forward"))

# Plot e, Porb, Prot
fig, axes = plt.subplots(ncols=3, figsize=(16,6), sharex=True)

# Left: e
axes[0].plot(cpl[:,0], cpl[:,6], lw=3, ls="-", color="C0", label="CPL")
axes[0].plot(ctl[:,0], ctl[:,6], lw=3, ls="-", color="C1", label="CTL")

axes[0].set_ylabel("Eccentricity")
axes[0].legend(loc="best", framealpha=0)

# Middle: Porb
axes[1].plot(cpl[:,0], cpl[:,9], lw=3, ls="-", color="C0", label="CPL")
axes[1].plot(ctl[:,0], ctl[:,9], lw=3, ls="-", color="C1", label="CTL")

axes[1].set_ylabel("Orbital Period [d]")

# Right: Prot
axes[2].plot(cpl[:,0], cpl[:,5], lw=3, ls="-", color="C0", label="CPL")
axes[2].plot(ctl[:,0], ctl[:,5], lw=3, ls="-", color="C1", label="CTL")

axes[2].axvline(cplLock, lw=3, ls="--", color="C0")
axes[2].axvline(ctlLock, lw=3, ls="--", color="C1")

axes[2].set_ylabel("Rotation Period [d]")

# Format all axes
for ax in axes:
    ax.set_xlim(1.0e6, cpl[-1,0])
    ax.set_xscale("log")
    ax.set_xlabel("Time [yr]")

# Save!
fig.tight_layout()
fig.savefig("../Plots/stellarTidalExample.pdf",bbox_inches="tight", dpi=600)
