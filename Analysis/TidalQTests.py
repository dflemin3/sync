import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os

#Typical plot parameters that make for pretty plots
mpl.rcParams['figure.figsize'] = (9,8)
mpl.rcParams['font.size'] = 22.0

## for Palatino and other serif fonts use:
mpl.rc('font',**{'family':'serif','serif':['Computer Modern']})
mpl.rc('text', usetex=True)

# Read in Data
path = "../Sims/TidalLocking"

dirs = [""]

# Note the output order
# saOutputOrder   Time -RotPer -OrbPer Ecce -TotEn -TotAngMom
tides_50_dirs = ["50_4","50_5","50_6","50_7"]
labels = ["$Q = 10^4$", "$Q = 10^5$", "$Q = 10^6$", "$Q = 10^7$"]
colors = ["C%d" % ii for ii in range(len(tides_50_dirs))]

# Extract data
notides = np.genfromtxt(os.path.join(path,"NoTides","notides.secondary.forward"))

tides_50 = []

for direct in tides_50_dirs:
    tides_50.append(np.genfromtxt(os.path.join(path,direct,"tides.secondary.forward")))

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

fig = plt.figure(figsize=(19,6))
gs = GridSpec(1, 5, width_ratios=[1, 0.01, 1, 0.2, 1])

# Left panel: Ecc
ax0 = fig.add_subplot(gs[0])

# Left: e
ax0.plot(cpl[:,0], cpl[:,6], lw=3, ls="-", color="C0", label="CPL")
ax0.plot(ctl[:,0], ctl[:,6], lw=3, ls="-", color="C1", label="CTL")

ax0.set_ylabel("Eccentricity")
ax0.legend(loc="best", framealpha=0)
ax0.set_xlim(1.0e6, cpl[-1,0])
ax0.set_xscale("log")
ax0.set_xlabel("Time [yr]")

# Middle panel: Prot
ax1 = fig.add_subplot(gs[2])

ax1.plot(cpl[:,0], cpl[:,5], lw=3, ls="-", color="C0", label="CPL")
ax1.plot(ctl[:,0], ctl[:,5], lw=3, ls="-", color="C1", label="CTL")

ax1.set_ylabel("Rotation Period [d]")
ax1.set_xlim(1.0e6, cpl[-1,0])
ax1.set_xscale("log")
ax1.set_xlabel("Time [yr]")

# Right panel: Prot + Qs
ax2 = fig.add_subplot(gs[4])

# Binaries with P=50 days
for ii, data in enumerate(tides_50):
    ax2.plot(data[:,0], data[:,1], lw=3, color=colors[ii], ls="--",
    label=labels[ii])

# No tides
ax2.plot(notides[:,0], notides[:,1], lw=3, ls="-", color="k", label="No Tides")

# Annotations
ax2.axhline(75, lw=2, ls=":", color="k")

ax2.set_xlabel("Time [yr]")
ax2.set_ylabel("Rotation Period [d]")
ax2.set_xlim(1.0e8,data[-1,0])
ax2.set_ylim(0.8,80)
ax2.set_xscale("log")
ax2.legend(loc="center left", fontsize=14, framealpha=0)

fig.savefig("../Plots/Qrot.pdf", bbox_inches="tight")
