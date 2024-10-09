import setuptools
import pybmd as package
with open("README.md", "r") as rm:
    long_description = rm.read()

setuptools.setup(
    name=package.__name__,
    version=package.__version__,
    author="wheheo",
    author_email="wheheohu@outlook.com",
    description="python library for Davinci Resolve(Repack)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WheheoHu/pybmd",
    packages=setuptools.find_packages(),
    install_requires=[
          'psutil',
          'dftt-timecode',
          'multimethod'
      ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],

)
