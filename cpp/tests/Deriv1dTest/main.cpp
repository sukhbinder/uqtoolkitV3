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

	/*******************************************
	Get derivative of a Legendre
	polynomial at x = 1.0 up to 4th order
	********************************************/

	PCBasis polybasis("LU");
	Array1D<double> derivevals(5,0); 

	double x = 1.0;
	polybasis.EvalDerivBasis(x,derivevals);

	printarray(derivevals);

	assert(derivevals(0) == 0.0);
	assert(derivevals(1) == 1.0);
	assert(derivevals(2) == 3.0);
	assert(derivevals(3) == 6.0);
	assert(derivevals(4) == 10.0);

	/*******************************************
	Get derivative of a Legendre
	polynomial at x = -1,-.5,0,.5,1.0 up to 4th order
	********************************************/
	Array2D<double> dpsi;
	int kord = 4; 
	Array1D<double> custPoints(5,0);
	for (int i = 0; i < 5; i++){
		custPoints(i) = 2*i/4.0 - 1.0;
	}
	polybasis.Eval1dDerivBasisAtCustPoints(dpsi,kord,custPoints);
	assert(dpsi(4,0) == 0.0);
	assert(dpsi(4,1) == 1.0);
	assert(dpsi(4,2) == 3.0);
	assert(dpsi(4,3) == 6.0);
	assert(dpsi(4,4) == 10.0);


	return 0; 

}
