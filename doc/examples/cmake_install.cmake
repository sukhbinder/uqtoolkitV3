# Install script for directory: /home/pi/PROJECTS/UQTk_v3.0/examples

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
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/examples/ops/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/examples/kle_ex1/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/examples/line_infer/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/examples/pce_bcs/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/examples/surf_rxn/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/examples/uqpc/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/examples/sensMC/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/examples/num_integ/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/examples/fwd_prop/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/examples/window/cmake_install.cmake")

endif()

