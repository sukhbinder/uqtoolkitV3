#!/usr/bin/env python
#=====================================================================================
#                     The UQ Toolkit (UQTk) version 3.0
#                     Copyright (2016) Sandia Corporation
#                     http://www.sandia.gov/UQToolkit/
#
#     Copyright (2016) Sandia Corporation. Under the terms of Contract DE-AC04-94AL85000
#     with Sandia Corporation, the U.S. Government retains certain rights in this software.
#
#     This file is part of The UQ Toolkit (UQTk)
#
#     UQTk is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     UQTk is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with UQTk.  If not, see <http://www.gnu.org/licenses/>.
#
#     Questions? Contact Bert Debusschere <bjdebus@sandia.gov>
#     Sandia National Laboratories, Livermore, CA, USA
#=====================================================================================
import math

try:
	import numpy as np
except ImportError:
	print "Numpy module could not be found"

try:
	from scipy import stats
except ImportError:
	print "Scipy stats module could not be found"

try:
	from scipy import optimize
except ImportError:
	print "Scipy optimize module could not be found"

try:
	import PyUQTk.uqtkarray as uqtkarray
except ImportError:
	print "PyUQTk array module not found"
try:
	import PyUQTk.quad as uqtkquad
except ImportError:
	print "PyUQTk quad module not found"
try:
	import PyUQTk.pce as uqtkpce
except ImportError:
	print "PyUQTk PCE module not found"
try:
	import PyUQTk.tools as uqtktools
except ImportError:
	print "PyUQTk tools module not found"
#################################################################

def compute_heat_flux(Ti,To,dw,kw,hi,ho):
	"""
	Computes heat flux, outside wall temp, and inside wall temp
	assuming no radiative heat transfer. Solves a linear system of 3 equations (the forward model).

	Input: Samples (scalars) of the 6 uncertain, Gaussian parameters.
	Output: Heat flux Q, inside window temperature T1, and outer window temperature T2

	"""
    # Commonly used dimensionless terms
	dhko = dw*ho/kw
	dhki = dw*hi/kw

    # Compute T2, the outside window temp
	T2 = (dhki*Ti/(1.0+dhki) + dhko*To)/(dhko + dhki/(1+dhki))

    # Compute T1, the inside window temp
	T1 = (dhki*Ti + T2)/(dhki + 1.0)

    # Compute Q, the conductive heat flux
	Q=kw*(T1-T2)/dw


	return (Q,T1,T2)

#
def r_heat_flux(Ti,To,dw,kw,hi,ho,TA, estimates):
	"""
	Function to compute Q,T1,and T2 assuming radiative heat transfer occurs.
	Assumes radiative heat transfer to atmosphere and requires solving a nonlinear system of equations

	Input: Samples of the 7 uncertain, Gaussian parameters
		   estimates: For the required estimates of Q,T1, and T2 needed to solve the nonlinear system,
		   we use the values obtained by solving the system assuming no radiative heat transfer

	Output: Heat Flux Q

	"""
	def equations((Q,T1,T2)):
		# Returns the three forward model equations given values of Q,T1, and T2
		# Used by optimize.fsolve function to solve the nonlinear system
		e=0.95 # Emissivity of uncoated glass
		SBC=5.67037321e-8 # Stefan-Boltzmann constant
		f1=hi*(Ti-T1)-Q
		f2=(kw/dw)*(T1-T2)-Q
		f3=ho*(T2-To)+e*SBC*(T2**4-TA**4)-Q
		return (f1,f2,f3)
	# Solve the nonlinear system of 3 equations using the estimates
	Q,T1,T2= optimize.fsolve(equations,estimates)
	return(Q)



def GalerkinProjection(pc_model,f_evaluations):
    """
    Obtain PC coefficients by Galerkin Projection
    Input:
        pc_model : PC object with info about basis to project on
        f_evaluations: 1D numpy array (vector) with function to be projected,
                       evaluated at the quadrature points
    Output:
        Numpy array with PC coefficients
    """

    # Get parameters
    if len(f_evaluations.shape) > 1:
        print "This function can only project single variables for now"
        exit(1)

    npce = pc_model.GetNumberPCTerms()
    nqp = f_evaluations.shape[0]        # Number of quadrature points

	# UQTk array for PC coefficients for one variable
    c_k_1d_uqtk = uqtkarray.dblArray1D(npce,0.0)

	# UQTk array for function evaluations at quadrature points for that variable
    f_uqtk = uqtkarray.dblArray1D(nqp,0.0)
    for ipt in range(nqp):
		f_uqtk[ipt]=f_evaluations[ipt]

	# Galerkin Projection
    pc_model.GalerkProjection(f_uqtk,c_k_1d_uqtk)

	# Put PC coefficients in numpy array
    c_k = np.zeros(npce)
    for ip in range(npce):
		c_k[ip] = c_k_1d_uqtk[ip]

	# Return numpy array of PC coefficients
    return c_k

def evaluate_pce(pc_model,pc_coeffs,germ_samples):
	"""
	Evaluate PCE at a set of samples of the germ of this PCE
	Input:
		pc_model: PC object with info about PCE
		pc_coeffs: 1D numpy array with PC coefficients of the RVs to be evaluated.
		           Each column corresponds to one RV.
		germ_samples: numpy array with samples of the PCE germ at which the RVs
		              are to be evaluated. Each line is one sample. The number
					  of columns is the number of RVs.

	Output:
		Numpy array with PCE evaluations
	"""

	# Get data set dimensions etc.
	n_test_samples = germ_samples.shape[0]
	ndim = germ_samples.shape[1]
	npce = pc_model.GetNumberPCTerms()

	# Put PC germ samples in a UQTk array
	std_samples_uqtk = uqtkarray.dblArray2D(n_test_samples, ndim)
	std_samples_uqtk.setnpdblArray(np.asfortranarray(germ_samples))

	# Numpy array to store all RVs evaluated from sampled PCEs
	rvs_sampled = np.zeros(n_test_samples)

	# Evaluate PCE for RVs in each dimension
	# Create and fill UQTk array for PC coefficients
	c_k_1d_uqtk = uqtkarray.dblArray1D(npce,0.0)
	for ip in range(npce):
		c_k_1d_uqtk[ip] = pc_coeffs[ip]

	# Create UQTk array to store outputs in
	rv_from_pce_uqtk = uqtkarray.dblArray1D(n_test_samples,0.0)

	# Evaluate the PCEs for each input RV at those random samples
	pc_model.EvalPCAtCustPoints(rv_from_pce_uqtk,std_samples_uqtk,c_k_1d_uqtk)

	# Put evaluated samples in numpy array
	for isamp in range(n_test_samples):
		rvs_sampled[isamp] = rv_from_pce_uqtk[isamp]

	# Return numpy array of PCE evaluations
	return rvs_sampled

def get_quadpts(pc_model,ndim):
	"""
	Generates quadrature points
	Input:
		pc_model: PC object with info about PCE
		ndim: number of dimensions of the PCE
	Output:
		qdpts: numpy array of quadrature points
	"""
	# Get the quadrature points
	qdpts_uqtk = uqtkarray.dblArray2D()
	pc_model.GetQuadPoints(qdpts_uqtk)
	totquat = pc_model.GetNQuadPoints() # Total number of quadrature points

	# Convert quad points to a numpy array
	qdpts = np.zeros((totquat,ndim))
	qdpts_uqtk.getnpdblArray(qdpts)
	return qdpts, totquat

def fwd_model(Ti_samples,To_samples, dw_samples, kw_samples,hi_samples,ho_samples,TA_samples):
	"""
	Evaluates the forward model
	Input:
		Samples of the 7 uncertain, Gaussian inputs
	Output:
		Q_evals: numpy array of evaluations of the forward model

	"""
	#Determine number of samples (totquat)
	totquat=len(Ti_samples)
	# List to store values of Q (assuming no radiative heat transfer) calculated from
	# the random samples of the parameters
	Q_samples_4PCE=[]
	# List to store values of Q assuming radiative heat transfer occurs
	#Q_r_samples_4PCE=[]
	# Calculate values of heat flux Q (assuming no radiative heat transfer)
	# for the different sample values and append to the list
	for i in range(totquat):
		(Q,T1,T2)=compute_heat_flux(Ti_samples[i], To_samples[i], dw_samples[i],\
			kw_samples[i], hi_samples[i], ho_samples[i])
		Q_samples_4PCE.append(Q)
		# Calculate values of heat flux Q assuming radiative heat transfer to atmosphere and append to list
		# For the required estimates of Q,T1, and T2 needed to solve the nonlinear system,
		# we use the values obtained by solving the system assuming no radiative heat transfer
		"""Q2=r_heat_flux(Ti_samples[i], To_samples[i], dw_samples[i], kw_samples[i],\
			hi_samples[i], ho_samples[i], TA_samples[i], (Q,T1,T2))
		Q_r_samples_4PCE.append(Q2)
	# Convert Q_r_samples_4PCE to numpy array
	Q_evals = np.array(Q_r_samples_4PCE)
	return Q_evals"""
		Convert Q_samples_4PCE to numpy array
		Q_evals = np.array(Q_samples_4PCE)
		return Q_evals"""


def KDE(fcn_evals):
	"""
	Performs kernel density estimation
	Input:
		fcn_evals: numpy array of evaluations of the forward model (values of heat flux Q)
	Output:
		xpts_pce: numpy array of points at which the PDF is estimated.
		PDF_data_pce: numpy array of estimated PDF values.
	"""
	# Perform KDE on fcn_evals
	kern_pce=stats.kde.gaussian_kde(fcn_evals)
	# Generate points at which to evaluate the PDF
	xpts_pce=np.linspace(fcn_evals.min(),fcn_evals.max(),200)
	# Evaluate the estimated PDF at these points
	PDF_data_pce=kern_pce(xpts_pce)
	return xpts_pce, PDF_data_pce
