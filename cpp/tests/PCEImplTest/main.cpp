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

	cout << "Testing PC implementations: " << endl;


	// Set up PC parameters
	int ndim = 3; 
	int nord = 3;
	string pctype = "HG";
	string impl = "ISP";


	// Define PCSet object
	PCSet pcmodel(impl,nord,ndim,pctype);


	cout << "====> Testing norm computation: " << endl;	

	Array1D<double> normsq, normsq_exact;
	// Get the norms computed by quadrature
	pcmodel.GetNormSq(normsq);
	// Evaluate the norms analytically
	pcmodel.EvalNormSqExact(normsq_exact);

	for (int i=0; i<normsq.Length(); i++){
		double rel_error=sqrt(fabs(normsq(i)-normsq_exact(i)))/sqrt(fabs(normsq_exact(i)));
		if ( rel_error > 1e-7 ){
			cout << "PC type = " << pctype << ", Dim = " << ndim << ", Order = " << nord << endl;
			throw Tantrum("====> Norm computation test failed.");
		}

	}

	cout << "====> Norm computation test passed." << endl;

	if (impl == "NISP"){
		// Testing Galerkin projection
		cout << "====> Testing Galerkin projection: " << endl;	

		// Get the quadrature points
		Array2D<double> x;
		pcmodel.GetQuadPoints(x);

		// Define test function to be evaluated
		// Test function is a polynomial of order nord
		Array1D<double> y(x.XSize(),0);
		for (int i = 0; i < x.XSize(); i++){
			double sum = 0.0;
			for (int j = 0; j < ndim; j++)
				sum += (x(i,j)/(j+1));
			y(i) = pow(sum,nord);
		} 

		
		// Get coefficients via Galerkin projection
		Array1D<double> ck; 
		pcmodel.GalerkProjection(y,ck);
		
		// Evaluate PC at quadrature points
		// PC should be exactly matching the polynomial test function
		Array1D<double> ytest(x.XSize(),0);
		pcmodel.EvalPCAtCustPoints(ytest,x,ck);
		double error = 0.0; 
		for (int i = 0; i < x.XSize(); i++){
			error += pow(y(i) - ytest(i),2);
		} 
		double rms_error=sqrt(error/x.XSize());
		if ( rms_error > 1e-10 ){
			cout << "PC type = " << pctype << ", Dim = " << ndim << ", Order = " << nord << endl;
			cout << "Error at quadrature points " << rms_error << endl;
			throw Tantrum("====> Galerkin projection test failed.");
		}

		cout << "====> Galerkin projection test passed." << endl;
	}

	else if (impl == "ISP"){
		cout << "ISP tests not implemented yet. " << endl;	
		//cout << "====> Testing triple products: " << endl;	
		//cout << "====> Testing 4-tuple products: " << endl;	
	}

	return 0; 

}
