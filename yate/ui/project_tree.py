import wx
import os
import glob

class ProjectTree(wx.TreeCtrl):
  def __init__(self, parent, project_path, size = None, show_hidden = False):
    wx.TreeCtrl.__init__(self, parent, size=size)
    self.project_path = os.path.realpath(project_path)
    self.show_hidden = False

    self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandItem)
    self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnCollapseItem)
    self.__collapsing = False
    root = self.AddRoot(os.path.basename(self.project_path.rstrip(os.sep)))
    self.SetPyData(root, self.project_path)
    self.SetItemHasChildren(root)

  def OnExpandItem(self, event):
    path = self.GetPyData(event.GetItem())

    if os.path.isdir(path):
      files = os.listdir(path)
      files.sort()

      for f in files:
        if not self.show_hidden and f.startswith('.'):
          continue

        child = self.AppendItem(event.GetItem(), f)
        self.SetPyData(child, os.path.join(path, f))
        self.SetItemHasChildren(child, os.path.isdir(os.path.join(path, f)))

  def OnCollapseItem(self, event):
    # Be prepared, self.CollapseAndReset below may cause
    # another wx.EVT_TREE_ITEM_COLLAPSING event being triggered.
    if self.__collapsing:
        event.Veto()
    else:
        self.__collapsing = True
        item = event.GetItem()
        self.CollapseAndReset(item)
        self.SetItemHasChildren(item)
        self.__collapsing = False

