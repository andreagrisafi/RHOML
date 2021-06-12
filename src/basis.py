import sys
import numpy as np

def basiset(basis):
   """Return basis set dimensions"""

   lmax = {}
   nmax = {}

   if basis=="FHI-aims-tight-svs":

      llmax = 8
      lmax["H"] = 4
      lmax["C"] = 8
      lmax["O"] = 8
      lmax["Al"] = 8
      lmax["Si"] = 8

      nnmax = 11
      # hydrogen
      nmax[("H",0)] = 8
      nmax[("H",1)] = 6
      nmax[("H",2)] = 6
      nmax[("H",3)] = 3
      nmax[("H",4)] = 1
      # carbon
      nmax[("C",0)] = 11
      nmax[("C",1)] = 10
      nmax[("C",2)] = 9
      nmax[("C",3)] = 8
      nmax[("C",4)] = 7
      nmax[("C",5)] = 5
      nmax[("C",6)] = 3
      nmax[("C",7)] = 2
      nmax[("C",8)] = 1
      # oxygen
      nmax[("O",0)] = 11
      nmax[("O",1)] = 11
      nmax[("O",2)] = 9
      nmax[("O",3)] = 8
      nmax[("O",4)] = 7
      nmax[("O",5)] = 5
      nmax[("O",6)] = 4
      nmax[("O",7)] = 2
      nmax[("O",8)] = 1
      # aluminium
      nmax[("Al",0)] = 10
      nmax[("Al",1)] = 9
      nmax[("Al",2)] = 8
      nmax[("Al",3)] = 8
      nmax[("Al",4)] = 7
      nmax[("Al",5)] = 4
      nmax[("Al",6)] = 2
      nmax[("Al",7)] = 2
      nmax[("Al",8)] = 1
      # silicon
      nmax[("Si",0)] = 11
      nmax[("Si",1)] = 11
      nmax[("Si",2)] = 10
      nmax[("Si",3)] = 9
      nmax[("Si",4)] = 9
      nmax[("Si",5)] = 5
      nmax[("Si",6)] = 4
      nmax[("Si",7)] = 2
      nmax[("Si",8)] = 1
      
   if basis=="RI-cc-pvqz":

      lmax["H"] = 4
      lmax["C"] = 5
      lmax["N"] = 5
      lmax["O"] = 5

      # hydrogen
      nmax[("H",0)] = 4
      nmax[("H",1)] = 3
      nmax[("H",2)] = 3
      nmax[("H",3)] = 2
      nmax[("H",4)] = 1
      # carbon
      nmax[("C",0)] = 10
      nmax[("C",1)] = 7
      nmax[("C",2)] = 5
      nmax[("C",3)] = 3
      nmax[("C",4)] = 2
      nmax[("C",5)] = 1
      # nytrogen
      nmax[("N",0)] = 10
      nmax[("N",1)] = 7
      nmax[("N",2)] = 5
      nmax[("N",3)] = 3
      nmax[("N",4)] = 2
      nmax[("N",5)] = 1
      # oxygen
      nmax[("O",0)] = 10
      nmax[("O",1)] = 7
      nmax[("O",2)] = 5
      nmax[("O",3)] = 3
      nmax[("O",4)] = 2
      nmax[("O",5)] = 1
   
   if basis=="FHI-aims-tight":

      llmax = 8
      lmax["H"] = 4
      lmax["C"] = 8
      lmax["O"] = 8
      lmax["Al"] = 8
      lmax["Si"] = 8

      nnmax = 11
      # hydrogen
      nmax[("H",0)] = 8
      nmax[("H",1)] = 6
      nmax[("H",2)] = 6
      nmax[("H",3)] = 3
      nmax[("H",4)] = 1
      # carbon
      nmax[("C",0)] = 11
      nmax[("C",1)] = 10
      nmax[("C",2)] = 9
      nmax[("C",3)] = 8
      nmax[("C",4)] = 7
      nmax[("C",5)] = 5
      nmax[("C",6)] = 3
      nmax[("C",7)] = 2
      nmax[("C",8)] = 1
      # oxygen
      nmax[("O",0)] = 9
      nmax[("O",1)] = 10
      nmax[("O",2)] = 9
      nmax[("O",3)] = 8
      nmax[("O",4)] = 6
      nmax[("O",5)] = 4
      nmax[("O",6)] = 4
      nmax[("O",7)] = 2
      nmax[("O",8)] = 1
      # aluminium
      nmax[("Al",0)] = 10
      nmax[("Al",1)] = 9
      nmax[("Al",2)] = 9
      nmax[("Al",3)] = 8
      nmax[("Al",4)] = 7
      nmax[("Al",5)] = 5
      nmax[("Al",6)] = 4
      nmax[("Al",7)] = 2
      nmax[("Al",8)] = 1
      # silicon
      nmax[("Si",0)] = 10
      nmax[("Si",1)] = 10
      nmax[("Si",2)] = 9
   
   if basis=="FHI-aims-b3lyp-svs":

      lmax["H"] = 4
      lmax["O"] = 5

      # hydrogen
      nmax[("H",0)] = 10
      nmax[("H",1)] = 9
      nmax[("H",2)] = 7
      nmax[("H",3)] = 3
      nmax[("H",4)] = 1
      # oxygen
      nmax[("O",0)] = 13
      nmax[("O",1)] = 12
      nmax[("O",2)] = 11
      nmax[("O",3)] = 10
      nmax[("O",4)] = 8
      nmax[("O",5)] = 6
      
   if basis=="FHI-aims-tight-iso":

      lmax["H"] = 4
      lmax["O"] = 5

      # hydrogen
      nmax[("H",0)] = 8
      nmax[("H",1)] = 6
      nmax[("H",2)] = 6
      nmax[("H",3)] = 3
      nmax[("H",4)] = 1
      # oxygen
      nmax[("O",0)] = 9
      nmax[("O",1)] = 10
      nmax[("O",2)] = 9
      nmax[("O",3)] = 8
      nmax[("O",4)] = 6
      nmax[("O",5)] = 4

   if basis=="FHI-aims-min":

      lmax["H"] = 0
      lmax["O"] = 2
      lmax["Al"] = 2
      lmax["Si"] = 2

      nmax[("H",0)] = 1
      nmax[("O",0)] = 3
      nmax[("O",1)] = 2
      nmax[("O",2)] = 1
      nmax[("Al",0)] = 7
      nmax[("Al",1)] = 7
      nmax[("Al",2)] = 3
      nmax[("Si",0)] = 7
      nmax[("Si",1)] = 7
      nmax[("Si",2)] = 3

   if basis=="CP2K-LRI-DZVP-MOLOPT-GTH-MEDIUM":
      
      lmax["H"] = 3
      lmax["O"] = 4

      # hydrogen
      nmax[("H",0)] = 10
      nmax[("H",1)] = 9 
      nmax[("H",2)] = 8 
      nmax[("H",3)] = 6
      # oxygen
      nmax[("O",0)] = 15
      nmax[("O",1)] = 13
      nmax[("O",2)] = 12
      nmax[("O",3)] = 11
      nmax[("O",4)] = 9

   return [lmax,nmax]
