"""

@author: David P. Fleming, University of Washington, Oct 2018
@email: dflemin3 (at) uw (dot) edu

Examing our tidal locking prescription in the weak-tides regime (large Porb
and large Q/small tau).

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

dir = "../Sims/LockingTest"

# saOutputOrder	Time -Radius -RotPer -RotRate -LostAngMom RadGyra -SurfEnFluxTotal
output = "bintide.primary.forward"

fig, ax = plt.subplots()

### CPL PLOTS ###

# Plot Qs
data = np.genfromtxt(os.path.join(dir, "q7", output))
ax.plot(data[:,0]/1.0e9, data[:,2], lw=3, ls="-", color="C0", label="$Q = 10^7$")

data = np.genfromtxt(os.path.join(dir, "q8", output))
ax.plot(data[:,0]/1.0e9, data[:,2], lw=3, ls="-", color="C1", label="$Q = 10^8$")

# Plot Qs: No Locking
data = np.genfromtxt(os.path.join(dir, "q7NoLock", output))
ax.plot(data[:,0]/1.0e9, data[:,2], lw=3, ls="--", color="C0",
        label="$Q = 10^7$, No Lock")

data = np.genfromtxt(os.path.join(dir, "q8NoLock", output))
ax.plot(data[:,0]/1.0e9, data[:,2], lw=3, ls="--", color="C1",
        label="$Q = 10^8$, No Lock")

# Plot taus
data = np.genfromtxt(os.path.join(dir, "tau0_1", output))
ax.plot(data[:,0]/1.0e9, data[:,2], lw=3, ls="-", color="C2", label=r"$\tau = 0.1$ s")

data = np.genfromtxt(os.path.join(dir, "tau0_01", output))
ax.plot(data[:,0]/1.0e9, data[:,2], lw=3, ls="-", color="C3", label=r"$\tau = 0.01$ s")

# Plot Qs: No Locking
data = np.genfromtxt(os.path.join(dir, "tau0_1NoLock", output))
ax.plot(data[:,0]/1.0e9, data[:,2], lw=3, ls="--", color="C2",
        label=r"$\tau = 0.1$ s, No Lock")

data = np.genfromtxt(os.path.join(dir, "tau0_01NoLock", output))
ax.plot(data[:,0]/1.0e9, data[:,2], lw=3, ls="--", color="C3",
        label=r"$\tau = 0.01$ s, No Lock")

# Plot Single Star
data = np.genfromtxt(os.path.join(dir, "single", output))
ax.plot(data[:,0]/1.0e9, data[:,2], lw=3, ls="-", color="k", label="Single Star")

ax.set_xlabel("Time [Gyr]")
ax.set_xlim(5, 8)
ax.set_ylim(49, 51)
ax.set_ylabel("Rotation Period [d]")
ax.legend(loc="best", framealpha=0, fontsize=12)

fig.savefig("../Plots/qLockTest.pdf", bbox_inches="tight", dpi=600)
