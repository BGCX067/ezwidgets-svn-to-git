#!/usr/bin/env python

"""@package xrcMixin
xrcMixin, an XRC mixin.

Copyright (c) 2009 Egor Zindy <ezindy@gmail.com>

Released under the MIT licence.
"""
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

__author__ = "Egor Zindy <ezindy@gmail.com>"
__copyright__ = "Copyright (c) 2009 Egor Zindy"
__license__ = "MIT"
__version__ = "1.0.1"
__date= "2009-12-16"
__status__ = "Production"

import wx
import wx.lib.newevent

DebugEvent, EVT_DEBUG = wx.lib.newevent.NewEvent()

class xrcMixin():
    def __init__(self,debug=False,InspectionTool=None):

        self.dict = {}
        for ctrl in self.GetChildren():
            name = ctrl.GetName()
            if name != "-1":
                setattr(self,name,ctrl)
                self.dict[name]=ctrl

        self.InspectionTool = InspectionTool
        self.SetDebug(debug)

    def SetDebug(self,debug):
        """Set the debug level.

        0 disables debugging output, 1 enables it (on panel double-click).
        """

        self.debug = debug

        if debug == 0:
            return

        #dealing with multiple names
        dict = {}
        is_multiple = 0
        s = "Multiple names:\n"
        for ctrl in self.GetChildren():
            name = ctrl.GetName()

            if name != "-1":
                ctrl.SetToolTip(wx.ToolTip(name))

                if name in dict.keys():
                    s+="\n%s" % name
                    is_multiple = 1

                dict[name]=1

        if is_multiple == 1:
            wx.MessageBox(s, '%s debug' % self.__class__.__name__)

        #binding a custom debug event
        self.Bind(wx.EVT_LEFT_DCLICK,self.OnDebug)

    def GetValues(self):
        """Values from panel controls

        Scans controls in the panels and returns the values as a dictionary
        @return a dictionary of the control values
        """
        dict = {}
        for key,ctrl in self.dict.items():
            methods = ctrl.__class__.__dict__.keys()
            if 'GetValue' in methods:
                dict[key]=ctrl.GetValue()
            elif 'GetSelections' in methods:
                dict[key]=ctrl.GetSelections()
            elif 'GetSelection' in methods:
                dict[key]=ctrl.GetSelection()
            elif 'GetCurrentSelection' in methods:
                dict[key]=ctrl.GetCurrentSelection()
        return dict

    def OnDebug(self,evt):
        if self.InspectionTool is None:
            s = "Control values:\n"
            for key,value in self.GetValues().items():
                s+="\n%s: %s" % (key,str(value))
            wx.MessageBox(s, '%s debug' % self.__class__.__name__)
        else:
            self.InspectionTool.Show(self)

        debug_event = DebugEvent( GetValues = self.GetValues)
        wx.PostEvent(self, debug_event)

        evt.Skip()

