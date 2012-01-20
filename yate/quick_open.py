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

    vbox.Add(self.filename, 0, wx.EXPAND)
    vbox.Add(self.fileList, 1, wx.EXPAND)

    self.filename.SetFocus()

    self.fileToOpen = None

  def OnSelect(self, event):
    self.fileToOpen = self.fileList.GetStringSelection()
    self.EndModal(wx.ID_OK)

  def OnChange(self, event):
    value = self.filename.GetValue()

    if len(value) == 0:
      self.fileList.SetItems(self.files)
    else:
      files = self.G.search(value)
      self.fileList.SetItems([f[0] for f in files])
#      files = []
#      i = 0
#      for f in self.files:
#        if i > 20:
#          break
#        
#        if f.startswith(value):
#          files.append(f)
#
#      self.fileList.SetItems(files)#[f for f in self.files if f.startswith(value)])
#difflib.get_close_matches(value, self.files))

if __name__ == '__main__':
  app = wx.App(0)
  dialog = QuickOpenDialog(None, files=['hola', 'chao', 'hasta luego'])
  dialog.ShowModal()
  dialog.Destroy()
  app.MainLoop()

