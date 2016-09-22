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
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle, Wedge, Polygon
from itertools import combinations

from pylab import *

sys.path.append(os.environ['UQTK_INS'])
import PyUQTk.utils.colors as ut

uqtkbin=os.environ['UQTK_INS']+"/bin/"


rc('legend',loc='upper left', fontsize=12)
rc('lines', linewidth=1, color='r')
rc('axes',linewidth=3,grid=True,labelsize=22)
rc('xtick',labelsize=20)
rc('ytick',labelsize=20)

#############################################################
def saveplot(figname):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        savefig(figname)
        clf()

#############################################################
def plot_pcpdf(pctype,mindex,cfs,nsam,custom_xlabel,figname='pcdens.eps',showplot=False):
    
    np.savetxt('mi',mindex,fmt='%d')
    np.savetxt('cfs',cfs)
    dim=mindex.shape[1]
    cmd=uqtkbin+"pce_rv -w'PCmi' -n"+str(nsam)+" -p"+str(dim)+" -f'cfs' -m'mi' -x"+pctype+" > pcrv.log"
    os.system(cmd)
    
    cmd=uqtkbin+"pdf_cl -i rvar.dat -g 1000 > pdfcl.log"
    os.system(cmd)
    xtarget=np.loadtxt('dens.dat')[:,:-1]
    dens=np.loadtxt('dens.dat')[:,-1:]
   

    #rv=np.loadtxt('rvar.dat')
    #xtarget=np.linspace(rv.min(),rv.max(),100)
    #kernlin=stats.kde.gaussian_kde(rv)
    #dens=kernlin.evaluate(xtarget)
    
    np.savetxt('pcdens.dat',np.vstack((xtarget,dens)).T)
    
    figure(figsize=(12,8))
    plot(xtarget,dens)
    xlabel(custom_xlabel)
    ylabel('PDF')
    
    saveplot(figname)
    if showplot:
        show()

    #cleanup
    os.system('rm mi cfs rvar.dat')
    
#############################################################

def plot_mindex(mindex,varfrac,varname,figname='mindex.eps',showplot=False):

    custom_xlabel='Param i'
    custom_ylabel='Param j'
    
    npc=mindex.shape[0]
    ndim=mindex.shape[1]
    plt.figure(figsize=(14,10))
    ij=[]
    acfs=[]
    k=0
    for basis in mindex:
        nzeros=np.nonzero(basis)[0]
        if nzeros.shape[0]==0:
            ij.append((0,0))
            acfs.append(varfrac[k])
        elif nzeros.shape[0]==1:
            ijcur=(0,nzeros[0]+1)
            if ijcur in ij:
                acfs[ij.index(ijcur)]+=varfrac[k]
            else:
                ij.append(ijcur)
                acfs.append(varfrac[k])
        elif nzeros.shape[0]==2:
            ijcur=(nzeros[0]+1,nzeros[1]+1)
            if ijcur in ij:
                acfs[ij.index(ijcur)]+=varfrac[k]
            else:
                ij.append(ijcur)
                acfs.append(varfrac[k])
        else:
            #print "More than a couple detected!", nzeros+1
            for cc in combinations(nzeros, 2):
                ijcur=(cc[0]+1,cc[1]+1) #[ic+1 for ic in cc]
                #print "adding to ",ijcur
                if ijcur in ij:
                    acfs[ij.index(ijcur)]+=varfrac[k]
                else:
                    ij.append(ijcur)
                    acfs.append(varfrac[k])
        k+=1
    ija=np.array(ij)
    #print "ija",ija,acfs

    pad=0.1
    plt.fill_between(range(ndim+2),-pad,range(ndim+2),color='lightgrey')
    plt.plot([-pad,ndim+pad],[-pad,ndim+pad],'k-',lw=1)
    if varfrac==[]:
        #plot(mindex[:,0],mindex[:,1],'bo',markersize=13)
        plt.scatter(ija[:,0],ija[:,1],s=320, marker = 'o',cmap = cm.jet )
    else:
        #print cfs
        plt.scatter(ija[:,0],ija[:,1],s=320, c=acfs, marker = 'o',vmin=0.0,vmax=max(acfs))
        
        #cp=get_cp()
        #cs=plt.gva().pcolor(abs(cfs),cmap=cp);
        plt.colorbar(pad=0.05,shrink=0.9)
        plt.gca().set_aspect('equal')
        #cbar=plt.colorbar(ticks=[0.,0.6,1.0])
        #cbar.ax.set_ylim([0.0,1.0])
        #cbar.set_ticklabels(['0.0', '0.6','1.0'])
        #plt.tight_layout()


    #plt.gca().xaxis.set_label_position('top')
    #plt.gca().xaxis.tick_top()
    plt.gca().set_xticks(range(ndim+1), minor=False)
    plt.gca().set_yticks(range(ndim+1), minor=False)
    plt.gca().xaxis.grid(True, which='major')
    plt.gca().yaxis.grid(True, which='major')

    plt.xlabel(custom_xlabel)
    plt.ylabel(custom_ylabel)
    plt.xlim([-pad, ndim+pad])
    plt.ylim([ndim+pad,-pad])

    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.text(int(ndim/2),int(ndim/3),varname,fontsize=37)
    

    saveplot(figname)
    if showplot:
        show()


def plot_micf(mindex,cfs=[],figname='micf.eps',showplot=False):
    """Plots 2d or 3d multiindices"""
    
    custom_xlabel='Dim 1'
    custom_ylabel='Dim 2'
    custom_zlabel='Dim 3'

    npc=mindex.shape[0]
    ndim=mindex.shape[1]

    if (ndim==2):
        if cfs==[]:
            #plot(mindex[:,0],mindex[:,1],'bo',markersize=13)
            scatter(mindex[:,0],mindex[:,1],s=150, marker = 'o',cmap = cm.jet )
        else:
            scatter(mindex[:,0],mindex[:,1],s=150, c=cfs, marker = 'o',cmap = cm.jet )
    elif (ndim==3):
        ax = figure().add_subplot(111, projection='3d')
        if cfs==[]:
            ax.scatter(mindex[:,0],mindex[:,1],mindex[:,2],s=50)
        else:
            ax.scatter(mindex[:,0],mindex[:,1],mindex[:,2],c=cfs,s=50)

        ax.set_zlabel(custom_zlabel)
        ax.set_zlim([-.5, max(mindex[:,2])+.5])

    else:
        raise NameError("Multi-index should be 2d or 3d")

    xlabel(custom_xlabel)
    ylabel(custom_ylabel)
    xlim([-.5, max(mindex[:,0])+.5])
    ylim([-.5, max(mindex[:,1])+.5])

    saveplot(figname)
    if showplot:
        show()



#############################################################
def plot_idm(data,model,errbar,sort='none',figname='idm.eps',showplot=False):
    """Plots data and model on the same axis"""
    erb=True

    axes_labels=['Run Id','Model / Surrogate']

    custom_xlabel=axes_labels[0]
    custom_ylabel=axes_labels[1]
    
    figure(figsize=(12,8))
    
    npts=data.shape[0]
    neach=1
    if (data.ndim>1):
        neach=data.shape[1]
    
    erbl,erbh=errbar
    
    if (sort=='model'):
        ind=argsort(model)
    elif (sort=='data'):
        ind=argsort(data)
    elif (sort=='none'):
        ind=range(npts)


    ddata=data.reshape(npts,neach)
    
    if (erb):
        errorbar(range(1,npts+1),model[ind],yerr=[erbl,erbh],fmt='o', markersize=2,ecolor='grey')
    
    if (sort!='model'):
        plot(range(1,npts+1),model[ind], 'bo', label='Surrogate')
    for j in range(neach):
        plot(range(1,npts+1),ddata[ind,j], 'ro',label='Model')
    if (sort=='model'):
        plot(range(1,npts+1),model[ind], 'bo', label='Surrogate')
    
    xlabel(custom_xlabel)
    ylabel(custom_ylabel)
    #title('Data vs Model')
    legend()
    
    
    saveplot(figname)
    if showplot:
        show()    

#############################################################
def plot_dm(datas,models,errorbars,labels,axes_labels,figname='dm.eps',showplot=False):
    """Plots data-vs-model and overays y=x"""
    erb=True

    custom_xlabel=axes_labels[0]
    custom_ylabel=axes_labels[1]

    figure(figsize=(10,10))
    ncase=len(datas)
    # Create colors list
    colors=ut.set_colors(ncase)
    yy=np.empty((0,1))
    for i in range(ncase):
        data=datas[i]
        model=models[i]
        erbl,erbh=errorbars[i]
        npts=data.shape[0]
        neach=1
        if (data.ndim>1):
            neach=data.shape[1]

        #neb=model.shape[1]-1# errbars not implemented yet

        
    
        ddata=data.reshape(npts,neach)


        for j in range(neach):
            yy=np.append(yy,ddata[:,j])
            if (erb):
                errorbar(ddata[:,j],model,yerr=[erbl,erbh],fmt='o', markersize=2,ecolor='grey')
            plot(ddata[:,j],model, 'o',color=colors[i],label=labels[i])

    delt=0.1*(yy.max()-yy.min())
    minmax=[yy.min()-delt, yy.max()+delt]
    plot(minmax,minmax,'r--',linewidth=2,label='y=x')

    xlabel(custom_xlabel)
    ylabel(custom_ylabel)
    #title('Data vs Model')
    legend()

    #xscale('log')
    #yscale('log')

    saveplot(figname)
    if showplot:
        show()

#############################################################

def plot_sens(sensdata,pars,cases,vis="bar",reverse=False,par_labels=[],case_labels=[],colors=[],figname='sens.eps',showplot=False):
    """Plots sensitivity for multiple observables"""
    
    ncases=sensdata.shape[0]
    npar=sensdata.shape[1]
    
    wd=0.6
    xlbl=''
    ylbl='Sensitivity'
    legend_show=True #False

    assert set(pars) <= set(range(npar))
    assert set(cases) <= set(range(ncases))
    
    # Set up the figure
    # TODO need to scale figure size according to the expected amount of legends
    xticklabel_size=25 
    if ncases>20:
        xticklabel_size=1000/ncases
    fig = plt.figure(figsize=(20,12))
    #fig = plt.figure(figsize=(18,12))
    fig.add_axes([0.1,0.3,0.8,0.65])
    
    #########
    
    # Default parameter names
    if (par_labels==[]):
        for i in range(npar):
            par_labels.append(('par_'+str(i+1)))
    # Default case names
    if (case_labels==[]):
        for i in range(ncases):
            case_labels.append(('case_'+str(i+1)))


    if(reverse):
        tmp=par_labels
        par_labels=case_labels
        case_labels=tmp
        tmp=pars
        pars=cases
        cases=tmp
        sensdata=sensdata.transpose()
    ##############################################################################

    npar_=len(pars)
    ncases_=len(cases)

    # Create colors list
    if colors==[]:
        colors=ut.set_colors(npar_)


    case_labels_=[]
    for i in range(ncases_):
        case_labels_.append(case_labels[cases[i]])

    if (vis=="graph"):
        for i in range(npar_):
            plot(np.array(range(1,ncases_+1)),sensdata[cases,i], '-o',color=colors[pars[i]], label=par_labels[pars[i]])
    elif (vis=="bar"):
        curr=np.zeros((ncases_))
        #print pars,colors
        for i in range(npar_):
            bar(np.array(range(1,ncases_+1)),sensdata[cases,i], width=wd,color=colors[pars[i]], bottom=curr, label=par_labels[pars[i]])
            curr=sensdata[cases,i]+curr
        if ncases>20:
            xticks(np.array(range(1,ncases_+1))+wd/2.,case_labels_,rotation='vertical')
        else:
            xticks(np.array(range(1,ncases_+1))+wd/2.,case_labels_)
        xlim(1-wd/2.,ncases_+1.5*wd)
    #ylim(0.0,1.0)
    #elif (vis=="stack"):
    #    fnx = lambda : np.random.randint(5, 50, 10)
    #    y = np.row_stack((fnx(), fnx(), fnx()))
    #    x = np.arange(10)
    #    print y
    #    fig, ax = plt.subplots()
    #    plt.stackplot(x, y)

    xlabel(xlbl)
    ylabel(ylbl)
    
    maxsens=max(max(curr),1.0)
    ylim([0,maxsens])
    if (legend_show):
        legend(bbox_to_anchor=(1.0, -0.05),fancybox=True, shadow=True,ncol=5,labelspacing=-0.1)
        #legend(bbox_to_anchor=(0.0, -0.05),fancybox=True, shadow=True,ncol=5,labelspacing=-0.1)

    zed = [tick.label.set_fontsize(xticklabel_size) for tick in gca().xaxis.get_major_ticks()]

    saveplot(figname)
    if showplot:
        show()

##################################################################################################


def plot_senscirc(varname, msens,jsens,inpar_names,figname='senscirc.eps',showplot=False):
    
    Nmain=min(len(np.nonzero(msens)[0]),6)
    Nsec=Nmain-1
    lwMax=10
    lwCut=0.2
    radMain=50
    radOut=15
    lext=0.4
    verbose=0
    
    nx,ny=jsens.shape
    

    #jsens=np.log10(jsens);
    #print msens
    ind=msens.argsort()[::-1];
    msensShort=msens[ind[0:Nmain]]
    if verbose > 0:
        for i in range(Nmain):
            print "Variable ",ind[i],", main sensitivity ",msens[ind[i]]
    fig = plt.figure(figsize=(10,8))
    ax=fig.add_axes([0.05, 0.05, 0.9, 0.9],aspect='equal')
    #circ=pylab.Circle((0,0),radius=0.5,color='r')
    circ=Wedge((0.0,0.0),1.01, 0, 360, width=0.02,color='r')
    ax.add_patch(circ)
    maxJfr=-1.e10;
    for i in range(Nmain):
        jfr_i=np.array(np.zeros(nx))
        iord=ind[i]
        for j in range(iord):
            jfr_i[j]=jsens[j,iord]
        for j in range(iord+1,nx):
            jfr_i[j]=jsens[iord,j]
        ind_j=jfr_i.argsort()[::-1];
        if jfr_i[ind_j[0]] > maxJfr: maxJfr = jfr_i[ind_j[0]];
        if verbose > 1:
            for j in range(Nsec):
                print iord," ",ind_j[j],jfr_i[ind_j[j]]
    if verbose > 1:
        print "Maximum joint sensitivity :",maxJfr
    gopar=[]
    for i in range(Nmain):
        jfr_i=np.array(np.zeros(nx))
        iord=ind[i]
        for j in range(iord):
            jfr_i[j]=jsens[j,iord]
        for j in range(iord+1,nx):
            jfr_i[j]=jsens[iord,j]
        ind_j=jfr_i.argsort()[::-1];
        elst=[]
        for j in range(Nsec):
            if maxJfr>0.0 and jfr_i[ind_j[j]]/maxJfr >= lwCut:
                posj=[k for k,x in enumerate(ind[:Nmain]) if x == ind_j[j]]
                if verbose > 2:
                    print j," ",posj
                if len(posj) > 0 :
                    x1=np.cos(0.5*np.pi+(2.0*np.pi*posj[0])/Nmain)
                    x2=np.cos(0.5*np.pi+(2.0*np.pi*i      )/Nmain)
                    y1=np.sin(0.5*np.pi+(2.0*np.pi*posj[0])/Nmain)
                    y2=np.sin(0.5*np.pi+(2.0*np.pi*i      )/Nmain)
                    lw=lwMax*jfr_i[ind_j[j]]/maxJfr
                    plt.plot([x1,x2],[y1,y2],'g-',linewidth=lw)
                    if ( verbose > 2 ):
                        print iord," ",ind[posj[0]]
                else:
                    elst.append(j)
        if len(elst) > 0:
            asft=[0,-1,1]
            for k in range(min(len(elst),3)):
                ang=0.5*np.pi+(2.0*np.pi*i)/Nmain+2*np.pi/12*asft[k]
                x2=np.cos(0.5*np.pi+(2.0*np.pi*i)/Nmain)
                y2=np.sin(0.5*np.pi+(2.0*np.pi*i)/Nmain)
                x1=x2+lext*np.cos(ang)
                y1=y2+lext*np.sin(ang)
                lw=lwMax*jfr_i[ind_j[elst[k]]]/maxJfr
                plt.plot([x1,x2],[y1,y2],'g-',linewidth=lw)
                plt.plot([x1],[y1],"wo",markersize=radOut,markeredgecolor='k',
                         markeredgewidth=2)
                if ( ind_j[elst[k]] > 32 ):
                    ltext=str(ind_j[elst[k]]+3)
                elif ( ind_j[elst[k]] > 30 ):
                    ltext=str(ind_j[elst[k]]+2)
                else:
                    ltext=str(ind_j[elst[k]]+1)
                plt.text(x1+(0.15)*np.cos(ang),y1+(0.15)*np.sin(ang),ltext,
                            ha='center',va='center',fontsize=16)
                posj=[k1 for k1,x in enumerate(gopar) if x == ind_j[elst[k]]]
                if len(posj)==0:
                    gopar.append(ind_j[elst[k]])
        if ( verbose > 2 ):
            print "------------------------"
    for i in range(Nmain):
        angl=0.5*np.pi+(2.0*np.pi*i)/Nmain
        xc=np.cos(angl);
        yc=np.sin(angl);
        msize=radMain*msens[ind[i]]/msens[ind[0]]
        plt.plot([xc],[yc],"bo",markersize=msize,markeredgecolor='k',markeredgewidth=2)
        da=1.0
        lab=0.2
        llab=lab*msens[ind[i]]/msens[ind[0]]
        
        ltext=str(ind[i]+1)
        lleg=ltext+" - "+inpar_names[ind[i]]
        plt.text(xc+(0.08+llab)*np.cos(angl+da),yc+(0.08+llab)*np.sin(angl+da),ltext,
                 ha='center',va='center',fontsize=16)
        plt.text(1.6,1.2-0.15*i,lleg,fontsize=16)
    for k in range(len(gopar)):
        lleg=str(gopar[k]+1)+" - "+inpar_names[gopar[k]]
        plt.text(1.6,1.2-0.15*Nmain-0.15*k,lleg,fontsize=16)

    plt.text(0.9,-1.2,varname,fontsize=27)

    ax.set_xlim([-1-1.6*lext,1.8+1.6*lext])
    ax.set_ylim([-1-1.6*lext,1+1.6*lext])
    ax.set_xticks([])
    ax.set_yticks([])
    
    saveplot(figname)
    if showplot:
        show()


##################################################################################################


def plot_sensmat(sensdata,pars,cases,vis="bar",reverse=False,par_labels=[],case_labels=[],figname='sensmat.eps',showplot=False):

    cdict = cm.jet._segmentdata.copy()
    cdict['red']=tuple([tuple([0.0,  1,   1  ]),
                        tuple([0.01, 0,   0  ]),
                        tuple([0.35, 0,   0  ]),
                        tuple([0.66, 1,   1  ]),
                        tuple([0.89, 1,   1  ]),
                        tuple([1,    0.5, 0.5])
                        ]
                       )
    cdict['green']=tuple([tuple([0.0,   1, 1]),
                          tuple([0.01,  0, 0]),
                          tuple([0.125, 0, 0]),
                          tuple([0.375, 1, 1]),
                          tuple([0.64,  1, 1]),
                          tuple([0.91,  0, 0]),
                          tuple([1,     0, 0])
                          ]
                         )
    cdict['blue']=tuple([tuple([0,    1.0,1.0]),
                         tuple([0.01, 0.5,0.5]),
                         tuple([0.11, 1,  1  ]),
                         tuple([0.34, 1,  1  ]),
                         tuple([0.65, 0,  0  ]),
                         tuple([1,    0,  0  ])
                         ]
                        )

    cp=matplotlib.colors.LinearSegmentedColormap('colormap',cdict,64)

    # Read varfrac files and retain indices of important params
    vlst=[]
    allSens=[]
    for nm in range(len(cases)):
        #vfr=np.array(column(readfile("varfrac."+nm+".dat")[0],0))
        vfr=sensdata[nm,:] #np.array(column(readfile(nm+".vf.dat")[0],0))
        allSens.append(vfr)
        vlst.append([ n for n,i in enumerate(vfr) if i>0.1 ])
    # Get union
    allV=[]
    for i in range(len(vlst)):
        allV=list(set(allV) | set(vlst[i]))
    allV=np.sort(allV)
    # Create matrix, populate, and rescale
    nobs=len(cases);
    npar=len(allV);
    print "Number of observables plotted = ", nobs
    print "Number of parameters plotted = ", npar
    jsens=np.array(np.zeros([nobs,npar]));
    for i in range(nobs):
        for j in range(npar):
            jsens[i,j]=allSens[i][allV[j]];
    #for i in range(nobs):
    #    jsens[i]=jsens[i]/jsens[i].max();
    jsens[np.where(jsens==0)]=0.5*jsens[np.where(jsens>0)].min();
    #for i in range(nobs):
     #   for j in range(npar):
      #      jsens[i,j]=np.log10(jsens[i,j]);

    par_labels_sorted=[];
    for i in allV:
        par_labels_sorted.append(par_labels[i]);
    # make fig
    fs1=13;
    fig = plt.figure(figsize=(10,3.9));
    ax=fig.add_axes([0.12, 0.27, 0.88, 0.68]);
    cs=ax.pcolor(jsens,cmap=cp);
    #cs=ax.pcolor(jsens,cmap=cm.jet)
    ax.set_xlim([0,npar]);
    ax.set_ylim([0,nobs]);
    ax.set_xticks([0.5+i for i in range(npar)]);
    ax.set_yticks([0.4+i for i in range(nobs)]);
    ax.set_yticklabels([case_labels[i] for i in range(nobs)],fontsize=fs1);
    ax.set_xticklabels([par_labels_sorted[i] for i in range(npar)],rotation=45,fontsize=fs1);
    ax.tick_params(length=0.0)
    cbar=plt.colorbar(cs)
    #cbar.set_ticks(range(-13,1,1))
    #cbar.set_ticklabels(['$10^{'+str(i)+'}$' for i in range(-13,1,1)])
   
        
    saveplot(figname)
    if showplot:
        show()


