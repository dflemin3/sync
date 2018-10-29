# Run all vplanet simulations
import subprocess
import sys
import os

# Find all subdirectories
dir_path = os.path.dirname(os.path.realpath(__file__))
dirs = ["20_4", "20_5", "20_6", "20_7", "50_4", "50_5", "50_6", "50_7"]

# Run simulations
for dir in dirs:
    os.chdir(os.path.join(dir_path,dir))

    # Run simulation
    subprocess.call(['vplanet', 'vpl.in'])
