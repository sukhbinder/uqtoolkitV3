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
/// \file post.cpp
/// \author K. Sargsyan  2016 -
/// \brief Posterior computation class

#include <math.h>
#include <cfloat>
#include <assert.h>

#include "func.h"
#include "mrv.h"
#include "post.h"

#include "tools.h"

#include "PCSet.h"
#include "error_handlers.h"
#include "arrayio.h"
#include "arraytools.h"

#define SIG_MAX 10


// Constructor
Post::Post()
{
    this->extraInferredParams_=0;
}


// Set the x- and y-data
void Post::setData(Array2D<double>& xdata,Array2D<double>& ydata)
{
	this->xData_=xdata;
	this->yData_=ydata;

	this->nData_=this->xData_.XSize();
	this->xDim_=this->xData_.YSize();
	assert(this->nData_==this->yData_.XSize());
	this->nEach_=this->yData_.YSize();

	this->yDatam_.Resize(this->nData_,0.e0);
	for(int i=0;i<this->nData_;i++){
        for(int j=0;j<this->nEach_;j++){
            this->yDatam_(i)+=this->yData_(i,j);
        }
        this->yDatam_(i)/=this->nEach_;
    }


	return;
}

// Set the magnitude of data noise
void Post::setDataNoise(Array1D<double>& sigma)
{
	this->inferDataNoise_=false;
	this->dataNoiseLogFlag_=false;

	this->dataNoiseSig_=sigma;

    this->extraInferredParams_+=0;

	return;
}

// Indicate inference of data noise stdev
void Post::inferDataNoise()
{

	this->inferDataNoise_=true;
	this->dataNoiseLogFlag_=false;

   this->extraInferredParams_+=1;

	return;
}

// Indicate inference of log of data noise stdev
void Post::inferLogDataNoise()
{
	this->inferDataNoise_=true;
	this->dataNoiseLogFlag_=true;

	this->extraInferredParams_+=1;
	return;
}

// Get data noise, whether inferred or fixed
Array1D<double> Post::dataSigma(double m_last)
{
	Array1D<double> sig;
	if (inferDataNoise_){
		if (dataNoiseLogFlag_){
			sig.Resize(this->nData_,exp(m_last));
		}
		else {
			sig.Resize(this->nData_,m_last);
		}
	}
	else
		sig=this->dataNoiseSig_;

	

	return sig;
}

// Set a pointer to the forward model f(p,x)
void Post::setModel(Array2D<double> (*forwardFcn)(Array2D<double>&, Array2D<double>&, void*), void* funcInfo)
{
	this->forwardFcn_=forwardFcn;
    this->funcinfo_=funcInfo;
	return;
}

// Set model input parameters' randomization scheme
void Post::setModelRVinput(int pdim,int order,Array1D<int>& rndInd,string pdfType,string rvpcType)
{
	this->pDim_=pdim;
	this->rndInd_=rndInd;
	this->pdfType_=pdfType;
    this->rvpcType_=rvpcType;

	this->Mrv_ = new Mrv(this->pDim_,this->pdfType_, this->rndInd_,order,this->rvpcType_, this->funcinfo_);
	this->chDim_=this->Mrv_->Parametrize()+this->extraInferredParams_;
	this->Mrv_->getBounds(this->lower_,this->upper_);
	if (inferDataNoise_ and dataNoiseLogFlag_){
		this->lower_.PushBack(-SIG_MAX);
		this->upper_.PushBack(SIG_MAX);
	}
	if (inferDataNoise_ and ~dataNoiseLogFlag_){
		this->lower_.PushBack(0.e0);
		this->upper_.PushBack(SIG_MAX);
	}


  	return;
	
}

// Get the dimensionailty of the posterior function
int Post::getChainDim()
{
	return chDim_;
}

// Set the prior type and its parameters
void Post::setPrior(string priorType, double priora, double priorb)
{
	this->priorType_=priorType;
	this->priora_=priora;
	this->priorb_=priorb;

	return;
}

// Evaluate log-prior
double Post::evalLogPrior(Array1D<double>& m)
{
    double pi=4.*atan(1.);

	double logPrior=0.0;
	if (this->priorType_=="uniform"){
   	   
        Array1D<int> pctermid;
        this->Mrv_->getPCTermId(pctermid);
    
        for (int ic=0;ic<pctermid.Length();ic++){
            if (pctermid(ic)==0)
                if (m(ic)<this->priora_ or m(ic)>this->priorb_)
                    return -1.e80;
        }


		logPrior=0.0;
	}

    else if (this->priorType_=="uniform_LUpci"){
        
        Array1D<int> pctermid;
        this->Mrv_->getPCTermId(pctermid);
        
        for (int ic=0;ic<pctermid.Length();ic++){
            if (pctermid(ic)==0){
                if (ic<pctermid.Length()-1 and pctermid(ic+1)!=0){
                    if (m(ic)-m(ic+1)<this->priora_ or m(ic)+m(ic+1)>this->priorb_)
                        return -1.e80;
                }
                else{
                    if (m(ic)<this->priora_ or m(ic)>this->priorb_)
                        return -1.e80;
                }
            }
        }



        logPrior=0.0;
    }

	else if (this->priorType_=="normal"){

   	    Array1D<int> pctermid;
        this->Mrv_->getPCTermId(pctermid);
    
        for (int ic=0;ic<pctermid.Length();ic++){
	        double ps=this->priorb_;
	        double mism=m(ic)-this->priora_;
	        logPrior-=( 0.5*mism*mism/(ps*ps) + 0.5*log(2.*pi) + log(ps) );
		}            
    }

    else if (this->priorType_=="inverse"){

        Array1D<int> pctermid;
        this->Mrv_->getPCTermId(pctermid);
    
        for (int ic=0;ic<pctermid.Length();ic++){
            if (pctermid(ic)==0)
                if (m(ic)<this->priora_ or m(ic)>this->priorb_)
                    return -1.e80;
            if (pctermid(ic)!=0)
                logPrior-=log(fabs(m(ic)));
        }
    }
	
    else if (this->priorType_=="wishart"){

        double nu = this->pDim_ + this->priora_;
        double theta = this->priorb_;

        

        bool covFlag = true;
        Array1D<double> parMean,parVar;
        Array2D<double> parCov;
        this->momParam(m, parMean, parVar, covFlag, parCov);

        //Array2D<double> paramPCcf=getParamPCcf(m);//npc x pdim
        //this->Mrv_->computeMoments(paramPCcf, fcnMean,fcnVar,covFlag, fcnCov);    //funccf is npc x nx


        logPrior = 0.5 * this->pDim_ * nu + 0.5 * (nu - pDim_ - 1.0) * logdeterm(parCov) - theta * trace(parCov);

        //double a = 0.5*(nu-this->pDim_+1.0);
        //double b = theta;
        //double logprior2=a*log(b) + (a-1.)*log(m(1)) - b*m(1) - lgamma(a) 
    }

    else if (this->priorType_=="jeffreys"){


        

        bool covFlag = true;
        Array1D<double> parMean,parVar;
        Array2D<double> parCov;
        this->momParam(m, parMean, parVar, covFlag, parCov);


        logPrior = - 0.5 * (this->pDim_ +1.) * logdeterm(parCov);

    }

    return logPrior;
}

// Extract parameter PC coefficients from a posterior input
Array2D<double> Post::getParamPCcf(Array1D<double>& m)
{
    Array1D<double> modelRVparams;
    for (int i=0;i<m.Length()-this->extraInferredParams_;i++)
        modelRVparams.PushBack(m(i));

    Array2D<double> paramPCcf=this->Mrv_->getMultiPCcf(modelRVparams);

    return paramPCcf;
}

// Sample model parameters given posterior input
Array2D<double> Post::samParam(Array1D<double>& m, int ns)
{
    Array2D<double> paramPCcf=this->getParamPCcf(m);

	Array2D<double> paramSamples=this->Mrv_->mcParam(paramPCcf, ns);

	return paramSamples;
}

// Get moments of parameters given posterior input
void Post::momParam(Array1D<double>& m, Array1D<double>& parMean, Array1D<double>& parVar, bool covFlag, Array2D<double>& parCov)
{
	   
    Array2D<double> paramPCcf=this->getParamPCcf(m);

//	Array2D<double> paramSamples=this->Mrv_->samParam(paramPCcf, ns);
    this->Mrv_->computeMoments(paramPCcf, parMean,parVar,covFlag, parCov);    

	return;
}

// Sample forward function at a given grid for given posterior input
Array2D<double> Post::samForwardFcn(Array1D<double>& m, Array2D<double>& xgrid, int ns)
{
    
    Array2D<double> paramPCcf=this->getParamPCcf(m);

    Array2D<double> funcSam=this->Mrv_->propMC(this->forwardFcn_, paramPCcf, xgrid,ns);


	return funcSam;
}

// Get moments of forward function at a given grid for given posterior input
void Post::momForwardFcn(Array1D<double>& m, Array2D<double>& xgrid, Array1D<double>& fcnMean, Array1D<double>& fcnVar, bool covFlag, Array2D<double>& fcnCov)
{
   
    Array2D<double> paramPCcf=this->getParamPCcf(m);

	Array2D<double> funcCf=this->Mrv_->propNISP(this->forwardFcn_, paramPCcf, xgrid);
    
    this->Mrv_->computeMoments(funcCf, fcnMean,fcnVar,covFlag, fcnCov);    
	return;
}
/****************************************************************************************/
/****************************************************************************************/
/****************************************************************************************/

// Evaluate full log-likelihood
double Lik_Full::evalLogLik(Array1D<double>& m)
{

    for (int ic=0;ic<m.Length();ic++){
    	if (m(ic)<this->lower_(ic) or m(ic)>this->upper_(ic)){
    		return -1.e+80;
    	}
    }

    double pi=4.*atan(1.);


	Array2D<double> ydatat;
    transpose(this->yData_,ydatat);

    Array1D<double> dataSig=this->dataSigma(m(m.Length()-1));

    Array2D<double> funcSam=samForwardFcn(m, this->xData_, this->nsam_);
    
    Array2D<double> dataNoiseSam(this->nsam_,this->nData_);
    generate_normal(dataNoiseSam, time(NULL));
    Array2D<double> tmp;
    Array2D<double> diagsig=diag(dataSig);
    prodAlphaMatMat(dataNoiseSam,diagsig,1.0,tmp);
    addinplace(funcSam,tmp);

    Array1D<double> weight(this->nsam_,1.e0);
    Array1D<double> dens(this->nEach_,0.e0);
    Array1D<double> bdw(this->nData_,this->bdw_);
    if (this->bdw_<=0)
        get_opt_KDEbdwth(funcSam,bdw);
    //cout << "BD " << bdw(0) << " " << bdw(1) << endl;
    getPdf_figtree(funcSam,ydatat,bdw,dens, weight);
    
    
    double logLik=0.;
    for (int ie=0;ie<this->nEach_;ie++){
        //cout << dens(ie) << endl;
        //ldens2(ie)=-(data(ie,0)-mu)*(data(ie,0)-mu)/(2.*std*std)-log(std*sqrt(2*pi)) ;
        if (dens(ie)==0)
            return -1.e80;
        else
            logLik +=log(dens(ie));
    }


	return logLik;
}

/****************************************************************************************/
/****************************************************************************************/
/****************************************************************************************/

// Evaluate marginal log-likelihood
double Lik_Marg::evalLogLik(Array1D<double>& m)
{
    for (int ic=0;ic<m.Length();ic++){
    	if (m(ic)<this->lower_(ic) or m(ic)>this->upper_(ic)){
    		return -1.e+80;
    	}
    }

    double pi=4.*atan(1.);

    Array1D<double> dataSig=this->dataSigma(m(m.Length()-1));
    Array2D<double> funcSam=samForwardFcn(m, this->xData_, this->nsam_);

    Array2D<double> ydatat;
    transpose(this->yData_,ydatat);


    Array2D<double> dataNoiseSam(this->nsam_,this->nData_);

    generate_normal(dataNoiseSam, time(NULL));
    Array2D<double> tmp;
    Array2D<double> diagsig=diag(dataSig);
    prodAlphaMatMat(dataNoiseSam,diagsig,1.0,tmp);
    addinplace(funcSam,tmp);

    double logLik=0.;

    for (int ix=0;ix<this->nData_;ix++){
    	Array2D<double> funcSam_ix(this->nsam_,1);
    	Array2D<double> ydatat_ix(this->nEach_,1);
    	for(int is=0;is<this->nsam_;is++)
            funcSam_ix(is,0)=funcSam(is,ix);
        for(int ie=0;ie<this->nEach_;ie++)
            ydatat_ix(ie,0)=ydatat(ie,ix);
	    Array1D<double> weight(this->nsam_,1.e0);
	    Array1D<double> dens(this->nEach_,0.e0);
	    Array1D<double> bdw(1,this->bdw_);
        if (this->bdw_<=0)
    	    get_opt_KDEbdwth(funcSam_ix,bdw);
	    getPdf_figtree(funcSam_ix,ydatat_ix,bdw,dens, weight);
	 
        for(int ie=0;ie<this->nEach_;ie++){
			if (dens(ie)==0)
            	return -1.e80;
        	else
            	logLik +=log(dens(ie));        	
        }


    }

    
	return logLik;
}

/****************************************************************************************/
/****************************************************************************************/
/****************************************************************************************/

// Evaluate mvn log-likelihood
double Lik_MVN::evalLogLik(Array1D<double>& m)
{
    for (int ic=0;ic<m.Length();ic++){
    	if (m(ic)<this->lower_(ic) or m(ic)>this->upper_(ic)){
    		return -1.e+80;
    	}
    }

    double pi=4.*atan(1.);

    Array1D<double> dataSig=this->dataSigma(m(m.Length()-1));
    
 	Array1D<double> fcnMean,fcnVar;
    Array2D<double> fcnCov;
 	momForwardFcn(m, this->xData_, fcnMean, fcnVar, true, fcnCov);

    
    Array2D<double> fcnCovN=fcnCov;

    for (int i=0;i<this->nData_;i++)
    	fcnCovN(i,i)+=(pow(dataSig(i),2.)+pow(this->nugget_,2.));

    double logLik=evalLogMVN(this->yDatam_,fcnMean,fcnCovN);


	return logLik;
}

/****************************************************************************************/
/****************************************************************************************/
/****************************************************************************************/

// Evaluate gaussian-marginal log-likelihood
double Lik_GausMarg::evalLogLik(Array1D<double>& m)
{
    for (int ic=0;ic<m.Length();ic++){
    	if (m(ic)<this->lower_(ic) or m(ic)>this->upper_(ic)){
    		return -1.e+80;
    	}
    }

    double pi=4.*atan(1.);

    Array1D<double> dataSig=this->dataSigma(m(m.Length()-1));
    
    Array1D<double> fcnMean,fcnVar;
    Array2D<double> fcnCov;
 	momForwardFcn(m, this->xData_, fcnMean, fcnVar, false, fcnCov);

    Array1D<double> dataVar=dotmult(dataSig,dataSig);

    double logLik=0.;
    for (int ix=0;ix<this->nData_;ix++){
        double err=fabs(this->yDatam_(ix)-fcnMean(ix));
        logLik-= ( 0.5*err*err/(fcnVar(ix)+dataVar(ix)) + 0.5*log(2.*pi) + 0.5*log(fcnVar(ix)+dataVar(ix)) );
    }

	return logLik;
}

/****************************************************************************************/
/****************************************************************************************/
/****************************************************************************************/

// Evaluate ABC log-likelihood
double Lik_ABC::evalLogLik(Array1D<double>& m)
{
    for (int ic=0;ic<m.Length();ic++){
    	if (m(ic)<this->lower_(ic) or m(ic)>this->upper_(ic)){
    		return -1.e+80;
    	}
    }

    double pi=4.*atan(1.);

    Array1D<double> dataSig=this->dataSigma(m(m.Length()-1));
    
    Array1D<double> fcnMean,fcnVar;
    Array2D<double> fcnCov;
 	momForwardFcn(m, this->xData_, fcnMean, fcnVar, false, fcnCov);


    Array1D<double> dataVar=dotmult(dataSig,dataSig);

   
    ////////
    double alpha=1.;
    double norm=0.0;
    double logLik=0.;
    for (int ix=0;ix<this->nData_;ix++){
        double err=fabs(this->yDatam_(ix)-fcnMean(ix));
        norm+=pow(err,2.);
        norm+=pow(alpha*err-sqrt(fcnVar(ix)+dataVar(ix)),2.);
    }
	logLik=-(0.5/(this->abceps_*this->abceps_))*(norm)-0.5*log(2.*pi)-log(this->abceps_);    

	return logLik;
}

/****************************************************************************************/
/****************************************************************************************/
/****************************************************************************************/

// Evaluate ABC-mean log-likelihood
double Lik_ABCm::evalLogLik(Array1D<double>& m)
{
    for (int ic=0;ic<m.Length();ic++){
    	if (m(ic)<this->lower_(ic) or m(ic)>this->upper_(ic)){
    		return -1.e+80;
    	}
    }

    double pi=4.*atan(1.);

    //Array1D<double> dataSig=this->dataSigma(m(m.Length()-1));
    
    Array1D<double> fcnMean,fcnVar;
    Array2D<double> fcnCov;
 	momForwardFcn(m, this->xData_, fcnMean, fcnVar, false, fcnCov);

    double norm=0.0;
    double logLik=0.;
    for (int ix=0;ix<this->nData_;ix++){
        double err=fabs(this->yDatam_(ix)-fcnMean(ix));
        norm+=pow(err,2.);
    }
	logLik=-(0.5/(this->abceps_*this->abceps_))*(norm)-0.5*log(2.*pi)-log(this->abceps_);    

	return logLik;
}

/****************************************************************************************/
/****************************************************************************************/
/****************************************************************************************/

// Evaluate Kennedy-O'Hagan log-likelihood
double Lik_Koh::evalLogLik(Array1D<double>& m)
{
    for (int ic=0;ic<m.Length();ic++){
        if (m(ic)<this->lower_(ic) or m(ic)>this->upper_(ic)){
            return -1.e+80;
        }
    }

    double pi=4.*atan(1.);

    Array1D<double> dataSig=this->dataSigma(m(m.Length()-1));
    double modelSig=m(m.Length()-2);

    Array1D<double> fcnMean,fcnVar;
    Array2D<double> fcnCov;
    momForwardFcn(m, this->xData_, fcnMean, fcnVar, false, fcnCov);

    
    Array2D<double> fcnCovKoh(this->nData_,this->nData_);

    for (int i=0;i<this->nData_;i++){
        fcnCovKoh(i,i)=pow(modelSig,2.0);
        for (int j=0;j<this->nData_;j++){
            double norm=0.0;
            for (int k=0;k<this->xDim_;k++) 
                norm+=pow(xData_(i,k)-xData_(j,k),2.0);
            norm=sqrt(norm);
            fcnCovKoh(i,j)=pow(modelSig,2.0)*exp(-0.5*pow(norm/this->corLength_,2.0));
            fcnCovKoh(j,i)=fcnCovKoh(i,j);
        }
    }


    for (int i=0;i<this->nData_;i++)
        fcnCovKoh(i,i)+=(pow(dataSig(i),2.));

    double logLik=evalLogMVN(this->yDatam_,fcnMean,fcnCovKoh);


    return logLik;
}

/****************************************************************************************/
/****************************************************************************************/
/****************************************************************************************/

// Evaluate classical log-likelihood
double Lik_Classical::evalLogLik(Array1D<double>& m)
{
    for (int ic=0;ic<m.Length();ic++){
    	if (m(ic)<this->lower_(ic) or m(ic)>this->upper_(ic)){
    		return -1.e+80;
    	}
    }

    double pi=4.*atan(1.);
    Array1D<double> dataSig=this->dataSigma(m(m.Length()-1));
    
    Array1D<double> fcnMean,fcnVar;
    Array2D<double> fcnCov;
 	momForwardFcn(m, this->xData_, fcnMean, fcnVar, false, fcnCov);
 	//or     fcnMean=samForwardFcn(m, this->xData_, 1);


    double logLik=0.;
    for (int ix=0;ix<this->nData_;ix++){
        for (int ie=0;ie<this->nEach_;ie++){
            double err=fabs(this->yData_(ix,ie)-fcnMean(ix));
            logLik-= ( 0.5*err*err/(dataSig(ix)*dataSig(ix)) + 0.5*log(2.*pi) + log(dataSig(ix)) );
        }
    }


	return logLik;
}

/****************************************************************************************/
/****************************************************************************************/
/****************************************************************************************/
