#! /usr/bin/python3
# -*- coding:utf-8 -*-


from setuptools import setup,find_packages,Command
import shutil
import os
import sys
import subprocess

# read version info
here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'framework', '__version__.py')) as f:
    exec(f.read(), about)
project_name = "legendarytest"

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        print("done")
        shutil.rmtree('{}.egg-info'.format(project_name))


def call(msg, commands, error_msg, exit_on_fail=False):
    print("{:*^50}".format(" {} ".format(msg)))
    try:
        for command in commands:
            subprocess.check_call(command)
    except Exception:
        print("{:!^50}".format(" {} ".format(error_msg)))
        if exit_on_fail:
            sys.exit()

setup(name='legendarytest',
      version=about['__version__'],
      license='MIT',
      author='Tuo LI',
      author_email='tuo.de.li@gmail.com',
      description='a Library to facilitate devices test',
      package_dir = {'':'.'},
      # packages=find_packages('magicpy',exclude=["vision","*.vision","*.vision.*","vision.*"]),
      packages = find_packages(),
      install_requires=[
          'pyserial',
          'colorama',
      ],
      long_description=open('README.md').read(),
      cmdclass={'clean': CleanCommand},
      zip_safe=False,)
