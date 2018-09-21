#*********************************************************************************
#* Copyright (C) 2017-2018  Brendan A. Smith, Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*
#*********************************************************************************/


import cmath
import math
import os
import sys

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

from libra_py import *
import aux_functs

class tmp:
    pass    

def compute_model(q, params, full_id):

    model = params["model"]
    res = None

    Id = Cpp2Py(full_id)
    indx = Id[-1]

    if model==1:
        res = models_Martens.Martens1(q.col(indx), params)
    if model==2:
        res = models_Martens.model2(q.col(indx), params) # Apparently, I called Martens2, model2. I can change this.

    return res

def run_QC(Nsnaps,Nsteps, params, case, ent_opt):

    """
    Runs tests for 2D model problems using ensembles of trajectories
    """
    
    ndia, nadi, nnucl, ntraj = 1, 1, 2, 1000

    # ======= Hierarchy of Hamiltonians =======
    ham = nHamiltonian(ndia, nadi, nnucl)
    ham.init_all(2)
    print "id=", ham.id, " level=", ham.level

    ham1 = []
    for tr in xrange(ntraj):
        ham1.append( nHamiltonian(ndia, nadi, nnucl) )
        #print ham1[tr].id, ham1[tr].level
        ham1[tr].init_all(2)
        ham.add_child(ham1[tr])
        #print Cpp2Py(ham1[tr].get_full_id())


    # Initialize Simulation 
    dt = params["dt"]
    params.update({"ndof":nnucl, "ntraj":ntraj})
 
    print "ent_opt = ", ent_opt
    print "model = ", params["model"]
    print "case = ", case

    # Get the q and p corrdinates from a previosu classical ensemble simualtion 
    # to be used in an ETHD simulation
    if (ent_opt == 0 and case == 1) or (ent_opt == 1 and case == 0):
        q, p = aux_functs.get_q_p_info(params, 0, 0)
    elif ent_opt == 1 and case == 1:
        q, p = aux_functs.get_q_p_info(params, 0, 1)
   
    # Dynamical variables and system-specific properties
    mean_q = MATRIX(nnucl,1);   
    sigma_q = MATRIX(nnucl,1);
    mean_p = MATRIX(nnucl,1);   
    sigma_p = MATRIX(nnucl,1);  

    # In this example, the mean position of the position 
    # dof are not equal. The uncertainty is asscoaited with 
    # a minimal uncertainty gaussian with a mass of 2,000 (a.u)
    # and omega = 0.004, which is associated with the ground 
    # state of the harmonic oscillator
    # Ex) sigma_q = sqrt( hbar/(2*m*w) ) 
    mean_q.set(0,0,params["q0"])  
    mean_q.set(1,0,params["q1"])
    sigma_q.set(0,0,params["sq0"])
    sigma_q.set(1,0,params["sq1"]) 

    # Calculate sigma_p from sigma_q choice. sigma_p will
    # be the minimum unertainty value based on the uncertainty
    # principle.
    mean_p.set(0,0,params["p0"])
    mean_p.set(1,0,params["p1"])
    sigma_p.set(0,0,0.5/sigma_q.get(0,0))
    sigma_p.set(1,0,0.5/sigma_q.get(1,0))
  
    if ent_opt == 0:
        rnd = Random()
        if case == 0:
            q = MATRIX(nnucl,ntraj);  tsh.sample(q, mean_q, sigma_q, rnd)        
            p = MATRIX(nnucl,ntraj);  tsh.sample(p, mean_p, sigma_p, rnd)   
        if case == 1:
            p = MATRIX(nnucl,ntraj);  tsh.sample(p, mean_p, sigma_p, rnd)

    # Save the q and p coordinates of classical ensemble, to be used by a seperate
    # ETHD ensemble
    aux_functs.save_q_p_info(q,p,params,ent_opt,case)

    # Initial calculations
    print "\n", "Showing q_matrix", "\n"
    q.show_matrix()

    # Set mass matricies  
    iM = MATRIX(nnucl,1);
    iM.set(0,0, 1.0/2000.0)
    iM.set(1,0, 1.0/2000.0)

    # Compute Initial trajectory probability distributions for all position dof
    # As it is currently implimented, this will produce a lot of text files
    # Momenta distrbutions coming soon.

    # aux_functs.bin(q, -8.0, 8.0, 0.05,"_q")
    # aux_functs.bin(p, -8.0, 8.0, 0.05,"_p")

    
    # Compute Hamiltonian properties
    ham.compute_diabatic(compute_model, q, params, 1)
    ham.compute_adiabatic(1, 1);
    if ent_opt == 1:
        ham.add_ethd_adi(q, iM, 1)

    out1 = open("_output_"+str(params["model"])+str(ent_opt)+str(case)+".txt", "w"); out1.close()   
    # Do the propagation
    for i in xrange(Nsnaps):

        # Count the number of trajectories that cross the barrier 
        react_prob = aux_functs.traj_counter(q, params["model"])

        # To make a movie, uncomment the next two lines
        #os.system("mkdir _2D_dist_case"+str(case))
        #aux_functs.bin2(q, -7.0, 7.0, 0.1, -5.0, 5.0, 0.1, "_2D_dist_case"+str(case)+"/_2D_distrib_"+str(i)+"_.txt")


        #=========== Properties ==========
        Ekin, Epot, Etot = aux_functs.compute_etot(ham, p, iM)

        # Print the ensemble average - kinetic, potential, and total energies
        # Print the tunneling information. Here, we count each trajectory across the barrier.
        out1 = open("_output_"+str(params["model"])+str(ent_opt)+str(case)+".txt", "a")
        out1.write( " %8.5f %8.5f %8.5f %8.5f %8.5f\n" % ( i*dt*Nsteps, Ekin, Epot, Etot, react_prob ) )
        out1.close()
        
        for j in xrange(Nsteps):
            Verlet1(dt, q, p, iM, ham, compute_model, params, ent_opt)


def init_params(model, case):
    """
    This function intiializes the params dictionary for a given case    
    """

    params = {"dt":1.0}

    if model == 1:    
        # Martens' model I
        if case == 0: 
            params.update({"model":1, "q0":-1.0, "q1":0.0, "p0":3.0, "p1":0.0, "sq0":0.25, "sq1":0.25, "sp0":0.0,  "sp1":0.0})
        elif case == 1:
            params.update({"model":1, "q0":-1.0, "q1":0.0, "p0":4.0, "p1":0.0, "sq0":0.25, "sq1":0.25, "sp0":0.0,  "sp1":0.0})


    elif model == 2:
        # Martens' model II
        if case == 0:
            params.update({"model":2, "q0":-1.0, "q1":0.0, "p0":3.0, "p1":0.0, "sq0":0.25, "sq1":0.25, "sp0":0.0,  "sp1":0.0})
        elif case == 1:
            params.update({"model":2, "q0":-1.0, "q1":0.0, "p0":4.0, "p1":0.0, "sq0":0.25, "sq1":0.25, "sp0":0.0,  "sp1":0.0})


    return params


def run2D(Nsnaps, Nsteps):
    for model in [1,2]:
        for ent_opt in [0,1]:
            for case in [0,1]:

                params = init_params(model, case)
                run_QC(Nsnaps, Nsteps, params, case, ent_opt)
  


Nsnaps = 100
Nsteps = 20
run2D(Nsnaps, Nsteps)

