#!/usr/bin/env python

import sys
import os

# fix sys.path for Mac OS X App Bundle
if (hasattr(sys, 'frozen') and sys.frozen == 'macosx_app'):
  prefix = os.environ['RESOURCEPATH']
  path = os.path.join(prefix, 'lib', 'python' + sys.version[:3], 'lib-dynload')

  sys.path.reverse()
  sys.path.append(path)
  sys.path.reverse()

import wx
import ngram
from ui.window import MainFrame

def main():
  filename = None
  project = None

  if len(sys.argv) > 1:
    if os.path.isfile(sys.argv[1]):
      filename = os.path.realpath(sys.argv[1])
    if os.path.isdir(sys.argv[1]):
      project = os.path.realpath(sys.argv[1])

  app = wx.App(0)
  frame = MainFrame(None, 'Edit', (800, 500), project=project)

  if project:
    for root, dirs, files in os.walk(project):
      dirs[:] = [d for d in dirs if not d.startswith(".")]

      for name in files:
        if not name.startswith("."):
          fullpath = os.path.join(root, name)
          frame.files.append(os.path.relpath(fullpath, project))

    frame.PrepareQuickOpen()

  frame.CenterOnScreen()

  if filename:
    frame.notebook.edit(filename)

  frame.Show()

  app.MainLoop()

if __name__ == '__main__':
  main()

