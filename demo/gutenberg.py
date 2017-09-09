#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2017 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2017-09-09
#

"""
"""

from __future__ import print_function, absolute_import

import json
import os

from bs4 import BeautifulSoup as BS

HTML = os.path.expanduser('~/Desktop/french.html')
JSON = os.path.join(os.path.dirname(__file__), 'french_books.json')
# HTML = os.path.expanduser('~/Desktop/german.html')
# JSON = os.path.join(os.path.dirname(__file__), 'german_books.json')


items = []

soup = BS(open(HTML), 'html.parser')
for tag in soup.find_all('li', 'pgdbetext'):
    book = tag.a
    title = book.get_text()
    url = 'http://www.gutenberg.org' + book['href']
    it = dict(title=title, subtitle=url, arg=url, uid=url)
    items.append(it)

print('%d books' % len(items))

with open(JSON, 'wb') as fp:
    json.dump(dict(items=items), fp, indent=2)
