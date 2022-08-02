# PyBMD
[![GitHub license](https://img.shields.io/github/license/WheheoHu/pybmd)](https://github.com/WheheoHu/pybmd/blob/master/LICENSE)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybmd)
![PyPI](https://img.shields.io/pypi/v/pybmd)


python library for Davinci Resolve(Repack)

*⚠️Currently support MacOS Only⚠️*

## How To Install

```
pip install pybmd
```

## How To Use
>**⚠️Run Davinci Resolve before you run script**

1. Init Reolve object use Bmd module
   ```python
    from pybmd import Bmd

    LOCAL_RESOLVE=Bmd()
    ```
    `Bmd()`  has an option arg named `davinci_ip` , default value is `127.0.0.1 `stands for local davinci, if you want to use remote davinci resolve object, change arg to remote ip.

2. You are free now ! 

    Play with APIs !
    
    Original API documentation could be found at my notion:
    [Davnci Resolve API in notion](https://wheheohu.notion.site/Davinci-Python-API-7c4f1038a36f44818b631ec7e4a537fa)

    Pybmd Library API documentation could be found at :[Pybmd API Documentation](https://wheheohu.github.io/pybmd/)

