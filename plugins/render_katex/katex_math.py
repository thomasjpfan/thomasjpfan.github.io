"""
Katex Render Plugin for Pelican
Literally no settings
"""
import os
import sys

from pelican import signals, generators
from bs4 import BeautifulSoup

from .pelican_katex_markdown_extension import PelicanKatexExtension


def process_settings(pelicanobj):
    """Sets user specified Katex settings"""

    katex_settings = {}

    katex_settings['auto_insert'] = True
    katex_settings['process_summary'] = True

    return katex_settings


def process_summary(article):
    """Ensures summaries are not cut off. Also inserts
    katex script so that math will be rendered"""

    summary = article.summary
    summary_parsed = BeautifulSoup(summary, 'html.parser')
    math = summary_parsed.find_all(class_='math')

    if len(math) > 0:
        last_math_text = math[-1].get_text()
        if len(last_math_text) > 3 and last_math_text[-3:] == '...':
            content_parsed = BeautifulSoup(
                article.content,
                'html.parser'
            )
            full_text = content_parsed.find_all(
                class_='math'
            )[len(math) - 1].get_text()
            math[-1].string = "%s ..." % full_text
            summary = summary_parsed.decode()

        article.summary = "%s<script type='text/javascript'>%s</script>" % (
            summary, process_summary.katex_script)


def process_katex_script(katex_settings):
    """Load the katex script template from file and render
    with settings"""

    with open(os.path.dirname(os.path.realpath(__file__))
              + '/katex_script_template', 'r') as script_template:
        return script_template.read()


def configure_typogrify(pelicanobj, katex_settings):
    """Instructs Typogrify to ignore math tags - which allows Typogrify
    to play nicely with math related content"""

    # If Typogrify is not being used, then just exit
    if not pelicanobj.settings.get('TYPOGRIFY', False):
        return

    try:
        import typogrify
        from distutils.version import LooseVersion

        if LooseVersion(typogrify.__version__) < LooseVersion('2.0.7'):
            raise TypeError('Incorrect version of Typogrify')

        from typogrify.filters import typogrify

        # At this point, we are happy to use Typogrify, meaning
        # it is installed and it is a recent enough version
        # that can be used to ignore all math
        # Instantiate markdown extension and append it to the current extensions
        pelicanobj.settings['TYPOGRIFY_IGNORE_TAGS'].extend(
            ['.math', 'script'])  # ignore math class and script

    except (ImportError, TypeError) as e:
        pelicanobj.settings['TYPOGRIFY'] = False  # disable Typogrify

        if isinstance(e, ImportError):
            print("\nTypogrify is not installed, so it is being ignored.\nIf you want to use it, please install via: pip install typogrify\n")

        if isinstance(e, TypeError):
            print("\nA more recent version of Typogrify is needed for the render_katex module.\nPlease upgrade Typogrify to the latest version (anything equal or above version 2.0.7 is okay).\nTypogrify will be turned off due to this reason.\n")


def katex_for_markdown(pelicanobj, katex_script, katex_settings):
    """Instantiates a customized markdown extension for handling
    katx related content"""

    config = {}
    config['katex_script'] = katex_script
    config['math_tag_class'] = 'math'
    config['auto_insert'] = katex_settings['auto_insert']

    try:
        if isinstance(pelicanobj.settings.get('MD_EXTENSIONS'), list):  # pelican 3.6.3 and earlier
            pelicanobj.settings['MD_EXTENSIONS'].append(PelicanKatexExtension(config))
        else:
            pelicanobj.settings['MARKDOWN'].setdefault(
                'extensions', []).append(PelicanKatexExtension(config))
    except:
        sys.excepthook(*sys.exc_info())
        sys.stderr.write(
            "\nError - the pelican katex markdown extension failed to configure. katex is non-functional.\n")
        sys.stderr.flush()


def rst_add_katex(content):
    """Adds katex script for reStructuredText"""

    # .rst is the only valid extension for reStructuredText files
    _, ext = os.path.splitext(os.path.basename(content.source_path))
    if ext != '.rst':
        return

    # If math class is present in text, add the javascript
    # note that RST hardwires mathjax to be class "math"
    if 'class="math"' in content.content:
        content.content += "<script type='text/javascript'>%s</script>" % rst_add_katex.katex_script


def mathjax_for_rst(pelicanobj, katex_script):
    """Setup math for RST"""
    docutils_settings = pelicanobj.settings.get('DOCUTILS_SETTINGS', {})
    docutils_settings['math_output'] = 'Katex'
    pelicanobj.settings['DOCUTILS_SETTINGS'] = docutils_settings
    rst_add_katex.katex_script = katex_script


def pelican_init(pelicanobj):
    """
    Loads the katex script. Instantiate the Python markdown
    extension, passing in the katex sript as config parameter
    """

    katex_settings = process_settings(pelicanobj)

    katex_script = process_katex_script(katex_settings)

    # Configure Typogrify
    configure_typogrify(pelicanobj, katex_settings)

    katex_for_markdown(pelicanobj, katex_script,
                       katex_settings)

    process_summary.katex_script = None
    if katex_settings['process_summary']:
        process_summary.katex_script = katex_script


def process_rst_and_summaries(content_generators):
    for generator in content_generators:
        if isinstance(generator, generators.ArticlesGenerator):
            for article in (
                generator.articles +
                generator.translations +
                generator.drafts
            ):
                rst_add_katex(article)
                if process_summary.katex_script is not None:
                    process_summary(article)
        elif isinstance(generator, generators.PagesGenerator):
            for page in generator.pages:
                rst_add_katex(page)


def register():
    """Plugin registration"""
    signals.initialized.connect(pelican_init)
    signals.all_generators_finalized.connect(process_rst_and_summaries)
