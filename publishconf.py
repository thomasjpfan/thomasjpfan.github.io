#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://thomasjpfan.com'
RELATIVE_URLS = False
SHORTSITEURL = "thomasjpfan.com"

FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'

DELETE_OUTPUT_DIRECTORY = True

MENUITEMS = (('Rss', FEED_ALL_ATOM),)

# Following items are often useful when publishing
PLUGINS = ['sitemap', 'tipue_search', 'feed_summary',
           'liquid_tags.youtube', 'liquid_tags.notebook',
           'minification', 'better_codeblock_line_numbering', 'assets',
           'render_katex', 'optimize_images']

# DISQUS_SITENAME = "thomasjpfan"
GOOGLE_ANALYTICS = "UA-46065142-1"
