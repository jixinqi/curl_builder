#!/usr/bin/env python3

from .builder_base import builder_base
from .environment_windows import environment_base

class builder_curl(builder_base):
    def __init__(self, build_type:str, env:environment_base):
        super().__init__("curl", build_type, env)

    def _do_build_impl(self):
        zlib_filename = "zs.lib"
        if(self.build_type == "Debug"):
            zlib_filename = "zsd.lib"

        self.env.run_commands(
            commands = [
                f'cmake -B        {self.build_dir}'
                    f' -DCMAKE_INSTALL_PREFIX={self.install_dir / self.build_type}'
                    f' -DCMAKE_BUILD_TYPE={self.build_type}'

                    f' -DBUILD_SHARED_LIBS='       f'OFF'
                    f' -DBUILD_STATIC_LIBS='       f'ON'
                    f' -DBUILD_TESTING='           f'ON'
                    f' -DCURL_TEST_BUNDLES='       f'ON'

                    f' -DCURL_USE_LIBPSL='         f'ON'
                    f' -DLIBPSL_INCLUDE_DIR='      f'"{ self.project_dir / "output" / "install" / "libpsl"  / self.build_type / "include" }"'
                    f' -DLIBPSL_LIBRARY='          f'"{ self.project_dir / "output" / "install" / "libpsl"  / self.build_type / "lib" / "psl.lib" }"'
                    f' -DLIBPSL_CFLAGS='           f'"-DPSL_API="'

                    f' -DCURL_BROTLI='             f'ON'
                    f' -DBROTLI_INCLUDE_DIR='      f'"{ self.project_dir / "output" / "install" / "brotli"  / self.build_type / "include" }"'
                    f' -DBROTLIDEC_LIBRARY='       f'"{ self.project_dir / "output" / "install" / "brotli"  / self.build_type / "lib" / "brotlidec.lib" }"'
                    f' -DBROTLICOMMON_LIBRARY='    f'"{ self.project_dir / "output" / "install" / "brotli"  / self.build_type / "lib" / "brotlicommon.lib"}"'

                    f' -DZLIB_INCLUDE_DIR='        f'"{ self.project_dir / "output" / "install" / "zlib"    / self.build_type / "include" }"'
                    f' -DZLIB_LIBRARY='            f'"{ self.project_dir / "output" / "install" / "zlib"    / self.build_type / "lib" / zlib_filename }"'

                    f' -DCURL_ZSTD=ON'
                    f' -DZSTD_INCLUDE_DIR='        f'"{ self.project_dir / "output" / "install" / "zstd"    / self.build_type / "include" }"'
                    f' -DZSTD_LIBRARY='            f'"{ self.project_dir / "output" / "install" / "zstd"    / self.build_type / "lib" / "zstd_static.lib" }"'
                    ,
                f'cmake --build   {self.build_dir} --config={self.build_type}',
                f'cmake --install {self.build_dir} --config={self.build_type}',
            ],
            cwd = self.pre_build_dir
        )

if(__name__ == "__main__"):
    pass
