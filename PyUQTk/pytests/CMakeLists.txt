project (UQTk)

set(PYTHON_EXECUTABLE python)

SET( CMAKE_SWIG_OUTDIR "${PROJECT_BINARY_DIR}" )

# Add python tests and run without "make install"
configure_file( PyModTest.py "${CMAKE_SWIG_OUTDIR}/PyModTest.py" COPYONLY )
add_test( NAME PyModTest COMMAND ${PYTHON_EXECUTABLE} PyModTest.py WORKING_DIRECTORY ${CMAKE_SWIG_OUTDIR} )

configure_file( PyArrayTest.py "${CMAKE_SWIG_OUTDIR}/PyArrayTest.py" COPYONLY )
add_test( NAME PyArrayTest COMMAND ${PYTHON_EXECUTABLE} PyArrayTest.py WORKING_DIRECTORY ${CMAKE_SWIG_OUTDIR} )

configure_file( PyArrayTest2.py "${CMAKE_SWIG_OUTDIR}/PyArrayTest2.py" COPYONLY )
add_test( NAME PyArrayTest2 COMMAND ${PYTHON_EXECUTABLE} PyArrayTest2.py WORKING_DIRECTORY ${CMAKE_SWIG_OUTDIR} )

configure_file( PyQuadTest.py "${CMAKE_SWIG_OUTDIR}/PyQuadTest.py" COPYONLY )
add_test( NAME PyQuadTest COMMAND ${PYTHON_EXECUTABLE} PyQuadTest.py WORKING_DIRECTORY ${CMAKE_SWIG_OUTDIR} )

