
from distutils.core import setup, find_packages
from io import open

setup(
    name='Strex',
    version='0.1.0',
    
    author='simw',
    author_email='jrh@example.com',
    
    packages=find_packages(exclude=['tests*']),
    
    url='http://github.com/simw/strex',
    license='LICENSE.txt',
    
    description='Extracts structure from unstructured data',
    long_description=open('README.md').read(),
    
    install_requires=[
        'lxml >= 3.3.0',
        'requests >= 2.4.0',
    ],

    extras_require = {
        'test': ['pytest'],
    },
)

