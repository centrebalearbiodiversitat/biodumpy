# Configuration file for the Sphinx documentation builder.

# -- Project location

import os
import sys

# Add the root directory of your project to the Python path
sys.path.insert(0, os.path.abspath("../../"))

from biodumpy.version import __version__ as version

# -- Project information

project = "biodumpy"
copyright = "2024, CBB Data Team"
author = "Cancellario, T.; Golomb, T.; Roldán, A.; Far, A."


# -- General configuration

extensions = [
	"sphinx.ext.duration",
	"sphinx.ext.doctest",
	"sphinx.ext.autodoc",
	"sphinx.ext.autosummary",
	"sphinx.ext.intersphinx",
]

intersphinx_mapping = {
	"python": ("https://docs.python.org/3/", None),
	"sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"
