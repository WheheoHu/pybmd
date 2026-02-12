# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyBMD is a Python wrapper library for DaVinci Resolve's API, providing programmatic control over DaVinci Resolve video editing software. The library supports both Windows and macOS platforms and offers comprehensive access to DaVinci Resolve's functionality including project management, media handling, timeline operations, and rendering.

## Development Commands

### Package Management
- **Build System**: Uses `pyproject.toml` with `hatchling` as build backend
- **Dependency Manager**: Uses `uv` for package management (see `uv.lock`)
- **Install Package**: `uv sync` to install dependencies and the package in editable mode
- **Python Requirement**: Python 3.12+

### Build and Documentation
- **Build Documentation**: From the `docs/` directory, run `make html` (uses Sphinx)
- **Documentation Dependencies**: Install with `uv sync --extra docs` (includes Sphinx, pydata-sphinx-theme)


### Core Dependencies
- `psutil` - Process management for auto-starting DaVinci Resolve
- `dftt-timecode` - Timecode handling
- `multimethod` - Multiple dispatch support
- `pydantic>=2.12.5` - Data validation and settings management

## Code Architecture

### Core Module Structure

The library follows a modular design mirroring DaVinci Resolve's object hierarchy:

**Main Entry Point**:
- `resolve.py`: The `Resolve` class is the main entry point for all DaVinci Resolve operations
  - `Resolve(resolve_ip="127.0.0.1", auto_start=False)`: Key initialization parameters
    - `resolve_ip`: IP address for remote DaVinci Resolve instances (default: "127.0.0.1" for local)
    - `auto_start`: Automatically launch DaVinci Resolve if not running (default: False)
- `_init_bmd.py`: Handles dynamic loading of DaVinci Resolve's fusionscript library

**Core Components**:
- `project_manager.py`: Project and database management
- `project.py`: Individual project operations and settings
- `media_pool.py` & `media_pool_item.py`: Media management and clip properties
- `media_storage.py`: File system and storage operations
- `timeline.py` & `timeline_item.py`: Timeline and clip editing operations
- `folder.py`: Media bin/folder organization

**Specialized Modules**:
- `gallery.py`, `gallery_still.py`, `gallery_still_album.py`: Still image management
- `fusion.py`, `fusion_comp.py`: Fusion compositor integration
- `ui_dispather.py`, `ui_manager.py`: GUI creation and management
- `toolkits.py`: High-level utility functions (includes `StillManager` for marker-based still export)
- `settings.py`: Configuration objects and enums
- `color_group.py`, `graph.py`: Color grading and node graph operations

### Key Design Patterns

1. **Wrapper Pattern**: Each Python class wraps the corresponding DaVinci Resolve API object
2. **Initialization Chain**: `Resolve()` → loads fusionscript → initializes all other components
3. **Auto-start Feature**: Optional automatic launching of DaVinci Resolve if not running
4. **Cross-platform Support**: Dynamic library loading for Windows/macOS/Linux

### Library Dependencies

The project dynamically loads DaVinci Resolve's fusionscript library from:
- **macOS**: `/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so`
- **Windows**: `C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll`
- **Linux**: `/opt/resolve/Developer/Scripting/Modules/`

### Version Compatibility

The library supports DaVinci Resolve 18.6+ through 20.0.0 and tracks API changes across versions. See `CHANGELOG.md` for version-specific feature additions and the evolution from DR 18.6 through 20.0.0.

## Important Notes

- **DaVinci Resolve Dependency**: DaVinci Resolve must be running before initializing the library (unless `auto_start=True`)
- **Platform-Specific Paths**: Library paths and executable locations are platform-dependent
- **API Version Tracking**: The library version follows DaVinci Resolve release cycles (2024.x.x, 2025.x.x, 2026.x.x)
- **Demo Application**: The `test.py` file is a complete GUI application (not a test suite) that demonstrates:
  - Fusion UI system integration with custom windows, tabs, and event handlers
  - Timeline marker-based still export workflows using `StillManager`
  - Custom logging integration into GUI components
  - Real-world usage patterns for the library's high-level APIs