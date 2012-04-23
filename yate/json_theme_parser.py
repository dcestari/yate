import sys
import os
import json
from style import Style

default = {}
styles  = {}

def loadTheme(filename):
  global default
  global styles

  prefix = os.path.dirname(__file__)
  if (hasattr(sys, 'frozen') and sys.frozen == 'macosx_app'):
    prefix = os.environ['RESOURCEPATH']

  theme = json.load(open(os.path.join(prefix, filename)))
  default = theme['defaults']

  for name in theme['styles']:
    style = theme['styles'][name]

    fore = None
    back = None
    fontStyle = None

    if "foreground" in style:
      fore = style["foreground"]

    if "background" in style:
      back = style["background"]

    if "fontStyle" in style:
      fontStyle = style["fontStyle"]

    styles[name] = Style(name, fore, back, fontStyle)

