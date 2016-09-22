# CMake generated Testfile for 
# Source directory: /home/pi/PROJECTS/UQTk_v3.0/PyUQTk/pytests
# Build directory: /home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/pytests
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(PyModTest "python" "PyModTest.py")
set_tests_properties(PyModTest PROPERTIES  WORKING_DIRECTORY "/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/pytests")
add_test(PyArrayTest "python" "PyArrayTest.py")
set_tests_properties(PyArrayTest PROPERTIES  WORKING_DIRECTORY "/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/pytests")
add_test(PyArrayTest2 "python" "PyArrayTest2.py")
set_tests_properties(PyArrayTest2 PROPERTIES  WORKING_DIRECTORY "/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/pytests")
add_test(PyQuadTest "python" "PyQuadTest.py")
set_tests_properties(PyQuadTest PROPERTIES  WORKING_DIRECTORY "/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/pytests")
