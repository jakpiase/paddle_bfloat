from setuptools import dist
dist.Distribution().fetch_build_eggs(['numpy>=1.13, <=1.19.3'])

import os
import sys
import shutil
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

PACKAGE_NAME='bfloat16'


if 'clean' in sys.argv:
    curdir = os.path.dirname(os.path.realpath(__file__))
    for filepath in ['build', 'dist', f'{PACKAGE_NAME}.egg-info', 'MANIFEST']:
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                os.remove(filepath)
            else:
                shutil.rmtree(filepath)

class my_build_ext(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

    def build_extensions(self):
        try:
            self.compiler.compiler_so.remove("-Wstrict-prototypes")
        except (AttributeError, ValueError):
            pass
        build_ext.build_extensions(self)

module1 = Extension(PACKAGE_NAME,
                    sources=['bfloat16.cc'],
                    extra_compile_args=['-std=c++11'])

setup(name=PACKAGE_NAME,
      version='1.1',
      description='Numpy bfloat16 package',
      license='Apache',
      author='GreenWaves Technologies',
      author_email='support@greenwaves-technologies.com',
      url='https://github.com/GreenWaves-Technologies/bfloat16',
      download_url = 'https://github.com/GreenWaves-Technologies/bfloat16/archive/refs/tags/1.0.tar.gz',
      setup_requires=['numpy'],
      ext_modules=[module1],
      packages=find_packages(),
      cmdclass={'build_ext': my_build_ext})
