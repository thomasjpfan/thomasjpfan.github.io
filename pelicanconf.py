#!/usr/local/bin python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import collections


AUTHOR = u'Thomas Fan'
SITENAME = u'thomasjpfan.com'
SITEURL = ''

TIMEZONE = u'EST'

DEFAULT_LANG = u'en'

DATE_FORMATS = {
    'en': ' %b %d, %Y',
}

OG_DESCRIPTION = ("This is my personal blog, where I share my"
                  "insights and what I have been learning.")
SUMMARY_MAX_LENGTH = 30

THEME = "theme/Final"
NOTEBOOK_DIR = 'notebooks'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['sitemap', 'tipue_search', 'feed_summary',
           'liquid_tags.youtube', 'liquid_tags.notebook',
           'minification', 'better_codeblock_line_numbering', 'assets',
           'render_katex', 'image_process', 'optimize_images']
FEED_USE_SUMMARY = True
# MD_EXTENSIONS = [
#     'codehilite(css_class=highlight, linenums=False)',
#     'extra'
# ]

IMAGE_PROCESS = {
    'major': ["scale_out 510 100 False"],
    'minor': ["scale_out 190 100 False"]
}

# IMAGE_PROCESS = {
#     'major': {
#         'type': 'responsive-image',
#         'srcset': [('1x', ["scale_out 510 100 False"]),
#                    ('2x', ["scale_out 1020 200 False"])],
#         'default': '1x'
#     },
#     'minor': ["scale_out 190 100 False"]
# }

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight',
                                           'linenums': False},
        'markdown.extensions.extra': {},
    },
    'output_format': 'html5',
}

ASSET_BUNDLES = (
    ('scss-main',
        ['scss/tfstyle.scss'],
     {'filters': 'compass,cssmin', 'output': 'css/style.min.css'}),
)

# MATH_JAX = {'responsive': True, 'linebreak_automatic': True,
#             'message_style': None, 'show_menu': False}

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.9,
        'indexes': 0.4,
        'pages': 0.6
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'monthly',
        'pages': 'monthly'
    },
    'exclude': ['topic/']
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

MARKUP = ('md',)

MENUITEMS = (('Rss', FEED_ALL_ATOM),)

# CATEGORY_URL = 'category/{slug}/'
# CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORY_URL = ''
CATEGORY_SAVE_AS = ''
AUTHOR_URL = ''
AUTHOR_SAVE_AS = ''

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_LANG_URL = '{date:%Y}/{date:%m}/{slug}-{lang}/'
PAGE_URL = 'pages/{slug}/'
PAGE_LANG_URL = 'pages/{slug}-{lang}/'
TAG_URL = 'topic/{slug}/'
TAGS_URL = 'topics/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'
ARTICLE_LANG_SAVE_AS = '{date:%Y}/{date:%m}/{slug}-{lang}/index.html'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}/index.html'
TAG_SAVE_AS = 'topic/{slug}/index.html'
TAGS_SAVE_AS = 'topics/index.html'

# YEAR_ARCHIVES_URL = 'archives/{date:%Y}/'
# YEAR_ARCHIVE_SAVE_AS = 'archives/{date:%Y}/index.html'
ARCHIVES_URL = 'archives/'
ARCHIVES_SAVE_AS = 'archives/index.html'

DEFAULT_CATEGORY = "Blog"

TEMPLATE_PAGES = {'search.html': 'search.html'}

DEFAULT_PAGINATION = 5

PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

STATIC_PATHS = ['images', 'extra/favicon_v4.ico',
                'extra/htaccess', 'extra/favicon_v4.png',
                'extra/favicon_v4_ios.png']

EXTRA_PATH_METADATA = {
    'extra/favicon_v4.ico': {'path': 'favicon_v4.ico'},
    'extra/htaccess': {'path': '.htaccess'},
    'extra/favicon_v4.png': {'path': 'favicon_v4.png'},
    'extra/favicon_v4_ios.png': {'path': 'favicon_v4_ios.png'}
}

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# JINJA FILTER


def unique(a):
    if isinstance(a, collections.Hashable):
        c = set(a)
    else:
        c = []
        for x in a:
            if x not in c:
                c.append(x)
    return c


def intersect(a, b):
    if isinstance(a, collections.Hashable) and isinstance(b, collections.Hashable):
        c = set(a) & set(b)
    else:
        c = unique(filter(lambda x: x in b, a))
    return c


JINJA_FILTERS = {'intersect': intersect}
