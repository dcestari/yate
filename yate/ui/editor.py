import wx
import wx.stc
import fnmatch

import yate.syntax
import yate.config
import yate.json_theme_parser as theme
from yate.c_indent import CIndent

class Editor(wx.stc.StyledTextCtrl):
  def __init__(self, parent, filename = None):
    wx.stc.StyledTextCtrl.__init__(self, parent, wx.ID_ANY)

    self.filename = filename

    if filename != None:
      self.Open(filename)

    self.Bind(wx.stc.EVT_STC_CHARADDED, self.OnCharAdded)

  def OnCharAdded(self, event):
    if self.indenter != None:
      self.indenter.AutoIndent(event.GetKey())

    event.Skip()

  def GetSyntaxConfig(self):
    if self.filename != None:
      for language in yate.syntax.config:
        cfg = yate.syntax.config[language]
        for pattern in cfg['file_patterns']:
          if fnmatch.fnmatch(self.filename, pattern):
            return cfg

    return None

  def SetStyle(self):
    syntaxConfig = self.GetSyntaxConfig()

    theme.loadTheme(yate.config.theme)

    self.StyleSetBackground(style=wx.stc.STC_STYLE_DEFAULT, back=theme.default["background"])
    self.StyleSetForeground(style=wx.stc.STC_STYLE_DEFAULT, fore=theme.default["foreground"])
    self.SetCaretForeground(fore=theme.default["caret"])

    # selection
    self.SetSelBackground(True, theme.default["selection"])

    # line
    self.SetCaretLineBack(theme.default["lineHighlight"][:7])

    if len(theme.default["lineHighlight"]) > 7:
      self.SetCaretLineBackAlpha(int(theme.default["lineHighlight"][7:]))

    self.SetCaretLineVisible(True)

    # reset all to be like the default
    self.StyleClearAll()

    if syntaxConfig:
      self.SetLexer(syntaxConfig['lexer'])
      self.SetStyleBits(syntaxConfig['style_bits'])
      self.SetKeyWords(syntaxConfig['keyword_index'], syntaxConfig['keywords'])

      self.indenter = None
      if 'indent_style' in syntaxConfig:
        if syntaxConfig['indent_style'] == 'cindent':
          self.indenter = CIndent(self)

      styles = syntaxConfig['styles']

      for style in styles:
        if style in theme.styles:
          for styleType in styles[style]:
            self.StyleSetSpec(styleType, theme.styles[style].GetStyleString())

  def Save(self):
    self.SaveFile(self.filename)

  def Open(self, filename):
    self.LoadFile(filename)
    self.SetStyle()
