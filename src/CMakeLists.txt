cmake_minimum_required(VERSION 3.19)

# === Environment-specific user configuration ===
set(PRODUCT_VERSION 2022)
set(MOBU_ROOT "C:/Program Files/Autodesk/MotionBuilder ${PRODUCT_VERSION}")

if(NOT WIN32)
    message(FATAL_ERROR "This module now only supports Windows.")
endif()

# Open Reality SDK setup
set(ORSDK_LIB_DIR "${MOBU_ROOT}/OpenRealitySDK/lib/x64")
set(ORSDK_INCLUDE_DIR "${MOBU_ROOT}/OpenRealitySDK/include")
math(EXPR MOBU_INTERNAL_VERSION "(${PRODUCT_VERSION} - 2000) * 1000")

# === Python version detection ===
if(PRODUCT_VERSION LESS 2020)
    message(FATAL_ERROR "Only MotionBuilder 2020 or above is supported.")
endif()

set(PYTHON_VERSION_MAP
    "2020\;27"
    "2022\;37"
    "2023\;39"
    "2024\;310"
    "2025\;311"
    "2026\;311"
)

set(PYTHON_VERSION "")
foreach(pair ${PYTHON_VERSION_MAP})
    list(GET pair 0 ver)
    list(GET pair 1 pyver)
    if(PRODUCT_VERSION EQUAL ver)
        set(PYTHON_VERSION ${pyver})
        break()
    endif()
endforeach()

if(PYTHON_VERSION STREQUAL "")
    message(FATAL_ERROR "Unsupported MotionBuilder version: ${PRODUCT_VERSION}")
endif()

# === Project Setup ===
project(mbpluginload)
add_library(${PROJECT_NAME} SHARED MBPluginLoader.cpp)
set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".pyd")

# === Include Paths ===
if(PRODUCT_VERSION EQUAL 2020)
    set(ORSDK_PY_INCLUDE_DIR "${ORSDK_INCLUDE_DIR}/python-2.7.11/include")
elseif(PRODUCT_VERSION EQUAL 2022)
    set(ORSDK_PY_INCLUDE_DIR "${ORSDK_INCLUDE_DIR}/python-3.7.7/include")
else()
    set(ORSDK_PY_INCLUDE_DIR "${ORSDK_INCLUDE_DIR}/python/include")
endif()

target_include_directories(${PROJECT_NAME} PRIVATE
    ${ORSDK_INCLUDE_DIR}
    ${ORSDK_PY_INCLUDE_DIR}
)

# === Compile Definitions : for Mobu SDK ===
target_compile_definitions(${PROJECT_NAME} PRIVATE PRODUCT_VERSION=${PRODUCT_VERSION})

# === Link Libraries ===
target_link_libraries(${PROJECT_NAME} PRIVATE
    "${ORSDK_LIB_DIR}/fbsdk.lib"
    "${ORSDK_LIB_DIR}/python${PYTHON_VERSION}.lib"
)

if(PRODUCT_VERSION EQUAL 2022)
    target_link_libraries(${PROJECT_NAME} PRIVATE "${ORSDK_LIB_DIR}/python37/pyfbsdk.lib")
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE "${ORSDK_LIB_DIR}/pyfbsdk.lib")
endif()

if(PRODUCT_VERSION EQUAL 2022)
    target_link_libraries(${PROJECT_NAME} PRIVATE "${ORSDK_LIB_DIR}/boost_python37.lib")
elseif(PRODUCT_VERSION EQUAL 2020)
    target_link_libraries(${PROJECT_NAME} PRIVATE "${ORSDK_LIB_DIR}/boost_python27.lib")
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE "${ORSDK_LIB_DIR}/boost_python.lib")
endif()

# === Post-build: Copy to Module Directory ===
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${PROJECT_NAME}>
    ${CMAKE_SOURCE_DIR}/mbpluginloader/pyd/${MOBU_INTERNAL_VERSION}/$<TARGET_FILE_NAME:${PROJECT_NAME}>
)