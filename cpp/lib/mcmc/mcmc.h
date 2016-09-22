/* =====================================================================================
                     The UQ Toolkit (UQTk) version 3.0
                     Copyright (2016) Sandia Corporation
                     http://www.sandia.gov/UQToolkit/

     Copyright (2013) Sandia Corporation. Under the terms of Contract DE-AC04-94AL85000
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
/// \file mcmc.h
/// \author K. Sargsyan, C. Safta, B. Debusschere, 2012 -     
/// \brief Header file for the Markov chain Monte Carlo class

#ifndef UQTKMCMC_H_SEEN
#define UQTKMCMC_H_SEEN


#include "dsfmt_add.h"
     
#include <iostream>
#include <string.h>
#include <stdio.h>
#include <sstream>

using namespace std; // needed for python string conversion

//*****************************************
class LikelihoodBase{
public:
  virtual double eval(Array1D<double>&){return 3.14;};
  virtual ~LikelihoodBase(){};
};
//*****************************************
     
/// \class MCMC
/// \brief Markov Chain Monte Carlo class.
///        Implemented single-site and adaptive MCMC algorithms
class MCMC {
public:
  /// \brief Constructor, given a pointer to logPosterior function, a pointer to additional info, e.g. data
  ///        and the chain dimaensionality
  MCMC(double (*logposterior)(Array1D<double>&, void *), void *postinfo);
  /// \brief Dummy constructor
  MCMC(){};

  //*****************************************

  MCMC(LikelihoodBase& L);
  int WRITE_FLAG; 
  void setWriteFlag(int I); 
  void resetChainState();
  dsfmt_t RandomState; 

  
  //*****************************************

  /// \brief Destructor
  ~MCMC(){};
  
  /// \brief Set the gradient function
  void setGradient(void (*gradlogPosterior)(Array1D<double>&, Array1D<double>&, void *));
  /// \brief Set the metric tensor function
  void setMetricTensor(void (*metricTensor)(Array1D<double>&, Array2D<double>&, void *));

  /// \brief Set defaults
  void initDefaults();

  /// \brief Print chain information on the screen
  void printChainSetup();

  /// \brief Set chain dimensionality
  void setChainDim(int chdim) ;
 
  /// \brief Initialize proposal covariance matrix given as a 2d-array
  ///        For aMCMC, this matrix is used only before adaptivity starts
  void initChainPropCov(Array2D<double>& propcov);
  /// \brief Initialize proposal covariance matrix given its 1d-array diagonal
  ///        For aMCMC, this matrix is used only before adaptivity starts
  void initChainPropCovDiag(Array1D<double>& sig);
  /// \brief Returns proposal covariance matrix
  void getChainPropCov(Array2D<double>& propcov);
  // / \brief Initialize the method used, 'am' or 'ss'
  void initMethod(string method);
  /// \brief Initialize adaptivity step parameters for aMCMC
  void initAdaptSteps(int adaptstart,int adaptstep, int adaptend);
  /// \brief Initialize the scaling factor gamma for aMCMC
  void initAMGamma(double gamma);
  /// \brief Initialize the covariance 'nugget' for aMCMC
  void initEpsCov( double eps_cov);
  /// \brief Initialize epsilon for MALA
  void initEpsMALA(double eps_mala);

  /// \brief Set output specification, type('txt' or 'bin'), filename, frequency of outputs to the file and to screen.
  void setOutputInfo(string outtype, string file,int freq_file, int freq_screen);
 
  /// \brief Set the indicator to confirm that the names of parameters are prepended in the output file
  void namesPrepended() {this->namePrepend_=true; return;}

  /// \brief Get the name of the chain file
  string getFilename(){return this->outputinfo_.filename;}

  /// \brief Reset to a new chain file
  void resetChainFilename(string filename){this->fullChain_.Clear(); this->lastwrite_=-1; this->outputinfo_.filename=filename; return;}

  /// \brief The optimization routine
  void runOptim(Array1D<double>& start);

  /// \brief The actual function that generates MCMC
  void runChain(int ncalls, Array1D<double>& chstart);

  /// \brief Structure that holds the chain state information
  struct chainstate{
    int step;
    Array1D<double> state;
    double alfa;
    double post;
  }; 

  /// \brief An auxiliary function to parse the binary file and produce an array of chain-states
  void parseBinChain(string filename, Array1D<chainstate>& readchain);
  /// \brief Write an array of chain-states to a file
  void writeFullChainTxt(string filename, Array1D<chainstate> fullchain);
  /// \brief Get full chain as an array of chain-states
  void getFullChain(Array1D<chainstate>& readchain) {  readchain=fullChain_;  return;}
  /// \brief Append MAP state to the end
  void appendMAP();


  /// \brief Get MAP parameters
  double getMode(Array1D<double>& MAPparams);

  /// \brief Check to see if a new mode was found during last call to runChain
  bool newModeFound();

  /// \brief Get the chain's acceptance ratio
  void getAcceptRatio(double * accrat);

  /// \brief Get the MCMC chain dimensionality
  int GetChainDim() const {return this->chainDim_;}
 
  /// \brief Function to evaluate the log-posterior
  double evalLogPosterior(Array1D<double>& m);

  /// \brief Function to evaluate the gradient of log-posterior
  void evalGradLogPosterior(Array1D<double>& m, Array1D<double>& grads);

  /// \brief Set random generation seed
  void setSeed(int seed);
    
  /// \brief Check if a point is in the domain
  bool inDomain(Array1D<double>& m);
    
  /// \brief Set lower bounds
  void setLower(double lower, int i);
  /// \brief Set upper bounds
  void setUpper(double upper, int i);
  /// \brief Set default unbounded domain
  void setDefaultDomain();
  
  /// \brief Get samples of the chain with burnin and thining
  void getSamples(int burnin, int every,Array2D<double>& samples);
  /// \brief Get all samples of the chain 
  void getSamples(Array2D<double>& samples);

private:

  //*****************************************
  int FLAG; 
  LikelihoodBase* L_;
  //*****************************************

  /// \brief Void pointer to the posterior info (e.g. data)

  /// \brief Chain dimensionality
  int chainDim_;

  /// \brief Pointer to log-posterior function (of tweaked parameters and a void pointer to any other info)
  ///        this pointer is set i the constructor to a user-defined function
  double (*logPosterior_)(Array1D<double>&, void *);
  void (*gradlogPosterior_)(Array1D<double>&, Array1D<double>&, void *);
  void (*metricTensor_)(Array1D<double>&, Array2D<double>&, void *);

  /// \brief Void pointer to the posterior info (e.g. data)
  void *postInfo_;

  /// \brief The Cholesky factor(square-root) of proposal covariance
  Array2D<double> propLCov_;

  /// \brief Random seed for MCMC
  int seed_;
  
  /// \brief The number of proposal steps within one MCMC step (=1 for AMCMC, =chaindim for MCMC_SS)
  int nSubSteps_;
  
  /// \brief Generating the proposal candidate vector of parameters according to the adaptive MCMC algorithm
  void proposalAdaptive(Array1D<double>& m_t,Array1D<double>& m_cand,int t);
  /// \brief Generating the proposal candidate vector of parameters according to the Single-Site algorithm
  void proposalSingleSite(Array1D<double>& m_t,Array1D<double>& m_cand,int dim);
  /// \brief Generating the proposal candidate vector of parameters according to the MALA algorithm
  void proposalMALA(Array1D<double>& m_t,Array1D<double>& m_cand);
  /// \brief Generating the proposal candidate vector of parameters according to the MMALA algorithm
  void proposalMMALA(Array1D<double>& m_t,Array1D<double>& m_cand);

  /// \brief Evaluate old|new and new|old probabilities
  double probOldNew(Array1D<double>& a, Array1D<double>& b);

  /// \brief Evaluate MVN
  double evallogMVN_diag(Array1D<double>& x,Array1D<double>& mu,Array1D<double>& sig2);


  /// \brief A structure to hold method-specific parameters
  struct methodpar
  {
    /// In adaptive MCMC, covariance of the chain values sampled so far
    Array2D<double> curcov;  
    /// In adaptive MCMC, mean of the chain values sampled so far
    Array1D<double> curmean; 
    /// In adaptive MCMC, the coefficient behind the covariance scaling factor 
    double gamma;            
    /// In adaptive MCMC, the offset epsilon for Cholesky to be computationally feasible
    double eps_cov;           
    /// In adaptive MCMC, a size=3 vector (t_start,t_step,t_end) that indicates 
    /// when the adaptivity starts, how often the proposal covariance is updated and when the adaptivity ends, respectively.
    Array1D<int> adaptstep;   
    /// Chain proposal distributions (before the adaptivity starts)
    Array2D<double> chcov;  
    /// Method type, 'am' or 'ss'
    string type;            
  }  methodinfo_;
  
  /// \brief Epsilon for MALA algorithm
  double epsMALA_;

  /// \brief A structure to hold parameters of output specification
  struct outputpar
  {
    /// Frequency of printing the chain progress on screen
    int freq_outscreen;     
    /// Frequency of printing the chain progress to a file
    int freq_chainfile;
    /// The name of the file
    string filename;
    /// The output type, 'txt' or 'bin'
    string type;
  } outputinfo_;

  /// \brief The current chain state
  chainstate currState_;
  /// \brief The current MAP state
  chainstate modeState_;
  
  /// \brief Array of chain states
  Array1D<chainstate> fullChain_;
 
  /// \brief Function to update the chain mode, i.e. the MAP location
  void updateMode();

  /// \brief Write the full chain as a text
  void writeChainTxt(string filename);
  /// \brief Write the full chain as a binary file
  void writeChainBin(string filename);
  /// \brief Indicates up to which state of the chain is already written to files
  int lastwrite_;
  /// \brief Indicates up to which state of the chain is already written to files
  bool namePrepend_;

  /// \brief Flag to indicate whether a new mode is found during last call to runChain
  bool newMode_;

  /// \brief Acceptance Ratio of the chain
  double accRatio_;

  //@{
  /// \brief Flag to indicate whether the corresponding parameters are initialized or not
  bool chaindimInit_;
  bool propcovInit_;
  bool methodInit_;
  bool outputInit_;
  bool adaptstepInit_;
  bool gammaInit_;
  bool epscovInit_;
  bool epsMalaInit_;
  //@}

  /// \brief Flag that indicates whether gradient information is given or not
  bool gradflag_;
  /// \brief Flag that indicates whether tensor information is given or not
  bool tensflag_;

  //@{
  /// \brief Default
  string default_method_;
  double default_gamma_;
  double default_eps_cov_;
  double default_eps_mala_;
  //@}

  /// \brief Lower bounds
  Array1D<double> Lower_;
  /// \brief Upper bounds
  Array1D<double> Upper_;
    
  ///\brief Lower bound existence flags
  Array1D<int> lower_flag_;
  ///\brief Upper bound existence flags
  Array1D<int> upper_flag_;
    

};

#endif /* UQTKMCMC_H_SEEN */

