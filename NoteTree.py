#!/usr/bin/env python
import sys, os
import wx
import pickle

def MsgBox (window, string, title):
     dlg=wx.MessageDialog(window, string, title, wx.OK)
     dlg.ShowModal()
     dlg.Destroy()

class main_window(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = (800, 500),
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        mainwindow = self
        self.sb = self.CreateStatusBar()

        self.mainmenu = wx.MenuBar()
        menu = wx.Menu()
        id = wx.NewId()
        menu.Append(id, '&ReRead', 'Reread .ini file')
        self.Connect(id, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.reread)
        id = wx.NewId()
        menu.Append(id, '&Save', 'Save .ini file')
        self.Connect(id, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.save)
        id = wx.NewId()
        menu.Append(id, 'e&Xit', 'Exit program')
        self.Connect(id, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.exit)
        self.mainmenu.Append (menu, '&Main')
        menu = wx.Menu()
        id = wx.NewId()
        menu.Append(id, '&New', 'Add note')
        self.Connect(id, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.new_item)
        id = wx.NewId()
        menu.Append(id, '&Delete', 'Remove note')
        self.Connect(id, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.delete_item)
        id = wx.NewId()
        self.mainmenu.Append (menu, '&Note')
        menu = wx.Menu()
        id = wx.NewId()
        menu.Append(id, '&About/Keys', 'About this application and its keyboard shortcuts')
        self.Connect(id, -1, wx.wxEVT_COMMAND_MENU_SELECTED, self.helppage)
        id = wx.NewId()
        self.mainmenu.Append (menu, '&Help')
        self.SetMenuBar (self.mainmenu)

        splitter = wx.SplitterWindow (self, -1, style=wx.NO_3D) # |wx.SP_3D
        splitter.SetMinimumPaneSize (1)

        self.tree = wx.TreeCtrl (splitter, -1,
            style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.root = self.tree.AddRoot("MyNotes")
        self.activeitem = self.root
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelChanging, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnTreeLabelEdit, self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnTreeLabelEditEnd, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeItemActivated, self.tree)
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.tree.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.tree.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.editor = wx.TextCtrl(splitter, -1, style=wx.TE_MULTILINE)
        self.editor.Enable (0)
        self.editor.Bind(wx.EVT_TEXT, self.OnEvtText)
        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_key)

        splitter.SplitVertically (self.tree, self.editor)
        splitter.SetSashPosition (180, True)
        splitter.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.Show(True)

    def on_key(self,event):
        # wat voor hotkeys?
        # tree: up, down , tab to text, F2 rename, del delete
        # text: ctrl Tab next/prev text, tab to tree
        # global: ctrl-S(ave), Ctrl-L(oad), Ctrl-H(ide)
        skip = True
        keycode = event.GetKeyCode()
        win = event.GetEventObject()
        if event.GetModifiers() == wx.MOD_CONTROL: # evt.ControlDown()
            if keycode == ord("L"): # 76: Ctrl-L reload tabs
                self.reread()
            elif keycode == ord("N"): # 78: Ctrl-N nieuwe tab
                self.new_item()
            elif keycode == ord("D"):
                self.delete_item()
            elif keycode == ord("H"): # 72: Ctrl-H Hide/minimize
                if self.opts["AskBeforeHide"]:
                    dlg = CheckDialog(self,-1,'Apropos')
                    ## ,                    style = wx.DEFAULT_DIALOG_STYLE | wx.OK | wx.ICON_INFORMATION)
                    dlg.ShowModal()
                    if dlg.Check.GetValue():
                        self.opts["AskBeforeHide"] = False
                    dlg.Destroy()
                self.tbi = wx.TaskBarIcon()
                self.tbi.SetIcon(self.apoicon,"Click to revive Apropos")
                wx.EVT_TASKBAR_LEFT_UP(self.tbi, self.revive)
                wx.EVT_TASKBAR_RIGHT_UP(self.tbi, self.revive)
                self.Hide()
                ## pass # nog uitzoeken hoe
            elif keycode == ord("S"): # 83: Ctrl-S saven zonder afsluiten
                self.save()
            elif keycode == ord("Q"): # 81: Ctrl-Q afsluiten na saven
                self.exit()
        elif keycode == wx.WXK_TAB and win == self.editor:
            if event.GetModifiers() == wx.MOD_CONTROL:
                item = self.tree.GetNextSibling(self.activeitem)
                if item.IsOk:
                    self.activate_item(item)
            elif event.GetModifiers() == wx.MOD_CONTROL | wx.MOD_SHIFT:
                item = self.tree.GetPrevSibling(self.activeitem)
                if item.IsOk:
                    self.activate_item(item)
        elif keycode == wx.WXK_F1:
            self.helppage()
        elif keycode == wx.WXK_F2 and win == self.tree:
            self.asktitle()
        elif keycode == wx.WXK_DELETE and win == self.tree:
            self.delete_item()
        elif keycode == wx.WXK_ESCAPE:
            self.exit()
        if event and skip:
            event.Skip()

    def OnEvtText(self,event): # seems to work
        self.editor.IsModified = True

    def OnRightDown(self, event): # wil ik hier wat mee?
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item:
            print(("OnRightDown: %s, %s, %s\n" % (self.tree.GetItemText(item),
                type(item), item.__class__)))
            self.tree.SelectItem(item)

    def OnRightUp(self, event): # wil ik hier wat mee?
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item:
            print(("OnRightUp: %s (manually starting label edit)\n" %
                self.tree.GetItemText(item)))
            self.tree.EditLabel(item)

    def OnLeftDClick(self, event): # wil ik hier wat mee?
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item:
            print(("OnLeftDClick: %s" % self.tree.GetItemText(item)))
            #~ parent = self.tree.GetItemParent(item)
            #~ self.tree.SortChildren(parent)
        event.Skip()

    def OnItemExpanded(self, event): # works (tm)
        item = event.GetItem()
        if item:
            print("OnItemExpanded: %s" % self.tree.GetItemText(item))
        event.Skip()

    def OnItemCollapsed(self, event): # works (tm)
        item = event.GetItem()
        if item:
            print(("OnItemCollapsed: %s" % self.tree.GetItemText(item)))
        event.Skip()

    def OnSelChanging(self, event=None): # works (tm)
        if event.GetItem() == self.root:
            event.Veto()

    def OnSelChanged(self, event=None): # works (tm)
        print("OnSelChanged"),
        self.check_active()
        self.activate_item(event.GetItem())
        event.Skip()

    def open(self):
        print "open(): {0}".format(self.project_file)
        try:
            file = open(self.project_file)
        except IOError:
            return
        try:
            data = pickle.load(file)
        except EOFError:
            return
        file.close()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot(os.path.splitext(os.path.split(self.project_file)[1])[0])
        for tag, text in data:
            item = self.tree.AppendItem (self.root, tag)
            self.tree.SetItemPyData(item, text)
        ## self.activeitem = self.root
        self.editor.Clear()
        self.editor.Enable (False)
        self.tree.Expand (self.root)
        item, dummy = self.tree.GetFirstChild(self.root)
        self.tree.SelectItem(item)
        self.tree.SetFocus()
        ## self.editor.SetInsertionPoint(0)
        ## self.editor.SetFocus()
        self.projectdirty = False

    def reread(self,event=None):
        dlg=wx.MessageDialog(self, 'OK to reload?', 'NoteTree', wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.open()

    def save(self,event=None):
        print "save(): {0}".format(self.project_file)
        if os.path.exists(self.project_file):
            pass # backup maken?
        data = []
        tag, cookie = self.tree.GetFirstChild(self.root)
        while tag.IsOk():
            data.append((self.tree.GetItemText(tag),
                self.tree.GetItemPyData(tag)))
            tag, cookie = self.tree.GetNextChild(self.root, cookie)
        file = open(self.project_file,"w")
        pickle.dump(data, file)
        file.close()

    def exit(self,event=None):
        self.save()
        self.Close()

    def new_item(self, event=None): # works
        # kijk waar de cursor staat (of altijd onderaan toevoegen?)
        dlg = wx.TextEntryDialog (self, "Geef een titel op voor het nieuwe item", "Notetree")
        if dlg.ShowModal() == wx.ID_OK:
            text = dlg.GetValue()
            self.check_active()
            item = self.tree.AppendItem (self.root, text)
            self.activeitem = item
            self.tree.SetItemPyData(item, "")

            self.tree.Expand (self.root)
            self.editor.Clear()
            self.editor.Enable(True)
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()
        dlg.Destroy()

    def delete_item(self, event=None):
        item = self.tree.GetSelection()
        if item != self.root:
            prev = self.tree.GetPrevSibling(item)
            self.tree.Delete(item)
            if prev.IsOk:
                print("changing to previous item")
                self.activeitem = None
                self.tree.SelectItem(prev, True)
        else:
            MsgBox(self, "Can't delete root", "Error")

    def asktitle(self):
        dlg = wx.TextEntryDialog(self, 'Nieuwe titel voor het huidige item:',
                'NoteTree', self.tree.GetItemText(self.activeitem))
        if dlg.ShowModal() == wx.ID_OK:
            self.tree.SetItemText(self.activeitem,dlg.GetValue())
        dlg.Destroy()

    def OnTreeLabelEdit(self, event):
        item=event.GetItem()
        if item != self.root:
            print("OnTreeLabelEdit: %s" % self.tree.GetItemText(item))
            event.Veto()

    def OnTreeLabelEditEnd(self, event):
        print("OnTreeLabelEditEnd: %s" % self.tree.GetItemText(item))
        ## self.projectdirty = True

    def OnTreeItemActivated(self, event):
        print("OnTreeItemActivated: %",)
        self.check_active()
        self.activate_item(event.GetItem())

    def check_active(self,message=None): # works, I guess
        if self.activeitem  and self.activeitem != self.root:
            self.tree.SetItemBold(self.activeitem, False)
            if self.editor.IsModified:
                if message:
                    print(message)
                self.tree.SetItemPyData(self.activeitem,self.editor.GetValue())

    def activate_item(self, item): # works too, it would seem
        self.activeitem = item
        print(self.tree.GetItemText(item))
        if item != self.root:
            print "item is not root"
            self.tree.SetItemBold(item, True)
            self.editor.SetValue(self.tree.GetItemPyData(item))
            self.editor.Enable(True)
        else:
            print "item is root"
            self.editor.Clear()
            self.editor.Enable(False)
        ## self.editor.SetInsertionPoint(0)
        ## self.editor.SetFocus()

    def helppage(self,event=None):
        info = [
            "NoteTree door Albert Visser",
            "Electronisch notitieblokje",
            "",
            "Ctrl-N                   - nieuwe notitie",
            "Ctrl-Tab    in editor of"
            " CursorDown in tree      - volgende notitie",
            "Ctrl-Shift-Tab in editor of"
            " CursorUp   in tree      - vorige notitie",
            "Ctrl-D of Delete in tree - verwijder notitie",
            "Ctrl-S                   - alles opslaan",
            "Ctrl-L                   - alles opnieuw laden",
            "Ctrl-Q, Esc              - opslaan en sluiten",
            "Ctrl-H                   - verbergen in system tray",
            "",
            "F1                       - deze (help)informatie",
            "F2                       - wijzig notitie titel",
            ]
        dlg = wx.MessageDialog(self, "\n".join(info),'Apropos',
            wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

class App(wx.App):
    def __init__(self,fn):
        self.fn = fn
        wx.App.__init__(self,False)
    ## def OnInit(self):
        frame = main_window(None, -1, "NoteTree - " + self.fn)
        self.SetTopWindow(frame)
        frame.project_file = self.fn
        frame.open()
        ## return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        INI = sys.argv[1]
    else:
        INI = 'MyMan.ini'
    app = App(INI)
    app.MainLoop()