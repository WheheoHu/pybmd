# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os
import tomllib
import pybmd._init_bmd
import pybmd as package

sys.path.append(os.path.abspath(".."))


# Mock the _resolve_object before importing pybmd
# This prevents import errors when building docs without DaVinci Resolve running
class MockResolveObject:
    """Mock object for DaVinci Resolve constants during documentation build."""

    def __getattr__(self, name):
        # Return incrementing float values for any attribute access
        # This ensures Enum classes can be defined without errors
        return hash(name) % 1000 + 0.0


# Inject the mock into pybmd._init_bmd before it gets imported

pybmd._init_bmd._resolve_object = MockResolveObject()


# Read version from pyproject.toml
with open(os.path.join(os.path.dirname(__file__), "..", "pyproject.toml"), "rb") as f:
    pyproject_data = tomllib.load(f)

project = package.__name__
copyright = "2026, Wheheo Hu"
author = "Wheheo Hu"
release = pyproject_data["project"]["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
]

autodoc_type_aliases = {
    "Project": "pybmd.project.Project",
    "Timeline": "pybmd.timeline.Timeline",
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.11", None),
}

autodoc_member_order = "bysource"
autodoc_typehints = "both"
autoclass_content = "both"
autosummary_generate = True


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_title = "PyBMD Docs"
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "show_nav_level": 2,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/WheheoHu/pybmd",
            "icon": "fab fa-github",
        },
    ],
}
html_static_path = ["_static"]
