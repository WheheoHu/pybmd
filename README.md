# PyBMD

[![PyPI](https://img.shields.io/pypi/v/pybmd)](https://pypi.org/project/pybmd/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybmd)](https://pypi.org/project/pybmd/)
[![GitHub license](https://img.shields.io/github/license/WheheoHu/pybmd)](https://github.com/WheheoHu/pybmd/blob/master/LICENSE)

A Pythonic toolkit for DaVinci Resolve — from full scripting-API access to high-level workflow helpers.

PyBMD gives you programmatic, Pythonic control over DaVinci Resolve. At its core it's a
complete wrapper around the Resolve scripting API — projects, media, timelines, color,
Fusion, and rendering. On top of that foundation it's growing into a **toolkit** of
higher-level helpers (such as marker-based still export in `toolkits.StillManager`) that
turn common workflows into a few lines of code, with more planned. It runs on **Windows**
and **macOS**, and tracks the Resolve API across versions (DaVinci Resolve 18.6 → 21.0.2).

## Features

**Core API wrapper**

- **Full API coverage** — projects, media pool & storage, timelines and timeline items,
  folders/bins, and rendering.
- **Color & Fusion** — color groups and node graphs, Fusion compositions, and Fusion-based
  UI creation (`UI_Dispather` / `UIManager`).
- **Gallery & stills** — galleries, still albums, and still management.
- **Version-aware** — query the running Resolve version and guard calls with
  `is_version_at_least()` and `check_api_compatibility()`.
- **Typed models** — data validation and structured settings powered by pydantic.
- **Convenient startup** — connect to a remote Resolve instance (`resolve_ip`) or launch a
  local one automatically (`auto_start`).

**Toolkit (high-level helpers)**

- Utilities built on top of the raw API that turn common workflows into a few lines of
  code — for example marker-based still export via `toolkits.StillManager`. This layer is
  actively growing.

## Requirements

- Python 3.12+
- DaVinci Resolve installed and running (Windows or macOS)

## Installation

```bash
pip install pybmd
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add pybmd
```

## Quick Start

> ⚠️ DaVinci Resolve must be running before you connect (or pass `auto_start=True` to launch it).

```python
from pybmd import Resolve

# Connect to a local DaVinci Resolve instance
resolve = Resolve()

project = resolve.get_project_manager().get_current_project()
timeline = project.get_current_timeline()
print(timeline.get_name())
```

`Resolve()` accepts two optional arguments:

| Argument | Default | Description |
| --- | --- | --- |
| `resolve_ip` | `"127.0.0.1"` | IP address of the DaVinci Resolve instance. Point it at a remote machine's IP to control a remote instance. |
| `auto_start` | `False` | When `True`, launch a local DaVinci Resolve automatically if it isn't already running. |

## Documentation

| Reference | Link |
| --- | --- |
| PyBMD API documentation | https://wheheohu.github.io/pybmd/ |
| DaVinci Resolve API reference | https://wheheohu.github.io/bmd_doc/ |

## License

Released under the [LGPL-3.0-or-later](LICENSE) license.
