#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import requests

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def parse_sorting_path(path):
  """Returns the section of the given path that should be used in sorting.
  Given the path "https://code.google.com/.../bar-abab-baaa.jpg" only the second
  word should be used to sort the path if it exists, i.e., "baaa.jpg".
  Otherwise the entire path should be used for sorting."
  """
  match = re.search(r'puzzle/\w-(\w+)-(\w+).jpg' , path)
  if match:
    return match.group(2)
  else:
    return path

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  file = open(filename, 'r')
  raw_paths = set(re.findall(
      r'GET (\S+puzzle\S+) HTTP',
      file.read()
  ))

  return sorted(['https://code.google.com' + path for path in raw_paths],
                key=parse_sorting_path)



def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  if not os.path.isdir(dest_dir):
    os.mkdir(dest_dir)

  html_start = "<verbatim>\n  <html>\n    <body>\n"
  html_imgs = ["      "]
  html_end = "\n    </body>\n  </html>\n</verbatim>\n"

  for idx, img_url in enumerate(img_urls):
    img_name = f"img{idx}"
    print(f'Retreiving {img_name} from {img_url}...')
    img_res = requests.get(img_url).content
    img_path = f'{dest_dir}/{img_name}'

    with open(img_path, 'wb') as handler:
      handler.write(img_res)

    html_imgs.append(f'<img src="{img_name}">')

  index_path = f'{dest_dir}/index.html'
  html_f = open(index_path, 'w')
  print(f"Creating {index_path}...")
  html_f.write(html_start + ''.join(html_imgs) + html_end)


def main():
  args = sys.argv[1:]

  if not args:
    print('usage: [--todir dir] logfile ')
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print('\n'.join(img_urls))

if __name__ == '__main__':
  main()
