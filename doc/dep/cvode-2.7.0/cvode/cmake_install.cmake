# Install script for directory: /home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/cvode

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/pi/PROJECTS/UQTk_v3.0/doc")
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
  MESSAGE("
Install CVODE
")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/pi/PROJECTS/UQTk_v3.0/doc/dep/cvode-2.7.0/cvode/libdepcvode.a")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/dep/cvode" TYPE FILE FILES
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode_band.h"
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode_bandpre.h"
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode_bbdpre.h"
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode_dense.h"
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode_diag.h"
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode_direct.h"
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode.h"
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode_spbcgs.h"
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode_spgmr.h"
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode_spils.h"
    "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/include/cvode/cvode_sptfqmr.h"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/dep/cvode" TYPE FILE FILES "/home/pi/PROJECTS/UQTk_v3.0/dep/cvode-2.7.0/cvode/cvode_impl.h")
endif()

