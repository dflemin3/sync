# Run all vplanet simulations
import subprocess
import sys
import os

# Find all subdirectories
dir_path = os.path.dirname(os.path.realpath(__file__))
dirs = ["q4", "q5", "q6", "q7", "tau10", "tau1", "tau0_1", "tau0_01", "single"]

# Run simulations
for dir in dirs:
    os.chdir(os.path.join(dir_path,dir))

    # Run simulation
    subprocess.call(['vplanet', 'vpl.in'])
