#!/bin/bash

## Job Name

#SBATCH --job-name=mcCPL

## Allocation Definition

## On mox and ikt, the account and partition options should be the same.
#SBATCH --account=vsm
#SBATCH --partition=vsm

## Resources

## Nodes

#SBATCH --nodes=1

## Walltime (10 hours). Do not specify a walltime substantially more than your job needs.

#SBATCH --time=10:00:00

## Memory per node. It is important to specify the memory since the default memory is very small.

## For mox, --mem may be more than 100G depending on the memory of your nodes.

## For ikt, --mem may be 58G or more depending on the memory of your nodes.

## See above section on "Specifying memory" for choices for --mem.

#SBATCH --mem=100G

## Specify the working directory for this job

#SBATCH --workdir=/gscratch/stf/dflemin3/sync/mcCPL

##turn on e-mail notification

#SBATCH --mail-type=ALL

#SBATCH --mail-user=dflemin3@uw.edu
module load parallel-20170722
find . -name "simulation_*.sh" | parallel -j 28 --joblog paralleltasks.log --resume
