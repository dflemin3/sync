# Run all vplanet simulations
import subprocess
import sys
import os

# Find all subdirectories
dir_path = os.path.dirname(os.path.realpath(__file__))
dirs = ["0.001", "0.01", "0.1", "6", "7", "8", "9"]

# Run simulations
for dir in dirs:
    os.chdir(os.path.join(dir_path,dir))

    # Run simulation
    subprocess.call(['vplanet', 'vpl.in'])
