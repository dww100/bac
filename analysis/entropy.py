# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 11:33:56 2014

@author: dave
"""

import sys
import numpy
import pyqcprot_bac as qcp

import MDAnalysis as mda
import MDAnalysis.analysis.align as align

topology = sys.argv[1]
init_pdb = sys.argv[2]
traj_file = sys.argv[3]
lig_name = sys.argv[4]

filter_lig = 'resname ' + lig_name
filter_structure = 'protein or ' + filter_lig

init = mda.Universe(topology, init_pdb) 
traj = mda.Universe(topology, traj_file) 
frames = traj.trajectory
nframes = len(frames)


align.rms_fit_trj(traj, init, select="protein and backbone")

ref = init
avg_select = ref.selectAtoms(filter_structure)

align_struct = traj.selectAtoms(filter_structure)

p_avg = numpy.zeros_like(avg_select.positions)

# do a quick average of the protein
for ts in frames:
    p_avg += align_struct.positions
p_avg /= nframes

# temporarily replace positions with the average
avg_select.set_positions(p_avg)

# just make sure that we have clean original coordinates again (start at the beginning)
#traj.trajectory.rewind()

# We are assuming trajectory is pre-aligned on the protein backbone atoms
# Now fit the drug onto itself

selections = {'reference':filter_lig,'target':filter_lig}

rmsd = numpy.zeros((nframes,))
com_track = numpy.zeros((nframes,3))
angle_track = numpy.zeros((nframes,3))

ref_atoms = ref.selectAtoms(selections['reference'])
traj_atoms = traj.selectAtoms(selections['target'])
natoms = traj_atoms.numberOfAtoms()

# reference centre of mass system
ref_com = ref_atoms.centerOfMass()
ref_coordinates = ref_atoms.coordinates() - ref_com

# allocate the array for selection atom coords
traj_coordinates = traj_atoms.coordinates().copy()

# R: rotation matrix that aligns r-r_com, x~-x~com   
# 	quat: raotation quaternion array
# (x~: selected coordinates, x: all coordinates)
# Final transformed traj coordinates: x' = (x-x~_com)*R + ref_com
for k,ts in enumerate(frames):
    # shift coordinates for rotation fitting
    # selection is updated with the time frame
    x_com = traj_atoms.centerOfMass()
    com_track[k] = x_com
    traj_coordinates[:] = traj_atoms.coordinates() - x_com
    R = numpy.zeros((9,),dtype=numpy.float64)
    quat = numpy.zeros((4,),dtype=numpy.float64)
    # Need to transpose coordinates such that the coordinate array is
    # 3xN instead of Nx3. Also qcp requires that the dtype be float64
    a = ref_coordinates.T.astype('float64')
    b = traj_coordinates.T.astype('float64')    
    rmsd[k] = qcp.CalcRMSDRotationalMatrix(a,b,natoms,R,quat,None)
    angle_track[k] = [2*numpy.arcsin(quat[1]),2*numpy.arcsin(quat[2]),2*numpy.arcsin(quat[3])]        


covar_x = numpy.cov(com_track.T)
eigenval_x,eigenvec_x = numpy.linalg.eig(covar_x)
#print eigenval_x

ztrans = ((2 * numpy.pi)**1.5) * numpy.sqrt(eigenval_x[0]*eigenval_x[1]*eigenval_x[2])

#print ztrans

angle_means =  numpy.mean(angle_track,axis=0)
for i in range(nframes):
    sig2_ang0 = (angle_track[i][0] - angle_means[0])**2
    sig2_ang1 = (angle_track[i][1] - angle_means[1])**2
    sig2_ang2 = (angle_track[i][2] - angle_means[2])**2

sig2_ang0 = sig2_ang0 / (nframes - 1)
sig2_ang1 = sig2_ang1 / (nframes - 1)
sig2_ang2 = sig2_ang2 / (nframes - 1)

zrot = ((2 * numpy.pi)**1.5) * numpy.sqrt(sig2_ang0 * sig2_ang1 * sig2_ang2)

#print zrot

dg_asoc = -1.9858775 * 10**-3 * 300 * numpy.log(1660 * zrot * ztrans/(8 * numpy.pi**2))

print dg_asoc

numpy.savetxt('rmsd.out',rmsd)
