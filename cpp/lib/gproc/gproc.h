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
/// \file gproc.h 
/// \author K. Sargsyan  2014 - 
/// \brief Header file for Gaussian Process class

#ifndef GPROC_H_SEEN
#define GPROC_H_SEEN

#include "Array1D.h"
#include "Array2D.h"
#include "PCSet.h"

/// \class	Gproc
/// \brief	Class for Gaussian processes
class Gproc {
public:
 
  /// \brief Constructor: initialize with covariance type, trend function basis
  ///  and roughness parameter vector
  Gproc(const string covtype, PCSet *PCModel, Array1D<double>& param);
  /// \brief Destructor: cleans up all memory and destroys object
  ~Gproc() {};

  /// \brief Setup the prior
  void SetupPrior();
  /// \brief Setup the data
  void SetupData(Array2D<double>& xdata, Array1D<double>& ydata);
  /// \brief Set the roughness parameter vector
  void setCorrParam(Array1D<double> param){param_=param; return;}
  
  /// \brief Build Gaussian Process regressor, i.e. compute internally
  /// all necessary matrices and vectors that describe the posterior GP
  void BuildGP();
  /// \brief Evaluate the Gaussian Process at a given grid
  /// msc controls whether only mean will be computed, or standard devation and covariance as well
  void EvalGP(Array2D<double>& xgrid, string msc, Array1D<double>& mst);
  /// \brief Get the number of data points
  int getNpt() const {return npt_;}
  /// \brief Get the dimensionality
  int getNdim() const {return ndim_;}
  /// \brief Get the number of basis terms in the trend
  int getNPC() const {return npc_;}
  /// \brief Get alpha parameter
  double getAl() const {return al_;}
  /// \brief Get beta parameter
  double getBe() const {return be_;}
  /// \brief Get Sigma-hat-squared, i.e. the posterior variance factor
  double getSig2hat() const {return sig2hat_;}
  /// \brief Get \f$V^*\f$, an auxiliary matrix
  void getVst(Array2D<double>& vst) {vst=Vst_; return;}
  /// \brief Get the correlation matrix \f$A\f$
  void getA(Array2D<double>& acor) {acor=A_; return;}
  /// \brief Get the roughness parameters
  void getParam(Array1D<double>& param) {param=param_; return;}
  /// \brief Get the posterior covariance matrix
  void getCov(Array2D<double>& cov) {cov=cov_;}
  /// \brief Get the covariance in a different format, with the x,x' values
  void getXYCov(Array2D<double>& xgrid,Array2D<double>& xycov);
  /// \brief Get the Student-t parameters
  void getSttPars(Array1D<double>& sttmat);
  /// \brief Function to find the best values for roughness parameters
  void findBestCorrParam();


 private:

  /// \brief Prior covariance function
  double covariance(Array1D<double>& x1, Array1D<double>& x2,Array1D<double>& param);
  /// \brief Compute the data covariance \f$A\f$
  void computeDataCov_(Array2D<double>& xdata,Array1D<double>& param,Array2D<double>& A);

  /// \brief xdata array
  Array2D<double> xdata_;
  /// \brief ydata array
  Array1D<double> ydata_;

  /// \brief Number of bases in the mean trend
  int npc_;
  /// \brief Inverse of the mean trend coefficient prior covariance
  Array2D<double> Vinv_;
  /// \brief Prior mean of the mean trend
  Array1D<double> z_;
  //double sig2f_;
  /// \brief Prior parameter \f$\alpha\f$
  double al_;
  /// \brief Prior parameter \f$\beta\f$
  double be_;
  /// \brief Data noise 'nugget'
  double sig2n_;
  /// \brief Posterior variance factor
  double sig2hat_;

  /// \brief Number of data points
  int npt_;
  /// \brief Dimensionality
  int ndim_;
  /// \brief Covariace type, only 'SqExp' implemented so far
  string covType_;
  /// \brief Basis set for the trend function
  PCSet *PCModel_;

  /// \brief Mean of the Student-t posterior
  Array1D<double> mst_;
  /// \brief Covariance of the Student-t posterior
  Array2D<double> cov_;
  /// \brief Roughness parameter vector
  Array1D<double> param_;
    
  //@{
  /// \brief Auxiliary matrix or vector, see the UQTk Manual
  Array2D<double> H_, Ht_;
  Array2D<double> A_, Ainv_;
  Array1D<double> Ainvd_;
  Array1D<double> Vinvz_;
  Array1D<double> HtAinvd_;
  Array2D<double> AinvH_;
  Array2D<double> HtAinvH_;
  Array2D<double> Vst_; // V^*
  Array1D<double> bhat_;
  Array1D<double> Hbhat_;
  Array1D<double> yHbhat_;
  Array1D<double> AinvyHbhat_;
  Array2D<double> Vstinv_;
  //@}


}; 
#endif /* GPROC_H_SEEN */
