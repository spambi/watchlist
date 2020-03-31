from sys import exit
import configparser
import wx

# Use matrix to put together wx widget and name


class addShowDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title)

        sizer = self.CreateTextSizer('Add Show')

        #sizer.Add(wx.Button(self, -1, 'Show Name'), 0, wx.ALL, 5)
        sizer.Add(wx.Button(self, -1, 'Add Show'), 0, wx.ALL, 5)

        showName = wx.TextCtrl(self, flag=wx.TE_PROCESS_ENTER | wx.TE_RICH)
        sizer.Add(showName, 0, wx.ALL, 5)
        #sizer.Add(wx.Button(self, -1, 'Button'), 0, wx.ALL, 5)
        #sizer.Add(wx.Button(self, -1, 'Button'), 0, wx.ALL, 5)
        #sizer.Add(wx.Button(self, -1, 'Button'), 0, wx.ALL | wx.ALIGN_CENTER,
                  #5)
        sizer.Add(wx.Button(self, -1, 'Button'), 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer)


class Watchlist(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Watchlist, self).__init__(*args, **kwargs)

        self.SetSize(512, 512)
        self.Center()

        self.InitUI()

    def InitUI(self):

        # Menubar
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        appendItem = fileMenu.Append(wx.ID_ANY, 'Add Show', 'Appends Show')
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        menuBar.Append(fileMenu, '&File')
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)
        self.Bind(wx.EVT_MENU, self.NewShow, appendItem)

        # Layout
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetBackgroundColour('#ffffff')

        midPan = wx.Panel(panel)
        midPan.SetBackgroundColour('#000000')

        testBut = wx.Button(panel, label='tetst')
        vbox.Add(testBut, flag=wx.Right | wx.TOP, border=5)
        testBut.Bind(wx.EVT_BUTTON, self.parseConf(self, "config.ini"))

        appendBut = wx.Button(midPan, label='Add Show')
        vbox.Add(appendBut, flag=wx.RIGHT | wx.TOP, border=5)

        appendBut.Bind(wx.EVT_BUTTON, self.NewShow)

        vbox.Add(midPan, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        panel.SetSizer(vbox)

        self.SetTitle("Watchlist")

    def NewShow(self, e):
        testDia = addShowDialog(None, -1, "Add Show")
        testDia.ShowModal()
        testDia.CenterOnScreen()
        testDia.Destroy()
        return True

    def addShow(self, showname, url):
        # Create new window to add show
        # Have showname, url (maybe parse aniDB further on)
        # Append show to config.ini
        # Append new verticalbox to main class
        pass

    def checkDuplicate(self, e):
        pass

    def parseConf(self, e, confCur):
        """Parses through the config.ini file, finding information and
        returning it"""
        # with open(confCur, "r") as f:
        #    c = configparser.ConfigParser()
        #    print(c.sections(f))
        pass

    def OnQuit(self, e):
        self.Close()


def main():
    try:
        japp = wx.App()
        jex = Watchlist(None)
        jex.Show()
        japp.MainLoop()
    except:
        print('idk')
        exit()


main()
