# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 21:30:29 2018

@author: dipayan
"""

import pandas as pd
from models1 import *

# number of blocks
I = 9

# number of programs
M = 1

# number of schools
N = 2

# number of scenarios
S = 100

# number of time periods
T = 3

# number of grades
K = 1

# program capacity
E = {(0, 0) : 20}

# school capacity
A = {(0, 0) : 60,
     (1, 0) : 60}

# program eligibility
gamma = {(0, 0) : 1,
         (0, 1) : 1}

# from file
file = 'test_data1.xlsx'
xl = pd.ExcelFile(file)

# q_exp
q_exp = {}
program_exp = xl.parse('program_exp')
for i in range(I):
    for m in range(M):
        q_exp[i, 0, m] = program_exp.loc[m, i]

# p_exp
p_exp = {}
for i in range(I):
    p_exp[i, 0] = 10

# distances
D = {}
distances = xl.parse('dis_school')
for i in range(I):
    for n in range(N):
        D[i, n] = distances.loc[i, n]
        
# scenarios
p = {}
scen_yr0 = xl.parse('block_total_scenarios1')
scen_yr1 = xl.parse('block_total_scenarios2')
scen_yr2 = xl.parse('block_total_scenarios3')
k = 0

t = 0
for i in range(I):
    for s in range(S):
        p[i, k, s, t] = scen_yr0.loc[s, i]

t = 1
for i in range(I):
    for s in range(S):
        p[i, k, s, t] = scen_yr1.loc[s, i]
        
t = 2
for i in range(I):
    for s in range(S):
        p[i, k, s, t] = scen_yr2.loc[s, i]
        
# solve model
district1(I, M, N, S, T, K, D, gamma, p, p_exp, q_exp, A, E)

'''
for m in range(M):
    for n in range(N):
        if z[m, n].x == 1:
            print("Program %.0f assigned to School %.0f" % (m, n))
'''
















