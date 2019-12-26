from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='yahoo_quote_download',
      version='0.2.1',
      description='Yahoo Quote Downloader',
      author='c0redumb',
      url='https://github.com/c0redumb/yahoo_quote_download',
      long_description=long_description,
      long_description_content_type="text/markdown",
          license="BSD 3-Clause License",
      packages=['yahoo_quote_download'],
      install_requires=[
          'six',
      ],
      classifiers=["Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 3",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   ],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'yqdownload=yahoo_quote_download.downloader:main',
          ],
      },
      )
