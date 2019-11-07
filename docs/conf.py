
"""Sphinx documentation builder configuration for msAI.

"""


import os
import sys


# Path setup
# --------------------------------------------------------------------------------
# Add directories containing modules to document to sys.path
# Make relative paths absolute
sys.path.insert(0, os.path.abspath('..'))


# Project information
# --------------------------------------------------------------------------------
project = 'msAI'
copyright = '2019'
author = 'Calvin Peters'

# Full version, including alpha/beta/rc tags
release = '1.3.1.dev0'

# File to use as the master doc
master_doc = 'index'


# General configuration
# --------------------------------------------------------------------------------
# Sphinx / custom extension modules
# extensions = ['sphinx.ext.autodoc']
extensions = ['sphinx.ext.napoleon',
              'sphinx_autodoc_typehints',
              'sphinx.ext.viewcode']

# Paths that contain templates, relative to this directory
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and directories to ignore
#   when looking for source files
# This pattern also affects html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# Options for HTML output
# --------------------------------------------------------------------------------
# Theme to use for HTML pages
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
# html_theme = 'default'


# Default role
# --------------------------------------------------------------------------------
# reST role to use as the default role, that is, for text marked up `like this`
default_role = 'py:obj'


# Autodoc configuration
# --------------------------------------------------------------------------------
# Default options for all autodoc directives
autodoc_default_options = {'member-order': 'bysource',
                           'special-members': '__init__',
                           'undoc-members': True,
                           'private-members': True,
                           'inherited-members': True,
                           'show-inheritance': True}

# Set if class init method is included/concatenated to main
# autoclass_content = "both"


# Napoleon ext configuration
# --------------------------------------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True


# Autodoc type hints ext configuration
# --------------------------------------------------------------------------------
set_type_checking_flag = True               # Set true to enable "expensive" typing imports
typehints_fully_qualified = False           # Set false to just display class names
always_document_param_types = False         # Set true to add stub documentation for undocumented parameters
typehints_document_rtype = True             # Set false to never add an :rtype: directive


# View code ext configuration
# --------------------------------------------------------------------------------
viewcode_follow_imported_members = False
