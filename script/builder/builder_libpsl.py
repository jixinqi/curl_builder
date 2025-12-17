#!/usr/bin/env python3

import textwrap

from .builder_base import builder_base
from .environment_windows import environment_base

class builder_libpsl(builder_base):
    def __init__(self, build_type:str, env:environment_base):
        super().__init__("libpsl", build_type, env)

    def __generate_suffixes_dafsa_h(self):
        self.env.run_commands(
            commands = [
                "python3 src/psl-make-dafsa --output-format=cxx+ list/public_suffix_list.dat suffixes_dafsa.h",
            ],
            cwd = self.pre_build_dir
        )

    def __generate_libpsl_h(self):
        psl_version        = ""
        psl_version_major  = ""
        psl_version_minor  = ""
        psl_version_patch  = ""
        psl_version_number = ""

        with open(self.pre_build_dir / "version.txt") as version_file:
            psl_version = version_file.read().strip()
            psl_version_major, psl_version_minor, psl_version_patch = psl_version.split(".")
            psl_version_number = f"0x{int(psl_version_major):02X}{int(psl_version_minor):02X}{int(psl_version_patch):02X}"

        libpsl_h_content = ""
        with open(self.pre_build_dir / "include" / "libpsl.h.in") as libpsl_h_in_file:
            libpsl_h_in_file_lines = libpsl_h_in_file.readlines()
            for line in libpsl_h_in_file_lines:
                line = line.replace("@LIBPSL_VERSION@",        f"{psl_version}")
                line = line.replace("@LIBPSL_VERSION_MAJOR@",  f"{psl_version_major}")
                line = line.replace("@LIBPSL_VERSION_MINOR@",  f"{psl_version_minor}")
                line = line.replace("@LIBPSL_VERSION_PATCH@",  f"{psl_version_patch}")
                line = line.replace("@LIBPSL_VERSION_NUMBER@", f"{psl_version_number}")
                libpsl_h_content += line

        with open(self.pre_build_dir / "include" / "libpsl.h", "w") as libpsl_h_file:
            libpsl_h_file.write(libpsl_h_content)

    def __generate_cmake_file(self):
        content = textwrap.dedent(
            '''
            cmake_minimum_required(VERSION 3.15)

            set(CMAKE_CXX_STANDARD 20)
            set(CMAKE_EXPORT_COMPILE_COMMANDS 1)

            project(psl)

            set(${PROJECT_NAME}_INC     "")
            set(${PROJECT_NAME}_INC_DIR "")
            set(${PROJECT_NAME}_SRC     "")
            set(${PROJECT_NAME}_SRC_DIR "")
            set(${PROJECT_NAME}_LIB     "")
            set(${PROJECT_NAME}_LIB_DIR "")

            set(PROGRAM_NAME
                "${PROJECT_NAME}"
            )
            add_library(psl STATIC
                "${CMAKE_SOURCE_DIR}/src/psl.c"
                "${CMAKE_SOURCE_DIR}/src/lookup_string_in_fixed_set.c"
            )
            target_include_directories(${PROJECT_NAME} PUBLIC
                "${CMAKE_SOURCE_DIR}/"
                "${CMAKE_SOURCE_DIR}/include/"
            )
            target_compile_definitions(${PROJECT_NAME} PUBLIC
                "ENABLE_BUILTIN"
                "PSL_STATIC"
                PACKAGE_VERSION="0.21.5"
            )
            install(DIRECTORY "${CMAKE_SOURCE_DIR}/include/"
                DESTINATION "include"
                FILES_MATCHING PATTERN "*.h"
            )
            install(TARGETS ${PROJECT_NAME}
                ARCHIVE DESTINATION "lib"
            )
            '''
        )
        with open(self.pre_build_dir / "CMakeLists.txt", "w") as libpsl_cmake_file:
            libpsl_cmake_file.write(content)

    def _do_build_impl(self):
        self.__generate_suffixes_dafsa_h()
        self.__generate_libpsl_h()
        self.__generate_cmake_file()

        self.env.run_commands(
            commands = [
                f'cmake -B        {self.build_dir}'
                    f' -DCMAKE_INSTALL_PREFIX={self.install_dir / self.build_type}'
                    f' -DCMAKE_BUILD_TYPE={self.build_type}'
                    ,
                f'cmake --build   {self.build_dir} --config={self.build_type}',
                f'cmake --install {self.build_dir} --config={self.build_type}',
            ],
            cwd = self.pre_build_dir
        )

if(__name__ == "__main__"):
    pass
