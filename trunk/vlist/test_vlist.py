#----------------------------------------------------------------------------
# Name:        test_vlist.py
# Purpose:     testbed for the VirtualList control (works as expected)
#
# Author:      Egor Zindy
#
# Created:     23-May-2005
# Licence:     public domain
#----------------------------------------------------------------------------

import wx
wx.SystemOptions.SetOptionInt("msw.remap", 0)
import wx.lib.mixins.listctrl  as  listmix
from vlist import VirtualList

#----------------------------------------------------------------------
# TestVirtualList uses VirtualList and:-
#   adds the autowidth mixin
#   adds some attributes and redefines OnGetItemAttr(self, item):
#   adds a few more symbols and redefines OnGetItemImage(self, item):
#   sets the sorting column and order
#   binds a few events
#----------------------------------------------------------------------

musicdata_short = {
1 : ("Bad English", "The Price Of Love", "Rock"),
6 : ("Michael Bolton", "How Am I Supposed To Live Without You", "Blues"),
32: ("Spyro Gyra", "End of Romanticism", "Jazz"),
54: ("David Lanz", "Leaves on the Seine", "New Age"),
}

musicdata = {
1 : ("Bad English", "The Price Of Love", "Rock"),
2 : ("DNA featuring Suzanne Vega", "Tom's Diner", "Rock"),
3 : ("George Michael", "Praying For Time", "Rock"),
4 : ("Gloria Estefan", "Here We Are", "Rock"),
5 : ("Linda Ronstadt", "Don't Know Much", "Rock"),
6 : ("Michael Bolton", "How Am I Supposed To Live Without You", "Blues"),
7 : ("Paul Young", "Oh Girl", "Rock"),
8 : ("Paula Abdul", "Opposites Attract", "Rock"),
9 : ("Richard Marx", "Should've Known Better", "Rock"),
10: ("Rod Stewart", "Forever Young", "Rock"),
11: ("Roxette", "Dangerous", "Rock"),
12: ("Sheena Easton", "The Lover In Me", "Rock"),
13: ("Sinead O'Connor", "Nothing Compares 2 U", "Rock"),
14: ("Stevie B.", "Because I Love You", "Rock"),
15: ("Taylor Dayne", "Love Will Lead You Back", "Rock"),
16: ("The Bangles", "Eternal Flame", "Rock"),
17: ("Wilson Phillips", "Release Me", "Rock"),
18: ("Billy Joel", "Blonde Over Blue", "Rock"),
19: ("Billy Joel", "Famous Last Words", "Rock"),
20: ("Billy Joel", "Lullabye (Goodnight, My Angel)", "Rock"),
21: ("Billy Joel", "The River Of Dreams", "Rock"),
22: ("Billy Joel", "Two Thousand Years", "Rock"),
23: ("Janet Jackson", "Alright", "Rock"),
24: ("Janet Jackson", "Black Cat", "Rock"),
25: ("Janet Jackson", "Come Back To Me", "Rock"),
26: ("Janet Jackson", "Escapade", "Rock"),
27: ("Janet Jackson", "Love Will Never Do (Without You)", "Rock"),
28: ("Janet Jackson", "Miss You Much", "Rock"),
29: ("Janet Jackson", "Rhythm Nation", "Rock"),
30: ("Janet Jackson", "State Of The World", "Rock"),
31: ("Janet Jackson", "The Knowledge", "Rock"),
32: ("Spyro Gyra", "End of Romanticism", "Jazz"),
33: ("Spyro Gyra", "Heliopolis", "Jazz"),
34: ("Spyro Gyra", "Jubilee", "Jazz"),
35: ("Spyro Gyra", "Little Linda", "Jazz"),
36: ("Spyro Gyra", "Morning Dance", "Jazz"),
37: ("Spyro Gyra", "Song for Lorraine", "Jazz"),
38: ("Yes", "Owner Of A Lonely Heart", "Rock"),
39: ("Yes", "Rhythm Of Love", "Rock"),
40: ("Cusco", "Dream Catcher", "New Age"),
41: ("Cusco", "Geronimos Laughter", "New Age"),
42: ("Cusco", "Ghost Dance", "New Age"),
43: ("Blue Man Group", "Drumbone", "New Age"),
44: ("Blue Man Group", "Endless Column", "New Age"),
45: ("Blue Man Group", "Klein Mandelbrot", "New Age"),
46: ("Kenny G", "Silhouette", "Jazz"),
47: ("Sade", "Smooth Operator", "Jazz"),
48: ("David Arkenstone", "Papillon (On The Wings Of The Butterfly)", "New Age"),
49: ("David Arkenstone", "Stepping Stars", "New Age"),
50: ("David Arkenstone", "Carnation Lily Lily Rose", "New Age"),
51: ("David Lanz", "Behind The Waterfall", "New Age"),
52: ("David Lanz", "Cristofori's Dream", "New Age"),
53: ("David Lanz", "Heartsounds", "New Age"),
54: ("David Lanz", "Leaves on the Seine", "New Age"),
}

class TestVirtualList(VirtualList, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent,log):
        VirtualList.__init__(self, parent,
                (("Artist",150),("Title",220),("Genre",100)),
                style=wx.LC_HRULES|wx.LC_VRULES)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        self.log=log

        symbols={"w_idx":wx.ART_WARNING,"e_idx":wx.ART_ERROR,"i_idx":wx.ART_QUESTION}
        self.SetSymbols(symbols)

        #adding some attributes (colourful background for each item rows)
        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("yellow")
        self.attr2 = wx.ListItemAttr()
        self.attr2.SetBackgroundColour("light blue")
        self.attr3 = wx.ListItemAttr()
        self.attr3.SetBackgroundColour("purple")

        #Setting the data (done in TestFrame)
        #self.SetItemMap(musicdata)

        #sort by genre (column 2), A->Z ascending order (1)
        self.SortListItems(2, 1)

        #events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

    def OnColClick(self,event):
        self.log.WriteText("OnColClick: %d\n" % event.GetColumn())
        event.Skip()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        self.log.WriteText('OnItemSelected: "%s", "%s", "%s", "%s"\n' %
                           (self.currentItem,
                            self.GetItemText(self.currentItem),
                            self.getColumnText(self.currentItem, 1),
                            self.getColumnText(self.currentItem, 2)))

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        self.log.WriteText("OnItemActivated: %s\nTopItem: %s\n" %
                           (self.GetItemText(self.currentItem), self.GetTopItem()))

    def OnItemDeselected(self, evt):
        self.log.WriteText("OnItemDeselected: %s" % evt.m_itemIndex)

    def OnGetItemImage(self, item):
        index=self.itemIndexMap[item]
        genre=self.itemDataMap[index][2]

        if genre=="Rock":
            return self.il_symbols["w_idx"]
        elif genre=="Jazz":
            return self.il_symbols["e_idx"]
        elif genre=="New Age":
            return self.il_symbols["i_idx"]
        else:
            return -1

    def OnGetItemAttr(self, item):
        index=self.itemIndexMap[item]
        genre=self.itemDataMap[index][2]

        if genre=="Rock":
            return self.attr2
        elif genre=="Jazz":
            return self.attr1
        elif genre=="New Age":
            return self.attr3
        else:
            return None

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

#----------------------------------------------------------------------
# The main window
#----------------------------------------------------------------------
# This is where you populate the frame with a panel from the demo.
#  original line in runTest (in the demo source):
#    win = TestPanel(nb, log)
#  this is changed to:
#    self.win=TestPanel(self,log)
#----------------------------------------------------------------------

class TestFrame(wx.Frame):

    def __init__(self, parent, id, title, size, style = wx.DEFAULT_FRAME_STYLE ):
        wx.Frame.__init__(self, parent, id, title, size=size, style=style)

        # Prepare the menu bar
        menuBar = wx.MenuBar()

        menu1 = wx.Menu()
        menu1.Append(101, "&Long list", "A long list of songs")
        menu1.Append(102, "&Short list", "A short list of songs")
        menu1.AppendSeparator()
        menu1.Append(104, "&Close", "Close this frame")
        menuBar.Append(menu1, "&File")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.Menu101, id=101)
        self.Bind(wx.EVT_MENU, self.Menu102, id=102)
        self.Bind(wx.EVT_MENU, self.CloseWindow, id=104)

        self.CreateStatusBar(1)
        log=Log()
        self.win = TestVirtualList(self, log)

    def Menu101(self, event):
        self.win.SetItemMap(musicdata)

    def Menu102(self, event):
        self.win.SetItemMap(musicdata_short)

    def CloseWindow(self, event):
        self.Close()

#----------------------------------------------------------------------
class Log:
    r"""\brief Needed by the wxdemos.
    The log output is redirected to the status bar of the containing frame.
    """

    def WriteText(self,text_string):
        print text_string
        self.write(text_string)

    def write(self,text_string):
        wx.GetApp().GetTopWindow().SetStatusText(text_string)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    f = TestFrame(None, -1, "ColumnSorterMixin used with a Virtual ListCtrl",wx.Size(500,300))
    f.Show()
    app.MainLoop()
