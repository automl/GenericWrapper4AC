import os
import shutil
import subprocess
import sys
import traceback
import setuptools
from setuptools.command.install import install

RUNSOLVER_LOCATION = 'runsolver/runsolver-3.3.4-patched/src/'
DOWNLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__), '.downloads/')
BINARIES_DIRECTORY = 'genericWrapper4AC/binaries'

class InstallRunsolver(install):

    def run(self):
        try:
            shutil.rmtree(DOWNLOAD_DIRECTORY)
        except Exception:
            #traceback.print_exc()
            pass

        try:
            os.makedirs(DOWNLOAD_DIRECTORY)
        except Exception:
            #traceback.print_exc()
            pass


        shutil.copytree(RUNSOLVER_LOCATION,os.path.join(DOWNLOAD_DIRECTORY,"runsolver"))
        runsolver_source_path = os.path.join(DOWNLOAD_DIRECTORY,"runsolver")

        # Build the runsolver
        sys.stdout.write('Building runsolver\n')
        cur_pwd = os.getcwd()
        os.chdir(runsolver_source_path)
        subprocess.check_call('make')
        os.chdir(cur_pwd)

        # Create a fresh binaries directory
        try:
            shutil.rmtree(BINARIES_DIRECTORY)
        except Exception:
            pass

        try:
            os.makedirs(BINARIES_DIRECTORY)
            with open(os.path.join(BINARIES_DIRECTORY, '__init__.py')):
                pass
        except Exception:
            pass

        # Copy the runsolver into the sources so it gets copied
        shutil.move(os.path.join(runsolver_source_path, 'runsolver'),
                    os.path.join(BINARIES_DIRECTORY, 'runsolver'))

        #install.do_egg_install(self)
        install.run(self)

        try:
            shutil.rmtree(BINARIES_DIRECTORY)
        except OSError:
            pass
        try:
            shutil.rmtree(DOWNLOAD_DIRECTORY)
        except OSError:
            pass
        
setuptools.setup(
    name='GenericWrapper4AC',
    description='Generic Wrapper to interface between algorithm configurators and algorithms to tune',
    version='1.0.0',
    packages=setuptools.find_packages(exclude=['test']),
    test_suite='nose.collector',
    cmdclass={'install': InstallRunsolver},
    include_package_data=True,
    author='Marius Lindauer',
    author_email='lindauer@informatik.uni-freiburg.de',
    license='BSD',
    platforms=['Linux'],
    classifiers=[],
    url='www.ml4aad.org')