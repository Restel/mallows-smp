
''' 
  * File: 	  ScoreGraph.py
  * Author:	  Nicholas Mattei (nicholas.mattei@nicta.com.au)
  * Date:	  May 20, 2014
  *
  * Copyright (c) 2014, Nicholas Mattei and NICTA
  * All rights reserved.
  *
  * Developed by: Nicholas Mattei
  *               NICTA
  *               http://www.nickmattei.net
  *               http://www.preflib.org
  *
  * Redistribution and use in source and binary forms, with or without
  * modification, are permitted provided that the following conditions are met:
  *     * Redistributions of source code must retain the above copyright
  *       notice, this list of conditions and the following disclaimer.
  *     * Redistributions in binary form must reproduce the above copyright
  *       notice, this list of conditions and the following disclaimer in the
  *       documentation and/or other materials provided with the distribution.
  *     * Neither the name of NICTA nor the
  *       names of its contributors may be used to endorse or promote products
  *       derived from this software without specific prior written permission.
  *
  * THIS SOFTWARE IS PROVIDED BY NICTA ''AS IS'' AND ANY
  * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  * DISCLAIMED. IN NO EVENT SHALL NICTA BE LIABLE FOR ANY
  * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
  * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
  * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.	
	

About
--------------------
	This file contains demo code presented at EXPLORE 2014 (www.preflib.org/beyond2014) during
	Nick's tutorial.  It shows how to use some of the PrefLib tools within Python to generate a
	variety of test instances and then graph based on the average margin of victory for Borda
	scoring.  This is meant to demonstrate some of the power of the PrefLib utility library.

	Note that this was written agains a devlopment version of the 0.2 library but is 
	compatiable with the posted 0.1 version of the library.  You must have SciPy installed
	(or at the very least Numpy and MatplotLib) and they must be in your Python include 
	directory.

'''
import copy
import random
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#Import PrefLib Libraries
sys.path.insert(0, "../")
import GenProfiles
import PreflibUtils

if __name__ == '__main__':

	# Candidate Range
	max_candidates = 8
	min_candidates = 3

	colors = ['r', 'y', 'b', 'g', 'k', 'c']
	markers = ["*", "h", "^", "o", "D", "x"]

	#Number of Voters
	num_voters = 100

	#Number of Iterations
	num_iterations = 100

	#Generate an instance for each number of candidates.
	#Plot the average margin of victory of the winner.
	margins_per_ncands = {}
	for c_candidates in range(min_candidates, max_candidates+1):
		candidate_set = GenProfiles.gen_cand_map(c_candidates)
		#PreflibUtils.pp_profile_toscreen(candidate_set, rankmaps=[], rankmapcounts=[])

		margins = []
		for cinst in range(num_iterations):
			ref_ranking = copy.copy(list(candidate_set.keys()))
			random.shuffle(ref_ranking)
			rmaps, rmapcounts = GenProfiles.gen_mallows(num_voters, candidate_set, [1.0], [1], [ref_ranking])

			#Print The Whole Thing...
			#PreflibUtils.pp_profile_toscreen(candidate_set, rmaps, rmapcounts)
			


			#Create and Evaluate the Borda Rule. 
			m = c_candidates
			svec = [m - i for i in range(1,m+1)]
			scores = PreflibUtils.evaluate_scoring_rule(candidate_set, rmaps, rmapcounts, svec)

			#Pretty print results
			#PreflibUtils.pp_result_toscreen(candidate_set, scores)

			#Margin of Victory.
			totals = sorted(list(scores.values()), reverse=True)
			margins.append(totals[0] - totals[1])

		
		#print(margins)
		#print(float(sum(margins)) / float(num_iterations))

		'''
		#Plot a Line.
		fig, ax = plt.subplots()
		ax.plot(range(0,num_iterations), margins, color="blue", marker="+", label="Margin on Iteration")
		ax.set_title("Margin Per iteration for " + str(c_candidates))
		ax.legend()
		plt.show()


		#Plot a Histogram
		fig, ax = plt.subplots()
		#Options: bins= changes the number of bins on the histogram.
		# 		  normed= sets the histogram to be normed.
		# 		  cumulative= sets the 
		ax.hist(margins, color="blue", label="Margin on Iteration", bins=100, normed=True)
		ax.set_title("Margin Per iteration for " + str(c_candidates))
		ax.legend()
		plt.show()
		exit()
		'''
		margins_per_ncands[c_candidates] = margins

	#Print all the averages..
	for c_candidates in sorted(margins_per_ncands.keys()):
		print(str(c_candidates) + " :: " + str(sum(margins_per_ncands[c_candidates]) / len(margins_per_ncands[c_candidates])))

	#Overlay all the plots...
	fig, ax = plt.subplots()
	i = 0
	for c_candidates in margins_per_ncands.keys():
		ax.plot(range(0,num_iterations), margins_per_ncands[c_candidates], color=colors[i], marker=markers[i], label="Margins for " +str(c_candidates) + " Cands.")
		i += 1
	ax.set_title("Margin Per iteration for " + str(c_candidates))
	ax.legend()
	plt.show()

	#Show Boxplots for each n_cand.
	fig, ax = plt.subplots()
	box_plots = []
	x_labels = []
	for i in sorted(margins_per_ncands.keys()):
		box_plots.append(margins_per_ncands[i])
		x_labels.append(i)
	ax.boxplot(box_plots)
	xtickNames = plt.setp(ax, xticklabels=x_labels)
	ax.set_title("Box Plots Margin Per nCand")
	ax.set_ylabel("Number of Candidates")
	ax.set_xlabel("Margin")
	plt.show()



