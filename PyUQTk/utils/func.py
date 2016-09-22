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

"""
Generic tools for evaluation of standard functions 
and their integrals
"""

try:
    import numpy as np
except ImportError:
    "Need numpy"


from math import *
import random as rnd
import itertools

###################################################################################################


def func(xdata,model,func_params):
    """Generic function evaluator.
    Note:
        * Currently only genz functions are implemented.
        * Note that conventional Genz arguments are in [0,1], here the expected input is on [-1,1]
    Arguments:
        * xdata       : Nxd numpy array of input, should be in [-1,1]^d
        * model       : Model name, options are 'genz_osc', 'genz_exp', 'genz_cont', 'genz_gaus', 'genz_cpeak', 'genz_ppeak'
        * func_params : Auxiliary parameters
                      : For genz functions, an array of size d+1, the first entry being the shift, and the rest of the entries are the weights.
                      : See UQTk Manual for Genz formulae.
    Returns:
        * ydata       : An array of outputs of size N.
    """

    # Get the input size
    sam=xdata.shape[0]
    dim=xdata.shape[1]
    
    # Check the function types and evaluate
    if model == 'genz_osc':
        xdata=0.5*(xdata+1.)
        ydata=empty((sam,))
        gcf=func_params[1:]
        xtmp=dot(xdata,gcf)
        for j in range(sam):
            ydata[j]=cos(2.*pi*func_params[0]+xtmp[j])
    
    elif model == 'genz_exp':
        xdata=0.5*(xdata+1.)
        ydata=empty((sam,))
        ww=func_params[0]
        gcf=func_params[1:]
        
        xtmp=dot(xdata-ww,gcf)
        for j in range(sam):
            ydata[j]=exp(xtmp[j])
    
    elif model == 'genz_cont':
        xdata=0.5*(xdata+1.)
        ydata=empty((sam,))
        ww=func_params[0]
        gcf=func_params[1:]
        
        xtmp=dot(abs(xdata-ww),gcf)
        for j in range(sam):
            ydata[j]=exp(-xtmp[j])
    
    elif model == 'genz_gaus':
        xdata=0.5*(xdata+1.)
        ydata=empty((sam,))
        ww=func_params[0]
        gcf=func_params[1:]
        
        xtmp=dot((xdata-ww)*(xdata-ww),gcf*gcf)
        for j in range(sam):
            ydata[j]=exp(-xtmp[j])
    
    elif model == 'genz_cpeak':
        xdata=0.5*(xdata+1.)
        ydata=empty((sam,))
        #ww=param[0]
        gcf=func_params[1:]
        
        xtmp=1.+(dot(xdata,gcf)) #use abs if defined on [-1,1]
        for j in range(sam):
            ydata[j]=exp(-(dim+1.)*log(xtmp[j]))
    
    elif model == 'genz_ppeak':
        xdata=0.5*(xdata+1.)
        ydata=empty((sam,))
        ww=func_params[0]
        gcf=func_params[1:]
        
        for j in range(sam):
            prod=1.
            for i in range(dim):
                prod = prod / (1./(gcf[i]**2.)+(xdata[j,i]-ww)**2.)
            ydata[j]=prod

    return ydata

def integ_exact(model,func_params):
    """Generic function integral evaluator.
    Note:
        * Currently only genz functions are implemented.
        * Note that conventional Genz arguments are in [0,1], here the expected input is on [-1,1]
    Arguments:
        * model       : Model name, options are 'genz_osc', 'genz_exp', 'genz_cont', 'genz_gaus', 'genz_cpeak', 'genz_ppeak'
        * func_params : Auxiliary parameters
                      : For genz functions, an array of size d+1, the first entry being the shift, and the rest of the entries are the weights.
                      : See UQTk Manual for Genz integral formulae.
    Returns:
        * integ_ex    : A real number that is the integral over [-1,1]^d
    """


    if (model=='genz_osc'):
        gcf=func_params
        dim=gcf.shape[0]-1
        integ_ex=cos(2.*pi*gcf[0]+0.5*sum(gcf[1:]))
        for i in range(1,dim+1):
            integ_ex*=(2.*sin(gcf[i]/2.)/gcf[i])
    elif (model=='genz_exp'):
        gcf=func_params
        dim=gcf.shape[0]-1
        integ_ex=1.
        for i in range(1,dim+1):
            at1=exp(-gcf[i]*gcf[0])
            at2=exp(gcf[i]*(1.-gcf[0]))
            integ_ex*=((at2-at1)/(gcf[i]))
    elif (model=='genz_cont'):
        gcf=func_params
        dim=gcf.shape[0]-1
        integ_ex=1.
        for i in range(1,dim+1):
            integ_ex*= ((2.-exp(gcf[i]*(-gcf[0]))-exp(gcf[i]*(gcf[0]-1.)))/gcf[i])
    elif (model=='genz_gaus'):
        gcf=func_params
        dim=gcf.shape[0]-1
        integ_ex=1.
        for i in range(1,dim+1):
            at1=math.erf(-gcf[i]*gcf[0])
            at2=math.erf(gcf[i]*(1.-gcf[0]))
            integ_ex*=((at2-at1)*sqrt(pi)/(2.*gcf[i]))
    elif (model=='genz_cpeak'):
        gcf=func_params
        dim=gcf.shape[0]-1
        numer=0.0
        count=1
        denom=1.
        for i in range(1,dim+1):
            comb=list(itertools.combinations(range(1,dim+1),i))
            for j in range(len(comb)):
                assert(i==len(comb[j]))
                #print i,j,pow(-1,i)
                numer+=(pow(-1,i)/(1.+sum(gcf[list(comb[j])])))
                count+=1
            denom*=(i*gcf[i])
        #print count, numer
        integ_ex=(1.+numer)/denom
    elif (model=='genz_ppeak'):
        gcf=func_params
        dim=gcf.shape[0]-1
        integ_ex=1.
        for i in range(1,dim+1):
            at1=arctan(-gcf[i]*gcf[0])
            at2=arctan(gcf[i]*(1.-gcf[0]))
            integ_ex*=(gcf[i]*(at2-at1))

    return integ_ex

