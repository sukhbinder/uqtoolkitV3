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
import shutil
import sys

try:
    import numpy as np
except ImportError:
    print "Numpy was not found. "

try:
    import matplotlib
except ImportError:
    print "Matplotlib was not found. "

try:
    from scipy import stats, mgrid, reshape, random
except ImportError:
    print "Scipy was not found. "

import math
import matplotlib.pyplot as plt
from pylab import *

sys.path.append(os.environ['UQTK_INS'])
import PyUQTk.utils.colors as ut

rc('legend',loc='upper left', fontsize=12)
rc('lines', linewidth=1, color='r')
rc('axes',linewidth=3,grid=True,labelsize=22)
rc('xtick',labelsize=20)
rc('ytick',labelsize=20)

#############################################################
def parallel_coordinates(parnames, values, labels, savefig=[]):
    """
    Plots parallel coordinates.
    Arguments:
        * parnames : list of d parameter names 
        * values   : (d,N) array of N data points with d parameters
        * labels   : list of N labels/categories, one per point
        * savefig  : figure name to save. If [], then shoe the plot
    """
    
    # Start the figure
    fig=figure(figsize=(14,7))
    fig.add_axes([0.1,0.15,0.8,0.8])
    ax = gca()
    
    # Categorize
    ulabels = np.unique(labels)
    n_labels = len(ulabels)
    
    # Set colors
    cmap = plt.get_cmap('prism')
    colors = cmap(np.arange(n_labels)*cmap.N/(n_labels+1))
    
    # Plot
    class_id = np.searchsorted(ulabels, labels)
    lines = plt.plot(values[:,:], 'ko-',ms=6,linewidth=0.7)
    [ l.set_color(colors[c]) for c,l in zip(class_id, lines) ]
    
    # Gridification
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_position(('outward', 5))
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('none')
    
    plt.xticks(np.arange(len(parnames)), parnames)
    plt.grid(axis='x', ls='-')
    
    leg_handlers = [ lines[np.where(class_id==id)[0][0]]
                    for id in range(n_labels)]
    ax.legend(leg_handlers, ulabels, frameon=False, loc='upper left',
                    ncol=len(labels),
                    bbox_to_anchor=(0, -0.03, 1, 0))

    # Show or save
    if (savefig==[]):
        plt.show()
    else:
        plt.savefig(savefig)
        plt.clf()


#############################################################

def plot_xx(d1,d2,parnames, values, labels, savefig=[]): #(x1,x2,inputs,labels,pnames,outfigdir='.'):
    """
    Plots one-dimension versus another with various labels.
    Arguments:
        * d1       : first dimension to plot
        * d2       : second dimension to plot
        * parnames : list of d parameter names 
        * values   : (d,N) array of N data points with d parameters
        * labels   : list of N labels/categories, one per point
        * savefig  : figure name to save. If [], then shoe the plot
    """

    # Start the figure
    fig=figure(figsize=(12,12))
    fig.add_axes([0.1,0.15,0.8,0.8])
    ax = gca()
    
    # Categorize
    ulabels = np.unique(labels)
    n_labels = len(ulabels)

    # Set colors
    cmap = plt.get_cmap('prism')
    colors = cmap(np.arange(n_labels)*cmap.N/(n_labels+1))
    
    # Plot
    class_id = np.searchsorted(ulabels, labels)
    for id in range(n_labels):
        plt.plot(values[class_id==id,d1],values[class_id==id,d2], 'o',color=colors[id],ms=7,label=ulabels[id])

    
    
    ax.legend(frameon=False, loc='upper left',
                  ncol=len(labels),
                  bbox_to_anchor=(0, -0.06, 1, 0))

    ax.set_xlabel(parnames[d1])
    ax.set_ylabel(parnames[d2])
    
    # Show or save
    if (savefig==[]):
        plt.show()
    else:
        plt.savefig(savefig)
        plt.clf()

#############################################################

def plot_xy(x,y,pname, outname, savefig=[]): 
    """
    Plots one array versus another.
    Arguments:
        * x        : array for x-axis
        * y        : array for y-axis
        * pname    : xlabel
        * outname  : ylabel
        * savefig  : figure name to save. If [], then shoe the plot
    """

    # Start the figure
    fig=figure(figsize=(12,8))
    ax = gca()

    # Plot
    plt.plot(x,y,'o')

    # Set labels
    ax.set_xlabel(pname)
    ax.set_ylabel(outname)
    
    # Show or save
    if (savefig==[]):
        plt.show()
    else:
        plt.savefig(savefig)
        plt.clf()









