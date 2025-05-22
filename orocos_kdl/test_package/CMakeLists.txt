cmake_minimum_required(VERSION 3.12)
project(test_package LANGUAGES CXX)

find_package(orocos-kdl CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE orocos-kdl::orocos-kdl)
