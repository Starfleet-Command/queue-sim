import wx
import wx.grid as grid
import mmsk
import M_M_s as mms

class InputFrame(wx.Frame):
    """
    The frame that receives inputs from the user to feed into queue models
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(InputFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self)

        # put some text with a larger bold font on it
        title = wx.StaticText(pnl, label="Queue simulator")
        font = title.GetFont()
        font.PointSize += 10
        font = font.Bold()
        title.SetFont(font)

        # number of servers
        self.lblserver = wx.StaticText(pnl, label="Number of servers")
        self.editserver = wx.TextCtrl(pnl, size=(140, -1), value="1")

        # lambda
        self.lbllambda = wx.StaticText(pnl, label="Average number of arrivals to the system:")
        self.editlambda = wx.TextCtrl(pnl, size=(140, -1), value="\u03bb".encode('utf-8'))
        
        #Miu
        self.lblmiu = wx.StaticText(pnl, label="Average number of exits from the system:")
        self.editmiu = wx.TextCtrl(pnl, size=(140, -1), value="\u00b5".encode('utf-8'))

        #K 
        self.lblk = wx.StaticText(pnl, label="number of expected clients:")
        self.editk = wx.TextCtrl(pnl, size=(140, -1), value="inf")

        # OK
        self.ok_btn = wx.Button(pnl, label='OK')
        #bind ok_btn to function
        self.ok_btn.Bind(wx.EVT_BUTTON, self.ok_onclick) 

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        sizer.Add(self.lblserver, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        sizer.Add(self.editserver, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        sizer.Add(self.lbllambda, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        sizer.Add(self.editlambda, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        sizer.Add(self.lblmiu, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        sizer.Add(self.editmiu, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        sizer.Add(self.lblk, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        sizer.Add(self.editk, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        sizer.Add(self.ok_btn, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))

        pnl.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to the queue simulator")

    def showError(self, verr):
        err = wx.RichMessageDialog(parent=None, message=f"Error, Enter only integers: \n{verr}", caption="Incorrect Data", style=wx.OK)
        err.ShowModal()

    def ok_onclick(self, event):
        try:
            s = int(self.editserver.GetValue())
            l = int(self.editlambda.GetValue())
            m = int(self.editmiu.GetValue())
            k = self.editk.GetValue()
            if k == "inf":
                res = mms.mms(l, m, 1, s)
            else:
                res = mmsk.get_mmsk(l, m, s, int(k))
            # print(res)
            # print (f"{s}, {l}, {m}")
            resFrame = ResultFrame(self, res)
            resFrame.Show(True)
        except ValueError as verr:
            self.showError(verr)

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "- Check only one box at a time for your respective model\n")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Small usage for user"""
        wx.MessageBox("Welcome to the Queue simulator. Insert values for:\n\t-s := number of servers\n\t-lambda := frequency of arrival\n\t-miu := frequency of clients leaving the system")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("A simple program written for the Quantitative Methods and Simulation class\nTecnológico de Monterrey\nNovember 2020",
                      "About Queue Simulator",
                      wx.OK|wx.ICON_INFORMATION)

class ResultFrame(wx.Frame):
    def __init__(self, parent, resList):
        wx.Frame.__init__(self, parent, -1, "Queue Simulator - Results", size=(275, 275))
        grid = ResultGrid(self, resList)

class ResultGrid(wx.grid.Grid):
    def __init__(self, parent, resList):
        wx.grid.Grid.__init__(self, parent, -1)
        self.CreateGrid(8, 1)
        self.SetColLabelValue(0, "Value")
        self.SetRowLabelValue(0, "P\u2080".encode('utf-8'))
        self.SetRowLabelValue(1, "P\u2099".encode('utf-8'))
        self.SetRowLabelValue(2, "C\u2099".encode('utf-8'))
        self.SetRowLabelValue(3, "\u03c1".encode('utf-8'))
        self.SetRowLabelValue(4, "L")
        self.SetRowLabelValue(5, "W")
        self.SetRowLabelValue(6, "Wq")
        self.SetRowLabelValue(7, "Lq")
        i = 0
        for res in resList:
            self.SetCellValue(i, 0, str(res))
            i += 1

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = InputFrame(None, title='Queue Simulator')
    frm.Show()
    app.MainLoop()
