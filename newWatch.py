import wx
import configparser


class watchListGUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        """Main GUI for the watchlist.

        """
        super(watchListGUI, self).__init__(*args, **kwargs, size=(1024, 1024))

        self.bgColor = "#d8bfd8"
        self.font = wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.Log = LogWindow(self, "Watch List Log")

        self.conf = confCtrl("config.ini")
        self.size = (1024, 1024)
        self.Center()
        self.InitUI()
        # self.Fit()

    def InitUI(self):
        # Init Stuff
        self.mainPanel = wx.Panel(self)
        self.mainBox = wx.BoxSizer(wx.VERTICAL)
        self.infoBox = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour(self.bgColor)
        self.mainPanel.SetBackgroundColour(self.bgColor)
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()

        # Menubar
        appendItem = fileMenu.Append(wx.ID_ANY,
                                     'Add Show', 'Appends Show')
        updateItem = fileMenu.Append(wx.ID_ANY,
                                     'Updates Config', 'Updates')
        logItem = fileMenu.Append(wx.ID_ANY,
                                  'Show Log', 'Inits the Log Window')
        quitItem = fileMenu.Append(wx.ID_EXIT,
                                   'Quit', 'Quit application')

        self.Bind(wx.EVT_MENU, self.quit, quitItem)
        self.Bind(wx.EVT_MENU, self.newShowWrapper, appendItem)
        self.Bind(wx.EVT_MENU, lambda EVT: self.boxUpdate(), updateItem)
        self.Bind(wx.EVT_MENU, self.initLog, logItem)

        appendBut = wx.Button(self.mainPanel, label="Add Show")
        appendBut.Bind(wx.EVT_BUTTON, self.newShowWrapper)

        # Add Shit
        menuBar.Append(fileMenu, '&File')
        self.mainBox.Add(appendBut, flag=wx.EXPAND | wx.BOTTOM, border=5)

        # Finish
        self.boxInit()
        self.mainBox.Add(self.infoBox, flag=wx.EXPAND | wx.ALL, border=5)
        self.SetMenuBar(menuBar)
        self.mainPanel.SetSizer(self.mainBox)
        self.mainPanel.Layout()

    def boxInit(self):
        """Adds info to self.mainBox"""
        showsList = self.conf.parseConf()
        self.mainPanel.Hide()
        for s in showsList:
            tempS = self.createBox(s)
            self.infoBox.Add(tempS)
        self.mainPanel.Show()
        self.mainPanel.Layout()

    def boxUpdate(self):
        """Will delete all info text and re-render them"""
        infoItems = self.infoBox.GetChildren()
        for i, hi in enumerate(infoItems):
            hi.DeleteWindows()
        self.boxInit()
        self.infoBox.Layout()
        # self.Fit()

    def createBox(self, show: dict) -> wx.GridBagSizer:
        """Will create a FlexGridSizer and return it"""
        sizer = wx.GridBagSizer(2, 3)
        # Probably a better way to do this with dictionary

        nameText = wx.StaticText(self.mainPanel, label=show['Name'])
        nameText.SetFont(self.font)
        urlText = wx.StaticText(self.mainPanel, label=show['URL'])
        urlText.SetFont(self.font)
        stateText = wx.StaticText(self.mainPanel, label=show['State'])
        stateText.SetFont(self.font)
        scoreText = wx.StaticText(self.mainPanel, label=show['Score'])
        scoreText.SetFont(self.font)
        epText = wx.StaticText(self.mainPanel, label="E{}".format(show['Episode']))
        epText.SetFont(self.font)
        deleteBut = wx.Button(self.mainPanel, label='Del')
        deleteBut.Bind(wx.EVT_BUTTON,
                       lambda event, temp=show['Name']:
                       self.deleteShowWrapper(show['Name']))

        editBut = wx.Button(self.mainPanel, label='Edit')
        editBut.Bind(wx.EVT_BUTTON,
                     lambda event, temp=show['Name']:
                     self.editShowWrapper(show['Name']))

        sizer.Add(nameText, pos=(0, 0),
                  flag=wx.TOP | wx.RIGHT, border=5)

        if show['URL']:
            sizer.Add(urlText, pos=(1, 0),
                      flag=wx.TOP | wx.LEFT)

        sizer.Add(stateText, pos=(0, 3),
                  flag=wx.TOP | wx.LEFT)
        # sizer.Add(scoreText, pos=(0, 3))
        sizer.Add(epText, pos=(1, 3))
        sizer.Add(editBut, pos=(2, 0), flag=wx.EXPAND | wx.RIGHT)
        sizer.Add(deleteBut, pos=(2, 3), flag=wx.EXPAND | wx.LEFT)

        return sizer

    def deleteShowWrapper(self, name: str):
        self.conf.deleteShow(name)
        self.log("Deleted show: {}".format(name))
        self.boxUpdate()

    def editShowWrapper(self, name: str):
        newDia = editShowDialog(None, -1, name, self.conf, self)
        newDia.Show()
        # self.conf.editShow(name)  # Fuck that's stupid as shit

    def addShow(self, newShowName, url, dia) -> bool:
        """Add's show to config
        """
        self.conf.appendShow(newShowName, url)
        if dia:
            self.boxUpdate()
            dia.Destroy()
            return True
        return True

    def newShowWrapper(self, e):
        """Opens addShowDialog
        """
        newDia = addShowDialog(None, -1, "Add Show", self)
        newDia.Show()
        return True

    def log(self, text: str):
        self.Log.log(text)

    def initLog(self, e):
        self.Log.Show()

    def quit(self, e):
        self.Close()


class editShowDialog(wx.Dialog):
    def __init__(self, parent, id: int, showName: str,
                 conf: configparser.ConfigParser, mainGui: wx.Frame):
        """Dialog for editing a show

        """
        wx.Dialog.__init__(self, parent, id, 'Editting {}'.format(showName))
        self.Centre()
        self.showName = showName
        self.conf = conf
        self.mainGui = mainGui

        sizer = self.CreateTextSizer("")

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.name = wx.TextCtrl(self, style=wx.TE_RICH | wx.EXPAND)
        self.name.AppendText(self.showName)

        self.showURL = wx.TextCtrl(self, style=wx.TE_RICH | wx.EXPAND)
        self.showURL.AppendText(self.conf[self.showName]['URL'])

        self.showState = wx.TextCtrl(self, style=wx.TE_RICH | wx.EXPAND)
        self.showState.AppendText(self.conf[self.showName]['State'])

        self.showEP = wx.TextCtrl(self, style=wx.TE_RICH | wx.EXPAND)
        self.showEP.AppendText(self.conf[self.showName]['Episode'])

        commitEdit = wx.Button(self, label="Commit Edits")
        commitEdit.Bind(wx.EVT_BUTTON, self.setEdit)

        hbox1.Add(self.name)
        hbox1.Add(self.showURL)
        hbox2.Add(self.showState)
        hbox2.Add(self.showEP)

        vbox.AddMany([(hbox1),
                      (hbox2),
                      (commitEdit)])

        # vbox.Add(commitEdit)
        sizer.Add(vbox)

        self.SetSizer(sizer)

    def setEdit(self, e):
        self.conf[self.showName]['URL'] = self.showURL.GetValue()
        self.conf[self.showName]['State'] = self.showState.GetValue()
        self.conf[self.showName]['Episode'] = self.showEP.GetValue()
        self.conf.writeFile()
        self.mainGui.Log.log(
            """Edited: {}:
{}
{}
{}""".format(self.conf[self.showName],
             self.conf[self.showName]['URL'],
             self.conf[self.showName]['State'],
             self.conf[self.showName]['Episode']))
        self.Destroy()
        self.mainGui.boxUpdate()


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


class LogWindow(wx.Dialog):
    """A basic dialog for logging out current processes and info
    """
    def __init__(self, parent, title):
        super(LogWindow, self).__init__(parent, title=title)
        self.InitUI()

    def InitUI(self):
        """Init's UI for LogWindow Class"""
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.logInfo = wx.TextCtrl(panel,
                                   style=wx.TE_READONLY |
                                   wx.TE_MULTILINE |
                                   wx.HSCROLL)

        hbox.Add(self.logInfo, proportion=1, flag=wx.EXPAND)

        panel.SetSizer(hbox)

    def log(self, info: str):
        self.logInfo.AppendText("{}\n".format(info))


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

    def deleteShow(self, name: str):
        self.remove_section(name)
        self.writeFile()

    def appendShow(self, name: str, url=None) -> bool:
        """Adds show to config
        """
        if not name:
            return False
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
