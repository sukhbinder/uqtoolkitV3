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
#=====================================================================================

import os
import getopt
import shutil
import sys
import numpy as np
import math
import random as rnd
import cPickle as pick

from model import model


uqtkbin=os.environ['UQTK_INS']+"/bin/"

#############################################################
def usage():
    # TODO more informative usage()
    # Usage string
    usage_str='uq_pc.py -r <run_regime> -p <pdomain_file> -m <method> -o <ord> -s <sam_method> -n <nqd> -v <nval>'
    def_str='uq_pc.py -r online_example -p pdomain_3d.txt -m proj -o 3 -s quad -n 7 -v 0'
    print "Correct syntax is"
    print usage_str
    print "Default values are"
    print def_str
    print "For more detailed information on parameters, refer to the UQTk Manual"
    

#############################################################

def model_pc(modelParam, pcparams):
    """PC surrogate evaluator"""
    #print "Running the surrogate model with parameters ", mparam

    np.savetxt('mindex.dat',pcparams[0],fmt='%d')
    np.savetxt('pccf.dat',pcparams[1])
    pctype=pcparams[2]

    np.savetxt('xdata.dat',modelParam)
    cmd=uqtkbin+"pce_eval -x'PC_mi' -f'pccf.dat' -s"+pctype+" -r'mindex.dat' > fev.log"
    print "Running", cmd
    os.system(cmd)
    pcoutput=np.loadtxt('ydata.dat')

    return pcoutput

#######################################################################################
#######################################################################################
#######################################################################################

def main(argv):
    
    # Defaults
    run_regime="online_example"  # Running regime, "online_example", "online_bb", "offline_prep" or "offline_post"
    inpc_file="pccf_all.txt"     # Input PC coefficient file
    pc_type="HG"                 # PC type
    in_pcdim=2                   # Input PC dimensionality
    in_pcord=1                   # Input PC order
    pred_mode="ms"               # Prediction mode, m, ms or msc
    
    pdomain_file="pdomain_3d.txt" # Parameter domain file
    method="proj"                 # Surrogate construction method, "proj", "bcs" or "lsq"
    sam_method="quad"             # Parameter sampling method, "quad" or "rand"
    sp_type="full"                # Quadrature sparsity type, "full" or "sparse"

    nqd=7                         # Number of quadrature points per dim (if "quad" method), or
                                  # number of  random samples (if "rand" method)
    nval=0                        # Number of random validation samples
    out_pcord=1                   # Output PC order
    tol=1.e-3                     # Default tolerance (currently for BCS only)
    
    # Flags for input checks
    rflag=False
    pflag=False
    sflag=False
    nflag=False
    mflag=False
    oflag=False
    vflag=False
    cflag=False
    xflag=False
    dflag=False
    qflag=False
    fflag=False
    iflag=False
    aflag=False
    bflag=False
    eflag=False

    # Hardwired names
    input_train='ptrain.dat'
    input_val='pval.dat'
    qd_train='qtrain.dat'
    wg_train='wtrain.dat'
    qd_val='qval.dat'
    output_train='ytrain.dat'
    output_val='yval.dat'
    
    try:
        opts, args = getopt.getopt(argv,"hr:p:c:x:d:m:o:s:n:v:q:f:t:i:a:b:e:",["regime=","pdom=","method=","ord=","sampl=","nqd=","nval="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-r", "--regime"):
            run_regime = arg
            rflag=True
        elif opt in ("-p", "--pdom"):
            pdomain_file = arg
            pflag=True
        elif opt in ("-c", "--pcfile"):
            inpc_file = arg
            cflag=True
        elif opt in ("-x", "--pctype"):
            pc_type = arg
            xflag=True
        elif opt in ("-d", "--pcdim"):
            in_pcdim = int(arg)
            dflag=True
        elif opt in ("-o", "--pcord"):
            in_pcord = int(arg)
            oflag=True
        elif opt in ("-m", "--method"):
            method = arg
            mflag=True
        elif opt in ("-s", "--sampl"):
            sam_method = arg
            sflag=True
        elif opt in ("-n", "--nqd"):
            nqd = int(arg)
            nflag=True
        elif opt in ("-v", "--nval"):
            nval = int(arg)
            vflag=True
        elif opt in ("-q", "--nqd"):
            nqd = int(arg)
            qflag=True
        elif opt in ("-f", "--sparsity"):
            sp_type = arg
            fflag=True
        elif opt in ("-t", "--outord"):
            out_pcord = int(arg)
            tflag=True
        elif opt in ("-i", "--pred"):
            pred_mode = arg
            iflag=True
        elif opt in ("-a", "--minout"):
            minout = int(arg)
            aflag=True
        elif opt in ("-b", "--maxout"):
            maxout = int(arg)
            bflag=True
        elif opt in ("-e", "--tolerance"):
            tol = float(arg)
            eflag=True
    # TODO Check that -r is given?

    # Argument checks
    if(pflag and cflag):
        print "Need to provide input domain or input PC file, not both. Exiting."
        sys.exit()
    
    if ( (pflag) and (dflag or oflag or xflag) ):
            print "No need to specify input dimension (-d) or order (-o) or pctype (-x), if domain file %s is given. Exiting. " % pdomain_file
            sys.exit()

    #if (not pflag and not cflag and not dflag):
    #    print "Need to specify either parameter domain file, or parameter PC file, or dimensionality. Exiting."
    #    sys.exit()

    if (cflag):
        if (os.path.isfile(inpc_file)):
            pcf_all=np.atleast_2d(np.loadtxt(inpc_file))
            # TODO sanity checks on inpc_dim and inpc_ord
        else:
            print "Error: The requested input PC coefficient file %s does not exist. Exiting." % inpc_file
            sys.exit()
    else:
        
        if (pflag):
            # Load parameter domain file
            if (os.path.isfile(pdomain_file)):
                pdom=np.loadtxt(pdomain_file).reshape(-1,2)
                assert(pdom.shape[1]==2)
                pcf_all=np.vstack((0.5*(pdom[:,1]+pdom[:,0]),np.diag(0.5*(pdom[:,1]-pdom[:,0]))))
                np.savetxt('inpccf.dat',pcf_all)
                in_pcdim=pcf_all.shape[1]
                in_pcord=1
                pc_type="LU"

                for i in range(pdom.shape[0]):
                    if(pdom[i,0]>pdom[i,1]):
                        print "Error: The domain file %s contains wrong bounds. Check the row number %d. Exiting." % (pdomain_file,i+1)
                        sys.exit()
            else:
                print "Error: The requested domain file %s does not exist. Exiting." % pdomain_file
                sys.exit()

        else:
                
            pcf_all=np.vstack((np.zeros((in_pcdim,)),np.eye(in_pcdim)))
            np.savetxt('inpccf.dat',pcf_all)
            in_pcord=1
            pc_type="LU"



    # Get the dimensions
    npar=pcf_all.shape[1]
    npc=pcf_all.shape[0] # not used



    # Print the inputs for reference
    print "Run regime                        ", run_regime
    if (cflag):
        print "Input PC coefficient file         ", inpc_file
        print "PC type                           ", pc_type
        print "Input PC dim                      ", in_pcdim
        print "Input PC order                    ", in_pcord
    else:
        print "Input parameter domain file       ", pdomain_file
    print "The number of input parameters    ", npar
    print "Method                            ", method
    print "Sampling method                   ", sam_method
    print " with parameter                   ", nqd
    print "Number of validation points       ", nval
  
    print "Sparsity type                     ", sp_type
    print " with parameter                   ", nqd
    print "Output PC order                   ", out_pcord


    # Sanity check to ensure projection uses quadrature points
    # TODO in principle, we can implement MC integration for the projection integral, too, 
    # but it is known to be quite inaccurate
    if run_regime!="offline_prep" and method=="proj" and sam_method!="quad":
        print "Projection requires quadrature sampling. Exiting."
        sys.exit(1)

    # (1) Generate sample points for online or offline_prep regimes 
    if run_regime!="offline_post":
        
        if sam_method=="quad":
            cmd=uqtkbin+"generate_quad -d"+str(in_pcdim)+"  -g"+pc_type+" -x"+sp_type+" -p"+str(nqd)+" > gq.log"
            print "Running "+cmd
            os.system(cmd)
            inqdp=np.loadtxt('qdpts.dat')
            inqdw=np.loadtxt('wghts.dat')
            np.savetxt(wg_train,inqdw)


        elif sam_method=="rand":
            seedval=np.random.randint(100, size=10)

            cmd=uqtkbin+"pce_rv -w PCvar -d"+str(in_pcdim)+"  -p"+str(in_pcdim)+" -x"+pc_type+" -n"+str(nqd)+" -s "+str(seedval[0])+" > pcrv.log"
            print "Running "+cmd
            os.system(cmd)

            inqdp=np.loadtxt('rvar.dat')
            
        else:
            print "Error: Sampling method is not recognized. Should be 'quad' or 'rand'. Exiting."
            sys.exit()

        np.savetxt(qd_train,inqdp)
        npt=inqdp.shape[0]
        print "Germ samples for training are in %s in a format %d x %d " % (qd_train,npt,in_pcdim)
        
        # Evaluate input PCs at quadrature points
        np.savetxt('xdata.dat',inqdp)
        inpar=np.empty((npt,npar))
        for i in range(npar):
            np.savetxt('pcf',pcf_all[:,i])
            cmd=uqtkbin+"pce_eval -x PC -s"+pc_type+" -o"+str(in_pcord)+" -f 'pcf' > pcev.log"
            print "Running "+cmd
            os.system(cmd)
            inpar[:,i]=np.loadtxt('ydata.dat')

        np.savetxt(input_train,inpar)
        print "Parameter samples for training are in %s in a format %d x %d " % (input_train,npt,npar)

        # Generate points, if requested, for the validation of the surrogate
        seedval=np.random.randint(100, size=10)
        if nval>0:
            cmd=uqtkbin+"pce_rv -w PCvar -d "+str(in_pcdim)+ " -n "+str(nval)+ " -p "+str(in_pcdim)+" -x "+pc_type+" -s "+str(seedval[1])+" >pcrv.log"
            print "Running",cmd
            os.system(cmd)
            qpar_val=np.loadtxt('rvar.dat')
            inpar_val=np.empty((nval,npar))
            for i in range(npar):
                np.savetxt('pcf',pcf_all[:,i])
                cmd="cp rvar.dat xdata.dat; "+uqtkbin+"pce_eval -x PC -s"+pc_type+" -o"+str(in_pcord)+" -f 'pcf' > pcev.log"
                print "Running "+cmd
                os.system(cmd)
                inpar_val[:,i]=np.loadtxt('ydata.dat')
            
            np.savetxt(qd_val,qpar_val)
            print "Germ samples for validation are in %s in a format %d x %d " % (qd_val,nval,in_pcdim)

            np.savetxt(input_val,inpar_val)
            print "Parameter samples for validation are in %s in a format %d x %d " % (input_val,nval,npar)

        # Exit if only sample preparation is required
        if run_regime=="offline_prep":
            print "Preparation of samples is done."
            sys.exit()
                
    ############################################################################
                
    # (2) Load sample points for online or offline_post regimes
    ptrain=np.loadtxt(input_train).reshape(-1,npar)
    inqdp=np.loadtxt(qd_train).reshape(-1,npar)
    if (nval>0):
        pval=np.loadtxt(input_val).reshape(-1,npar)
        qpar_val=np.loadtxt(qd_val).reshape(-1,npar)

    npt=ptrain.shape[0]
    print "Number of training points for surrogate construction : "+str(npt)

    ############################################################################

    # (3) Get model outputs

    # Run the model online or....
    if run_regime=="online_example":
        ytrain=model(ptrain)
        if (nval>0):
            yval=model(pval)

    elif run_regime=="online_bb":
        # TODO check model.x existence
        os.system('./model.x '+input_train+' '+output_train)
        ytrain=np.loadtxt(output_train).reshape(npt,-1)
        if (nval>0):
            os.system('./model.x '+input_val+' '+output_val)
            yval=np.loadtxt(output_val).reshape(nval,-1)

    # ...or read the results from offline simulations
    elif run_regime=="offline_post":
        ytrain=np.loadtxt(output_train).reshape(npt,-1)
        if (nval>0):
            yval=np.loadtxt(output_val).reshape(nval,-1)

    # Read the number of output observables or the number of values of deisgn parameters (e.g. location, time etc..) 
    nout_all=ytrain.shape[1]
    print "Number of output observables of the model : ", nout_all


    ############################################################################


    # (4) Obtain the PC surrogate using model simulations

    if (aflag):
        if (bflag):
            outrange=range(minout-1,maxout)
        else:
            outrange=range(minout-1,minout)
    else:
        if (bflag):
            outrange=range(maxout-1,maxout)
        else:
            outrange=range(nout_all)

    # put checks in
    nout = len(outrange)
    print "Number of output observables being analyzed : ", nout


    # Empty arrays and lists to store results
    pccf_all=[]
    mindex_all=[]
    varfrac_all=[]
    ccov_all=[]
    allsens_main=np.empty((nout,in_pcdim))
    allsens_total=np.empty((nout,in_pcdim))
    allsens_joint=np.empty((nout,in_pcdim, in_pcdim))
    ytrain_pc=np.empty((npt,nout))
    yval_pc=np.empty((nval,nout))
    errcheck_pc=np.empty((npt,nout))
    errcheck_val_pc=np.empty((nval,nout))

    err_training=np.empty((nout,))
    err_val=np.empty((nout,))

    # Generate PC multiindex
    cmd=uqtkbin+"gen_mi -x'TO' -p"+str(out_pcord)+" -q"+str(in_pcdim)+" > gmi.log; mv mindex.dat mi.dat"
    print "Running "+cmd
    os.system(cmd)
    mi=np.loadtxt('mi.dat')
    npc=mi.shape[0]

    inpar=np.loadtxt(input_train)
    xcheck=inqdp.copy()
    if (nval>0):
        inpar_val=np.loadtxt(input_val)
        qpar_val=np.loadtxt(qd_val).reshape(nval,-1)
        xcheck=np.vstack((inqdp,qpar_val))
    ncheck=xcheck.shape[0]


    # Loop over all output observables/locations

    i = 0

    for j in outrange:
        ################################
        
        # (4a) Build PC surrogate
        print "##################################################"
        print "Building PC for observable %d / %d" % (j+1,nout_all)
        np.savetxt('ydata.dat',ytrain[:,j])

        if method=="proj":

            inqdp=np.loadtxt(qd_train)
            inqdw=np.loadtxt(wg_train)
            np.savetxt('qdpts.dat',inqdp)
            np.savetxt('wghts.dat',inqdw)
            
            cmd=uqtkbin+"pce_resp -x"+pc_type+" -o"+str(out_pcord)+" -d"+str(in_pcdim)+" -e > pcr.log"
            print "Running "+cmd
            os.system(cmd)

            # Get the PC coefficients and multiindex
            pccf=np.loadtxt('PCcoeff_quad.dat')
            mindex=np.loadtxt('mindex.dat',dtype='int')

            ycheck_var=np.zeros((ncheck,))
            sig2=0.0
            ccov=np.zeros((mindex.shape[0],mindex.shape[0]))
            erb=np.zeros((ncheck,))

        elif method=="bcs":
            np.savetxt('xdata.dat',inqdp)
            np.savetxt('xcheck.dat',xcheck)
            np.savetxt('regparams.dat',np.ones((npc,)))
            cmd=uqtkbin+'regression -x xdata.dat -y ydata.dat -b PC_MI -s '+pc_type+' -p mi.dat -w regparams.dat -m '+pred_mode+' -r wbcs -t xcheck.dat -c '+str(tol)+' > regr.log'
            print "Running "+cmd
            os.system(cmd)

            # Get the PC coefficients and multiindex and the predictive errorbars
            pccf=np.loadtxt('coeff.dat')
            mindex=np.loadtxt('mindex_new.dat',dtype='int')

            ycheck_var=np.zeros((ncheck,))
            sig2=0.0
            ccov=np.zeros((mindex.shape[0],mindex.shape[0]))
            if (pred_mode!='m'):
                sig2=max(0.0,np.loadtxt('sigma2.dat'))
                ccov=np.loadtxt('Sig.dat')
                #if os.path.isfile('ycheck_var.dat'):
                ycheck_var=np.loadtxt('ycheck_var.dat')

            erb=np.sqrt(ycheck_var+sig2)


        elif method=="lsq":
            np.savetxt('xdata.dat',inqdp)
            np.savetxt('xcheck.dat',xcheck)
            np.savetxt('regparams.dat',np.ones((npc,)))
            cmd=uqtkbin+'regression -l0 -x xdata.dat -y ydata.dat -b PC_MI -s '+pc_type+' -p mi.dat -m '+pred_mode+' -r lsq -t xcheck.dat > regr.log'
            print "Running "+cmd
            os.system(cmd)
            #sys.exit()
            # Get the PC coefficients and multiindex and the predictive errorbars
            pccf=np.loadtxt('coeff.dat')
            mindex=np.loadtxt('mi.dat',dtype='int')

            ycheck_var=np.zeros((ncheck,))
            sig2=0.0
            ccov=np.zeros((mindex.shape[0],mindex.shape[0]))
            if (pred_mode!='m'):
                sig2=max(0.0,np.loadtxt('sigma2.dat'))
                ccov=np.loadtxt('Sig.dat')
                # This is a cheap hack to tolerate Cholesky error during LSQ when simpler polynomials are given much more complex mindices
                #if os.path.isfile('ycheck_var.dat'):
                ycheck_var=np.loadtxt('ycheck_var.dat')

            erb=np.sqrt(ycheck_var+sig2)


        else:
            print "Method not recognized, Exiting"
            sys.exit()

 



        # Append the results
        pccf_all.append(pccf)
        mindex_all.append(mindex)
        ccov_all.append(ccov)

        ################################

        # (4b) Evaluate the PC surrogate at training and validation points
        print "Evaluating surrogate at %d training points" % (npt)
        ytrain_pc[:,i]=model_pc(inqdp,[mindex,pccf,pc_type])
        err_training[i]=np.linalg.norm(ytrain[:,j]-ytrain_pc[:,i])/np.linalg.norm(ytrain[:,j])
        print "Surrogate relative error at training points : ", err_training[i]

        errcheck_pc[:,i]=erb[:npt]


        if (nval>0):

            print "Evaluating surrogate at %d validation points" % (nval)
            yval_pc[:,i]=model_pc(qpar_val,[mindex,pccf,pc_type])
            err_val[i]=np.linalg.norm(yval[:,j]-yval_pc[:,i])/np.linalg.norm(yval[:,j])
            print "Surrogate relative error at validation points : ", err_val[i]
            #np.savetxt('yval_pc.'+str(i+1)+'.dat',yval_pc)
            errcheck_val_pc[:,i]=erb[npt:]

        ################################
        
        # (4c) Compute sensitivities
        np.savetxt('PCcoeff.dat',pccf)
        cmd=uqtkbin+"pce_sens -m'mindex.dat' -f'PCcoeff.dat' -x"+pc_type+" > pcsens.log"
        print "Running "+cmd
        os.system(cmd)
        allsens_main[i,:]=np.loadtxt('mainsens.dat')
        allsens_total[i,:]=np.loadtxt('totsens.dat')
        allsens_joint[i,:,:]=np.loadtxt('jointsens.dat')
        print "Sum of main sensitivities :",sum(allsens_main[i,:])
        print "Sum of total sensitivities :",sum(allsens_total[i,:])
        varfrac=np.loadtxt('varfrac.dat')
        varfrac_all.append(varfrac)

        i+=1
    ############################################################################


    # Results container
    if(nval>0):
        results = {'outs':(outrange),'training':(inqdp,inpar,ytrain,ytrain_pc,errcheck_pc),'validation':(qpar_val,inpar_val,yval,yval_pc,errcheck_val_pc),'pcmi':(pccf_all,mindex_all,varfrac_all,ccov_all,pc_type),'sens':(allsens_main,allsens_total,allsens_joint),'err':(err_training,err_val)}
    else:
        results = {'outs':(outrange),'training':(inqdp,inpar,ytrain,ytrain_pc,errcheck_pc),'pcmi':(pccf_all,mindex_all,varfrac_all,ccov_all,pc_type),'sens':(allsens_main,allsens_total,allsens_joint),'err':(err_training)}

    # Save results
    pick.dump(results,open('results.pk','wb'),-1)


    # Cleanup of unneeded leftovers
    #del_cmd='rm -rf pcf ycheck*.dat'
    #os.system(del_cmd)

if __name__ == "__main__":
   main(sys.argv[1:])
