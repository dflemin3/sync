# Run all vplanet simulations
import subprocess
import sys
import os

# Find all subdirectories
dir_path = os.path.dirname(os.path.realpath(__file__))
dirs = ["5", "10", "20", "30", "40", "50", "60"]

# Run simulations
for dir in dirs:
    os.chdir(os.path.join(dir_path,dir))

    # Run simulation
    subprocess.call(['vplanet', 'vpl.in'])
