"""Choose random entries from sequences in a YAML file

"""

from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='gametables',
      version='0.1.0',
      description='Choose random entries from sequences in a YAML file',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/encodis/gametables',
      author='Philip Hodder',
      author_email='philip.hodder@encodis.com',
      license='MIT',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Games/Entertainment :: Role-Playing'
      ],
      keywords='gametables tables games playing',
      py_modules=['gametables'],
      install_requires=[
        'pyyaml>=5.1',
        'py_expression_eval'
      ],
      entry_points={
        'console_scripts': [
            'gametables = gametables:main',
        ],
      }
      )
