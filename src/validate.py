import sys
import numpy as np
import time
import ase
from ase import io
from ase.io import read
#import argparse

import basis

from lib import prediction

sys.path.insert(0, './')
import inp

# Is automatic cross-validation requested?
xv = inp.xv

# read species
spelist = inp.species
spe_dict = {}
for i in xrange(len(spelist)):
    spe_dict[i] = spelist[i]

# read basis
[lmax,nmax] = basis.basiset(inp.dfbasis)

llist = []
nlist = []
for spe in spelist:
    llist.append(lmax[spe])
    for l in xrange(lmax[spe]+1):
        nlist.append(nmax[(spe,l)])
llmax = max(llist)
nnmax = max(nlist)

# read system
xyzfile = read(inp.filename,":")
ndata = len(xyzfile)

# number of sparse environments
M = inp.Menv

# system parameters
atomic_symbols = []
atomic_valence = []
natoms = np.zeros(ndata,int)
for i in xrange(len(xyzfile)):
    atomic_symbols.append(xyzfile[i].get_chemical_symbols())
    atomic_valence.append(xyzfile[i].get_atomic_numbers())
    natoms[i] = int(len(atomic_symbols[i]))
natmax = max(natoms)

# atomic species arrays
species = np.sort(list(set(np.array([item for sublist in atomic_valence for item in sublist]))))
nspecies = len(species)
spec_list = []
spec_list_per_conf = {}
atom_counting = np.zeros((ndata,nspecies),int)
for iconf in xrange(ndata):
    spec_list_per_conf[iconf] = []
    for iat in xrange(natoms[iconf]):
        for ispe in xrange(nspecies):
            if atomic_valence[iconf][iat] == species[ispe]:
               atom_counting[iconf,ispe] += 1
               spec_list.append(ispe)
               spec_list_per_conf[iconf].append(ispe)
spec_array = np.asarray(spec_list,int)
nenv = len(spec_array)

# atomic indexes sorted by valence
atomicindx = np.zeros((natmax,nspecies,ndata),int)
for iconf in xrange(ndata):
    for ispe in xrange(nspecies):
        indexes = [i for i,x in enumerate(spec_list_per_conf[iconf]) if x==ispe]
        for icount in xrange(atom_counting[iconf,ispe]):
            atomicindx[icount,ispe,iconf] = indexes[icount]


#====================================== reference environments 
fps_indexes = np.loadtxt("sparse_set_"+str(M)+".txt",int)[:,0]
fps_species = np.loadtxt("sparse_set_"+str(M)+".txt",int)[:,1]

# basis set arrays 
bsize = np.zeros(nspecies,int)
almax = np.zeros(nspecies,int)
anmax = np.zeros((nspecies,llmax+1),int)
for ispe in xrange(nspecies):
    spe = spe_dict[ispe]
    almax[ispe] = lmax[spe]+1
    for l in xrange(lmax[spe]+1):
        anmax[ispe,l] = nmax[(spe,l)]
        bsize[ispe] += nmax[(spe,l)]*(2*l+1)

# problem dimensionality 
collsize = np.zeros(M,int)
for iref in xrange(1,M):
    collsize[iref] = collsize[iref-1] + bsize[fps_species[iref-1]]
totsize = collsize[-1] + bsize[fps_species[-1]]

# dataset partitioning
trainrangetot = np.loadtxt("training_set.txt",int)
testrange = np.setdiff1d(range(ndata),trainrangetot)

for iloop in range(2):
    # Two loops only performed when cross-validating
    if iloop == 1 and not xv: continue
    
    if iloop == 1: testrange = trainrangetot
    ntest = len(testrange)
    natoms_test = natoms[testrange]

    print "Number of test configurations = ", ntest
    print "Predicting the baselined expansion coefficients for the test set ..."

    # define testing indexes 
    test_configs = np.array(testrange,int)
    atomicindx_test = atomicindx[:,:,testrange]
    atom_counting_test = atom_counting[testrange]
    test_species = np.zeros((ntest,natmax),int)
    for itest in xrange(ntest):
        for iat in xrange(natoms_test[itest]):
            test_species[itest,iat] = spec_list_per_conf[testrange[itest]][iat]

    # sparse kernel sizes 
    kernel_sizes = np.zeros(ntest,int)
    itest = 0
    for iconf in testrange:
        for iref in xrange(M):
            ispe = fps_species[iref]
            spe = spe_dict[ispe]
            for l in xrange(lmax[spe]+1):
                msize = 2*l+1
                for im in xrange(msize):
                    for iat in xrange(atom_counting_test[itest,ispe]):
                        for imm in xrange(msize):
                            kernel_sizes[itest] += 1
        itest += 1

# load regression weights

    if iloop == 0:
        weights = np.load("weights.npy")
    else:
        weights = np.load("weights_p.npy")

    # unravel regression weights with explicit indexing
    ww = np.zeros((M,llmax+1,nnmax,2*llmax+1),float)
    i = 0
    for ienv in xrange(M):
        ispe = fps_species[ienv]
        al = almax[ispe]
        for l in xrange(al):
            msize = 2*l+1
            anc = anmax[ispe,l]
            for n in xrange(anc):
                for im in xrange(msize):
                    ww[ienv,l,n,im] = weights[i] 
                    i += 1

    path2kerns = inp.path2ml+"kernels/"

    coeffs = prediction.prediction(path2kerns,kernel_sizes,fps_species,atom_counting_test,atomicindx_test,nspecies,ntest,natmax,llmax,nnmax,natoms_test,test_configs,test_species,almax,anmax,M,ww)

    av_coefs = {}
    for spe in spelist:
        av_coefs[spe] = np.load("averages_"+str(spe)+".npy")

    for itest,iconf in enumerate(testrange):
        atoms = atomic_symbols[iconf]
        for iat in xrange(natoms[iconf]):
            for n in xrange(nmax[(atoms[iat],0)]):
                coeffs[itest,iat,0,n,0] += av_coefs[atoms[iat]][n]

    if iloop == 0:
        np.save("pred_coeffs.npy",coeffs)
    else:
        np.save("pred_coeffs_p.npy",coeffs)
