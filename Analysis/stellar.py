
"""

@author: David P Fleming, University of Washington, Oct 2018
@email dflemin3 (at) uw (dot) edu

This script examines our stellar evolution model, a bicubic interpolation of the
Baraffe+2015 stellar evolution model, coupled with the Matt+2015 magnetic
braking model.

"""

import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (9,8)
mpl.rcParams['font.size'] = 25.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif','serif':['Computer Modern']})
mpl.rc('text', usetex=True)

# Read in output files
path = "../Sims/StellarEvolution/"

# saOutputOrder Time -Radius -RotPer RadGyra
g = np.genfromtxt(os.path.join(path,"stellar.g.forward"))
k = np.genfromtxt(os.path.join(path,"stellar.k.forward"))
m = np.genfromtxt(os.path.join(path,"stellar.m.forward"))

# All on same time grid
time = g[:,0]

# Find time indices of approximate ZAMS times from Henny Lamers'
# stellar evolution notes
ind_g = np.argmin(np.fabs(time-6.2e7))
ind_k = np.argmin(np.fabs(time-1.0e8))
ind_m = np.argmin(np.fabs(time-3.0e8))

# Plot!
ncols = 3
fig, ax = plt.subplots(ncols=ncols, figsize=(9*ncols,8))

# Left panel: Stellar radius evolution
ax[0].plot(time, g[:,1], lw=2.5, color="C0", label=r"$1$ M$_{\odot}$")
ax[0].plot(time, k[:,1], lw=2.5, color="C1", label=r"$0.7$ M$_{\odot}$")
ax[0].plot(time, m[:,1], lw=2.5, color="C2", label=r"$0.2$ M$_{\odot}$")

# Plot points to indicate ZAMS
ax[0].scatter(time[ind_g], g[ind_g,1], s=75, color="C0")
ax[0].scatter(time[ind_k], k[ind_k,1], s=75, color="C1")
ax[0].scatter(time[ind_m], m[ind_m,1], s=75, color="C2")

# Format
ax[0].legend()
ax[0].set_ylabel("Radius [R$_{\odot}$]")
ax[0].set_xlabel("$t - t_0$ [yr]")

ax[0].set_xlim(1.0e6,time[-1])
ax[0].set_xscale("log")

# Middle panel: Stellar radius of gyration evolution
ax[1].plot(time, g[:,5], lw=2.5, color="C0")
ax[1].plot(time, k[:,3], lw=2.5, color="C1")
ax[1].plot(time, m[:,3], lw=2.5, color="C2")

# Plot points to indicate ZAMS
ax[1].scatter(time[ind_g], g[ind_g,5], s=75, color="C0")
ax[1].scatter(time[ind_k], k[ind_k,3], s=75, color="C1")
ax[1].scatter(time[ind_m], m[ind_m,3], s=75, color="C2")

# Format
ax[1].set_ylabel("Radius of Gyration")
ax[1].set_xlabel("$t - t_0$ [yr]")
ax[1].set_xlim(1.0e6,time[-1])
ax[1].set_xscale("log")

# Right panel: Stellar rotation period evolution
ax[2].plot(time, g[:,2], lw=2.5, color="C0")
ax[2].plot(time, k[:,2], lw=2.5, color="C1")
ax[2].plot(time, m[:,2], lw=2.5, color="C2")

# Plot points to indicate ZAMS
ax[2].scatter(time[ind_g], g[ind_g,2], s=75, color="C0")
ax[2].scatter(time[ind_k], k[ind_k,2], s=75, color="C1")
ax[2].scatter(time[ind_m], m[ind_m,2], s=75, color="C2")

# Format
ax[2].set_ylabel("Rotation Period [d]")
ax[2].set_xlabel("$t - t_0$ [yr]")
ax[2].set_xlim(1.0e6,time[-1])
ax[2].set_ylim(0.5e-1,1.0e2)
ax[2].set_xscale("log")
ax[2].set_yscale("log")

# Save!
fig.tight_layout()
fig.savefig("../Plots/stellarExample.pdf", bbox_inches="tight")
