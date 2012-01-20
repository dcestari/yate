import wx
import difflib
import ngram

class QuickOpenDialog(wx.Dialog):
  def __init__(self, parent, files, G):
    wx.Dialog.__init__(self, parent, wx.ID_ANY, 'Quick Open')
    panel = wx.Panel(self)
    vbox = wx.BoxSizer(wx.VERTICAL)
    panel.SetSizer(vbox)
    self.filename = wx.TextCtrl(panel)
    self.fileList = wx.ListBox(panel)
    
    self.files = files

    if not G:
      self.G = ngram.NGram(self.files)
    else:
      self.G = G

    self.fileList.SetItems(self.files[:20])
    
    self.Bind(wx.EVT_TEXT, self.OnChange, self.filename)
    self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelect, self.fileList)
    self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyDown)

    vbox.Add(self.filename, 0, wx.EXPAND)
    vbox.Add(self.fileList, 1, wx.EXPAND)

    self.filename.SetFocus()

    self.fileToOpen = None

  def OnSelect(self, event):
    self.OpenSelected()

  def OpenSelected(self):
    self.fileToOpen = self.fileList.GetStringSelection()
    self.EndModal(wx.ID_OK)

  def OnChange(self, event):
    value = self.filename.GetValue()

    if len(value) == 0:
      self.fileList.SetItems(self.files)
    else:
      files = self.G.search(value)
      self.fileList.SetItems([f[0] for f in files[:20]])

      if len(files) > 0:
        self.fileList.SetSelection(0)

  def OnKeyDown(self, event):
    keycode = event.GetKeyCode()

    if keycode == wx.WXK_ESCAPE:
      self.EndModal(wx.ID_OK)
    elif keycode == wx.WXK_RETURN:
      self.OpenSelected()
    elif keycode == wx.WXK_DOWN and wx.Window.FindFocus() == self.filename:
      self.fileList.SetFocus()
    elif keycode == wx.WXK_UP and wx.Window.FindFocus() == self.fileList and self.fileList.GetSelection() == 0:
      self.filename.SetFocus()
    else:
      event.Skip()

