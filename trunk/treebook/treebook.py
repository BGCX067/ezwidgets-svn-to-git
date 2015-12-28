import  wx

class Treebook(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                    size=wx.DefaultSize, orientation=wx.HORIZONTAL,
                    style=wx.NO_BORDER|wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT):

        wx.Panel.__init__(self, parent, wx.ID_ANY,
                    style=wx.NO_BORDER|wx.CLIP_CHILDREN|wx.TAB_TRAVERSAL)

        #This is the main sizer which could be either horizontal or vertical
        self.hbox = wx.BoxSizer(orientation)

        #adding a tree control to the hbox
        self.tree = wx.TreeCtrl(self, id, pos, size, style)
        self.n_pages=0

        if orientation==wx.HORIZONTAL:
            self.vbox = wx.BoxSizer(wx.VERTICAL)
            self.hbox.Add(self.tree, 0, wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
            #doing the raised panel
            self.rpanel = wx.Panel(self, -1,style=wx.RAISED_BORDER)
            #doing the static box sizer
            self.sbox = wx.StaticBoxSizer(wx.StaticBox(self.rpanel,-1,""))
            #this one is for adding a 5 pixel border all around the static box.
            box = wx.BoxSizer(wx.VERTICAL)
            box.Add(self.sbox, 1, wx.EXPAND|wx.ALL, 5)
            self.rpanel.SetSizer(box)
            box.Layout()
            #adding the raised panel to vbox (right side)
            self.vbox.Add(self.rpanel, 1, wx.EXPAND|wx.ALL, 5)
            #adding the right side to the hbox
            self.hbox.Add(self.vbox, 1, wx.EXPAND|wx.ALL, 0)
        else:
            self.hbox.Add(self.tree, 0, wx.EXPAND|wx.ALL, 5)
            self.vbox=self.hbox
            self.rpanel = wx.Panel(self, -1)
            #doing the static box sizer
            self.sbox = wx.StaticBoxSizer(wx.StaticBox(self.rpanel,-1,""))
            self.rpanel.SetSizer(self.sbox)
            self.sbox.Layout()
            #adding the raised panel to hbox (bottom half)
            self.hbox.Add(self.rpanel,1,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,5)

        self.hbox.Layout()
        self.SetSizer(self.hbox)

        #adding a root to the tree control (remember, root is invisible)
        self.root = self.tree.AddRoot("")
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)

        if "__WXGTK__" in wx.PlatformInfo:
            self.tree.SetFocus()

    def AddPage(self, parentItem, text, page,name=None):
        page.Reparent(self.rpanel)
        page.Hide()
        item = self.tree.AppendItem(parentItem, text)
        self.tree.SetPyData(item, page)
        #Was a name passed to AddPage?
        if name is None:
            try: name=page._name
            except: page._name=""
        else:
            page._name = name
        #each page is tagged with an id, n_pages is the total number of pages
        page._id = self.n_pages
        self.n_pages+=1

        return item

    def ShowPage(self,item):
        newpage = self.tree.GetPyData(item)
        self.sbox.GetStaticBox().SetLabel(newpage._name)
        self.sbox.Add(newpage, 1, wx.EXPAND|wx.ALL, 5)
        newpage.Show()
        self.sbox.Layout()

    def OnSelChanged(self, evt):
        olditem = evt.GetOldItem()
        if not olditem.IsOk(): return
        item = evt.GetItem()
        oldpage = self.tree.GetPyData(olditem)
        self.sbox.Remove(oldpage)
        oldpage.Hide()
        self.ShowPage(item)

class TreebookDialog(wx.Dialog):
    def __init__(self,parent,size,orientation=wx.HORIZONTAL):
        wx.Dialog.__init__(self, parent, -1, "Treebook Dialog", size=size)

        self.tb=Treebook(self,-1,size=(125,65),orientation=orientation)
        self.tree = self.tb.tree
        self.root = self.tb.root
        self.AddPage = self.tb.AddPage
        self.ShowPage = self.tb.ShowPage

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.tb, 1, wx.EXPAND|wx.ALL,5)

        #horizontal sizer for the buttons
        self.bbox = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_back = wx.Button(self.tb, wx.ID_BACKWARD,"< Back")
        self.btn_back.Disable()
        self.btn_back.Bind(wx.EVT_BUTTON, self.OnButton)
        self.btn_next = wx.Button(self.tb, wx.ID_FORWARD,"Next >")
        self.btn_next.Bind(wx.EVT_BUTTON, self.OnButton)
        self.btn_ok = wx.Button(self.tb, wx.ID_OK)
        self.btn_cancel = wx.Button(self.tb, wx.ID_CANCEL)

        self.bbox.Add(self.btn_back, 0, wx.LEFT, 20)
        self.bbox.Add(self.btn_next, 0, wx.LEFT, 5)
        self.bbox.Add(self.btn_ok, 0, wx.LEFT, 5)
        self.bbox.Add(self.btn_cancel, 0, wx.LEFT, 5)

        #add the sizer to tb.vbox, the right/bottom half of the treectrl
        self.tb.vbox.Add(self.bbox, 0, wx.BOTTOM, 5)
        self.tb.vbox.Layout()

        box.Layout()
        self.SetSizer(box)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)

    def OnButton(self,evt):
        id=evt.GetId()
        item=self.tree.GetSelection()
        page=self.tree.GetPyData(item)

        if id == wx.ID_FORWARD:
            if page._id < self.tb.n_pages-1:
                item=self.tree.GetNextVisible(item)
                self.tree.SelectItem(item)
        elif id == wx.ID_BACKWARD:
            if page._id > 0:
                item=self.tree.GetPrevVisible(item)
                self.tree.SelectItem(item)

        #Expand collapsed items (easier to navigate the tree with buttons only)
        if self.tree.ItemHasChildren(item) and self.tree.IsExpanded(item)==0:
            self.tree.Expand(item)

    def OnSelChanged(self,evt):
        """This method checks the value of panel._id and changes the state of
        the buttons accordingly. It then skips the event for Treebook"""

        item=self.tree.GetSelection()
        page=self.tree.GetPyData(item)

        if page._id==0:
            if self.btn_back.IsEnabled()==1: self.btn_back.Disable()
            if self.btn_next.IsEnabled()==0: self.btn_next.Enable()
        elif page._id==self.tb.n_pages-1:
            if self.btn_next.IsEnabled()==1: self.btn_next.Disable()
            if self.btn_back.IsEnabled()==0: self.btn_back.Enable()
        else:
            if self.btn_back.IsEnabled()==0: self.btn_back.Enable()
            if self.btn_next.IsEnabled()==0: self.btn_next.Enable()

        evt.Skip()

if __name__ == "__main__":

    class AboutPanel(wx.Panel):
        def __init__(self, parent,text,name="About Treebook for wxPython"):
            wx.Panel.__init__(self, parent, -1)
            self._name=name
            box = wx.BoxSizer(wx.VERTICAL)
            if text.rfind("---") > -1:
                about,ver=text.split("---")
                box.Add(wx.StaticText(self,-1,about),1,wx.EXPAND)
                box.Add(wx.StaticText(self,-1,ver),0,wx.EXPAND|wx.ALIGN_BOTTOM)
            else:
                box.Add(wx.StaticText(self,-1,text),1,wx.EXPAND)
            box.Layout()
            self.SetSizer(box)

    class ColorPanel(wx.Panel):
        def __init__(self, parent, color=None):
            wx.Panel.__init__(self, parent, -1)
            if color is None:
                self._name="Empty panel"
            else:
                self.SetBackgroundColour(color)
                self._name="Colour: %s" % str(color)

    # TBDExample is derived from TreebookDialog,
    # this is how you want to build your own dialogs based of TreebookDialog
    class TBDExample(TreebookDialog):
        def __init__(self,parent,orientation=wx.HORIZONTAL,show_images=1):
            TreebookDialog.__init__(self,parent,wx.Size(500,400),orientation)

            #create some panels...
            MyAboutPanel = AboutPanel(self,str_about+"---"+str_version)
            MyHowPanel = AboutPanel(self,str_how)
            MyTodoPanel = AboutPanel(self,str_todo)
            MyEmptyPanel = ColorPanel(self) #Will appear twice in the treebook
            MyRedPanel = ColorPanel(self, "red")
            MyGreenPanel = ColorPanel(self, "green")
            MyBluePanel = ColorPanel(self, "blue")
            MyYellowPanel = ColorPanel(self, "yellow")

            items=[] #will be used for adding icons to the treectrl items
            child = self.AddPage(self.root, "About",MyAboutPanel) 
            items.append(child)
            items.append(self.AddPage(child, "How", MyHowPanel))
            items.append(self.AddPage(child, "Todo", MyTodoPanel))
            child = self.AddPage(self.root, "Colour panels", MyEmptyPanel)
            items.append(child)
            items.append(self.AddPage(child, "Red", MyRedPanel))
            items.append(self.AddPage(child, "Green", MyGreenPanel))
            child = self.AddPage(self.root, "More panels", MyEmptyPanel)
            items.append(child)
            items.append(self.AddPage(child, "Blue", MyBluePanel))
            items.append(self.AddPage(child, "Yellow", MyYellowPanel))
            
            self.ShowPage(items[0]) #show (and select) the "about" page
            #caution, the following is only safe if the item has children!
            self.tree.Expand(items[0]) #expand the "about" children

            #Add a few images to the treectrl (if show_images is true)
            if show_images:
                isz = (16,16)
                il = wx.ImageList(isz[0], isz[1])
                fld = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,
                                                          wx.ART_OTHER, isz))
                fldo = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,
                                                          wx.ART_OTHER, isz))
                file = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE,
                                                          wx.ART_OTHER, isz))
                self.tree.SetImageList(il)
                for it in items:
                    if self.tree.ItemHasChildren(it): #use a folder icon
                        self.tree.SetItemImage(it,fld,wx.TreeItemIcon_Normal)
                        self.tree.SetItemImage(it,fldo,wx.TreeItemIcon_Expanded)
                    else: #use a file icon
                        self.tree.SetItemImage(it,file,wx.TreeItemIcon_Normal)

                self.tree.il=il #This prevents the imagelist from being lost

        def Success(self,val):
            #you can call this before the dialog is destroyed
            if val == wx.ID_OK:
                s = "OK"
            else: s = "Cancel"
            return "You pressed %s. You can resize this frame." % s

    class Frame(wx.Frame):
        def __init__(self, pos=wx.DefaultPosition, size=(500,400)):
            wx.Frame.__init__(self, None, -1, "Treebook in a frame", pos, size)
            self.CreateStatusBar()

    str_about = """Usage:\n
Navigate the pages using either the tree control or the buttons."""
    
    str_version = """Treebook Dialog v1.0 - Egor Zindy - Public domain
Thanks to Ricardo Pedroso for the original Treebook sample"""

    str_how = """Things to try in main():\n
    - set show_images to 0 to remove the icons in the treectrl\n
    - set orientation to either wx.HORIZONTAL or wx.VERTICAL\n
Design considerations:\n
    - Treebook.AddPage appends an integer _id to each page and increments \
Treebook.n_pages, the number of pages. This is then used in TreebookDialog \
to activate/deactivate the [back] and [next] buttons at the bounds.\n
    - Treebook.AddPage also changes the page parent to treebook.rpanel \
(this hides the internal structure of the dialog).\n
    - Treebook.ShowPage handles the display of pages and changes the staticbox \
label to page._name.\n"""
    
    str_todo = "Todo:\n\n    - Sort-out the treebook layout: V/H duplicate code"

    def main():
        app = wx.PySimpleApp()

        ### First example, a treebook panel in a modal dialog
        

        tbd = TBDExample(None,orientation=wx.HORIZONTAL,show_images=1)
        val=tbd.ShowModal()
        s=tbd.Success(val)

        ### Next example, a treebook panel in a frame (not a complete example)

        f = Frame(tbd.GetPosition())
        # There's a treebook in TBDExample. Look away while I reparent it...
        tbd.tb.Reparent(f) #reparenting the treebook as a child of Frame f
        tbd.tb.vbox.Hide(tbd.bbox) #hiding the buttons
        tbd.tree.Unbind(wx.EVT_TREE_SEL_CHANGED) #this is OnSelChanged in tbd
        tbd.Destroy() #tbd can now safely be destroyed

        f.Show()
        f.SetStatusText(s)
        app.MainLoop()

    main()

