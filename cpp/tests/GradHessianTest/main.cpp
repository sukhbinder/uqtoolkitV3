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
#include "dsfmt_add.h"
#include "arrayio.h"
#include "arraytools.h"
#include "PCBasis.h"
#include "PCSet.h"
#include "quad.h"
#include "assert.h"


using namespace std; 

/*************************************************
Begin main code
*************************************************/
int main(int argc, char ** argv){

	/********************************************
	Test gradient of Legendre PCE
	********************************************/

	// get 1d legendre polynomials
	int ndim = 3; 
	int norder = 4;
	PCSet polymodel("NISPnoq",norder,ndim,"LU"); 
	// polymodel.PrintMultiIndex();

	// define alpha, which is a specific multiindex
	Array1D<int> alpha(ndim);
	alpha(0) = 1;
	alpha(1) = 3;
	alpha(2) = 2;

	// define evaluation point and gradient
	Array1D<double> x(ndim,1); 
	Array1D<double> grad; 

	// get derivative of 3d legendre polynomial 
	// defined by the multiindex above
	polymodel.dPhi_alpha(x, alpha, grad);
	// printarray(grad);
 	assert(grad(0) == 1.0);
 	assert(grad(1) == 6.0);
 	assert(grad(2) == 3.0);

	/********************************************
	Test Hessian of Legendre PCE
	********************************************/

	// get 1d legendre polynomials
	int ndim2 = 2; 
	int norder2 = 4;
	PCSet polymodel2("NISPnoq",norder2,ndim2,"LU"); 
	// polymodel2.PrintMultiIndex();

	// define alpha, which is a specific multiindex
	Array1D<int> alpha2(ndim2,0);
	alpha2(0) = 1;
	alpha2(1) = 2;

	// define evaluation point and gradient
	Array1D<double> x2(ndim2,0);
	x2(0) = 1; 
	x2(1) = 2; 
	Array1D<double> grad2; 
	Array2D<double> hessian; 

	// get derivative of 3d legendre polynomial 
	// defined by the multiindex above
	polymodel2.dPhi_alpha(x2, alpha2, grad2);
	printarray(grad2);

 	polymodel2.ddPhi_alpha(x2, alpha2, hessian);
 	printarray(hessian);
 	assert(hessian(0,0) == 0.0);
 	assert(hessian(1,1) == 3.0);
 	assert(hessian(0,1) == 6.0);
 	assert(hessian(1,0) == 6.0);

	/********************************************
	Test 3D Hessian of Legendre PCE
	********************************************/
	int ndim3 = 3; 
	int norder3 = 4;
	PCSet polymodel3("NISPnoq",norder3,ndim3,"LU"); 
	// polymodel3.PrintMultiIndex();

	// define alpha, which is a specific multiindex
	Array1D<int> alpha3(ndim3,0);
	alpha3(0) = 1;
	alpha3(1) = 1;
	alpha3(2) = 2;

	// define evaluation point and gradient
	Array1D<double> x3(ndim3,0);
	x3(0) = 1; 
	x3(1) = 2; 
	x3(2) = 3; 
	Array1D<double> grad3; 
	Array2D<double> hessian2; 

	// get derivative of 3d legendre polynomial 
	// defined by the multiindex above
	polymodel3.dPhi_alpha(x3, alpha3, grad3);
	printarray(grad3);

 	polymodel3.ddPhi_alpha(x3, alpha3, hessian2);
 	printarray(hessian2);
 	assert(hessian2(0,0) == 0.0);
 	assert(hessian2(1,1) == 0.0);
 	assert(hessian2(2,2) == 6.0);
 	assert(hessian2(0,1) == 13.0);
 	assert(hessian2(0,2) == 18.0);
 	assert(hessian2(1,2) == 9.0);

 	// check to make sure Hessian is symmetric
 	Array2D<double> hessian2T; 
 	hessian2T = Trans(hessian2);
 	for (int i = 0; i < ndim3; i++){
 		for (int j = 0; j < ndim3; j++){
 			assert(hessian2(i,j) == hessian2T(i,j)); 
 		}		
 	}





	return 0; 

}
