from setuptools import setup, find_packages
from Cython.Build import cythonize
import numpy as np

setup(
    name = 'modmat',
    version = '0.1',
    packages = find_packages(),
    ext_modules = cythonize("modmat/*.pyx"),
    include_dirs = [np.get_include()],

    install_requires = [
        'networkx==1.6'
    ],

    entry_points = {
        'console_scripts': [
            'modmat = modmat.command.modmat:main',
            'modmatp = modmat.command.modmatp:main',
            'plotmultihistmse = modmat.command.plotmultihistmse:main',
            'plotmultihistseries3d = modmat.command.plotmultihistseries3d:main',
        ],
    }
)
