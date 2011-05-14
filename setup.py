from distutils.core import setup
from Cython.Distutils import extension
from Cython.Distutils import build_ext

ext_modules = [extension.Extension("openzwave", ["openzwave.pyx"],
                         libraries=['udev', 'stdc++'],
                         language="c++",
                         extra_objects=['openzwave/cpp/lib/linux/openzwave.a'], 
                         include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform']
)]
setup(
  name = 'py-openzwave',
  author='Maarten Damen',
  author_email='m.damen@gmail.com',
  url='http://projects.maartendamen.com/projects/pyopenzwave/',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)