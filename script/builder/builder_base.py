#!/usr/bin/env python3

import pathlib
import abc
import shutil

from .environment_windows import environment_base

class builder_base(abc.ABC):
    def __init__(self, module_name:str, build_type:str, env:environment_base):
        self._module_name = module_name
        self._build_type = build_type

        self._project_dir = pathlib.Path(__file__).parent.parent.parent

        self._source_dir = pathlib.Path(__file__).parent.parent.parent / "third_party" / module_name

        self._output_dir      = self._project_dir / "output"
        self._pre_build_dir   = self._output_dir / "pre_build"  / self._module_name / self._build_type
        if(not self._pre_build_dir.exists()):
            self._pre_build_dir.mkdir(parents=True)

        self._build_dir   = self._output_dir / "build"  / self._module_name / self._build_type
        if(not self._build_dir.exists()):
            self._build_dir.mkdir(parents=True)

        self._install_dir = self._output_dir / "install" / self._module_name
        if(not self._install_dir.exists()): 
            self._install_dir.mkdir(parents=True)

        self._env = env

    @property
    def module_name(self):
        return self._module_name

    @property
    def source_dir(self):
        return self._source_dir

    @property
    def project_dir(self):
        return self._project_dir

    @property
    def pre_build_dir(self):
        return self._pre_build_dir

    @property
    def build_dir(self):
        return self._build_dir

    @property
    def install_dir(self):
        return self._install_dir

    @property
    def build_type(self):
        return self._build_type

    @property
    def env(self):
        return self._env

    def check_env(self):
        pass

    def do_build(self):
        shutil.rmtree(self._pre_build_dir)
        shutil.copytree(self._source_dir, self._pre_build_dir)
        self._do_build_impl()

    @abc.abstractmethod
    def _do_build_impl(self):
        pass

