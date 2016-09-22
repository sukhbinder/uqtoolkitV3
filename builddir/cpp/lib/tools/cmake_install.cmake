# Install script for directory: /home/pi/PROJECTS/UQTk_v3.0/cpp/lib/tools

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/pi/PROJECTS/UQTk_v3.0/builddir/cpp/lib/tools/libuqtktools.a")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/uqtk" TYPE FILE FILES
    "/home/pi/PROJECTS/UQTk_v3.0/cpp/lib/tools/combin.h"
    "/home/pi/PROJECTS/UQTk_v3.0/cpp/lib/tools/gq.h"
    "/home/pi/PROJECTS/UQTk_v3.0/cpp/lib/tools/minmax.h"
    "/home/pi/PROJECTS/UQTk_v3.0/cpp/lib/tools/multiindex.h"
    "/home/pi/PROJECTS/UQTk_v3.0/cpp/lib/tools/pcmaps.h"
    "/home/pi/PROJECTS/UQTk_v3.0/cpp/lib/tools/probability.h"
    "/home/pi/PROJECTS/UQTk_v3.0/cpp/lib/tools/rosenblatt.h"
    "/home/pi/PROJECTS/UQTk_v3.0/cpp/lib/tools/func.h"
    "/home/pi/PROJECTS/UQTk_v3.0/cpp/lib/tools/tools.h"
    )
endif()

