import wx

config = {
  'php' : {
    'lexer'    : wx.stc.STC_LEX_HTML,
    'file_patterns' : ['*.php'],
    'style_bits' : 7,
    'keywords'   : "class function public protected private require_once dirname error_reporting ini_set include echo true false __FILE__ __DIR__ __CLASS__ chdir die static in_array array switch case if list foreach for while",
    'keyword_index' : 4,
    'styles'   : {
      'default'  : [wx.stc.STC_H_DEFAULT, wx.stc.STC_HPHP_DEFAULT],
      'comment'  : [wx.stc.STC_H_COMMENT, wx.stc.STC_HPHP_COMMENT, wx.stc.STC_HPHP_COMMENTLINE],
      'keyword'  : [wx.stc.STC_HPHP_WORD],
      'variable' : [wx.stc.STC_HPHP_VARIABLE],
      'string'   : [wx.stc.STC_HPHP_HSTRING, wx.stc.STC_HPHP_SIMPLESTRING],
      'string.variable' : [wx.stc.STC_HPHP_HSTRING_VARIABLE],
      'tag'      : [wx.stc.STC_H_TAG],
      'attribute': [wx.stc.STC_H_ATTRIBUTE],
      'xmlstart' : [wx.stc.STC_H_XMLSTART],
      'constant' : [wx.stc.STC_HPHP_NUMBER],
    },
  },
}

