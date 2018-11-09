# Run all vplanet simulations
import subprocess
import sys
import os

# Find all subdirectories
dir_path = os.path.dirname(os.path.realpath(__file__))
dirs = ["single", "q7", "q8", "tau0_01NoLock", "tau0_1NoLock", "q7NoLock", "q8NoLock", "tau0_01", "tau0_1"]

# Run simulations
for dir in dirs:
    os.chdir(os.path.join(dir_path,dir))

    # Run simulation
    subprocess.call(['vplanet', 'vpl.in'])
