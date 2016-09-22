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
Proof-of-concept functions to play around with several ordering
sequences, e.g.
  1. lexicographical order (lex)
  2. colexicographic order (colex)
  3. reverse lexicographical order (revlex)
  4. reverse colexicographical order (revcolex)
"""

import os
import sys

try:
    import numpy as npy
except ImportError:
    print "Numpy was not found. "

def sort_lex(a,b):
"""
  Indicator function for lexicographical order
"""
    n=a.shape[0]
    for i in range(n):
        if (a[i]>b[i]):
            return (1)
        elif (b[i]>a[i]):
            return (-1)
    return(0);

def sort_colex(a,b):
"""
  Indicator function for colexicographical order
"""
    n=a.shape[0]
    for i in range(n-1,0,-1):
        if (a[i]>b[i]):
            return (1)
        elif (b[i]>a[i]):
            return (-1)
    return(0);

def sort_revlex(a,b):
"""
  Indicator function for reverse lexicographical order
"""
    n=a.shape[0]
    for i in range(n):
        if (a[i]<b[i]):
            return (1)
        elif (b[i]<a[i]):
            return (-1)
    return(0);

def sort_revcolex(a,b):
"""
  Indicator function for reverse colexicographical order
"""
    n=a.shape[0]
    for i in range(n-1,0,-1):
        if (a[i]<b[i]):
            return (1)
        elif (b[i]<a[i]):
            return (-1)
    return(0);

def graded_sorted(mi,fsort):
"""
  Function implementing graded sort (all multi-indeces of a certain
  order are grouped together)
"""
    if mi.shape[0]<2: return mi
    ist=1; ien=1
    iord = 0;
    while ist < mi.shape[0]:
        iord += 1
        ist=mi.shape[0]
        for i in range(mi.shape[0]):
            if mi[i].sum() == iord:
                ist = i
                break
        ien = mi.shape[0]
        for i in range(ist,mi.shape[0]):
            if mi[i].sum() == iord+1:
                ien = i
                break
        if ist < mi.shape[0]:
            print iord,ist,ien
            miS = npy.array(sorted(mi[ist:ien],fsort))
            for i in range(ist,ien):
                mi[i] = miS[i-ist].copy()
    return mi
    
def getNPC(ndim, norder):
"""
  No of PCE terms (total order)
"""
  if (norder==-1): return 0
  enume=1
  denom=1
  minNO = min(norder,ndim)
  for k in range(minNO):
    enume = enume*(norder+ndim-k)
    denom = denom*(k+1)
  return (enume/denom);

def getMIndex(ndim, norder,type):
"""
  Returns sorted no. of PCE terms and sorted multi-index
"""
  if ( ndim==0 ): return -1,npy.zeros(1);
  npc=getNPC(ndim,norder);
  ic=npy.ones(ndim,dtype='int');
  iup  = 0;
  mi=npy.zeros((npc,ndim))
  if (norder > 0):
    #-----------first order terms---------------------------
    for idim in range(ndim):
      iup+=1
      mi[iup,idim] = 1; 
  if (norder > 1):
    #-----------higher order terms--------------------------
    for iord in range(2,norder+1):
      lessiord = iup;
      for idim in range(ndim):
        for ii in range(idim+1,ndim):
          ic[idim] += ic[ii];
      for idimm in range(ndim):
        for ii in range(lessiord-ic[idimm]+1,lessiord+1):
          iup+=1
          mi[iup]=mi[ii].copy()
          mi[iup,idimm] += 1
  if type == 'lex':
    return npc,graded_sorted(mi,sort_lex)
  elif type == 'colex':
    return npc,graded_sorted(mi,sort_colex)
  elif type == 'colex':
    return npc,graded_sorted(mi,sort_colex)
  elif type == 'colex':
    return npc,graded_sorted(mi,sort_colex)
  else:
    print 'Unknown multi-index order type: ',type
    return -1,mi



      
