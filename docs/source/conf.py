# Configuration file for Sphinx documentation on GitHub Pages
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath("../.."))

# Project information
project = "ndp-ep"
copyright = "2025, NDP EP Team"
author = "NDP EP Team"
release = "0.1.0"
version = "0.1.0"

# Extensions - minimal set for GitHub Pages
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

# Templates and exclusions
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML output
html_theme = "sphinx_rtd_theme"
html_static_path = []

# GitHub Pages specific settings
html_baseurl = "https://sci-ndp.github.io/ndp-ep-py/"
html_theme_options = {
    "canonical_url": html_baseurl,
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# Mock imports for modules that might not be available during build
autodoc_mock_imports = []

# Suppress warnings
suppress_warnings = ["toc.not_readable"]

# Master document
master_doc = "index"
