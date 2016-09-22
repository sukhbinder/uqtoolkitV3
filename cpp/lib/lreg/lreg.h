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
/// \file lreg.h 
/// \author K. Sargsyan  2015 -
/// \brief Header file for the linear regression class


#ifndef LREG_H_SEEN
#define LREG_H_SEEN

#include "Array1D.h"
#include "Array2D.h"

/// \class	Lreg
/// \brief	Class for linear parameteric regression
class Lreg {
public:
 
    /// \brief Constructor
    Lreg() {residFlag_=false; diagPFlag_=false; return;};
    /// \brief Destrcutor
    ~Lreg() {};

    
    /// \brief Set multiindex
    virtual void SetMindex(Array2D<int>& mindex){};
    /// \brief Get multiindex
    virtual void GetMindex(Array2D<int>& mindex){};
    /// \brief Set centers (for RBF)
    virtual void SetCenters(Array2D<double>& centers){};
    /// \brief Set widths (for RBF)
    virtual void SetWidths(Array1D<double>& widths){};
    /// \brief Set parameters (for RBF)
    virtual void SetParamsRBF(){};
    /// \brief Evaluate bases
    virtual void EvalBases(Array2D<double>& xx,Array2D<double>& bb){};// dummy
    /// \brief Strip bases
    virtual void StripBases(Array1D<int>& used){};

    /// \brief Initialize
    void InitRegr();
    /// \brief Setup data (1d ydata)
    void SetupData(Array2D<double>& xdata, Array1D<double>& ydata);
    /// \brief Setup data (2d ydata)
    void SetupData(Array2D<double>& xdata, Array2D<double>& ydata);
    /// \brief Set the regression mode
    void SetRegMode(string regmode){regMode_=regmode; return;}
    /// \brief Set weights
    void SetRegWeights(Array1D<double>& weights);
    /// \brief Build BCS regression
    void BCS_BuildRegr(Array1D<int>& selected, double eta);
    /// \brief Build LSQ regression
    void LSQ_BuildRegr();
    /// \brief Evaluate the regression expansion
    void EvalRegr(Array2D<double>& xcheck, Array1D<double>& ycheck,Array1D<double>& yvar,Array2D<double>& ycov);

    /// \brief Get the number of points
    int GetNpt() const {return npt_;}
    /// \brief Get dimensionality
    int GetNdim() const {return ndim_;}
    /// \brief Get the number of bases
    int GetNbas() const {return nbas_;}
    /// \brief Get the variance
    double GetSigma2() const {return sigma2_;}
    /// \brief Get coefficient covariance
    void GetCoefCov(Array2D<double>& coef_cov)  {coef_cov=coef_cov_; return;}
    /// \brief Get coefficients
    void GetCoef(Array1D<double>& coef)  {coef=coef_; return;}
    /// \brief Project
    void Proj(Array1D<double>& array,Array1D<double>& proj_array);
    /// \brief Compute the best values for regulariation parameter vector lambda, for LSQ
    Array1D<double> LSQ_computeBestLambdas();
    /// \brief Compute the best value for regulariation parameter lambda, for LSQ
    double LSQ_computeBestLambda();
    /// \brief Compute validation error
    double computeRVE(Array2D<double>& xval,Array1D<double>& yval,Array1D<double>& yval_regr);
    /// \brief Compote error according to a selected metrics
    Array1D<double> computeErrorMetrics(string method);
    /// \brief Compute the residual vector, if not already computed
    void getResid();
    /// \brief Compute the diagonal of projection matrix, if not already computed
    void getDiagP();


 protected:

    /// \brief xdata array
    Array2D<double> xdata_;
    /// \brief ydata array
    Array1D<double> ydata_;

    /// \brief Number of samples
    int npt_;
    /// \brief Number of bases
    int nbas_;
    /// \brief Dimensionality
    int ndim_;
    /// \brief Variance
    double sigma2_;
    /// \brief Weights
    Array1D<double> weights_;
    /// \brief Residuals
    Array1D<double> resid_;
    /// \brief Flag to indicate whether residual is computed
    bool residFlag_;
    /// \brief Diagonal of projection matrix
    Array1D<double> diagP_;
    /// \brief Flag to indicate whether diagonal of projetion matrix is computed
    bool diagPFlag_;

    //@{
    /// \brief Auxiliary matrix or vector; see UQTk Manual
    Array2D<double> bdata_,A_,A_inv_,coef_cov_;
    Array1D<double> Hty_,coef_,coef_erb_;
    //@}

private:

    /// \brief Compute Leave-one-out error for LSQ
    double LSQ_computeLOO();
    /// \brief COmpute generalized-cross-validation error for LSQ
    double LSQ_computeGCV();
    /// \brief Flag to indicate whether data has been set or not
    bool dataSetFlag_;
    /// \brief Regression mode (m, ms, msc for mean-only, mean+variance, mean+covariance)
    string regMode_;

}; 

/// \class RBFreg
/// \brief Derived class for RBF regression
class RBFreg: public Lreg {
public:
    /// \brief Constructor:
    RBFreg(Array2D<double>& centers, Array1D<double>& widths);
    /// \brief Destructor
    ~RBFreg() {};

    /// \brief Set centers
    void SetCenters(Array2D<double>& centers);
    /// \brief Set widths
    void SetWidths(Array1D<double>& widths);
    
    /// \brief Evaluate the bases
    void EvalBases(Array2D<double>& xx,Array2D<double>& bb);
    /// \brief Strip the bases
    void StripBases(Array1D<int>& used);

private:
    /// \brief RBF centers
    Array2D<double> centers_;
    /// \brief RBF bases' widhts
    Array1D<double> widths_;

};

/// \class PCreg 
/// \brief Derived class for PC regression
class PCreg: public Lreg {
public:
    /// \brief Constructors:
    PCreg(string strpar,int order,int dim);
    PCreg(string strpar,Array2D<int>& mindex);
    /// \brief Destructor
    ~PCreg() {};
    
    /// \brief Evaluate the bases
    void EvalBases(Array2D<double>& xx,Array2D<double>& bb);
    /// \brief Strip the bases
    void StripBases(Array1D<int>& used);
    /// \brief Set multiindex
    void SetMindex(Array2D<int>& mindex);
    /// \brief Get multiindex
    void GetMindex(Array2D<int>& mindex){mindex=mindex_;return;}

private:
    /// \brief Multiindex
    Array2D<int> mindex_;
    /// \brief PC type
    string pctype_;

};

/// \class PLreg
/// \brief Derived class for polynomial regression
class PLreg: public Lreg {
public:
    /// \brief Constructors:
    PLreg(int order, int dim);
    PLreg(Array2D<int>& mindex);
    /// \brief Destructor
    ~PLreg() {};
    
    /// \brief Evaluate the bases
    void EvalBases(Array2D<double>& xx,Array2D<double>& bb);
    /// \brief Strip the bases
    void StripBases(Array1D<int>& used);
    /// \brief Set multiindex
    void SetMindex(Array2D<int>& mindex);
    /// \brief Get multiindex
    void GetMindex(Array2D<int>& mindex){mindex=mindex_;return;}
    

private:
    /// \brief Multiindex
    Array2D<int> mindex_;
    
};

#endif /* LREG_H_SEEN */
