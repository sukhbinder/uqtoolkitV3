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

using namespace std; 

/*************************************************
Begin main code
*************************************************/
int main(int argc, char ** argv){

	/**********************************
	Read and write 1D Array
	*********************************/
	
	int m = 3; 
	int n = 3;

	// Create nxm array with all ones
	Array2D<double> A(m,n,1);

	// Write array to file
	write_datafile(A,"A.dat");

	// create dim-D array of zeros
	Array2D<double> B(m,n,0);

	// read in data file to B
	read_datafile(B,"A.dat");

	/**********************************
	Fill in normal r.v.'s to 1D Array
	*********************************/
	
	// Feed in uniform random numbers to array
	dsfmt_t RandomState; 
	int seed = 1; 
	dsfmt_init_gen_rand(&RandomState,seed);
	for (int i = 0; i < m; i++){
		for (int j = 0; j < n; j++){
			A(i,j) = dsfmt_genrand_urv(&RandomState); 
		}
	}

	// Write array to file
	write_datafile(A,"A_nrv.dat");
	cout << "\nA : " << endl;
	printarray(A);

	/*********************************
	Linaer alg. operations on arrays
	********************************/

	// matrix vector product
	Array1D<double> x(3,1);
	Array1D<double> b = dot(A,x);
	cout << "\nb = " << endl;
	printarray(b); 

	// print transpose
	Array2D<double> AT = Trans(A);
	cout << "\nTranspose:" << endl;
	printarray(AT);

	// get inverse of square matrix A
	if ( n == m){
		Array2D<double> Ainv = INV(A);
		cout << "\nA inverse:" << endl;
		printarray(Ainv);
	}

	// get least squares solution
	x.Resize(3,0);
	LSTSQ(A,b,x);
	cout << "\nleast squares solution:" << endl;
	printarray(x);

	// get QR factorization
	Array2D<double> Q,R;
	QR(A,Q,R);
	cout << "\nQ:" << endl;
	printarray(Q);
	cout << "\nR:" << endl;
	printarray(R);

	// get SVD factorization
	Array2D<double> U,VT;
	Array1D<double> S; 
	SVD(A,U,S,VT);
	cout << "\nU:" << endl;
	printarray(U);
	cout << "\nS:" << endl;
	printarray(S);
	cout << "\nVT:" << endl;
	printarray(VT);


}
