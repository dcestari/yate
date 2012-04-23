import os
import wx
import wx.stc
import wx.aui

from yate.ui.editor import Editor

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
