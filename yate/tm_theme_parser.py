import plistlib
import pprint
import re

from style import Style

names = {
  'comment'  : 'comment',
  'keyword'  : 'keyword',
  'meta.tag' : 'tag',
  'entity.name.tag' : 'tag',
  'entity.other.attribute-name' : 'attribute',
  'string'   : 'string',
  'entity.name' : 'variable',
  'variable'    : 'variable',
  'entity'    : 'variable',
  'meta.tag.preprocessor.xml' : 'xmlstart',
  'text' : 'default',
  'constant' : 'constant',
  'string variable' : 'string.variable',
}

default = {}
styles = {}

def loadTheme(path):
  global default
  dom = plistlib.readPlist(open(path))
  default = dom["settings"][0]["settings"]

  i=1
  while i < len(dom["settings"]):
    setting = dom["settings"][i]
    i += 1

    if not "scope" in setting:
      continue

    scopes = setting["scope"]

    for scope in scopes.split(","):
      m = re.search('^([\w\.]+)( -[^ ]+)+$', scope)
      if m:
        scope = m.group(1)

      name = scope.strip().lower()
      if name in names:
        name = names[name]
        fore = None
        back = None
        fontStyle = None

        if "foreground" in setting["settings"]:
          fore = setting["settings"]["foreground"]

        if "background" in setting["settings"]:
          back = setting["settings"]["background"]

        if "fontStyle" in setting["settings"]:
          fontStyle = setting["settings"]["fontStyle"]

        styles[name] = Style(name, fore, back, fontStyle)

if __name__ == "__main__":
  import sys
  loadTheme(sys.argv[1])
  pprint.pprint(default)
  pprint.pprint(styles)

