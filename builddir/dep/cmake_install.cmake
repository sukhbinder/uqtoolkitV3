# Install script for directory: /home/pi/PROJECTS/UQTk_v3.0/dep

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/pi/PROJECTS/UQTk_v3.0/builddir/dep/libdepuqtk.a")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/pi/PROJECTS/UQTk_v3.0/builddir/dep/slatec/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/builddir/dep/blas/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/builddir/dep/lapack/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/builddir/dep/dsfmt/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/builddir/dep/lbfgs/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/builddir/dep/cvode-2.7.0/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/builddir/dep/ann/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/builddir/dep/figtree/cmake_install.cmake")

endif()
