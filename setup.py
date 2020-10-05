from setuptools import setup, find_packages


readme = open('README.md').read()

setup(name="PythonPackaging",
      version='0.0.1',
      packages=find_packages(),
      description="Python Packaging Demo",
      long_description=readme,
      author="David Antliff",
      author_email="user@example.com",
      url="https://github.com/DavidAntliff/PythonPackaging",
      install_requires=[
          "PythonPackagingDependency @ git+https://github.com/DavidAntliff/PythonPackagingDependency@0.0.1#egg=PythonPackagingDependency-0.0.1",
      ],
      scripts=['bin/do_something.py', 'bin/do_something_more.py'],
      entry_points={
          'console_scripts': [
              'PythonPackaging = packageB.__main__:main',
          ]
      },
      )
