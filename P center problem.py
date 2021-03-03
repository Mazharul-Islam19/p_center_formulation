# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:11:14 2019

@author: Shuvro
"""
from gurobipy import *
import numpy as np
#dataset
file = "PC001.dat"
with open(file) as fn:
    content = fn.readlines()
    for line in content:
        l=line.split()
        if len(l)==2:
            if l[0]=='N:':
                n=int(l[1])
            elif l[0]=='P:':
                p=int(l[1])

def openfile(file,n):
    b=np.zeros((n,n))
    i=0
    for line in content[5:-2]:
        a=np.array(line.split())
        b[i] = a 
        i=i+1
    return b
data = openfile(file,n)

#name of the model
m = Model("P_center")

#variable
x = m.addVars(n,n, vtype=GRB.BINARY, name = "[Non-center,Center]")
z = m.addVar(name = "Max_distance")

#objective function
m.setObjective(z,GRB.MINIMIZE)

#constraints
m.addConstrs((quicksum(x[i,j] for j in range(n)) == 1) for i in range(n))
m.addConstrs((x[i,j] <= x[j,j]) for j in range(n) for i in range(n) if i!=j)
m.addConstrs(data[i,j]*x[i,j] <= z for i in range(n) for j in range(n) if i!=j)
m.addConstr(quicksum(x[i,j] for j in range(n) for i in range(n) if i==j) <= p)

#optimization
m.Params.timelimit = 600
m.optimize()
m.printAttr('x')
a = m.getAttr("x", m.getVars())[:-1]
zeroset = np.zeros((n,n))
value = np.array(a).reshape((n,n))

if m.status == GRB.OPTIMAL:
    print("\n\n\nOptimal maximum distance is equal to %d" % m.objVal, "\n\n")
    for j in range(n):
        for i in range(n):
           if i != j:
               if value[i,j] ==1:
                   print("Center Point "+str(j)+" is connected to point "+str(i))
else:
    print("Optimum not found.\nMinimum maximum distance found within the time limit is %d" % m.objVal,
          "\nGurobi status code: ",m.status,"\n")
    for j in range(n):
        for i in range(n):
           if i != j:
               if value[i,j] ==1:
                   print("Center Point "+str(j)+" is connected to point "+str(i))
m.write("P_center.sol")
m.write("P_center.lp")