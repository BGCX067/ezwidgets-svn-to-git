"""
Simple calculator that uses XRC.
"""

import wx
import calc_xrc
import xrcMixin

class MainPanel(calc_xrc.xrcMainPanel, xrcMixin.xrcMixin):
    def __init__(self, *args, **kwargs):
        calc_xrc.xrcMainPanel.__init__(self,*args, **kwargs)
        xrcMixin.xrcMixin.__init__(self)
        self.InitValues()

    def InitValues(self):
        self.FirstArg.SetValue("1")
        self.SecondArg.SetValue("2")
        self.Result.SetValue("")

    def InitArgs(self):
        try:
            self.first = float(self.FirstArg.GetValue())
        except ValueError:
            return self.BadFloatValue(self.FirstArg)
        try:
            self.second = float(self.SecondArg.GetValue())
        except ValueError:
            return self.BadFloatValue(self.SecondArg)
        return True

    def BadFloatValue(self, control):
        dlg = wx.MessageDialog(self, "I can't convert this to float.",
                              'Conversion error', wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        control.SetFocus()
        control.SetSelection(-1, -1)
        return False

class MainFrame(calc_xrc.xrcMainFrame):
    def __init__(self, *args, **kwargs):
        calc_xrc.xrcMainFrame.__init__(self,*args, **kwargs)
        self.panel = MainPanel(self)

        sizer = self.panel.GetSizer()
        sizer.Fit(self)
        sizer.SetSizeHints(self)

    def OnMenu_AddMenuItem(self, evt):
        if self.panel.InitArgs():
            self.panel.Result.SetValue(str(self.panel.first + self.panel.second))
    def OnMenu_SubtractMenuItem(self, evt):
        if self.panel.InitArgs():
            self.panel.Result.SetValue(str(self.panel.first - self.panel.second))
    def OnMenu_MultiplyMenuItem(self, evt):
        if self.panel.InitArgs():
            self.panel.Result.SetValue(str(self.panel.first * self.panel.second))
    def OnMenu_DivideMenuItem(self, evt):
        if self.panel.InitArgs():
            if self.panel.second != 0:
                self.panel.Result.SetValue(str(self.panel.first / self.panel.second))
            else:
                self.panel.Result.SetValue("#ERROR")

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None)
        self.frame.Show()
        return True

def main():
    app = MyApp(0)
    app.MainLoop()

if __name__ == '__main__':
    main()

