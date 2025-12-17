#!/usr/bin/env python3

from .builder_base import builder_base
from .environment_windows import environment_base

class builder_zstd(builder_base):
    def __init__(self, build_type:str, env:environment_base):
        super().__init__("zstd", build_type, env)

    def _do_build_impl(self):
        self.env.run_commands(
            commands = [
                f'cmake -B        {self.build_dir}'
                    f' -DCMAKE_INSTALL_PREFIX={self.install_dir / self.build_type}'
                    f' -DCMAKE_BUILD_TYPE={self.build_type}'

                    f' -DZSTD_BUILD_CONTRIB=OFF'
                    f' -DZSTD_BUILD_TESTS=OFF'
                    f' -DZSTD_LEGACY_SUPPORT=OFF'
                    f' -DZSTD_BUILD_PROGRAMS=OFF'
                    f' -DZSTD_PROGRAMS_LINK_SHARED=OFF'
                    f' -DZSTD_BUILD_SHARED=OFF'
                    f' -DZSTD_BUILD_STATIC=ON'
                    f' -DZSTD_MULTITHREAD_SUPPORT=ON'
                    ,
                f'cmake --build   {self.build_dir} --config={self.build_type}',
                f'cmake --install {self.build_dir} --config={self.build_type}',
            ],
            cwd = self.pre_build_dir
        )

if(__name__ == "__main__"):
    pass
