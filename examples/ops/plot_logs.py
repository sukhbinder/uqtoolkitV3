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

import os
import sys
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from   matplotlib.lines import Line2D
from   pylab import *
import scipy as spy
from   scipy import stats

#if ( len(sys.argv) > 1 ):
#    sample_file_name=sys.argv[1]
#else:
#    print "Need file name as argument"
#    quit()

# Get scipy version
spv=[]
spver=spy.__version__
for i,c in enumerate(spver):
    if c==".": spv.append(i)
spver=int(spver[spv[0]+1:spv[1]])
print "scipy version: ",spver

#
# Load data for a, loga_int and loga_tay; set up KDE
#
a_samples=np.genfromtxt("samples.a.dat")
xa=np.linspace(a_samples.min(),a_samples.max(),200)
kernsa=stats.kde.gaussian_kde(a_samples)
pdfa=kernsa(xa)

lai_samples=np.genfromtxt("samples.loga_int.dat")
xlai=np.linspace(lai_samples.min(),lai_samples.max(),200)
kernslai=stats.kde.gaussian_kde(lai_samples)
pdflai=kernslai(xlai)

lat_samples=np.genfromtxt("samples.loga_tay.dat")
xlat=np.linspace(lat_samples.min(),lat_samples.max(),200)
kernslat=stats.kde.gaussian_kde(lat_samples)
pdflat=kernslat(xlat)

#if spver > 10:
#    kernsS.set_bandwidth(bw_method=kernsS.factor/2.0)
#    pdf2=kernsS(xS);
#    kernsS.set_bandwidth(bw_method=kernsS.factor*4.0)
#    pdf3=kernsS(xS);

#
#  Make the figure
#
lw1=2
fs1=18

# Plot pdf of a
fig = plt.figure(figsize=(8,6))
ax=fig.add_axes([0.10, 0.10, 0.85, 0.85]) ;
l1=plt.plot(xa,pdfa,linewidth=lw1,label="a")
#if spver > 10:
#    l2=plt.plot(xS,pdf2,linewidth=lw1,label="optimal/2")
#    l3=plt.plot(xS,pdf3,linewidth=lw1,label="optimal*2")

#xlb=sample_file_name.replace("samples.","").replace(".dat","")
#if xlb=="a":
#  xlb="\hat{a}"
#else:
#  xlb="\log(\hat{a})"
#ax.set_xlabel("$"+xlb+"$",fontsize=fs1)
#ax.set_ylabel("$PDF("+xlb+")$",fontsize=fs1)
ax.set_xlabel("$a$",fontsize=fs1)
ax.set_ylabel("$PDF(a)$",fontsize=fs1)
plt.legend(loc="upper left")
#ax.set_xlim([0.0,0.55])
#ax.set_ylim([0.0,5.0])
#ax.set_xticks([0,0.1,0.2,0.3,0.4,0.5])
#ax.set_yticks([0,1,2,3,4])
#leg=plt.legend( (l1[0],l2[0]),
#                ("Monte-Carlo samples","Polynomial Chaos"),'upper center' )
fig_file_name="pdf_a.pdf"
plt.savefig(fig_file_name)
    
# Plot pdf of ln(a)
fig2 = plt.figure(figsize=(8,6))
ax=fig2.add_axes([0.10, 0.10, 0.85, 0.85]) ;
l1=plt.plot(xlai,pdflai,linewidth=lw1,label="ln(a), Int")
l2=plt.plot(xlat,pdflat,linewidth=lw1,label="ln(a), Tay")

ax.set_xlabel("$ln(a)$",fontsize=fs1)
ax.set_ylabel("$PDF(ln(a))$",fontsize=fs1)
plt.legend(loc="upper left")
#ax.set_xlim([0.0,0.55])
#ax.set_ylim([0.0,5.0])
#ax.set_xticks([0,0.1,0.2,0.3,0.4,0.5])
#ax.set_yticks([0,1,2,3,4])
#leg=plt.legend( (l1[0],l2[0]),
#                ("Monte-Carlo samples","Polynomial Chaos"),'upper center' )
fig_file_name="pdf_lna.pdf"
plt.savefig(fig_file_name)
