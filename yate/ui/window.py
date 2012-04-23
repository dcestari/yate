import os
import wx
import ngram

from yate.ui.project_tree import ProjectTree
from yate.ui.quick_open import QuickOpenDialog
from yate.ui.editor import Editor
from yate.ui.notebook import Notebook

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

