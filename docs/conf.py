# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os
import tomllib
sys.path.append(os.path.abspath(".."))

import pybmd as package

# Read version from pyproject.toml
with open(os.path.join(os.path.dirname(__file__), "..", "pyproject.toml"), "rb") as f:
    pyproject_data = tomllib.load(f)

project = package.__name__
copyright = '2023, Wheheo Hu'
author = 'Wheheo Hu'
release = pyproject_data["project"]["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration




extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode',
              'sphinx.ext.autosummary',
              'sphinx.ext.intersphinx',
              'sphinx.ext.todo',
            ]

autodoc_type_aliases = {
    "Project":"pybmd.project.Project",
    "Timeline":"pybmd.timeline.Timeline",
   
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.11", None),
}

autodoc_member_order = "bysource"
autodoc_typehints = "both"
autoclass_content = "both"
autosummary_generate = True


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_title = 'PyBMD Docs'
html_theme = "pydata_sphinx_theme"
html_theme_options={
    "show_nav_level": 2,
    "icon_links":[
                {
            "name": "GitHub",
            "url": "https://github.com/WheheoHu/pybmd",
            "icon": "fab fa-github",
        },
    ]
}
html_static_path = ['_static']
