"""

@author: David P. Fleming, University of Washington, Feb. 2019
@email: dflemin3 (at) uw (dot) edu

Analytic torque balance for CTL dw/dt and Matt+2015 magnetic braking.

"""

import numpy as np
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

#Typical plot parameters that make for pretty plots
mpl.rcParams['font.size'] = 22.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif'})
mpl.rc('text', usetex=True)

DAYSEC = 86400.0 # Number of seconds in a day

def ctlMatt2015Obj(Prot, Porb, k2Tau):
    """
    CTL, Matt+2015 torque balance
    """

    return (Prot**3 / Porb**5) * (1.0 - Porb/Prot) - 6.17e-16/k2Tau
# end function


def ctlMatt2015(Porb, logK2Tau):
    """
    Solve for the Prot such that dw/dt_tides + dw/dt_mg = 0

    Parameters
    ----------
    Porb : float
        Orbital period [d]
    logK2Tau : float
        log10(tidal time lag in s multipled by the Love number of degree 2, k2)

    Returns
    -------
    Prot : float
        rotation period [d] such that
    """

    # Convert Porb from [d] to [s]
    Pb = Porb*DAYSEC

    # Unlog k2Tau
    k2Tau = 10**logK2Tau

    # Solve assuming Porb as the initial guess
    Pr = fsolve(ctlMatt2015Obj, Pb, args=(Pb, k2Tau))[0]

    # Return Prot in [d]
    return Pr/DAYSEC
# end function

nbins = 100
logK2Taus = np.log10(0.5 * np.logspace(-1.8, 0.3, nbins))[::-1]
Porbs = np.linspace(20, 80, nbins)
res = np.zeros((nbins, nbins)) # = Prot/Peq

for ii in range(nbins):
    for jj in range(nbins):
        # Since e = 0, psi = 0, Peq = Porb in CTL model
        res[ii, jj] = ctlMatt2015(Porbs[ii], logK2Taus[jj])/Porbs[ii]

# Plot!
fig, ax = plt.subplots()

extent = [logK2Taus[0], logK2Taus[-1], Porbs[0], Porbs[-1]]
im = plt.imshow(res, cmap="viridis", aspect="auto", interpolation="nearest",
                origin="lower", extent=extent, vmin=1, vmax=1.5)

ax.set_xlabel(r"log$_{10}$($k_2 \tau$)")
ax.set_ylabel("Orbital Period [d]")

cbar = fig.colorbar(im)
cbar.set_label("P$_{rot}$/P$_{eq}$")

# Plot line at k2tau combination
ax.axvline(np.log10(0.5*0.1), lw=2.5, color="white", ls="--")

fig.savefig("../Plots/analyticTorque.pdf", bbox_inches="tight", dpi=200)
