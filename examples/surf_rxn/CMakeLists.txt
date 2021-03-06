project (UQTk)

SET(copy_CPP_FILES
   SurfRxnNISP.cpp 
   SurfRxnNISP_MC.cpp
   SurfRxnISP.cpp
   SurfRxnDet.cpp
   Utils.cpp
   model.h 
   XMLreader.h 
   posterior.h 
   Utils.h
  )

SET(copy_XML_FILES
 forUQ_surf_rxn.in.xml.templ
 )

SET(copy_PY_FILES
 forUQ_sr.py
 forUQ_BB_sr.py
 forUQ_BB_utils.py
 SurfRxnMulti.py
 file_utils.py
 plPDF_method.py
 plSurfRxnMstd.py
 plot_utils.py
 utils.py
 )

# SurfRxnNISP.x
add_executable (SurfRxnNISP.x    SurfRxnNISP.cpp    Utils.cpp)
add_executable (SurfRxnNISP_MC.x SurfRxnNISP_MC.cpp Utils.cpp)
add_executable (SurfRxnISP.x     SurfRxnISP.cpp     Utils.cpp)
add_executable (SurfRxnDet.x     SurfRxnDet.cpp     Utils.cpp)

target_link_libraries (SurfRxnNISP.x  uqtkpce uqtkmcmc uqtkquad uqtktools uqtkarray uqtkxmlutils)
target_link_libraries (SurfRxnNISP.x  depdsfmt deplbfgs depcvode depnvec
depslatec deplapack depblas depfigtree depann)

target_link_libraries (SurfRxnNISP_MC.x uqtkpce uqtkmcmc uqtkquad uqtktools uqtkarray uqtkxmlutils)
target_link_libraries (SurfRxnNISP_MC.x depdsfmt deplbfgs depcvode depnvec
depslatec deplapack depblas depfigtree depann)

target_link_libraries (SurfRxnISP.x  uqtkpce uqtkmcmc uqtkquad uqtktools uqtkarray uqtkxmlutils)
target_link_libraries (SurfRxnISP.x  depdsfmt deplbfgs depcvode depnvec
depslatec deplapack depblas depfigtree depann )

target_link_libraries (SurfRxnDet.x  uqtkpce uqtkmcmc uqtkquad uqtktools uqtkarray uqtkxmlutils)
target_link_libraries (SurfRxnDet.x  depdsfmt deplbfgs depcvode depnvec
depslatec deplapack depblas depfigtree depann )

# Link fortran libraries
if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
  # using GCC
  if ("${GnuLibPath}" STREQUAL "")
    target_link_libraries (SurfRxnNISP.x    gfortran stdc++)
    target_link_libraries (SurfRxnNISP_MC.x gfortran stdc++)
    target_link_libraries (SurfRxnISP.x     gfortran stdc++)
    target_link_libraries (SurfRxnDet.x     gfortran stdc++)
  else()
    target_link_libraries (SurfRxnNISP.x    ${GnuLibPath}/libgfortran.a ${GnuLibPath}/libquadmath.a stdc++)
    target_link_libraries (SurfRxnNISP_MC.x ${GnuLibPath}/libgfortran.a ${GnuLibPath}/libquadmath.a stdc++)
    target_link_libraries (SurfRxnISP.x     ${GnuLibPath}/libgfortran.a ${GnuLibPath}/libquadmath.a stdc++)
    target_link_libraries (SurfRxnDet.x     ${GnuLibPath}/libgfortran.a ${GnuLibPath}/libquadmath.a stdc++)
  endif()
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Intel")
  # using Intel
  if ("${IntelLibPath}" STREQUAL "")
    target_link_libraries (SurfRxnNISP.x    ifcore ifport)
    target_link_libraries (SurfRxnNISP_MC.x ifcore ifport)
    target_link_libraries (SurfRxnISP.x     ifcore ifport)
    target_link_libraries (SurfRxnDet.x     ifcore ifport)
  else()
    target_link_libraries (SurfRxnNISP.x    ${IntelLibPath}/libifcore.a ${IntelLibPath}/libifport.a)
    target_link_libraries (SurfRxnNISP_MC.x ${IntelLibPath}/libifcore.a ${IntelLibPath}/libifport.a)
    target_link_libraries (SurfRxnISP.x     ${IntelLibPath}/libifcore.a ${IntelLibPath}/libifport.a)
    target_link_libraries (SurfRxnDet.x     ${IntelLibPath}/libifcore.a ${IntelLibPath}/libifport.a)
  endif()
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  # using Clang
  if ("${ClangLibPath}" STREQUAL "")
    target_link_libraries (SurfRxnNISP.x    gfortran stdc++)
    target_link_libraries (SurfRxnNISP_MC.x gfortran stdc++)
    target_link_libraries (SurfRxnISP.x     gfortran stdc++)
    target_link_libraries (SurfRxnDet.x     gfortran stdc++)
  else()
    target_link_libraries (SurfRxnNISP.x    ${ClangLibPath}/libgfortran.dylib ${ClangLibPath}/libquadmath.dylib ${ClangLibPath}/libstdc++.dylib)
    target_link_libraries (SurfRxnNISP_MC.x ${ClangLibPath}/libgfortran.dylib ${ClangLibPath}/libquadmath.dylib ${ClangLibPath}/libstdc++.dylib)
    target_link_libraries (SurfRxnISP.x     ${ClangLibPath}/libgfortran.dylib ${ClangLibPath}/libquadmath.dylib ${ClangLibPath}/libstdc++.dylib)
    target_link_libraries (SurfRxnDet.x     ${ClangLibPath}/libgfortran.dylib ${ClangLibPath}/libquadmath.dylib ${ClangLibPath}/libstdc++.dylib)
  endif()
endif()

target_link_libraries (SurfRxnNISP.x    expat )
target_link_libraries (SurfRxnNISP_MC.x expat )
target_link_libraries (SurfRxnISP.x     expat )
target_link_libraries (SurfRxnDet.x     expat )

include_directories(../../examples/line_infer)
include_directories(../../cpp/lib/include    )
include_directories(../../cpp/lib/array      )
include_directories(../../cpp/lib/pce        )
include_directories(../../cpp/lib/quad       )
include_directories(../../cpp/lib/mcmc       )
include_directories(../../cpp/lib/tools      )
include_directories(../../cpp/lib/xmlutils   )

include_directories(../../dep/dsfmt)
include_directories(../../dep/figtree)
include_directories(../../dep/cvode-2.7.0/include)
include_directories("${PROJECT_BINARY_DIR}/../../dep/cvode-2.7.0/include")

INSTALL(TARGETS SurfRxnNISP.x    
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ 
        DESTINATION examples/surf_rxn)
INSTALL(TARGETS SurfRxnNISP_MC.x 
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ 
        DESTINATION examples/surf_rxn)
INSTALL(TARGETS SurfRxnISP.x     
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ 
        DESTINATION examples/surf_rxn)
INSTALL(TARGETS SurfRxnDet.x     
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ 
        DESTINATION examples/surf_rxn)

INSTALL(FILES ${copy_CPP_FILES} DESTINATION examples/surf_rxn)
INSTALL(FILES ${copy_XML_FILES} DESTINATION examples/surf_rxn)
INSTALL(FILES ${copy_PY_FILES} 
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ 
        DESTINATION examples/surf_rxn)
