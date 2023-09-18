# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys, os
sys.path.append(os.path.abspath(".."))

import pybmd as package

project = package.name
copyright = '2023, Wheheo Hu'
author = 'Wheheo Hu'
release = package.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration




extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode',
            ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_title = 'PyBMD Docs'
html_theme = "pydata_sphinx_theme"
html_theme_options={
    "icon_links":[
                {
            "name": "GitHub",
            "url": "https://github.com/WheheoHu/pybmd",
            "icon": "fab fa-github",
        },
    ]
}
html_static_path = ['_static']
