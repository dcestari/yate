from setuptools import setup, find_packages
import sys, os

version = '0.4'

setup(name='yate',
      version=version,
      description="Yet Another Text Editor",
      long_description="""\
""",
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development"
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Daniel Cestari',
      author_email='dcestari@gmail.com',
      url='http://dcestari.github.com/yate',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'ngram',
        'wxPython',
      ],
      package_data={
        'yate':['themes/*.json']
      },
      entry_points={
        'console_scripts': [
          'yate = yate.main:main'
        ]
      }
)
