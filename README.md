# Fair Stable Matching meets Correlated Preferences

The following repo provides the source code for experiments described in:

Angelina Brilliantova and Hadi Hosseini. 2022. 
Fair Stable Matching MeetsCorrelated Preferences. In Proc. of the 21st International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2022), Online, 
May 9–13,2022, IFAAMAS.

Usage:

## Fair Matchings under the Mallows
```
python3 main.py [number of agents] [phi_m] [phi_w]
```

main.py generates samples from the Mallows model (using the sampler from PrefLibTools https://github.com/PrefLib/PrefLib-Tools), and for each sample produce a csv file with optimal and pessimal scores for each instance, the size of the stable lattice, the rotation poset and other statics

## Comparing of a pre-processed DA with other algorithms

This section is the modified code from https://github.com/ntzia/stable-marriage, with an additional pre-processed step for the Deferred Acceptance algorithm (DA*), 
and some new scripts comparing the performance of LDS, EDS, PB, iBILS with DA* when applied to the stable matching instances sampled from the Mallows model.

Usage:
TBA
