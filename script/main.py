#!/usr/bin/env python3

import builder
import sys

env = None
if(sys.platform.startswith("win")):
    env = builder.environment_windows()
elif sys.platform.startswith("linux"):
    pass

if(env != None):
    builder_libpsl_obj = builder.builder_libpsl("Debug", env)
    builder_libpsl_obj.do_build()

    builder_brotli_obj = builder.builder_brotli("Debug", env)
    builder_brotli_obj.do_build()

    builder_zlib_obj = builder.builder_zlib("Debug", env)
    builder_zlib_obj.do_build()

    builder_zstd_obj = builder.builder_zstd("Debug", env)
    builder_zstd_obj.do_build()

    builder_curl_obj = builder.builder_curl("Debug", env)
    builder_curl_obj.do_build()
