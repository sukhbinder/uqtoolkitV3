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
try:
	import numpy as np
except ImportError:
	print "Numpy module could not be found"

try:
	import matplotlib.pyplot as plt
	from matplotlib import rc
	rc('mathtext', default='regular')
except ImportError:
	print "Matplotlib not found"

try:
	from scipy import stats
except ImportError:
	print "Scipy stats module could not be found"

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

try:
    from heat_transfer_pce_tools import *
except ImportError:
    print "File with PCE utilities not found."


#####################################################################

# The uncertain, Gaussian parameters used to calculate the heat flux
Ti=293.0 # Room temperature in K
To=273.0    # Outside temperature in K
dw = 0.01  # Window thickness in m
kw = 1.0  # Window conductivity in W/mK
hi = 2.0  # Inner convective heat transfer coefficient in W/m^2K
ho = 6.0  # Outer wall convective heat transfer coefficient in W/m^2K
TA=  150 # Atmospheric temperature in K. Only used to calculate heat flux
		 # when it is assumed that radiative heat transfer occurs

# Set the standard deviations of these uncertain parameters
std_Ti=Ti*0.005
std_To=To*0.005
std_dw=dw*0.01
std_kw=kw*0.05
std_hi=hi*0.15
std_ho=ho*0.15
#td_TA=TA*0.1

######### Forward Propagation using Monte Carlo sampling #########

# Number of random samples
n = 100000

# Generate random samples of the uncertain parameters
samp_Ti=np.random.normal(Ti, std_Ti, n)
samp_To=np.random.normal(To, std_To, n)
samp_dw=np.random.normal(dw, std_dw, n)
samp_kw=np.random.normal(kw, std_kw, n)
samp_hi=np.random.normal(hi, std_hi, n)
samp_ho=np.random.normal(ho, std_ho, n)
#samp_TA=np.random.normal(TA, std_TA, n)
# Create list of sample arrays
samples=[samp_Ti, samp_To, samp_dw, samp_kw, samp_hi, samp_ho]

# List to store values of Q (assuming no radiative heat transfer) calculated from
# the random samples of the parameters
Q_samples=[]
# List to store values of Q assuming radiative heat transfer occurs
#Q_r_samples=[]
# Calculate values of heat flux Q (assuming no radiative heat transfer)
# for the different sample values and append to the list
for i in range(n):
	(Q)=compute_heat_flux(samp_Ti[i], samp_To[i], samp_dw[i], samp_kw[i], \
		samp_hi[i], samp_ho[i])
	Q_samples.append(Q)
# Calculate values of heat flux Q assuming radiative heat transfer to atmosphere and append to list
# For the required estimates of Q,T1, and T2 needed to solve the nonlinear system,
# we use the values obtained by solving the system assuming no radiative heat transfer
"""	Q2=r_heat_flux(samp_Ti[i], samp_To[i], samp_dw[i], samp_kw[i], samp_hi[i], \
		samp_ho[i], samp_TA[i], (Q,T1,T2))
	Q_r_samples.append(Q2)

# Convert Q_r_samples into numpy array
Q_r_samples=np.array(Q_r_samples)

# Perform KDE on Q_r_samples
xpts_Q2, PDF_data_Q2= KDE(Q_r_samples)
"""
Convert Q_samples into numpy array
Q_samples=np.array(Q_samples)

# Perform KDE on Q_r_samples
xpts_Q, PDF_data_Q= KDE(Q_samples)
#############################################

######### Forward Propagation using PCEs ##########
# Set verbose to 1 if you want intermediate print statements, otherwise set to 0
verbose = 0
nord = 3 # Order of the PCE
ndim = 6 # Number of dimensions of the PCE
pc_type = "HG"
pc_alpha = 0.0
pc_beta = 1.0
param= nord+1 # Parameter for quadrature point generation
# Equal to number of quad points per dimension for full quadrature or level for sparse quadrature

# Instantiate both PC objects

# Instantiate PC Object with full quadrature methods
print "\nInstantiating PC Objects\n"

pc_model = uqtkpce.PCSet("NISP", nord,ndim,pc_type, pc_alpha,pc_beta)
pc_model.SetQuadRule(pc_type, 'full', param)
npce = pc_model.GetNumberPCTerms() # Number of terms in the PCE
if verbose > 0:
	print "The number of terms in each PCE is",npce
	pc_model.PrintMultiIndexNormSquared()


# Instantiate PC Object with sparse quadrature methods
pc_model2 = uqtkpce.PCSet("NISP", nord,ndim,pc_type, pc_alpha,pc_beta)
pc_model2.SetQuadRule(pc_type, 'sparse', param)
npce2 = pc_model.GetNumberPCTerms() # Number of terms in the PCE
if verbose > 0:
	print "The number of terms in each PCE is",npce2
	pc_model.PrintMultiIndexNormSquared()

print "\nInstantiation complete"


########## Full quadrature methods ###########

#Get numpy array of quadrature points
qdpts, totquat= get_quadpts(pc_model,ndim)

# Convert Quadrature points in \xi_i to equivalent samples of input parameters
# (taking advantage of the fact that inputs are assumed to be Gaussian)
Ti_samples = Ti + std_Ti * qdpts[:,0]
To_samples = To + std_To * qdpts[:,1]
dw_samples= dw + std_dw * qdpts[:,2]
kw_samples= kw + std_kw * qdpts[:,3]
hi_samples= hi + std_hi * qdpts[:,4]
ho_samples= ho + std_ho * qdpts[:,5]
#TA_samples= TA + std_TA * qdpts[:,6]

# Evaluate Forward model for sampled parameters
Q_evals=fwd_model(Ti_samples,To_samples, dw_samples, kw_samples,hi_samples,ho_samples)
# Do the actual Galerkin Projection
c_k = GalerkinProjection(pc_model,Q_evals)
# Generate germ samples
germ_samples=np.random.normal(0,1, (n,ndim))
# Evaluate the PCE at the germ samples
pce_evals=evaluate_pce(pc_model,c_k,germ_samples)
#Peform kernel density estimation
xpts_pce, PDF_data_pce= KDE(pce_evals)
"""
##### Sparse quadrature methods ######

#Get numpy array of quadrature points
qdpts2, totquat2= get_quadpts(pc_model2,ndim)


# Convert Quadrature points in \xi_i to equivalent samples of input parameters
# (taking advantage of the fact that inputs are assumed to be Gaussian)
Ti_samples2 = Ti + std_Ti * qdpts2[:,0]
To_samples2 = To + std_To * qdpts2[:,1]
dw_samples2= dw + std_dw * qdpts2[:,2]
kw_samples2= kw + std_kw * qdpts2[:,3]
hi_samples2= hi + std_hi * qdpts2[:,4]
ho_samples2= ho + std_ho * qdpts2[:,5]
TA_samples2= TA + std_TA * qdpts2[:,6]

# Evaluate Forward model for sampled parameters
Q_evals2=fwd_model(Ti_samples2,To_samples2, dw_samples2, kw_samples2,hi_samples2,ho_samples2, TA_samples2)
# Do the actual Galerkin Projection
c_k2 = GalerkinProjection(pc_model2,Q_evals2)
# Generate germ samples
germ_samples2=np.random.normal(0,1, (n,ndim))
# Evaluate the PCE at the germ samples
pce_evals2=evaluate_pce(pc_model2,c_k2,germ_samples2)
#Peform kernel density estimation
xpts_pce2, PDF_data_pce2= KDE(pce_evals2)
"""
# Print statements to indicate number of samples used
print "\nMonte Carlo sampling used %s points" %(n)
print "Full quadrature method used %s points"%(totquat)
print "Sparse quadrature method used %s points"%(totquat2)


# Plot the three PDF curves on the same figure
plt.figure(figsize=(10,10))
plt.plot(xpts_pce, PDF_data_pce, linewidth=2, color='r', label='NISP full quadrature method')
#plt.plot(xpts_Q2, PDF_data_Q2, linewidth=2, color='b', label='Monte Carlo Sampling')
#plt.plot(xpts_pce2, PDF_data_pce2, linewidth=2, color='g', label= 'NISP sparse quadrature method')

# Label Axes
plt.xlabel("Total Heat Flux ($W/m^2$)", size=16)
plt.ylabel("PDF", size=16)
# Add title
plt.suptitle("Heat Transfer Through a Window", size=20)
# Change tick size
plt.tick_params(axis='both', labelsize=14)
# Pad tick labels
plt.gca().tick_params(pad=6)
# Create legend
plt.legend(loc='upper left', prop={'size':12})
# Save figure
fig_name="heat_flux_pce.pdf"
plt.savefig(fig_name)
print "\nheat_flux_pce.pdf has been saved."
# Show figure
plt.show()
