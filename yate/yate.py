#!/usr/bin/env python

import sys
import os
import wx
import wx.stc
import wx.aui
import fnmatch
import ngram

import syntax
import config
import json_theme_parser as theme
from project_tree import ProjectTree
from quick_open import QuickOpenDialog

faces = {
  'times': 'Times',
  'mono' : 'Courier New',
  'helv' : 'Helvetica',
  'other': 'new century schoolbook',
  'size' : 12,
  'size2': 10,
}

class Editor(wx.stc.StyledTextCtrl):
  def __init__(self, parent, filename = None):
    wx.stc.StyledTextCtrl.__init__(self, parent, wx.ID_ANY)

    self.filename = filename

    if filename != None:
      self.Open(filename)

  def GetSyntaxConfig(self):
    if self.filename != None:
      for language in syntax.config:
        cfg = syntax.config[language]
        for pattern in cfg['file_patterns']:
          if fnmatch.fnmatch(self.filename, pattern):
            return cfg

    return None

  def SetStyle(self):
    syntaxConfig = self.GetSyntaxConfig()

    theme.loadTheme(config.theme)

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

class Notebook(wx.aui.AuiNotebook):
  def __init__(self, parent):
    wx.aui.AuiNotebook.__init__(self, parent, style=wx.aui.AUI_NB_DEFAULT_STYLE | wx.aui.AUI_NB_WINDOWLIST_BUTTON)
    self.editors = {}

    self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnClosePage)

  def GetCurrentEditor(self):
    page = self.GetSelection()

    if page != wx.NOT_FOUND:
      return self.GetPage(page)

    return None

  def GoToLine(self, line):
    page = self.GetSelection()

    if page != wx.NOT_FOUND:
      editor = self.GetPage(page)
      if editor:
        editor.GotoLine(line)

  def edit(self, filename):
    filename = os.path.realpath(filename)
    if filename in self.editors:
      tab = self.editors[filename]
      for tab_id in range(self.GetPageCount()):
        if self.GetPage(tab_id) == tab:
          self.SetSelection(tab_id)
          break
    else:
      editor = Editor(self, filename)
      self.editors[filename] = editor
      self.Bind(wx.stc.EVT_STC_MODIFIED, self.onEditorModified, editor)
      self.AddPage(editor, os.path.basename(filename), True)

  def onEditorModified(self, event):
    editor = event.GetEventObject()

    if editor and editor.GetModify():
      page = self.find(editor)
      if page != wx.NOT_FOUND:
        self.SetPageText(page, os.path.basename(editor.filename) + " *")

  def OnClosePage(self, event):
    page = self.GetSelection()
    self.close(page)
    event.Veto()

  def find(self, tab):
    for tab_id in range(self.GetPageCount()):
      if self.GetPage(tab_id) == tab:
        return tab_id

    return wx.NOT_FOUND

  def close(self, page = None):
    if not page:
      page = self.GetSelection()

    if page != wx.NOT_FOUND:
      editor = self.GetPage(page)
      if editor:
        if editor.GetModify():
          dialog = wx.MessageDialog(self,
              "Save changes before closing?",
              "Confirm Exit", wx.YES_NO|wx.CANCEL|wx.ICON_ERROR)
          result = dialog.ShowModal()
          dialog.Destroy()

          if result == wx.ID_YES or result == wx.ID_NO:
            if result == wx.ID_YES:
              editor.Save()
            del self.editors[os.path.realpath(editor.filename)]
            self.DeletePage(page)
        else:
          del self.editors[os.path.realpath(editor.filename)]
          self.DeletePage(page)

  def save(self):
    page = self.GetSelection()
    if page != wx.NOT_FOUND:
      editor = self.GetPage(page)
      if editor:
        if editor.GetModify():
          editor.Save()
          self.SetPageText(page, os.path.basename(editor.filename))


class MainFrame(wx.Frame):
  def __init__(self, parent, title, size, project):
    wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=size)

    self.files = []

    panel = wx.Panel(self)
    vbox = wx.BoxSizer(wx.HORIZONTAL)

    panel.SetSizer(vbox)

    self.notebook = Notebook(panel)

    if project:
      self.project = project
      self.project_tree = ProjectTree(panel, project, (200, 200))
      self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnProjectTreeClick, self.project_tree)
      vbox.Add(self.project_tree, 0, wx.EXPAND)

    vbox.Add(self.notebook, 1, wx.EXPAND)

    self.Bind(wx.EVT_CLOSE, self.OnClose)

    menuBar = wx.MenuBar()
    menu = wx.Menu()
    m_new = menu.Append(wx.ID_NEW, "New\tCtrl-N", "New tab.")
    self.Bind(wx.EVT_MENU, self.OnNewTab, m_new)
    m_open = menu.Append(wx.ID_OPEN, "Open\tCtrl-O", "Open file.")
    self.Bind(wx.EVT_MENU, self.OnOpenTab, m_open)
    m_close = menu.Append(wx.ID_CLOSE, "Close\tCtrl-W", "Close tab.")
    self.Bind(wx.EVT_MENU, self.OnCloseTab, m_close)
    m_save = menu.Append(wx.ID_SAVE, "&Save\tCtrl-S", "Save tab.")
    self.Bind(wx.EVT_MENU, self.OnSaveTab, m_save)
    m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
    self.Bind(wx.EVT_MENU, self.OnClose, m_exit)

    menuBar.Append(menu, "&File")

    menu = wx.Menu()
    m_quick_open = menu.Append(wx.NewId(), "Go To File\tCtrl-T", "Go to file.")
    self.Bind(wx.EVT_MENU, self.OnQuickOpenTab, m_quick_open)
    m_go_to = menu.Append(wx.NewId(), "Go To Line\tCtrl-L", "Go to line.")
    self.Bind(wx.EVT_MENU, self.OnGoToLine, m_go_to)
    m_next = menu.Append(wx.NewId(), "Next Tab\tCtrl-PAGEDOWN", "Next tab.")
    self.Bind(wx.EVT_MENU, self.onNextTab, m_next)
    m_prev = menu.Append(wx.NewId(), "Prev Tab\tCtrl-PAGEUP", "Prev tab.")
    self.Bind(wx.EVT_MENU, self.onPrevTab, m_prev)

    menuBar.Append(menu, "&Navigation")

    self.SetMenuBar(menuBar)

  def PrepareQuickOpen(self):
    self.files.sort()
    self.G = ngram.NGram(self.files)

  def OnGoToLine(self, event):
    editor = self.notebook.GetCurrentEditor()

    if editor:
      count = editor.GetLineCount()
      current = editor.GetCurrentLine()
      dlg = wx.NumberEntryDialog(self, 'Line Number', 'Go To Line', '', current, 1, count)

      if dlg.ShowModal() == wx.ID_OK:
        self.notebook.GoToLine(dlg.GetValue())
      dlg.Destroy()

  def onNextTab(self, event):
    self.notebook.AdvanceSelection()

  def onPrevTab(self, event):
    self.notebook.AdvanceSelection(False)

  def OnCloseTab(self, event):
    self.notebook.close()

  def OnSaveTab(self, event):
    self.notebook.save()

  def OnNewTab(self, event):
    # FIXME: needs work, it crashes
    self.notebook.AddPage(Editor(self.notebook), 'Untitled 1', True)

  def OnOpenTab(self, event):
    dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
      path = dlg.GetPath()
      if os.path.isfile(path):
        self.notebook.edit(path)
    dlg.Destroy()

  def OnQuickOpenTab(self, event):
    dialog = QuickOpenDialog(None, self.files, self.G)
    result = dialog.ShowModal()

    if result == wx.ID_OK:
      filename = dialog.fileToOpen

      if filename:
        self.notebook.edit(os.path.join(self.project, filename))

    dialog.Destroy()

  def OnProjectTreeClick(self, event):
    newFile = self.project_tree.GetPyData(event.GetItem())

    if os.path.isfile(newFile):
      self.notebook.edit(newFile)

  def OnClose(self, event):
    if len(self.notebook.editors) == 0:
      self.Destroy()
    else:
      for filename in self.notebook.editors:
        editor = self.notebook.editors[filename]
        if (editor.GetModify()):
          dialog = wx.MessageDialog(self,
              "Save changes before closing?",
              "Confirm Exit", wx.YES_NO|wx.CANCEL|wx.ICON_ERROR)
          result = dialog.ShowModal()
          dialog.Destroy()

          if result == wx.ID_YES or result == wx.ID_NO:
            if result == wx.ID_YES:
              editor.Save()
            self.Destroy()
        else:
          self.Destroy()

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

