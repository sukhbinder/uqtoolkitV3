/* =====================================================================================
                     The UQ Toolkit (UQTk) version 3.0
                     Copyright (2016) Sandia Corporation
                     http://www.sandia.gov/UQToolkit/

     Copyright (2016) Sandia Corporation. Under the terms of Contract DE-AC04-94AL85000
     with Sandia Corporation, the U.S. Government retains certain rights in this software.

     This file is part of The UQ Toolkit (UQTk)

     UQTk is free software: you can redistribute it and/or modify
     it under the terms of the GNU Lesser General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     UQTk is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU Lesser General Public License for more details.

     You should have received a copy of the GNU Lesser General Public License
     along with UQTk.  If not, see <http://www.gnu.org/licenses/>.

     Questions? Contact Bert Debusschere <bjdebus@sandia.gov>
     Sandia National Laboratories, Livermore, CA, USA
===================================================================================== */
/// \file gproc.cpp 
/// \author K. Sargsyan  2014 - 
/// \brief Gaussian Process class

#include <math.h>
#include <cfloat>
#include <iostream>

#include "gproc.h"
#include "error_handlers.h"
#include "gen_defs.h"
#include "arraytools.h"
#include "arrayio.h"

#include "tools.h"
#include "lbfgs_routines.h"

#include <assert.h>

/// Function to compote negative log posterior (needed to maximize with respect to roughness parameter)
double neglogPostParam(int ndim, double* m, void* classpointer);

Gproc::Gproc(const string covtype, PCSet *PCModel, Array1D<double>& param)
{
// Set the PC regression
  PCModel_=PCModel;
  npc_=PCModel_->GetNumberPCTerms();  
  printf("gproc : Number of PC terms : %d\n",npc_);


  ndim_=PCModel_->GetNDim();
  param_=param;
  covType_=covtype;

  return;
}


void Gproc::SetupPrior()
{
   // Input the prior parameters
  Vinv_.Resize(npc_,npc_,0.e0); //V^-1
  z_.Resize(npc_,0.e0); //z
  //sig2f_=0.0;
  al_=0.0;
  be_=0.e0;
  //  if (sig2f_!=0.0)
  //   be_=al_*sig2f_;
  sig2n_=1e-6; //!!!



  return;
}




void Gproc::SetupData(Array2D<double>& xdata, Array1D<double>& ydata)
{
    xdata_=xdata;
    ydata_=ydata;
    npt_=xdata.XSize();
    return;
}

void Gproc::BuildGP()
{

  int npts=xdata_.XSize();
  int ndim=xdata_.YSize();
  assert(ndim==ndim_);

    // Fill in the projection matrix H_
    PCModel_->EvalBasisAtCustPts(xdata_,H_);
    transpose(H_,Ht_);

 // Fill in the covariance matrix A_
    computeDataCov_(xdata_,param_,A_);


//  cout << "gproc : Computing the inverse of the covariance matrix at the data points...." << endl;
  Ainv_=INV(A_);
  //cout << "gproc : Done computing the inverse." << endl;


// Matrix manipulations to arrive to the answer(this should be done more efficiently)
  prodAlphaMatVec(Ainv_, ydata_, 1.0, Ainvd_) ;
  prodAlphaMatVec(Ht_,Ainvd_, 1.0, HtAinvd_) ;
  prodAlphaMatMat(Ainv_,H_, 1.0, AinvH_) ;
  prodAlphaMatMat(Ht_,AinvH_, 1.0, HtAinvH_) ;
  Array2D<double> tmp;
  tmp=add(Vinv_,HtAinvH_);
  Vst_=INV(tmp);
  Array1D<double> temp;
  prodAlphaMatVec(Vinv_, z_, 1.0, Vinvz_) ;
  temp=add(Vinvz_,HtAinvd_);
  prodAlphaMatVec(Vst_, temp, 1.0, bhat_) ;
  prodAlphaMatVec(H_, bhat_, 1.0, Hbhat_) ;
  yHbhat_=subtract(ydata_,Hbhat_);
  prodAlphaMatVec(Ainv_, yHbhat_, 1.0, AinvyHbhat_) ;
 
  // Get the sigma_^2_hat
  sig2hat_=2.*be_;
  sig2hat_+=prod_vecTmatvec(z_,Vinv_,z_);
  sig2hat_+=prod_vecTmatvec(ydata_,Ainv_,ydata_);
  Vstinv_=INV(Vst_);
  sig2hat_-=prod_vecTmatvec(bhat_,Vstinv_,bhat_);
  sig2hat_ /= (npts+2.*al_-npc_-2.);

  



  return;
}


void Gproc::EvalGP(Array2D<double>& xgrid, string msc, Array1D<double>& mst)
{
  assert(ndim_==xgrid.YSize());
  int totgrid=xgrid.XSize();
  int npts=xdata_.XSize();

// Get the mean values at the grid points
  PCModel_->EvalPCAtCustPoints(mst,xgrid,bhat_);




  // Fill in appropriate matrices
  Array2D<double> H_atgrid;
  PCModel_->EvalBasisAtCustPts(xgrid,H_atgrid);


if (msc != "m")
  cov_.Resize(totgrid,totgrid,0.e0);

  // Compute the covariance structure of the student-t process
  for(int it=0;it<totgrid;it++){
    Array1D<double> xcurr(ndim_,0.e0);
    for (int id=0;id<ndim_;id++)
      xcurr(id)=xgrid(it,id);

    Array1D<double> tt(npts,0.e0);
    for(int ipts=0;ipts<npts;ipts++){
      Array1D<double> xdata_i(ndim_,0.e0);
      for (int id=0;id<ndim_;id++)
        xdata_i(id)=xdata_(ipts,id);
      tt(ipts)=covariance(xcurr,xdata_i,param_);
    }
    
    double correction=dot(tt,AinvyHbhat_);
    mst(it)+=correction;
  

if (msc != "m"){
    Array1D<double> ttAinvH;
    prodAlphaMatTVec(AinvH_,tt,1.0,ttAinvH);
    
    Array1D<double> ht(npc_,0.e0);
    for(int ipc=0;ipc<npc_;ipc++)
      ht(ipc)=H_atgrid(it,ipc);
    
    
    Array1D<double> httAinvH;
    httAinvH=subtract(ht,ttAinvH);

    
    for(int jt=it;jt<totgrid;jt++){

      //cout << it << " " << jt << endl;
      Array1D<double> xcurra(ndim_,0.e0);
      for (int id=0;id<ndim_;id++)
        xcurra(id)=xgrid(jt,id);
      
      Array1D<double> tta(npts,0.e0);
      for(int ipts=0;ipts<npts;ipts++){
        Array1D<double> xdata_i(ndim_,0.e0);
        for (int id=0;id<ndim_;id++)
          xdata_i(id)=xdata_(ipts,id);
        
        tta(ipts)=covariance(xcurra,xdata_i,param_);
      }
      
      Array1D<double> ttaAinvH;
      prodAlphaMatTVec(AinvH_,tta,1.0,ttaAinvH);

      
      Array1D<double> hta(npc_,0.e0);
      for(int ipc=0;ipc<this->npc_;ipc++)
        hta(ipc)=H_atgrid(jt,ipc);
      
      
      Array1D<double> ht_t_AinvH;
      ht_t_AinvH=subtract(hta,ttaAinvH);

      double correction2=prod_vecTmatvec(httAinvH,Vst_,ht_t_AinvH);
      double correction1=prod_vecTmatvec(tt,Ainv_, tta);

      cov_(it,jt)=(sig2hat_*(covariance(xcurr,xcurra,param_)+sig2n_*(it==jt)-correction1+correction2));
      if (it!=jt)
	cov_(jt,it)=cov_(it,jt);

      if (msc != "msc") break;

    }//jt=it
 }//if m

  }//it

 
  return;
}


void Gproc::getSttPars(Array1D<double>& sttmat)
{
  sttmat.Clear();
  // check that full cov_ already defined(i.e. msc) not just diagonal
  int npts=xdata_.XSize();
  int totgrid=cov_.XSize();


    for(int it=0;it<totgrid;it++)
      for(int jt=it;jt<totgrid;jt++)
	sttmat.PushBack(cov_(it,jt)*(npts+2.*al_-npc_-2.)/(npts+2.*al_-npc_)); 
  
  
  sttmat.PushBack(npts+2.*al_-npc_-2.);



  return;
}

void Gproc::getXYCov(Array2D<double>& xgrid,Array2D<double>& xycov)
{
  // check that full cov_ already defined(i.e. msc) not just diagonal
  int totgrid=cov_.XSize();

xycov.Resize(totgrid*totgrid,2*ndim_+1,0.e0);
  int ii=0;
  for(int it=0;it<totgrid;it++){
    for(int jt=0;jt<totgrid;jt++){
      for (int id=0;id<ndim_;id++)
        xycov(ii,id)=xgrid(it,id);
      for (int id=0;id<ndim_;id++)
        xycov(ii,ndim_+id)=xgrid(jt,id);
      if (it<=jt)
        xycov(ii,2*ndim_)=cov_(it,jt);
      else 
        xycov(ii,2*ndim_)=cov_(jt,it);
      ii++;
    }
  }

return;
}

double Gproc::covariance(Array1D<double>& x1, Array1D<double>& x2,Array1D<double>& param)
{

  //put an 'if' check for covtype_!!
  int n=x1.XSize();
  int nn=x2.XSize();
  if (nn!=n ) {printf("Gproc:covariance() : Error message: covariance: matrix dimensions do not match! \n"); exit(1);}

  double cov=0.0;
  
  Array2D<double> B(nn,nn,0.e0);
  for(int i=0;i<nn;i++)
    B(i,i)=1./param(i);
  
  
  Array1D<double> x12;
  x12=subtract(x1,x2);
  
  Array1D<double> Bx12;
prodAlphaMatVec (B, x12, 1.0, Bx12) ;
  
  cov=exp(-dot(x12,Bx12));

  return cov;
}

void Gproc::computeDataCov_(Array2D<double>& xdata,Array1D<double>& param,Array2D<double>& A)
{
    int npts=xdata.XSize();
    int ndim=xdata.YSize();
    A.Resize(npts,npts,0.e0);
    for(int i=0;i<npts;i++){
        for(int j=0;j<npts;j++){
            Array1D<double> xdatai(ndim,0.e0);
            Array1D<double> xdataj(ndim,0.e0);
            for(int id=0;id<ndim;id++){
                xdatai(id)=xdata(i,id);
                xdataj(id)=xdata(j,id);
            }
            A(i,j)=covariance(xdatai,xdataj,param)+sig2n_*(i==j);
        }
    }
return;
}

void Gproc::findBestCorrParam()
{
    Array1D<double> logparam(ndim_,0.0);
    int n=ndim_;
    int m=5;
    Array1D<int> nbd(n,0);
    Array1D<double> l(n,0.e0);
    Array1D<double> u(n,0.e0);
    
    void* info=this;

     lbfgsDR(n,m,logparam.GetArrayPointer(),nbd.GetArrayPointer(),l.GetArrayPointer(),u.GetArrayPointer(),neglogPostParam,NULL,info) ;
    
    
    for (int i=0;i<ndim_;i++)
        param_(i)=exp(logparam(i));
    
    return;
}

/// Function to compote negative log posterior (needed to maximize with respect to roughness parameter)
double neglogPostParam(int ndim, double* mm, void* classpointer)
{
    
    Gproc* thisClass=(Gproc*) classpointer;

    assert(ndim==thisClass->getNdim());
    Array1D<double> param(ndim,0.e0);
    
    for(int i=0;i<ndim;i++)
        param(i)=exp(mm[i]);

       
    thisClass->setCorrParam(param);
    thisClass->BuildGP();
    
    double lpp=-(thisClass->getNpt()+2.*thisClass->getAl()-thisClass->getNPC())/2.;
    
    lpp*=log(thisClass->getSig2hat());
    
    
    Array2D<double> vst;
    thisClass->getVst(vst);
    
    Array2D<double> acor;
    thisClass->getA(acor);

    //cout << vst(0,1) << " " << vst(1,0) << endl;
    //write_datafile(vst,"vst.dat");
    lpp+=0.5*logdeterm(vst);
    //cout << acor(0,1) << " " << acor(1,0) << endl;
    lpp-=0.5*logdeterm(acor);
    
    return -lpp;
}



