
#! -*- coding:utf-8 -*-
""" 
Master CyberSecurite & CyberCriminalite - Ensa Tanger
Author : BATALI OUALID 
Date : 12 NOVEMBRE 2019
Python version : Python 3.6.7 

################## CONCEPTION D'UN GNPA ################
###################  EN UTILISANT ######################
############# LES AUTOMATES CELLULAIRES ################
"""
# REMARQUE IMPORTANTE : CA VA PAS MARCHER AVEC PYTHON2! 
import os
from spongent import SPONGENT
def rule2bin(rule):
    rule = bin(rule)[2:].zfill(8)
    return rule


def newState(initialState, rule):
    """  La fonction de transition """
    V = [[0, 0, 0], [0, 0, 1],
         [0, 1, 0], [0, 1, 1],
         [1, 0, 0], [1, 0, 1],
         [1, 1, 0], [1, 1, 1]]
    Voutput1 = list()
    rule = rule2bin(rule)
    for i in range(0, 8):
        if rule[7-i] == '1':
            Voutput1.append(V[i])
    state = initialState
    newstate = list()
    n = len(state)  
    for i in range(n):

        v = [state[i-1], state[i], state[(i+1)%n]]

        if v in Voutput1:
            newstate.append(1)
        else:
            newstate.append(0)
    return newstate


def present(state, numberIter):
    rule = 30 # Rule predefinie
    rslt = list()
    for i in range(numberIter):
        rslt.append(state)
        state = newState(state, rule)
    return state


def genkey():
    state = [0,0,1,1,1,0,0,0 ,1,0,0,0,1,0,0,0
         ,1,0,0,1,0,0,0,1, 0,0,0,0,1,0,0,1
         ,0,1,0,0,0,0,1,0, 1,0,0,1,1,1,0,1
         ,0,1,0,0,1,1,0,1,  0,0,1,0,0,1,1,0]
    numberIter = int.from_bytes(os.urandom(1),'little')
    output = present(state, numberIter)
    password = int.from_bytes(bytes(output), 'little')
    return password
va = genkey()
val = hex(va)
A = SPONGENT(n=256, c=256, r=16, R=140)
valHahed = hash(val)
print ("[---->]Le nombre generée par le GNPA  : {}".format(va))
print("[---->]Le hash du nombre generée avec SPONGENT est : {}".format(valHahed))



