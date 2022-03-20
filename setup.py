import setuptools

with open("README.md", "r") as rm:
    long_description = rm.read()

setuptools.setup(
    name="pybmd",
    version="2022.3",
    author="wheheo",
    author_email="wheheohu@outlook.com",
    description="python libery for Davinci Resolve(Repack)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WheheoHu/pybmd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X"
    ],
    install_requires=[
        "dataclasses"
        ],

)
