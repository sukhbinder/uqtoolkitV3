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
/// \file lreg.cpp 
/// \author K. Sargsyan  2015 -
/// \brief Linear regression class


#include <math.h>
#include <cfloat>
#include <iostream>

#include "lreg.h"
#include "gen_defs.h"
#include "error_handlers.h"

#include "arraytools.h"
#include "arrayio.h"
#include "PCSet.h"

#include "bcs.h"

#include "ftndefs.h"
#include "depblas.h"
#include "deplapack.h"


#include "tools.h"
#include "lbfgs_routines.h"

#include <assert.h>
//#define DEBUG

double loo(int ndim, double* m, void* classpointer);



RBFreg::RBFreg(Array2D<double>& centers, Array1D<double>& widths)
{
    centers_=centers;
    widths_=widths;
    ndim_=centers.YSize();
    nbas_=centers.XSize();
    assert(ndim_==widths.XSize());
    
    return;
}

PCreg::PCreg(string strpar,int order, int dim)
{
    Array2D<int> mindex;
    computeMultiIndex(dim,order,mindex);

    this->SetMindex(mindex);
    pctype_=strpar;
    
    nbas_=this->mindex_.XSize();
    ndim_=this->mindex_.YSize();

    return;
}

PCreg::PCreg(string strpar,Array2D<int>& mindex)
{
    this->SetMindex(mindex);
    pctype_=strpar;

    nbas_=this->mindex_.XSize();
    ndim_=this->mindex_.YSize();

    
    return;
}

PLreg::PLreg(int order, int dim)
{
    Array2D<int> mindex;
    computeMultiIndex(dim,order,mindex);
    
    this->SetMindex(mindex);
    
    nbas_=this->mindex_.XSize();
    ndim_=this->mindex_.YSize();

    return;
}

PLreg::PLreg(Array2D<int>& mindex)
{
    this->SetMindex(mindex);

    nbas_=this->mindex_.XSize();
    ndim_=this->mindex_.YSize();

    return;
}

/////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////

void Lreg::InitRegr()
{
    weights_.Resize(this->nbas_,0.e0);
    dataSetFlag_=false;
    regMode_="m";
}

void Lreg::SetRegWeights(Array1D<double>& weights)
{
    weights_=weights;
    assert(this->nbas_==weights_.XSize());

  return;
}


void PCreg::SetMindex(Array2D<int>& mindex)
{
    mindex_=mindex;
    return;
}


void PLreg::SetMindex(Array2D<int>& mindex)
{
    mindex_=mindex;
    return;
}

void RBFreg::SetCenters(Array2D<double>& centers)
{
    centers_=centers;
    assert(ndim_==centers.YSize());
    assert(nbas_==centers.XSize());
    return;
}

void RBFreg::SetWidths(Array1D<double>& widths)
{
    widths_=widths;
    assert(ndim_==widths.XSize());
    
    
    return;
}


void Lreg::SetupData(Array2D<double>& xdata, Array1D<double>& ydata)
{
    xdata_=xdata;
    ydata_=ydata;
    npt_=xdata.XSize();
    assert(npt_=ydata.XSize());
    assert(ndim_==xdata.YSize());

    dataSetFlag_=true;

    return;
}

void Lreg::SetupData(Array2D<double>& xdata, Array2D<double>& ydata)
{
    
    int nx=xdata.XSize();
    assert(ndim_==xdata.YSize());
    assert(nx==ydata.XSize());
    int numeach=ydata.YSize();
    
    
    npt_=nx*numeach;
    
    xdata_.Resize(npt_,ndim_);
    ydata_.Resize(npt_);
    
    
    int j=0;
    for(int i=0; i<nx; i++){
        for(int ie=0;ie<numeach;ie++){
            for(int id=0;id<ndim_;id++){
                xdata_(j,id)=xdata(i,id);
            }
            ydata_(j)=ydata(i,ie);
            j++; 
        }
    }
   
    dataSetFlag_=true;

    return;
}

void PCreg::EvalBases(Array2D<double>& xx,Array2D<double>& bb)
{
    assert(xx.YSize()==ndim_);
    
    
        PCSet currPCModel("NISPnoq",mindex_,pctype_,0.,1.);
        
        // int npc=currPCModel.GetNumberPCTerms();
        currPCModel.EvalBasisAtCustPts(xx,bb);
        
    
    return;

}


void PLreg::EvalBases(Array2D<double>& xx,Array2D<double>& bb)
{
    assert(xx.YSize()==ndim_);
    int nx=xx.XSize();
        bb.Resize(nx,nbas_,0.e0);
        
        for(int is=0;is<nx;is++){
            for(int ipc=0;ipc<nbas_;ipc++){
                bb(is,ipc)=1;
                for(int id=0;id<ndim_;id++){
                    bb(is,ipc)*=pow(xx(is,id),mindex_(ipc,id));
                }
            }
        }
 
    
    return;
    
}



void RBFreg::EvalBases(Array2D<double>& xx,Array2D<double>& bb)
{
    assert(xx.YSize()==ndim_);
    int nx=xx.XSize();
    
            
        bb.Resize(nx,nbas_,0.e0);
        for(int is=0;is<nx;is++){
            for(int ib=0;ib<nbas_;ib++){
                double norm2=0.0;
                for(int id=0;id<ndim_;id++){
                    double diff=(xx(is,id)-centers_(ib,id))/widths_(id);
                    norm2+=diff*diff;
                }
                bb(is,ib)=exp(-norm2/2.);
            }
            
            
        }
        
    
    
    return;
    
}

void Lreg::BCS_BuildRegr(Array1D<int>& used, double eta)
{
    assert(dataSetFlag_);
    int ntot=ydata_.XSize();
    // Work variables
    Array1D<double> lambda_init,weights, errbars, basis, alpha ;
    Array2D<int> newmindex;
    Array2D<double> Sig;
    
    int    adaptive = 0      ;
    int    optimal  = 1      ;
    double scale    = 0.1    ;
    int    verbose  = 0      ;
    sigma2_= (double) (ntot/(ntot-1.))*pow(get_std(ydata_),2)/1.0e6;
    double lambda ;
    /* lambda = 0; % Gaussian priors (BCS) */
    /* lambda = <a_positive_value> -- Laplace priors with fixed lambda */
    
    //for (int i=0;i<10;i++)
    //  lambda_init(i)=1.e+5;
    
    
    this->EvalBases(xdata_,bdata_);

    
    // Run the BCS
    lambda_init=weights_;
    WBCS(bdata_,ydata_,sigma2_,eta,lambda_init,adaptive, optimal,scale,
                 verbose,coef_,used,coef_erb_,basis,alpha,lambda,coef_cov_);

    this->StripBases(used);
	
    

    
    return;
}

void PCreg::StripBases(Array1D<int>& used)
{
    int nused=used.Length();
    Array2D<int> mindex_new(nused,ndim_,0);
	for (int i=0;i<nused;i++)
        for (int j=0;j<ndim_;j++)
            mindex_new(i,j)=mindex_(used(i),j);
	
    SetMindex(mindex_new);
    this->nbas_=nused;
    return;
}
void PLreg::StripBases(Array1D<int>& used)
{
    int nused=used.Length();
    Array2D<int> mindex_new(nused,ndim_,0);
	for (int i=0;i<nused;i++)
        for (int j=0;j<ndim_;j++)
            mindex_new(i,j)=mindex_(used(i),j);
	
    SetMindex(mindex_new);
    this->nbas_=nused;
    return;
}
void RBFreg::StripBases(Array1D<int>& used)
{
    int nused=used.Length();
    Array2D<double> centers_new(nused,ndim_,0.);
    Array1D<double> widths_new(nused,0.);

	for (int i=0;i<nused;i++){
        for (int j=0;j<ndim_;j++)
            centers_new(i,j)=centers_(used(i),j);
        widths_new(i)=widths_(used(i));
    }
    SetCenters(centers_new);
    SetWidths(widths_new);
    this->nbas_=nused;

    return;
}

void Lreg::LSQ_BuildRegr()
{
   assert(dataSetFlag_);

    this->EvalBases(xdata_,bdata_);
    A_=MatTMat(bdata_) ;

    for (int i=0;i<nbas_;i++)
        A_(i,i)+=weights_(i);

    this->A_inv_ = INV(this->A_);
    //write_datafile(this->A_,"a");
    //write_datafile(this->A_inv_,"ai");


    prodAlphaMatTVec(bdata_, ydata_, 1.0, Hty_) ;
    prodAlphaMatVec(A_inv_, Hty_, 1.0, coef_) ;
    
 

    if (this->regMode_=="ms" or this->regMode_=="msc"){
        double s1=0.0,s2=0.0;
    
        for(int it=0;it<npt_;it++)
          s1 += ( ydata_(it)*ydata_(it) );
        for(int ip=0;ip<nbas_;ip++)
          s2 += ( Hty_(ip)*coef_(ip) );
        double betta_add=(s1-s2)/2.;



        double alfa=0.0;
        double betta=0.0;
        // alpha>>1, beta>>1, beta/alpha=sigma for fixed sigma
        // alpha=beta=0 for Jeffreys prior 1/sigma^2

        sigma2_=(betta+betta_add)/(alfa+0.5*(npt_-nbas_)-1.);
        if (sigma2_<0.0){
            cout << "Negative (should be very small) data noise, set to zero. Sigma2=" << sigma2_ << endl;
            sigma2_=0.0;
        }
        coef_cov_.Resize(nbas_,nbas_,0.e0);
        for(int ib=0;ib<nbas_;ib++)
          for(int jb=0;jb<nbas_;jb++)
            coef_cov_(ib,jb)=sigma2_*A_inv_(ib,jb);//-1 due to eta/eta-2 factor in cov

        coef_erb_.Resize(nbas_,0.e0);
        for ( int i = 0; i<this->nbas_; i++) coef_erb_(i) = sqrt(coef_cov_(i,i));

    }

  return;
}


void Lreg::EvalRegr(Array2D<double>& xcheck, Array1D<double>& ycheck,Array1D<double>& yvar,Array2D<double>& ycov)
{
    assert(ndim_==xcheck.YSize());
    int ncheck=xcheck.XSize();
    Array2D<double> bcheck;

    this->EvalBases(xcheck,bcheck);
    prodAlphaMatVec(bcheck, coef_, 1.0, ycheck) ;


    if (this->regMode_=="ms" or this->regMode_=="msc"){
        if (sigma2_==0.0){
            yvar.Resize(ncheck,0.0);
            ycov.Resize(ncheck,ncheck,0.0);
            return;
        }

        Array2D<double> L=coef_cov_;

        // Cholesky factorization of the covariance 
        int nd=L.XSize();
        assert(nd==this->nbas_);
        int chol_info=0;
        char lu='L';
        FTN_NAME(dpotrf)(&lu,&nd, L.GetArrayPointer(),&nd,&chol_info);
        
        // Catch the error in Cholesky factorization
        if (chol_info != 0 ){
            printf("Lreg::EvalRegr():Error in Cholesky factorization, info=%d\n", chol_info);
            exit(1);
        }
    
        Array2D<double> A;
        prodAlphaMatMat(bcheck,L,1.0,A);

        yvar.Resize(ncheck);
        for (int i=0;i<ncheck;i++){
            double sum=0.0;
            for (int k=0;k<nd;k++)
                sum+=A(i,k)*A(i,k);
            yvar(i)=sum;


            if (this->regMode_=="msc"){

                ycov.Resize(ncheck,ncheck);
                ycov(i,i)=yvar(i);
                for (int j=0;j<i;j++){
                 double sum=0.0;
                    for (int k=0;k<ncheck;k++)
                        sum+=A(i,k)*A(j,k);
                    ycov(i,j)=sum;
                    ycov(j,i)=sum;
                }
            }
        }
    }
 
  return;
}

void Lreg::Proj(Array1D<double>& array,Array1D<double>& proj_array)
{
    assert(array.XSize()==npt_);
    Array1D<double> tmp,tmp2;
    prodAlphaMatTVec(bdata_,array,1.0,tmp);
    prodAlphaMatVec(A_inv_,tmp,1.0,tmp2);
    prodAlphaMatVec(bdata_,tmp2,1.0,proj_array);

    for (int i=0;i<proj_array.XSize();i++){
        proj_array(i)=array(i)-proj_array(i);
    }
    
    return;
}

void Lreg::getResid()
{

    if (!residFlag_){
       Array1D<double> tmp;
        prodAlphaMatVec(bdata_,coef_,1.0,tmp);
        resid_=subtract(ydata_,tmp);  
        residFlag_=true;      
    }

    return;
}

void Lreg::getDiagP()
{
       if (!diagPFlag_){
    diagP_.Resize(npt_,1.e0);
 for (int i=0;i<npt_;i++){
        for (int j=0;j<nbas_;j++){
            for (int k=0;k<j;k++)
                diagP_(i)-=2.*bdata_(i,j)*A_inv_(j,k)*bdata_(i,k);
            diagP_(i)-=bdata_(i,j)*A_inv_(j,j)*bdata_(i,j);
        }
    }
    diagPFlag_=true;
}

    return;
}
Array1D<double> Lreg::computeErrorMetrics(string method)
{
    Array1D<double> err(2,-999.);
    if (method=="lsq"){
        err(0)=this->LSQ_computeLOO();
        err(1)=this->LSQ_computeGCV();
    }
    else{
        printf("Computation of errors not implemented for %s method\n",method.c_str());
    }

    return err;
}

double Lreg::LSQ_computeLOO()
{
    this->getResid();
   
    this->getDiagP();

    Array1D<double>   resid_scaled=dotdivide(resid_,diagP_);
    
    return norm(resid_scaled)/sqrt(npt_);

}

double Lreg::LSQ_computeGCV()
{

           this->getResid();

   
 this->getDiagP();

double sum=0.0;
for (int i=0;i<npt_;i++)
    sum+=diagP_(i);

return  norm(resid_)*sqrt(npt_)/sum;

//     Array1D<double> tmp1;

//     this->Proj(ydata_,tmp1);
//     double numer=npt_*dot(tmp1,tmp1);
//     double denom=0.0;

//     for (int i=0;i<npt_;i++){
//         cout << i << "/" << npt_ << endl;

//         Array1D<double> hi,tmp;
//         getRow(bdata_,i,hi);
// time_t start,end;
// start=time(NULL);
// cout << "GCV    : ";

//         prodAlphaMatVec(A_inv_,hi,1.0,tmp);
// end=time(NULL);
// cout << difftime(end,start) << endl;
// start=end;
//         denom += (1.-dot(hi,tmp));
//     }
//    return sqrt(numer)/denom;

}

double Lreg::computeRVE(Array2D<double>& xval,Array1D<double>& yval,Array1D<double>& yval_regr)
{
    int nval=xval.XSize();
    assert(ndim_==xval.YSize());
    assert(nval==yval.XSize());
    
    double sum=0.0;
    Array1D<double> dummy_var;     Array2D<double> dummy_cov;
    this->SetRegMode("m");
    this->EvalRegr(xval,yval_regr, dummy_var,dummy_cov);
    for (int i=0;i<nval;i++){
        double err=yval(i)-yval_regr(i);
        sum += (err*err);
    }
    sum /= nval;
    sum=sqrt(sum);
    
    return sum;
}

double Lreg::LSQ_computeBestLambda()
{
    
    double lambda=0.1;
    int n=1;//ndim_;
    int m=5;
    Array1D<int> nbd(n,1);
    Array1D<double> l(n,0.e0);
    Array1D<double> u(n,0.e0);
    
    void* info=this;
    
    lbfgsDR(n,m,&lambda,nbd.GetArrayPointer(),l.GetArrayPointer(),u.GetArrayPointer(),loo,NULL,info) ;
    
        
    return lambda;
}

Array1D<double> Lreg::LSQ_computeBestLambdas()
{
    
    Array1D<double> lambda(nbas_,0.1);
    int n=nbas_; //1;//ndim_;
    int m=5;
    Array1D<int> nbd(n,1);
    Array1D<double> l(n,0.e0);
    Array1D<double> u(n,0.e0);
    
    void* info=this;
    
    lbfgsDR(n,m,lambda.GetArrayPointer(),nbd.GetArrayPointer(),l.GetArrayPointer(),u.GetArrayPointer(),loo,NULL,info) ;
    
        
    return lambda;
}

double loo(int ndim, double* mm, void* classpointer)
{
    
    Lreg* thisClass=(Lreg*) classpointer;
    
    Array1D<double> lam(thisClass->GetNbas());
    if (ndim==1)
        lam.Resize(thisClass->GetNbas(),mm[0]);
    else{
        assert(ndim==thisClass->GetNbas());
        for (int i=0;i<ndim;i++)
            lam(i)=mm[i];
    }



    thisClass->SetRegWeights(lam);
    thisClass->LSQ_BuildRegr();

    Array1D<double> errors=thisClass->computeErrorMetrics("lsq");
    double err_loo=errors(0);
    return err_loo;
    
}
