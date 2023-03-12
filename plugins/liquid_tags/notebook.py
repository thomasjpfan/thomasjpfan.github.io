"""
Notebook Tag
------------
This is a liquid-style tag to include a static html rendering of an IPython
notebook in a blog post.

Syntax
------
{% notebook filename.ipynb [ cells[start:end] language[language] ]%}

The file should be specified relative to the ``notebooks`` subdirectory of the
content directory.  Optionally, this subdirectory can be specified in the
config file:

    NOTEBOOK_DIR = 'notebooks'

The cells[start:end] statement is optional, and can be used to specify which
block of cells from the notebook to include.

The language statement is obvious and can be used to specify whether ipython2
or ipython3 syntax highlighting should be used.

Requirements
------------
- The plugin requires IPython version 1.0 or above.  It no longer supports the
  standalone nbconvert package, which has been deprecated.

Details
-------
Because the notebook relies on some rather extensive custom CSS, the use of
this plugin requires additional CSS to be inserted into the blog theme.
After typing "make html" when using the notebook tag, a file called
``_nb_header.html`` will be produced in the main directory.  The content
of the file should be included in the header of the theme.  An easy way
to accomplish this is to add the following lines within the header template
of the theme you use:

    {% if EXTRA_HEADER %}
      {{ EXTRA_HEADER }}
    {% endif %}

and in your ``pelicanconf.py`` file, include the line:

    EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

this will insert the appropriate CSS.  All efforts have been made to ensure
that this CSS will not override formats within the blog theme, but there may
still be some conflicts.
"""
import warnings
import re
import os
from functools import partial
from io import open

from .mdx_liquid_tags import LiquidTags

import IPython

IPYTHON_VERSION = IPython.version_info[0]

try:
    import nbformat
except:
    pass


try:
    from nbconvert.filters.highlight import _pygments_highlight
except ImportError:
    try:
        from IPython.nbconvert.filters.highlight import _pygments_highlight
    except ImportError:
        # IPython < 2.0
        from IPython.nbconvert.filters.highlight import (
            _pygment_highlight as _pygments_highlight,
        )

from pygments.formatters import HtmlFormatter

try:
    from nbconvert.exporters import HTMLExporter
except ImportError:
    from IPython.nbconvert.exporters import HTMLExporter

try:
    from traitlets.config import Config
except ImportError:
    from IPython.config import Config

try:
    from nbconvert.preprocessors import Preprocessor
except ImportError:
    try:
        from IPython.nbconvert.preprocessors import Preprocessor
    except ImportError:
        # IPython < 2.0
        from IPython.nbconvert.transformers import Transformer as Preprocessor

try:
    from traitlets import Integer
except ImportError:
    from IPython.utils.traitlets import Integer

from copy import deepcopy


# ----------------------------------------------------------------------
# Create a custom preprocessor
class SliceIndex(Integer):
    """An integer trait that accepts None"""

    default_value = None

    def validate(self, obj, value):
        if value is None:
            return value
        else:
            return super(SliceIndex, self).validate(obj, value)


class SubCell(Preprocessor):
    """A transformer to select a slice of the cells of a notebook"""

    start = SliceIndex(0, config=True, help="first cell of notebook to be converted")
    end = SliceIndex(None, config=True, help="last cell of notebook to be converted")

    def preprocess(self, nb, resources):
        nbc = deepcopy(nb)
        if IPYTHON_VERSION < 3:
            for worksheet in nbc.worksheets:
                cells = worksheet.cells[:]
                worksheet.cells = cells[self.start : self.end]
        else:
            nbc.cells = nbc.cells[self.start : self.end]

        return nbc, resources

    call = preprocess  # IPython < 2.0


# ----------------------------------------------------------------------
# Custom highlighter:
#  instead of using class='highlight', use class='highlight-ipynb'
def custom_highlighter(source, language="ipython", metadata=None):
    formatter = HtmlFormatter(cssclass="highlight-ipynb")
    if not language:
        language = "ipython"
    output = _pygments_highlight(source, formatter, language)
    return output.replace("<pre>", '<pre class="ipynb">')


# ----------------------------------------------------------------------
# Below is the pelican plugin code.
#
SYNTAX = (
    "{% notebook /path/to/notebook.ipynb [ cells[start:end] ] [ language[language] ] %}"
)
FORMAT = re.compile(
    r"""^(\s+)?(?P<src>\S+)(\s+)?((cells\[)(?P<start>-?[0-9]*):(?P<end>-?[0-9]*)(\]))?(\s+)?((language\[)(?P<language>-?[a-z0-9\+\-]*)(\]))?(\s+)?$"""
)


@LiquidTags.register("notebook")
def notebook(preprocessor, tag, markup):
    match = FORMAT.search(markup)
    if match:
        argdict = match.groupdict()
        src = argdict["src"]
        start = argdict["start"]
        end = argdict["end"]
        language = argdict["language"]
    else:
        raise ValueError(
            "Error processing input, " "expected syntax: {0}".format(SYNTAX)
        )

    if start:
        start = int(start)
    else:
        start = 0

    if end:
        end = int(end)
    else:
        end = None

    language_applied_highlighter = partial(custom_highlighter, language=language)

    nb_dir = preprocessor.configs.getConfig("NOTEBOOK_DIR")
    nb_path = os.path.join("content", nb_dir, src)

    if not os.path.exists(nb_path):
        raise ValueError("File {0} could not be found".format(nb_path))

    # Create the custom notebook converter
    c = Config(
        {
            "CSSHTMLHeaderTransformer": {
                "enabled": True,
                "highlight_class": ".highlight-ipynb",
            },
            "SubCell": {"enabled": True, "start": start, "end": end},
        }
    )

    subcell_kwarg = dict(preprocessors=[SubCell])

    from pathlib import Path

    template_path = Path.cwd() / "pelicanhtml_3.tpl"

    exporter = HTMLExporter(
        config=c,
        template_file=str(template_path),
        filters={"highlight2html": language_applied_highlighter},
        **subcell_kwarg
    )

    # read and parse the notebook
    with open(nb_path, encoding="utf-8") as f:
        nb_text = f.read()
        if IPYTHON_VERSION < 3:
            nb_json = IPython.nbformat.current.reads_json(nb_text)
        else:
            try:
                nb_json = nbformat.reads(nb_text, as_version=4)
            except:
                nb_json = IPython.nbformat.reads(nb_text, as_version=4)

    (body, resources) = exporter.from_notebook_node(nb_json)

    # this will stash special characters so that they won't be transformed
    # by subsequent processes.
    body = preprocessor.configs.htmlStash.store(body)
    return body


# ----------------------------------------------------------------------
# This import allows notebook to be a Pelican plugin
from liquid_tags import register
