#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mimetypes
import alfred
import sqlite3
import os
import sys
import plistlib

HOME = os.path.expanduser('~')
DB_DIR = HOME + '/Library/Application Support/Alfred/Databases'
IMAGES_DIR = DB_DIR + '/clipboard.alfdb.data'
DB_PATH = DB_DIR + '/clipboard.alfdb'

WORKFLOW_DIR = sys.path[0]

CLIPBOARD_IMAGE_QUERY = u'''
    SELECT ts, app, item, dataHash, dataType
    FROM clipboard
    WHERE (dataType == 1 AND item LIKE "Image:%") OR (dataType == 2 AND item LIKE "File:%")
    ORDER BY ts DESC
'''

def get_image_path(plist_path):
  pl = plistlib.readPlist(plist_path)
  img_path = pl[0]
  mimetype = mimetypes.guess_type(img_path)[0]
  return img_path if mimetype is not None and mimetype.startswith("image/") else None

def image_results(db):
  for row in db.execute(CLIPBOARD_IMAGE_QUERY):
    (ts, app_name, title, filename, dataType) = row
    file_path = IMAGES_DIR + '/' + filename
    if dataType == 1:
      yield alfred.Item({u'arg': file_path, u'autocomplete': title, u'type': 'file:skipcheck'}, title, app_name or str(ts), file_path)
    elif dataType == 2:
      image_path = get_image_path(file_path)
      if image_path is not None:
        yield alfred.Item({u'arg': image_path, u'autocomplete': title, u'type': 'file'}, title, app_name or str(ts), image_path)

db = sqlite3.connect(DB_PATH)

alfred.write(alfred.xml(image_results(db)))
