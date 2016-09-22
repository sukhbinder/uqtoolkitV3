#!/bin/bash
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

usage ()
{
  echo "No command-line parameters, execute as is"
  exit
}

while getopts ":h" opt; do
  case $opt in
    h) usage
    ;;
    \?) echo "Invalid option -$OPTARG" >&2; usage
    ;;
  esac
done

cmake -DCMAKE_INSTALL_PREFIX:PATH=$PWD/../UQTk_v3.0-install     \
      -DCMAKE_Fortran_COMPILER=/opt/intel/fc/Compiler/11.1/080/bin/ia64/ifort \
      -DCMAKE_C_COMPILER=/opt/intel/cc/Compiler/11.1/080/bin/ia64/icc \
      -DCMAKE_CXX_COMPILER=/opt/intel/cc/Compiler/11.1/080/bin/ia64/icpc \
      -DIntelLibPath=/opt/intel/fc/Compiler/11.1/080/lib/ia64 \
      -DINTEL-GROVER=YES \
      -DPyUQTk=OFF \
      ../UQTk_v3.0
