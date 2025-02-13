# Configuration file for the Sphinx documentation builder.

# -- Project location

import os
import sys

# Add the root directory of your project to the Python path
sys.path.insert(0, os.path.abspath("../../"))

from biodumpy.version import __version__ as version

# -- Project information

project = "biodumpy"
copyright = "2024, Centre Balear de Biodiversitat (CBB) - Data Team"
author = "Cancellario, T.; Golomb, T.; Roldán, A.; Far, A."


# -- General configuration

extensions = ["sphinx.ext.duration", "sphinx.ext.doctest", "sphinx.ext.autodoc", "sphinx.ext.autosummary",
              "sphinx.ext.intersphinx", "sphinxcontrib.bibtex", 'sphinx_togglebutton']

bibtex_bibfiles = ["references.bib"]
bibtex_reference_style = "author_year"  # This will give you numbered references

intersphinx_mapping = {"python": ("https://docs.python.org/3/", None), "sphinx": ("https://www.sphinx-doc.org/en/master/", None)}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"
html_static_path = ['./']
html_css_files = ['custom.css']

# -- Options for EPUB output
epub_show_urls = "footnote"

# -- Control the “hint” text that is displayed next to togglebuttons
togglebutton_hint = "Output format file"
togglebutton_hint_hide = "Output format file"
