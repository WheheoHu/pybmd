# PyBMD
[![GitHub license](https://img.shields.io/github/license/WheheoHu/pybmd)](https://github.com/WheheoHu/pybmd/blob/master/LICENSE)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybmd)
![PyPI](https://img.shields.io/pypi/v/pybmd)


Python library for DaVinci Resolve (Repack)

*🔥 PyBMD Now Support Both Windows & macOS 🔥*

## How To Install

```
pip install pybmd
```

## How To Use

>**⚠️Run DaVinci Resolve before you run script**

1. Initialize Resolve object use Bmd module
 
   ```python
    from pybmd import Bmd

    LOCAL_RESOLVE = Bmd()
    ```
   
    `Bmd()` has an optional arg named `davinci_ip`, default value is `127.0.0.1` stands for local DaVinci. If you want to use remote DaVinci Resolve object, change arg to remote IP.

2. You are free now! 

    Play with APIs!
    
    Original API documentation: [DaVinci Resolve API in Notion](https://wheheohu.notion.site/Davinci-Python-API-7c4f1038a36f44818b631ec7e4a537fa)

    PyBMD Library API documentation: [PyBMD API Documentation](https://wheheohu.github.io/pybmd/)