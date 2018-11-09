"""

@author: David P. Fleming, University of Washington, Oct 2018
@email: dflemin3 (at) uw (dot) edu

Determine approximate tidal Q for circular, non-synchronous orbit using Eqn. 18
from Leconte+2010 and Eqn. 19 for nearly synchronous orbits

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


DAYSEC = 86400.0 # Seconds in a day

def leconte18(w, tau, n=(2.0*np.pi/50.0)):
    """
    w : float
        rotation rate in 1/days
    tau : float
        tidal tau in s
    """
    return 1.0/(2.0*tau/DAYSEC*np.fabs(w-n))
# end function

def leconte19(tau, n=(2.0*np.pi/50.0)):
    """
    tau : float
        tidal tau in s
    """
    return 1.0/(tau/DAYSEC*n)
# end function

dir = "../Sims/LockingTest"

# saOutputOrder	Time -Radius -RotPer -RotRate -LostAngMom RadGyra -SurfEnFluxTotal
output = "bintide.primary.forward"

fig, ax = plt.subplots()

data = np.genfromtxt(os.path.join(dir, "tau0_1NoLock", output))
qeffNoSync = leconte18(data[:,3], 0.1)
qeffSync = leconte19(0.1)*np.ones(len(data))
ax.plot(data[:,0], qeffNoSync, lw=3, ls="-", color="C0", label=r"$\tau = 0.1$ s Non-Sync")
ax.plot(data[:,0], qeffSync, lw=3, ls="--", color="C0", label=r"$\tau = 0.1$ s Near Sync")

data = np.genfromtxt(os.path.join(dir, "tau0_01NoLock", output))
qeffNoSync = leconte18(data[:,3], 0.01)
qeffSync = leconte19(0.01)*np.ones(len(data))
ax.plot(data[:,0], qeffNoSync, lw=3, ls="-", color="C1", label=r"$\tau = 0.01$ s Non-Sync")
ax.plot(data[:,0], qeffSync, lw=3, ls="--", color="C1", label=r"$\tau = 0.01$ s Near Sync")

ax.set_xlabel("Time [Gyr]")
ax.set_ylabel("Effective Tidal Q")
ax.set_xscale("log")
ax.set_yscale("log")
ax.legend(loc="best", framealpha=0, fontsize=12)

plt.show()
