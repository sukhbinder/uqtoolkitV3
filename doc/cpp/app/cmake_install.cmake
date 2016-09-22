# Install script for directory: /home/pi/PROJECTS/UQTk_v3.0/cpp/app

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
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/gen_mi/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/generate_quad/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/model_inf/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/pce_eval/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/pce_quad/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/pce_resp/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/pce_rv/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/pce_sens/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/pdf_cl/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/sens/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/regression/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/gp_regr/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/cpp/app/gkpSparse/cmake_install.cmake")

endif()

