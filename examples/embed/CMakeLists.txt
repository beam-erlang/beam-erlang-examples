cmake_minimum_required(VERSION 3.25)
project(example_embed VERSION 0.1.0 LANGUAGES C)

find_package(BEAM CONFIG REQUIRED COMPONENTS Runtime CLI)

set(module_source "${CMAKE_CURRENT_SOURCE_DIR}/answer.erl")
set(module_directory "${CMAKE_CURRENT_BINARY_DIR}/ebin")
set(module_file "${module_directory}/answer.beam")
set(module_header "${CMAKE_CURRENT_BINARY_DIR}/generated/answer_beam.h")

add_custom_command(OUTPUT "${module_file}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${module_directory}"
    COMMAND $<TARGET_FILE:BEAM::CLI> compile
        --depfile "${module_file}.d" -o "${module_directory}" -- "${module_source}"
    DEPFILE "${module_file}.d"
    DEPENDS "${module_source}" BEAM::CLI
    COMMENT "Compiling answer.erl with the installed BEAM compiler"
    VERBATIM)

add_custom_command(OUTPUT "${module_header}"
    COMMAND "${CMAKE_COMMAND}"
        "-DINPUT=${module_file}" "-DOUTPUT=${module_header}"
        -P "${CMAKE_CURRENT_SOURCE_DIR}/EmbedBytes.cmake"
    DEPENDS "${module_file}" "${CMAKE_CURRENT_SOURCE_DIR}/EmbedBytes.cmake"
    COMMENT "Embedding answer.beam in the C host"
    VERBATIM)

add_executable(example-embed main.c "${module_header}")
set_target_properties(example-embed PROPERTIES
    C_STANDARD 99 C_STANDARD_REQUIRED YES C_EXTENSIONS NO)
target_include_directories(example-embed PRIVATE
    "${CMAKE_CURRENT_BINARY_DIR}/generated")
target_link_libraries(example-embed PRIVATE BEAM::Runtime)

beam_target_deployment(example-embed PROFILE bare)
beam_install_deployment(example-embed)
install(FILES LICENSE.txt README.md DESTINATION share/example-embed)
