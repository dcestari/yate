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
  'ruby' : {
    'lexer' : wx.stc.STC_LEX_RUBY,
    'file_patterns' : ['*.rb'],
    'style_bits' : 5,
    'keywords'  : 'def class module require if end self true false nil ' +
      # ActiveRecord
      'belongs_to has_many validates_presence_of validates_length_of',
    'keyword_index' : 0,
    'styles'   : {
      'default'  : [wx.stc.STC_RB_DEFAULT],
      'comment'  : [wx.stc.STC_RB_COMMENTLINE],
      'keyword'  : [wx.stc.STC_RB_WORD],
      'variable' : [wx.stc.STC_RB_INSTANCE_VAR, wx.stc.STC_RB_CLASS_VAR],
      'string'   : [wx.stc.STC_RB_STRING, wx.stc.STC_RB_CHARACTER, wx.stc.STC_RB_STRING_Q, wx.stc.STC_RB_STRING_QQ, wx.stc.STC_RB_STRING_QX, wx.stc.STC_RB_STRING_QR, wx.stc.STC_RB_STRING_QW],
      'constant' : [wx.stc.STC_RB_SYMBOL, wx.stc.STC_RB_NUMBER],
    },
  },
}

