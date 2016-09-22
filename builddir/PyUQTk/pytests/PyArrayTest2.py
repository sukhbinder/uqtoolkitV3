#=====================================================================================
#                     The UQ Toolkit (UQTk) version 3.0
#                     Copyright (2016) Sandia Corporation
#                     http://www.sandia.gov/UQToolkit/
#
#     Copyright (2016) Sandia Corporation. Under the terms of Contract DE-AC04-94AL85000
#     with Sandia Corporation, the U.S. Government retains certain rights in this software.
#
#     This file is part of The UQ Toolkit (UQTk)
#
#     UQTk is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     UQTk is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with UQTk.  If not, see <http://www.gnu.org/licenses/>.
#
#     Questions? Contact Bert Debusschere <bjdebus@sandia.gov>
#     Sandia National Laboratories, Livermore, CA, USA
#=====================================================================================
# include path to include PyUQTk
import sys
sys.path.append('../uqtkarray/')

try:
	import numpy as np
except ImportError:
	"Need numpy to test PyUQTk"

try:
	import uqtkarray
	from uqtkarray import numpy2uqtk
	from uqtkarray import uqtk2numpy
except ImportError:
	print "PyUQTk array module not found"
	print "If installing in a directory other than the build directory, make sure PYTHONPATH includes the install directory"

'''
This file tests to make sure conversion from numpy -> uqtkarray does
not change the row-major (C contiguous) format of the original numpy array

Also, when converting form uqtkarray-> numpy we want to make sure that the 
resulting numpy array is *only* row major (C contiguous)

'''

# create numpy matrix and show flags
a_np = np.array([[0, 2.00],[0.1, 1],[1, 5.0]])
print "flags for a_np to show whether C or F contiguous"
print a_np.flags

# get a uqtk array from a numpy array (memory is copied, not shared)
a_uqtk = numpy2uqtk(a_np)
print "\nflags for original numpy array to make sure it hasn't changed to F continguous after converting"
# verify that the original numpy array is only C contiguous
assert a_np.flags['F_CONTIGUOUS'] == False
assert a_np.flags['C_CONTIGUOUS'] == True

print "\nConvert uqtk array back to numpy array and make sure C contiguous"
b_np = uqtk2numpy(a_uqtk)
# test to make sure new numpy array is *only* C contiguous (row - major)
assert b_np.flags['F_CONTIGUOUS'] == False
assert b_np.flags['C_CONTIGUOUS'] == True

# test for the dot product
print "\ncompute dot product which should be [2,1.1,6] (Note that if F contigous, the dot product would be [.1,3,6]:"
dp = np.dot(b_np,np.ones(2))
assert np.alltrue( dp ==  np.array([2.,1.1,6.]))
