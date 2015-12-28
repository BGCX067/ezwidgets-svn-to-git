#----------------------------------------------------------------------------
# Name:        vlist.py
# Purpose:     virtual list with mix-in ColumnSorter class
#
# Author:      Egor Zindy
#
# Created:     26-June-2005
# Licence:     public domain
#----------------------------------------------------------------------------

import wx
import wx.lib.mixins.listctrl  as  listmix

class VirtualList(wx.ListCtrl, listmix.ColumnSorterMixin):
    def __init__(self, parent,columns,style=0):
        wx.ListCtrl.__init__( self, parent, -1,
                style=wx.LC_REPORT|wx.LC_VIRTUAL|style)
        listmix.ColumnSorterMixin.__init__(self, len(columns))

        self.itemDataMap={}

        self.il = wx.ImageList(16, 16)
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.il_symbols={}

        #adding some art (sm_up and sm_dn are used by ColumnSorterMixin
        #symbols can be added to self.il using SetSymbols
        symbols={"sm_up":wx.ART_GO_UP,"sm_dn":wx.ART_GO_DOWN}
        self.SetSymbols(symbols)

        #building the columns
        self.SetColumns(columns)

    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...

    def OnGetItemText(self, item, col):
        index=self.itemIndexMap[item]
        s = self.itemDataMap[index][col]
        return s
    
    def OnGetItemImage(self, item):
        return -1

    def OnGetItemAttr(self, item):
        return None

    #---------------------------------------------------
    # These methods are Used by the ColumnSorterMixin,
    # see wx/lib/mixins/listctrl.py

    def GetListCtrl(self):
        return self

    def GetSortImages(self):
        return self.il_symbols["sm_dn"],self.il_symbols["sm_up"]

    def SortItems(self,sorter=None):
        r"""\brief a SortItem which works with virtual lists
        The sorter is not actually used (should it?)
        """

        #These are actually defined in ColumnSorterMixin
        #col is the column which was clicked on and
        #the sort flag is False for descending (Z->A)
        #and True for ascending (A->Z).

        col=self._col

        #creating pairs [column item defined by col, key]
        items=[]
        for k,v in self.itemDataMap.items():
            items.append([v[col],k])

        #sort the pairs by value (first element), then by key (second element).
        #Multiple same values are okay, because the keys are unique.
        items.sort()

        #getting the keys associated with each sorted item in a list
        k=[key for value, key in items]

        #False is descending (starting from last)
        if self._colSortFlag[col]==False:
            k.reverse()

        #storing the keys as self.itemIndexMap (is used in OnGetItemText,Image,ItemAttr).
        self.itemIndexMap=k

        #redrawing the list
        self.Refresh()

    #---------------------------------------------------
    # These methods should be used to interact with the
    # controler

    def SetItemMap(self,itemMap):
        r"""\brief sets the items to be displayed in the control
        \param itemMap a dictionary {id1:("item1","item2",...), id2:("item1","item2",...), ...} and ids are unique
        """
        l=len(itemMap)
        self.itemDataMap=itemMap
        self.SetItemCount(l)

        #This regenerates self.itemIndexMap and redraws the ListCtrl
        self.SortItems()

    def SetColumns(self,columns):
        r"""\brief adds columns to the control
        \param columns a list of columns (("name1",width1),("name2",width2),...)
        """

        i=0
        for name,s in columns:
            self.InsertColumn(i, name)
            self.SetColumnWidth(i, s)
            i+=1

    def SetSymbols(self,symbols,provider=wx.ART_TOOLBAR):
        r"""\brief adds symbols to self.ImageList
        Symbols are provided by the ArtProvider
        \param symbols a dictionary {"name1":wx.ART_ADD_BOOKMARK,"name2":wx.ART_DEL_BOOKMARK,...}
        \param provider an optional provider
        """

        for k,v in symbols.items():
            self.il_symbols[k]=self.il.Add(wx.ArtProvider_GetBitmap(v,provider,(16,16)))

