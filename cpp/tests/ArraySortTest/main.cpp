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
#include "probability.h"
#include "arrayio.h"
#include "arraytools.h"
#include "assert.h"

using namespace std; 

/*************************************************
Begin main code
*************************************************/
int main(int argc, char ** argv){

	int nrow=10;
	int ncol=3;
	Array2D<double> unsorted_array(nrow,ncol);
	int seed = 13;
	generate_uniform(unsorted_array,seed);
	
	Array1D<int> oldInd(nrow);
	for (int i=0; i<nrow; i++)
		oldInd(i)=i;

	Array1D<int> newInd;

	cout << "====> Testing sort-by-column:" << endl;

	int sorting_col = 1;
	Array2D<double> array = unsorted_array;
	shell_sort_col(array,sorting_col,newInd, oldInd);

	for (int i=0; i<nrow; i++){
		//cout << newInd(i) << ":  ";
		for (int j=0; j<ncol; j++){
			double sanity = unsorted_array(oldInd(i),j) - array(i,j);
			assert (sanity == 0.0);
		}
	}

	for (int i=0; i<nrow; i++){
		for (int j=0; j<ncol; j++){
			double sanity = array(newInd(i),j) - unsorted_array(i,j);
			assert (sanity == 0.0);
		}
	}
	
	cout << "====> Sort-by-column test passed." << endl;

	// Sorting by columns sequentially, i.e. if elements are equal in the first column, the next column breaks the tie, and so on.
	cout << "====> Testing sort-by-all:" << endl;
	for (int i=0; i<nrow; i++)
		oldInd(i)=i;
	newInd.Clear();

	// Artificially setting some values equal to each other
	unsorted_array(3,0)=unsorted_array(1,0);
	unsorted_array(5,0)=unsorted_array(1,0);
	unsorted_array(8,0)=unsorted_array(1,0);

	unsorted_array(3,1)=unsorted_array(1,1);
	unsorted_array(8,1)=unsorted_array(1,1);

	array=unsorted_array;

	shell_sort_all(array,newInd, oldInd);
	for (int i=0; i<nrow; i++){
		//cout << newInd(i) << ":  ";
		for (int j=0; j<ncol; j++){
			double sanity = unsorted_array(oldInd(i),j) - array(i,j);
			assert (sanity == 0.0);
		}
	}

	for (int i=0; i<nrow; i++){
		for (int j=0; j<ncol; j++){
			double sanity = array(newInd(i),j) - unsorted_array(i,j);
			assert (sanity == 0.0);
		}
	}
	cout << "====> Sort-by-all test passed." << endl;

	//void shell_sort_incr(Array2D<double>& array,int col, Array1D<int>& newInd, Array1D<int>& oldInd);


	for (int i=0; i<nrow; i++){
		for (int j=0; j<ncol; j++){
			cout << array(i,j) << " ";
		}
	cout << endl;
	}

	return 0; 

}
