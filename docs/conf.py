
# Configuration file for the Sphinx documentation builder

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
author = 'Calvin'

# Full version, including alpha/beta/rc tags
release = '1.1.1.dev0'

# File to use as the master doc
master_doc = 'index'


# General configuration
# --------------------------------------------------------------------------------
# Sphinx / custom extension modules
# extensions = ['sphinx.ext.autodoc']
extensions = ['sphinx.ext.napoleon', 'sphinx.ext.viewcode']

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

# Paths that contain custom static files (such as style sheets), relative to this directory
#   These are copied after the builtin static files,
#   so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']


# Autodoc configuration
# --------------------------------------------------------------------------------
# Default options for all autodoc directives
autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    # 'exclude-members': '__weakref__',
    'private-members': True,
    # 'inherited-members': True,
    # 'imported-members': True,
    'show-inheritance': True,
}

# Set if class init method is included/concatenated to main
autoclass_content = "class"
# autoclass_content = "both"


# Napoleon configuration
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


# Default role
# --------------------------------------------------------------------------------
# reST role to use as the default role, that is, for text marked up `like this`
default_role = 'py:obj'
