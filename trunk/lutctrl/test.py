#!/usr/bin/env python

"""
LUT Controls test cases

Original LUT data located on http://rsb.info.nih.gov/ij/download/luts/
Rasband, W.S., ImageJ, U. S. National Institutes of Health, Bethesda,
Maryland, USA, http://rsb.info.nih.gov/ij/, 1997-2005.

The latest version of this file is stored in my google code repository:
    http://code.google.com/p/ezwidgets/

Copyright (c) 2007 Egor Zindy <ezindy@gmail.com>

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
__copyright__ = "Copyright (c) 2007 Egor Zindy"
__license__ = "MIT"
__version__ = "1.0"
__date= "2007-10-11"
__status__ = "Production"

import wx
import ctrl
from data import LutData
import numpy

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Lut, Opacity and Histogram", size=(320,340))
        self.CreateStatusBar()


        LD = LutData([0,1,8,9,10,15,17,18,48,52,53,54,59,60,61,65,79,92,93,95,96,112,120,129,134])
        #LD = LutData()

        p = wx.Panel(self,-1)
        box = wx.BoxSizer(wx.VERTICAL)

        #different lut controls
        if 1:
            lc1=ctrl.LutCtrl(p,LD,0,style=ctrl.LUT_CHOICE)
            box.Add(lc1,0,wx.EXPAND|wx.ALL,2)
            lc1.Bind(ctrl.EVT_LUT, self.OnLut)

            lc2=ctrl.LutCtrl(p,LD,1,style=ctrl.LUT_SPIN)
            box.Add(lc2,0,wx.EXPAND|wx.ALL,2)
            lc2.Bind(ctrl.EVT_LUT, self.OnLut)

            lc3=ctrl.LutCtrl(p,LD,14,style=ctrl.LUT_CHOICE|ctrl.LUT_SPIN)
            box.Add(lc3,0,wx.EXPAND|wx.ALL,2)
            lc3.Bind(ctrl.EVT_LUT, self.OnLut)

        #opacity control
        if 1:
            absrange = (0,100)
            lutrange = (20,80)
            oc = ctrl.OpacityCtrl(p,LD,14)
            box.Add(oc,0,wx.EXPAND|wx.ALL,2)
            oc.SetRange(absrange[0],absrange[1])

            #make a more complicated opacity function
            f = numpy.array([[0,0],[0.2,0.6],[0.75,1],[1,0.25]])
            oc.SetOpacity(f)
            oc.Bind(ctrl.EVT_UPDATE, self.OnOpacity)
            self.oc = oc

        #histogram control
        if 1:
            hc = ctrl.HistogramCtrl(p,LD,14,minspan=10)
            hc.Bind(ctrl.EVT_RANGE, self.OnHistogram)

            box.Add(hc,1,wx.EXPAND|wx.ALL,2)

            #generate some random data to use as a histogram
            data = 1000 * numpy.random.random_sample(1000)
            hc.SetData(data,current_range=(100,900))
            self.hc = hc

        box.Layout()
        p.SetSizer(box)

    def OnHistogram(self,event):
        r = event.GetRange()
        s = "Histogram range: (%.2f,%.2f)" %(r[0],r[1])
        self.SetStatusText(s)

    def OnOpacity(self,event):
        active_node = event.GetActiveIndex()
        if active_node is None:
            s = "Removed a node..."
        else:
            s = "Node %d: (%.2f,%.2f)" %(active_node,event.GetActivePosition(),event.GetActiveOpacity())
        self.SetStatusText(s)

    def OnLut(self,event):
        s = "LUT %d of %d is '%s'" % (
            event.GetLutIndex(),
            event.GetLutCount(),
            event.GetLutName())

        #The event.GetLUT() and event.GetLUTRGB() are also available.
        #They return and RGB string (interleaved) or separate R,G,B strings
        #These are easy to convert to numarray, Numeric or numpy...
        #
        #r,g,b = event.GetLutRGB()
        #r_array = Numeric.array(r)
        #g_array = Numeric.array(r)
        #b_array = Numeric.array(r)

        self.SetStatusText(s)
        #self.lp.SetLutIndex(event.GetLutIndex())
        if hasattr(self,'oc'):
            self.oc.SetLutIndex(event.GetLutIndex())
        if hasattr(self,'hc'):
            self.hc.SetLutIndex(event.GetLutIndex())

def test():
    app = wx.PySimpleApp()
    f = TestFrame()
    f.Show()
    app.MainLoop()

if __name__ == "__main__":
    test()



