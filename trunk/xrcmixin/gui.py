#!/usr/bin/env python

"""@package gui
gui.py, a gui to test the XRC panel

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
import wx.lib.inspection

import gui_xrc
import xrcMixin
import validator

UpdateEvent, EVT_UPDATE = wx.lib.newevent.NewEvent()

#==============================================================================
class TestPanel(xrcMixin.xrcMixin,gui_xrc.xrcmypanel):
    def __init__(self, *args, **kwargs):

        #initialising both the xrc panel we want (panel) and the xrcPanel class
        gui_xrc.xrcmypanel.__init__(self,*args, **kwargs)
        xrcMixin.xrcMixin.__init__(self,debug=1, InspectionTool = wx.lib.inspection.InspectionTool())

        #adding the validators...
        self.text1.Validator = validator.CharValidator(validator.FLOAT_DIGITS) 
        self.text2.Validator = validator.CharValidator(validator.LETTERS) 

    def OnButton_button(self, evt):
        update_event = UpdateEvent( GetValues = self.GetValues)
        wx.PostEvent(self, update_event)

#==============================================================================
class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        """
        Class constructor

        @param args: Arguments
        @param kwargs: Keyword Arguments
        """
        wx.Frame.__init__(self, *args, **kwargs)
        self.CreateStatusBar()

        p = TestPanel(self)
        p.Bind(EVT_UPDATE, self.OnUpdate)

    def OnUpdate(self,evt):
        """
        Catches the update events

        @param evt The event 
        """
        s = "Values:\n"
        for key,value in evt.GetValues().items():
            s+="\n%s: %s" % (key,str(value))
        wx.MessageBox(s, 'Feedback')

class TestApp(wx.App):
    def OnInit(self):
        f = TestFrame(None,title="Test frame", size=(300,480))
        f.Show()
        self.SetTopWindow(f)
        return True

#==============================================================================
if __name__ == '__main__':
    app = TestApp(False)
    app.MainLoop()

