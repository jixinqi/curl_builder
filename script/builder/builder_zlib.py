#!/usr/bin/env python3

from .builder_base import builder_base
from .environment_windows import environment_base

class builder_zlib(builder_base):
    def __init__(self, build_type:str, env:environment_base):
        super().__init__("zlib", build_type, env)

    def _do_build_impl(self):
        self.env.run_commands(
            commands = [
                f'cmake -B        {self.build_dir}'
                    f' -DCMAKE_INSTALL_PREFIX={self.install_dir / self.build_type}'
                    f' -DCMAKE_BUILD_TYPE={self.build_type}'

                    f' -DZLIB_BUILD_TESTING=OFF'
                    ,
                f'cmake --build   {self.build_dir} --config={self.build_type}',
                f'cmake --install {self.build_dir} --config={self.build_type}'
            ],
            cwd = self.pre_build_dir
        )

if(__name__ == "__main__"):
    pass
