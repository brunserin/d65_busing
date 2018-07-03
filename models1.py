# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 16:15:40 2018

@author: dipayan
"""

from gurobipy import *
import csv
import numpy as np
import time
from random import *

def district1(I, M, N, S, T, K, D, gamma, p, p_exp, q_exp, A, E):
    model = Model("DISTRICTING")

    model.Params.UpdateMode = 1
    
    model.setParam('OutputFlag', 0)
    # start_time = time.time()
    
    ##### MODEL #####

    ## define variables ##
    u = {}
    x = {}
    z = {} 
    
    # construct x variables
    for i in range(I):
        for n in range(N):
            x[i,n] = model.addVar(vtype = GRB.BINARY, name = "x_{}_{}".format(i,n))
            
    # construct z variables
    for m in range(M):
        for n in range(N):
            z[m, n] = model.addVar(vtype = GRB.BINARY, name = "z_{}_{}".format(m, n))
            
    # construct u variables, constraint (6)
    for n in range(N):
        for k in range(K):
            for s in range(S):
                for t in range(T):
                    u[n, k, s, t] = model.addVar(lb=0, vtype = GRB.CONTINUOUS, name = "u_{}_{}_{}_{}".format(n, k, s, t))
                         
    # constraint (1) #
    for m in range(M):
        model.addConstr(quicksum(z[m, n] for n in range(N)) == 1, name = "c1_{}".format(m))
        
    # constraint (2) #
    for m in range(M):
        for n in range(N):
            model.addConstr(z[m, n] <= gamma[m, n], name = "c2_{}_{}".format(m, n))
    
    # constraint (3) #
    for i in range(I):
        model.addConstr(quicksum(x[i, n] for n in range(N)) == 1, name = "c3_{}_{}".format(m, n))
        
    # constraint (4) #
    for n in range(N):
        for k in range(K):
            model.addConstr(quicksum(p_exp[i, k] * x[i, n] for i in range(I)) <= 
            (A[n, k] - quicksum(z[m, n] * E[m, k] for m in range(M))), 
            name = "c4_{}_{}".format(n, k))
            
    # constraint (5), (7) #
    for n in range(N):
        for k in range(K):
            for s in range(S):
                for t in range(T):
                    model.addConstr(quicksum(p[i, k, s, t] * x[i, n] for i in range(I)) - u[n, k, s, t] <= 
                    (A[n, k] - quicksum(z[m, n] * E[m, k] for m in range(M))), 
                    name = "c5_{}_{}_{}_{}".format(n, k, s, t))
                    
                    model.addConstr(u[n, k, s, t] <= 0.15 * A[n, k], name = "c7_{}_{}_{}_{}".format(n, k, s, t))
         
            
    # define objective function
    model.setObjective(quicksum(p_exp[i, k] * D[i, n] * x[i, n] for i in range(I) for k in range(K) for n in range(N)) +
    quicksum(q_exp[i, k, m] * D[i, n] * z[m, n] for i in range(I) for k in range(K) for n in range(N) for m in range(M)) +
    quicksum(u[n, k, s, t] for t in range(T) for n in range(N) for k in range(K) for s in range(S)), GRB.MINIMIZE)
    
    model.optimize()
    
    '''
    for m in range(1, M + 1):
        for n in range(N):
            for i in range(Gamma[n]):
                if x[n, i, m].x == 1:
                    display(x[n, i, m])
    '''
    
    # IP_Obj = model.objVal
    # print('Opt Val: %g' % model.objVal)
     
    #curr_time = time.time()
    #time_taken = curr_time - start_time
    
    #print("Solve time: %.2f seconds" % (time_taken))
    
    # print(x)
    
    print("\n")
    for m in range(M):
        for n in range(N):
            if z[m, n].x == 1:
                print("Program %.0f assigned to School %.0f" % (m, n))
                
    print("\n")
    for n in range(N):
        for i in range(I):
            if x[i, n].x == 1:
                print("Block %.0f assigned to School %.0f" % (i, n))
                
    print("\n")
    totOver = 0
    for s in range(S):
        overCap = (quicksum(u[n, k, s, t] for t in range(T) for n in range(N) for k in range(K))).getValue()
        totOver = totOver + overCap
    
    avgOver = totOver/(T * S * N)
    
    print("On avgerage, capacity is exceeded by %.2f students per school per year" % (avgOver))
    
    
    
    
    
    
    
    
    return(u, x, z)