# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import sphinx_rtd_theme
import pathlib
import sys
import os
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())
sys.path.insert(0, os.path.abspath('../ycv/'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ycv'
copyright = '2023, Md Arif Shaikh'
author = 'Md Arif Shaikh'
release = '0.0.dev4'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_rtd_theme',
              'sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.mathjax',
              'numpydoc',
              'nbsphinx',
              'sphinx.ext.autosectionlabel',
              'sphinx_tabs.tabs',
              "sphinx.ext.viewcode",
              'sphinx.ext.doctest',
              'sphinx.ext.napoleon',
              'myst_parser'
              ]

autosummary_generate = True
numpydoc_show_class_members = False
source_suffix = ['.rst', '.md', '.txt']
templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
