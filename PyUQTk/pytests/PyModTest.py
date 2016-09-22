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
# include path to include PyUQTk
""" Test to make sure all Python modules load. """
import sys

print "Loading array module:"
sys.path.append('../uqtkarray/')
import uqtkarray 

print "Loading quadrature module:"
sys.path.append('../quad/')
import quad 

print "Loading bayesian compressed sensing module:"
sys.path.append('../bcs/')
import bcs

print "Loading polynomial chaos module:"
sys.path.append('../pce/')
import pce 

print "Loading tools module:"
sys.path.append('../tools')
import tools

#print "Loading dfi module:"
#sys.path.append('../dfi/')
#import dfi
