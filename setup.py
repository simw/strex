from distutils.core import setup

setup(
    name='Strex',
    version='0.1.0',
    author='simw',
    author_email='jrh@example.com',
    packages=['strex', 'tests'],
    url='http://github.com/simw/strex',
    license='LICENSE.txt',
    description='HTML / XML to object structure extractor',
    long_description=open('README.md').read(),
    install_requires=[
        "lxml >= 3.3.0",
    ],
)
