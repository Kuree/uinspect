cmake_minimum_required(VERSION 3.1 FATAL_ERROR)
project(uinspect)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(extern/pybind11)

pybind11_add_module(uinspect uinspect.cc)