import os
import json
from style import Style

default = {}
styles  = {}

def loadTheme(filename):
  global default
  global styles

  theme = json.load(open(os.path.join(os.path.dirname(__file__), filename)))
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

