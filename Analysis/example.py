"""

@author: David P. Fleming, University of Washington, Oct 2018
@email: dflemin3 (at) uw (dot) edu

This script plots the Prot evolution of 1-1 Msun binary undergoing stellar-tidal
evolution with Porb = 50 d for various tidal Qs and taus.

Interpretation:

For all stars, early spin down is due to stellar radius contraction along the
pre-main sequence.  All stars then begin to spin down over long timescales
due to magnetic braking and tidal torques in binaries. For the CPL model,
ALL binaries tidally lock while for the CTL model, only
binaries with tau > 0.1 s tidally lock.  Binaries with tau < 0.1 s have tides
that are weak and get overpowered by magnetic braking toques that spin down the
star.  Note how when CPL models tidally lock, it's in synchronous rotation
since e = 0.1  CTL models lock into slighty *supersynchronous* rotation since
Peq = f(e, Porb) * Porb where f(e, Porb) < 1 for e > 0. Binaries with sufficiently
large tau can also modify e owing to stronger tidal torques, working to
circularize the orbit, to stars with large tau have larger Peq due to smaller e.
For our choice of Q and tau, the CPL model has stronger torques than the CTL model,
locking systems earlier.  Note that for long Porb and for systems of a given age,
binaries will have longer Prot than single star systems owing to tidal torques
spinning-down the star towards the tidally locked state.  Using gyrochronlogy
models, this would incorrect making the systems appear old than they actually
are.

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

# Where simulation results live
qs = ["q4", "q5", "q6", "q7"]
taus = ["tau10", "tau1", "tau0_1", "tau0_01"]
colors = ["C0", "C1", "C2", "C3"]
labels = [r"$Q = 10^4, \tau = 10$ s",
          r"$Q = 10^5, \tau = 1$ s",
          r"$Q = 10^6, \tau = 10^{-1}$ s",
          r"$Q = 10^7, \tau = 10^{-2}$ s"]

### Plot! ###

fig, ax = plt.subplots()

for ii in range(len(qs)):

    # Qs
    qData = np.genfromtxt(os.path.join("../Sims/tauQ/",qs[ii],
                                       "bintide.secondary.forward"))

    # taus
    tauData = np.genfromtxt(os.path.join("../Sims/tauQ/",taus[ii],
                                         "bintide.secondary.forward"))

    ax.plot(qData[:,0], qData[:,5], lw=3, color=colors[ii], label=labels[ii],
            ls="-", zorder=1)
    ax.plot(tauData[:,0], tauData[:,5], lw=3, color=colors[ii], ls="--",
            zorder=1)

# Plot single star evolution
single = np.genfromtxt(os.path.join("../Sims/tauQ/single/bintide.primary.forward"))
ax.plot(single[:,0], single[:,2], lw=3, color="black", label="Single Star", zorder=2)

# Plot dummy lines for legend
ax.plot([100], [100], lw=3, ls="-", color="grey", label="CPL")
ax.plot([100], [100], lw=3, ls="--", color="grey", label="CTL")

# Format plot
ax.set_xlabel("Time [yr]", fontsize=30)
ax.set_ylabel("Rotation Period [d]", fontsize=30)
ax.set_xlim(1.0e7, qData[-1,0])
ax.set_xscale("log")
ax.set_ylim(0.05,60)
ax.set_yscale("log")
ax.legend(loc="upper left", framealpha=0.0, fontsize=16)

### INSET ###

inset = fig.add_axes([0.55, 0.2, 0.3, 0.3])

for ii in range(len(qs)):

    # Qs
    qData = np.genfromtxt(os.path.join("../Sims/tauQ/",qs[ii],
                                       "bintide.secondary.forward"))

    # taus
    tauData = np.genfromtxt(os.path.join("../Sims/tauQ/",taus[ii],
                                         "bintide.secondary.forward"))

    inset.plot(qData[:,0]/1.0e9, qData[:,5], lw=3, color=colors[ii], label=labels[ii],
            ls="-", zorder=1)
    inset.plot(tauData[:,0]/1.0e9, tauData[:,5], lw=3, color=colors[ii], ls="--",
            zorder=1)

# Plot single star evolution
single = np.genfromtxt(os.path.join("../Sims/tauQ/single/bintide.primary.forward"))
inset.plot(single[:,0]/1.0e9, single[:,2], lw=3, color="black", label="Single Star", zorder=2)

# Plot orbital period
inset.axhline(50.0, lw=3, ls="-.", color="k")

# Format plot
inset.set_xlabel("Time [Gyr]", fontsize=14)
inset.set_ylabel("Rotation Period [d]", fontsize=14)
inset.set_xlim(1.0e8/1.0e9, qData[-1,0]/1.0e9)
inset.set_ylim(20,52)
for tick in inset.xaxis.get_major_ticks():
                tick.label.set_fontsize(14)
for tick in inset.yaxis.get_major_ticks():
                tick.label.set_fontsize(14)

# Save!
fig.savefig("../Plots/example.pdf", bbox_inches="tight", dpi=600)

# Done!
