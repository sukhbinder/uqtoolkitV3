# Install script for directory: /home/pi/PROJECTS/UQTk_v3.0/cpp/tests

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

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/ArrayReadAndWrite/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/ArrayDelColumn/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/Array1DMiscTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/Array2DMiscTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/ArraySortTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/MultiIndexTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/CorrTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/QuadLUTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/MCMC2dTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/MCMCRandomTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/MCMCNestedTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/Deriv1dTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/SecondDeriv1dTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/GradHessianTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/GradientPCETest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/PCE1dTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/PCEImplTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/Hessian2dTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/BCS1dTest/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/tests/BCS2dTest/cmake_install.cmake")

endif()

