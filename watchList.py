from sys import exit
import configparser
import wx

# Use matrix to put together wx widget and name
config = configparser.ConfigParser()
exurl = 'https://horriblesubs.info/shows/nekopara/'

# Config Defaults
config['DEFAULT'] = {'State': 'UW',  # UW | CW | DW
                     'Episode': '1',
                     'URL': 'https://goat.si',
                     'Score': 'N\\A'}


class addShowDialog(wx.Dialog):
    def __init__(self, parent, id, title, watchList):
        wx.Dialog.__init__(self, parent, id, title)

        sizer = self.CreateTextSizer('Add Show')

        # Show name widgets
        showName = wx.TextCtrl(self, style=wx.TE_RICH)
        showNameText = wx.StaticText(self, label="Show's Name")
        # Show URL widgets
        showURL = wx.TextCtrl(self, style=wx.TE_RICH)
        showURLText = wx.StaticText(self, label="Show's URL")
        # Add Show But
        addShowBut = wx.Button(self, label="Add Show")

        sizer.Add(showName, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(showNameText, 0, wx.ALL, 5)
        sizer.Add(showURL, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(showURLText, 0, wx.ALL, 5)

        sizer.Add(addShowBut, 0, wx.ALL, 5)

        # Use lamda evt to stop wx from autorunning program
        addShowBut.Bind(wx.EVT_BUTTON, lambda evt: watchList.addShow(showName.GetValue(), showURL.GetValue(), self))

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

        midPan = wx.Panel(panel)

        appendBut = wx.Button(midPan, label='Add Show')
        vbox.Add(appendBut, flag=wx.EXPAND | wx.TOP, border=5)

        appendBut.Bind(wx.EVT_BUTTON, self.NewShow)

        vbox.Add(midPan, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        panel.SetSizer(vbox)

        self.SetTitle("Watchlist")

    def NewShow(self, e):
        testDia = addShowDialog(None, -1, "Add Show", self)
        testDia.ShowModal()
        testDia.CenterOnScreen()
        testDia.Destroy()
        return True

    def addShow(self, newShowName, url, dia):
        # Debug
        print('Reached addShow func')
        newShowSec = configparser.ConfigParser()
        # Make sure config is not overwritten
        with open('config.ini', 'r', encoding="utf8") as curFile:
            try:
                newShowSec.read_file(curFile)
            except configparser.Error as err:
                raise Exception(err)
                return False

        newShowSec['{}'.format(newShowName)] = {}
        newShowSec[newShowName]['URL'] = '{}'.format(url)
        newShowSec[newShowName]['State'] = 'UW'
        # Episode required for later config
        newShowSec[newShowName]['Episode'] = '1'
        newShowSec[newShowName]['Score'] = 'N\\A'
        with open('config.ini', 'w', errors='ignore') as curFile:
            newShowSec.write(curFile)
            print('wrote to file')
            if dia:
                dia.Destroy()

    def checkDuplicate(self, a, b):
        if a in b:
            return False
        else:
            return True
        pass

    def parseConf(self, e, confCur):
        """Parses through the config.ini file, finding information and
        returning it"""
        with open(confCur, "r") as f:
            c = configparser.ConfigParser()
            c.read_file(f)
            c.sections()
            return c
        pass

    def OnQuit(self, e):
        self.Close()


def main():
    try:
        app = wx.App()
        ex = Watchlist(None)
        ex.Show()
        app.MainLoop()
    except:
        print('idk')
        exit()


main()
