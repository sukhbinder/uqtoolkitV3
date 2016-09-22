# Install script for directory: /home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pi/PROJECTS/UQTk_v3.0/builddir")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP.x" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP.x")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP.x"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/examples/surf_rxn" TYPE EXECUTABLE PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ FILES "/home/pi/PROJECTS/UQTk_v3.0/builddir/examples/surf_rxn/SurfRxnNISP.x")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP.x" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP.x")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP.x")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP_MC.x" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP_MC.x")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP_MC.x"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/examples/surf_rxn" TYPE EXECUTABLE PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ FILES "/home/pi/PROJECTS/UQTk_v3.0/builddir/examples/surf_rxn/SurfRxnNISP_MC.x")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP_MC.x" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP_MC.x")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnNISP_MC.x")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnISP.x" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnISP.x")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnISP.x"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/examples/surf_rxn" TYPE EXECUTABLE PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ FILES "/home/pi/PROJECTS/UQTk_v3.0/builddir/examples/surf_rxn/SurfRxnISP.x")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnISP.x" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnISP.x")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnISP.x")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnDet.x" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnDet.x")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnDet.x"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/examples/surf_rxn" TYPE EXECUTABLE PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ FILES "/home/pi/PROJECTS/UQTk_v3.0/builddir/examples/surf_rxn/SurfRxnDet.x")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnDet.x" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnDet.x")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/examples/surf_rxn/SurfRxnDet.x")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/examples/surf_rxn" TYPE FILE FILES
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/SurfRxnNISP.cpp"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/SurfRxnNISP_MC.cpp"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/SurfRxnISP.cpp"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/SurfRxnDet.cpp"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/Utils.cpp"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/model.h"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/XMLreader.h"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/posterior.h"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/Utils.h"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/examples/surf_rxn" TYPE FILE FILES "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/forUQ_surf_rxn.in.xml.templ")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/examples/surf_rxn" TYPE FILE PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ FILES
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/forUQ_sr.py"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/forUQ_BB_sr.py"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/forUQ_BB_utils.py"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/SurfRxnMulti.py"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/file_utils.py"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/plPDF_method.py"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/plSurfRxnMstd.py"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/plot_utils.py"
    "/home/pi/PROJECTS/UQTk_v3.0/examples/surf_rxn/utils.py"
    )
endif()

