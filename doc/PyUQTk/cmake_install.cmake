# Install script for directory: /home/pi/PROJECTS/UQTk_v3.0/PyUQTk

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/PyUQTk" TYPE FILE PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ FILES "/home/pi/PROJECTS/UQTk_v3.0/PyUQTk/__init__.py")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/inference/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/plotting/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/sens/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/multirun/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/utils/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/uqtkarray/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/quad/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/tools/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/pce/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/bcs/cmake_install.cmake")
  include("/home/pi/PROJECTS/UQTk_v3.0/doc/PyUQTk/pytests/cmake_install.cmake")

endif()

