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
from xml.etree import ElementTree as ET

XML = os.path.expanduser('~/Desktop/standard_ebooks.xml')
JSON = os.path.join(os.path.dirname(__file__), 'books.json')

tree = ET.parse(XML)
root = tree.getroot()

items = []

for entry in root:
    if entry.tag != 'entry':
        continue

    title = entry.find('title').text
    url = entry.find('id').text
    author = entry.find('author').find('name').text
    it = dict(title=title, subtitle=author, arg=url)
    print(it)
    items.append(it)

with open(JSON, 'wb') as fp:
    json.dump(dict(items=items), fp, indent=2)
