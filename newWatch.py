import wx
import configparser


class watchListGUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        """Main GUI for the watchlist.

        """
        super(watchListGUI, self).__init__(*args, **kwargs)

        self.conf = confCtrl("config.ini")
        self.size = (512, 512)
        self.Center()
        self.InitUI()

    def InitUI(self):
        # Init Stuff
        self.mainPanel = wx.Panel(self)
        self.mainBox = wx.BoxSizer(wx.VERTICAL)
        self.infoBox = wx.BoxSizer(wx.VERTICAL)
        menuBar = wx.MenuBar()

        # Menubar
        fileMenu = wx.Menu()
        appendItem = fileMenu.Append(wx.ID_ANY,
                                     'Add Show', 'Appends Show')
        updateItem = fileMenu.Append(wx.ID_ANY,
                                     'Updates Config', 'Updates')
        quitItem = fileMenu.Append(wx.ID_EXIT,
                                   'Quit', 'Quit application')

        self.Bind(wx.EVT_MENU, self.quit, quitItem)
        self.Bind(wx.EVT_MENU, self.newShowWrapper, appendItem)
        self.Bind(wx.EVT_MENU, lambda EVT: self.boxUpdate(), updateItem)

        appendBut = wx.Button(self.mainPanel, label="Add Show")
        appendBut.Bind(wx.EVT_BUTTON, self.newShowWrapper)

        # Add Shit
        menuBar.Append(fileMenu, '&File')
        self.mainBox.Add(appendBut, flag=wx.EXPAND | wx.BOTTOM, border=5)

        # Finish
        self.boxInit()
        self.mainBox.Add(self.infoBox)
        self.mainPanel.SetBackgroundColour("#d8bfd8")
        self.SetMenuBar(menuBar)
        self.mainPanel.SetSizer(self.mainBox)
        self.mainPanel.Layout()

    def boxInit(self):
        """Adds info to self.mainBox"""
        showsList = self.conf.parseConf()
        for s in showsList:
            tempS = self.createBox(s)
            self.infoBox.Add(tempS)
        self.mainPanel.Layout()
        pass

    def boxUpdate(self):
        """IT WORKS"""
        infoItems = self.infoBox.GetChildren()
        for i, hi in enumerate(infoItems):
            hi.DeleteWindows()
            self.infoBox.Layout()
            self.Fit()
        self.boxInit()

    def createBox(self, show: dict) -> wx.GridBagSizer:
        sizer = wx.FlexGridSizer(rows=1, cols=5, vgap=5, hgap=5)
        # Probably a better way to do this with dictionary
        nameText = wx.StaticText(self.mainPanel, label=show['Name'])
        urlText = wx.StaticText(self.mainPanel, label=show['URL'])
        stateText = wx.StaticText(self.mainPanel, label=show['State'])
        scoreText = wx.StaticText(self.mainPanel, label=show['Score'])
        epText = wx.StaticText(self.mainPanel, label=show['Episode'])

        sizer.AddMany([(nameText),
                       (urlText),
                       (stateText),
                       (scoreText),
                       (epText)])
        return sizer

    def addShow(self, newShowName, url, dia) -> bool:
        """Add's show to config
        """
        print("Reached addShow func")
        self.conf.appendShow(newShowName, url)
        if dia:
            self.boxUpdate()
            dia.Destroy()
            return True
        else:
            return False
        return True

    def newShowWrapper(self, e):
        """Opens addShowDialog
        """
        newDia = addShowDialog(None, -1, "Add Show", self)
        newDia.Show()
        return True

    def quit(self, e):
        self.Close()


class addShowDialog(wx.Dialog):
    """Dialog for adding a show

    """
    def __init__(self, parent, id: int, title: str, watchList):
        wx.Dialog.__init__(self, parent, id, title)

        sizer = self.CreateTextSizer("")

        # Show name widgets
        showName = wx.TextCtrl(self, style=wx.TE_RICH)
        showNameText = wx.StaticText(self, label="Show's Name")
        # Show URL widgets
        showURL = wx.TextCtrl(self, style=wx.TE_RICH)
        showURLText = wx.StaticText(self, label="Show's URL")
        # Add Show But
        addShowBut = wx.Button(self, label="Add Show")

        sizer.Add(showNameText, 0, wx.ALL, 5)
        sizer.Add(showName, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(showURLText, 0, wx.ALL, 5)
        sizer.Add(showURL, 0, wx.ALL | wx.EXPAND, 5)

        sizer.Add(addShowBut, 0, wx.ALL, 5)

        # Uses an anonymous function to stop wx from autorunning function
        addShowBut.Bind(wx.EVT_BUTTON,
                        lambda evt:
                        watchList.addShow(showName.GetValue(),
                                          showURL.GetValue(),
                                          self))
        self.SetSizer(sizer)


class confCtrl(configparser.ConfigParser):
    """Config Management

    """
    def __init__(self, file="config.ini"):
        super(confCtrl, self).__init__(configparser.ConfigParser())
        self.file = file
        self.currConf = self.parseConf()

    def readFile(self) -> bool:
        with open(self.file, "r", encoding="utf8") as f:
            try:
                self.read_file(f)
                self.sections()
                return True
            except self.Error as err:
                raise Exception(err)
                return False

    def writeFile(self) -> bool:
        with open(self.file, "w", encoding="utf8") as f:
            try:
                self.write(f)
                return True
            except self.Error as err:
                raise Exception(err)
                return False

    def parseConf(self) -> list:
        """Parsers config regarding watchlist info
        """
        parsedDics = []

        self.readFile()

        for sec in self.sections():
            tempDic = {'Name': '',
                       'URL': '',
                       'State': '',
                       'Episode': '',
                       'Score': ''}
            tempDic['Name'] = sec
            # Access the configs num(i) section's URL/STATE/etc.
            tempDic['URL'] = self[sec]['URL']
            tempDic['State'] = self[sec]['State']
            tempDic['Episode'] = self[sec]['Episode']
            tempDic['Score'] = self[sec]['Score']
            parsedDics.append(tempDic)

        return parsedDics

    def appendShow(self, name: str, url=None) -> bool:
        """Adds show to config
        """
        self.readFile()
        self['{}'.format(name)] = {}
        self[name]['URL'] = str(url)
        self[name]['State'] = 'UW'
        self[name]['Episode'] = '0'
        self[name]['Score'] = 'N\\A'
        if self.writeFile():
            return True
        else:
            return False


app = wx.App()
ex = watchListGUI(None, title="AHAHA")
ex.Show()
app.MainLoop()
