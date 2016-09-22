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
#include <iostream>
#include "math.h"
#include "Array1D.h"
#include "Array2D.h"
#include "mcmc.h"
#include "quad.h"
#include "arrayio.h"
#include "PCBasis.h"
#include "PCSet.h"
#include "arraytools.h"
#include "dsfmt_add.h"
#include "bcs.h"
#include "assert.h"


using namespace std; 


int main(){

int nord = 8; 
int ndim = 1; 
int level = 16; 
Quad q("LU","full",ndim,level);

Array2D<double> x; 
Array1D<double> w; 
Array2D<int> index; 
q.SetRule();
q.GetRule(x,w,index);

// get pc object
PCSet pcmodel("NISPnoq",nord,ndim,"LEG"); 

// get projection matrix
Array2D<double> Phi; 
pcmodel.EvalBasisAtCustPts(x,Phi);

// get y at x points
Array1D<double> y(x.XSize(),0.0);
for (int i = 0; i < x.XSize(); i++){
y(i) = 1.0/(1.0 + x(i,0)*x(i,0));
}

// Main inputs are Phi, ydata, sigma
double sigma = 1e-8; 

// params
double eta = 1e-8; 
Array1D<double> lambda_init; 
double scale = .1; 

// outputs
Array1D<double> weights, errbars, basis, alpha;
Array1D<int> used; 
double lambda = 0.0; 

int adaptive=1;
int optimal=1;
int verbose=0;
// run bcs
//bcs(Phi,y,sigma,eta,scale,weights,used,errbars);
BCS(Phi,y,sigma,eta,lambda_init,adaptive,optimal,scale,verbose,weights,used,errbars,basis,alpha,lambda);

printarray(weights);
printarray(used);
printarray(errbars);

cout << fabs(0.785397 - weights(0)) << endl;
cout << fabs(-0.353987 - weights(1)) << endl;
cout << fabs(0.00316971 - weights(4)) << endl;
cout << fabs(used(1) - 2) << endl;
cout << fabs(used(2) - 4) << endl;
cout << fabs(used(4) - 8) << endl;

assert(fabs(0.785397 - weights(0)) < 1e-6);
assert(fabs(-0.353987 - weights(1)) < 1e-6);
assert(fabs(0.00316971 - weights(4)) < 1e-6);
assert(fabs(used(1) - 2) < 1e-16);
assert(fabs(used(2) - 4) < 1e-16);
assert(fabs(used(4) - 8) < 1e-16);




return 0; 

}
