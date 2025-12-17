#!/usr/bin/env python3

import abc
import pathlib
import subprocess

class environment_base(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def run_commands(self, commands:list[str], cwd):
        pass

if(__name__ == "__main__"):
    pass
