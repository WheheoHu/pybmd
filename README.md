# PyBMD
[![GitHub license](https://img.shields.io/github/license/WheheoHu/pybmd)](https://github.com/WheheoHu/pybmd/blob/master/LICENSE)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybmd)
![PyPI](https://img.shields.io/pypi/v/pybmd)


Python wrapper library for DaVinci Resolve API

*🔥 Pybmd Now Support Both Windows & macOS 🔥*

## How To Install

```
pip install pybmd
```

## How To Use
>**⚠️Run Davinci Resolve before you run script**

1. Init Resolve object use Bmd module
   ```python
    from pybmd import Resolve

    LOCAL_RESOLVE = Resolve()
    ```
    `Resolve()` has an option arg named `resolve_ip` , default value is `127.0.0.1 `stands for local davinci, if you want to use remote DaVinci Resolve object, change arg to remote ip.
    
    `Resolve()` has an option arg named `auto_start` , default value is `true `stands for open davinci automatically if it's not running, if you want to open davinci manually, change arg to `false`.

2. You are free now! 

    Play with APIs!
    
    Original API documentation could be found at my notion:
    [Davnci Resolve API](https://wheheohu.github.io/bmd_doc/)

    Pybmd Library API documentation could be found at :[Pybmd API Documentation](https://wheheohu.github.io/pybmd/)