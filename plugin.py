import wx

import pcbnew
from .push_thread import *
from .result_event import *

class PushToStatusForm(wx.Frame):
    def __init__(self):
        wx.Dialog.__init__( self, None, id = wx.ID_ANY, title = "Pushing to AISLER in progress...", pos = wx.DefaultPosition, style = wx.DEFAULT_DIALOG_STYLE )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        self.textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL, size=(485,300) )
        bSizer1.Add( self.textCtrl1, 0, wx.ALL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )
    
        EVT_RESULT(self, self.updateDisplay)
        PushThread(self)
        
        
    def updateDisplay(self, msg):
        if msg.data == -1:
            self.Destroy()
        else:
            self.textCtrl1.write(msg.data + '\n')

class PushForKiCadPlugin(pcbnew.ActionPlugin):
    def __init__(self):
        self.name = 'Push layout to AISLER'
        self.category = "Manufacturing"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')
        self.description = "Push current layout to AISLER"
        
        
    def Run(self):   
        PushToStatusForm().Show()