# Install script for directory: /home/pi/PROJECTS/UQTk_v3.0/PyUQTk/utils

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/PyUQTk/utils" TYPE FILE PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ FILES
    "/home/pi/PROJECTS/UQTk_v3.0/PyUQTk/utils/__init__.py"
    "/home/pi/PROJECTS/UQTk_v3.0/PyUQTk/utils/colors.py"
    "/home/pi/PROJECTS/UQTk_v3.0/PyUQTk/utils/crps.py"
    "/home/pi/PROJECTS/UQTk_v3.0/PyUQTk/utils/pdf_kde.py"
    "/home/pi/PROJECTS/UQTk_v3.0/PyUQTk/utils/multiindex.py"
    "/home/pi/PROJECTS/UQTk_v3.0/PyUQTk/utils/regr.py"
    "/home/pi/PROJECTS/UQTk_v3.0/PyUQTk/utils/func.py"
    )
endif()
