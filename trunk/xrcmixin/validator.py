#Based on http://aspn.activestate.com/ASPN/Mail/Message/wxpython-users/3689627

import string
import wx

DECIMAL_DIGITS = 1
HEX_DIGITS = 2
LETTERS = 3
FLOAT_DIGITS = 4
NEGATIVE_DIGITS = 5

float_string = string.digits+"-eE."
negative_string = string.digits+"-"

class CharValidator(wx.PyValidator):
    def __init__(self, flag):
        wx.PyValidator.__init__(self)

        if flag == DECIMAL_DIGITS:
            self.valid_string = string.digits
        elif flag == NEGATIVE_DIGITS:
            self.valid_string = negative_string
        elif flag == FLOAT_DIGITS:
            self.valid_string = float_string
        elif flag == HEX_DIGITS:
            self.valid_string = string.hexdigits
        else:
            self.valid_string = string.letters

        self.flag = flag

        self.Bind(wx.EVT_CHAR, self.OnChar)
    
    def Clone(self):
        '''
        every validator must implement Clone() method!
        '''
        return CharValidator(self.flag)

    def OnChar(self, event):
        keyCode = event.GetKeyCode()
        if keyCode in range(256) and keyCode not in (8, 9, 127): 
            #8 = Backspace-Key, #9 = Tab 127 = Delete-Key
            key = chr(event.GetKeyCode())
            if key not in self.valid_string:
                return

        event.Skip()

