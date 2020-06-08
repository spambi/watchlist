#!/usr/bin/env pythonimport configparser
import wx
import configparser

# Use matrix to put together wx widget and name
config = configparser.ConfigParser()
showsDicts = []

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

        # Uses an anonymous function to stop wx from autorunning function
        addShowBut.Bind(wx.EVT_BUTTON, lambda evt: watchList.addShow(showName.GetValue(), showURL.GetValue(), self))

        self.SetSizer(sizer)


class Watchlist(wx.Frame):
    # Set class public variables here
    vbox = wx.BoxSizer(wx.VERTICAL)
    panel = None

    def __init__(self, *args, **kwargs):
        super(Watchlist, self).__init__(*args, **kwargs)

        self.panel = wx.Panel(self)
        self.SetTitle("Watchlist")
        self.InitUI()
        self.SetSize(512, 512)
        self.Center()

    def InitUI(self):
        # Sizer for show's and info
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        butSizer = wx.BoxSizer(wx.HORIZONTAL)
        showSizer = wx.BoxSizer(wx.VERTICAL)

        # Menubar
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        appendItem = fileMenu.Append(wx.ID_ANY, 'Add Show', 'Appends Show')
        refreshShows = fileMenu.Append(wx.ID_ANY, 'Refresh Contents',
                                       'Will refresh the show\'s contents')
        clearBox = fileMenu.Append(wx.ID_ANY, 'Clear', 'clears shit')
        quitGUI = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        menuBar.Append(fileMenu, '&File')
        self.SetMenuBar(menuBar)

        self.refreshShowsGUI(showSizer)
        self.Bind(wx.EVT_MENU, self.OnQuit, quitGUI)
        self.Bind(wx.EVT_MENU, self.NewShow, appendItem)
        # lambda EVT to stop to stop wx auto running functions
        self.Bind(wx.EVT_MENU, lambda evt: self.clearSizerElements(showSizer), clearBox)
        self.Bind(wx.EVT_MENU, lambda evt: self.refreshShowsGUI(showSizer), refreshShows)

        appendBut = wx.Button(self.panel, label='Add Show')
        butSizer.Add(appendBut, flag=wx.EXPAND | wx.BOTTOM, border=5)
        appendBut.Bind(wx.EVT_BUTTON, self.NewShow)

        mainSizer.Add(showSizer)
        mainSizer.Add(butSizer)

        self.panel.SetSizer(mainSizer)

    def NewShow(self, e):
        """Opens the addShowDialog class"""
        newshowDia = addShowDialog(None, -1, "Add Show", self)
        newshowDia.ShowModal()
        newshowDia.Destroy()
        return True

    def addShow(self, newShowName, url, dia):
        """Will interact with config file and add necessary details"""
        # Debug
        print('Reached addShow func')
        newShowSec = configparser.ConfigParser()
        # Make sure config is not overwritten
        with open('config.ini', 'r', encoding="utf8") as curFile:
            try:
                newShowSec.read_file(curFile)
                newShowSec.sections()
            except configparser.Error as err:
                raise Exception(err)
                return False

        # Formatting of dict for config
        newShowSec['{}'.format(newShowName)] = {}
        newShowSec[newShowName]['URL'] = '{}'.format(url)
        newShowSec[newShowName]['State'] = 'UW'
        newShowSec[newShowName]['Episode'] = '1'
        newShowSec[newShowName]['Score'] = 'N\\A'
        # Open file for writing
        with open('config.ini', 'w', errors='ignore') as curFile:
            newShowSec.write(curFile)
            print('wrote to file')
        # Check if the is still running and close it
        if dia:
            dia.Destroy()

    def clearSizerElements(self, sizer):
        # Use true in wx functinos for it to be recursive
        try:  # If no try was here, and used twice in a row, crash GUI
            sizer.Clear(True)
            sizer.Destroy(True)
        except:
            pass

    def refreshShowsGUI(self, sizer):
        """Will retrieve shows and display them in the show sizer"""
        # Retrieve items needed for config
        conf = confCtrl("config.ini")
        conf.readFile()
        shows = conf.parseConf()
        currentName = conf.getShowNames(shows)
        self.Refresh()

        # Iterate through shows and pipe them into self.createShowBox()
        self.clearSizerElements(sizer)
        for i, ele in enumerate(currentName):
            sizer.Add(self.createShowBox(shows, currentName[i], i),
                      flag=wx.EXPAND)
        sizer.Layout()

    def createShowBox(self, showDict, showName, iteration=0):
        """Will create a box of a show from the config file, and
        return it"""
        # Create box sizer
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        # Creates text from show's name dic
        # CURRENT: TYPE ERROR FOR LINE BELOW FUCK THIS PIECE OF SHIT LMAO
        tempName = wx.StaticText(self.panel, label=showDict[iteration]['Name'],
                                 style=wx.ALIGN_LEFT)
        tempURLS = wx.StaticText(self.panel,
                                 label=showDict[iteration]['URL'])
        tempState = wx.StaticText(self.panel,
                                  label=showDict[iteration]['State'])
        tempEp = wx.StaticText(self.panel,
                               label=showDict[iteration]['Episode'])
        tempScore = wx.StaticText(self.panel,
                                  label=showDict[iteration]['Score'])
        # This adds the static text to the boxsizer
        hbox.Add(tempName, flag=wx.RIGHT | wx.EXPAND, border=8)
        hbox.Add(tempURLS, flag=wx.RIGHT | wx.EXPAND, border=8)
        hbox.Add(tempState, flag=wx.RIGHT | wx.EXPAND, border=8)
        hbox.Add(tempEp, flag=wx.RIGHT | wx.EXPAND, border=8)
        hbox.Add(tempScore, flag=wx.RIGHT | wx.EXPAND, border=8)
        # Returns the sizer
        print('returning hbox')
        return hbox

    def editShow(self, showBox):
        """Will open a dialog to edit a show """
        pass

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


class confCtrl():

    config = configparser.ConfigParser()
    file = None

    def __init__(self, file, **kwargs):
        # self.read_file("config.ini")
        self.file = file
        pass

    def checkDuplicate(self, e):
        pass

    def getShowNames(self, showsList):
        """Basic loop to get showname list"""
        tempList = []
        for show in showsList:
            tempList.append(show['Name'])
        return tempList

    def parseConf(self):
        """Parses through the config.ini file, finding information and
        returning it as a dictionary"""
        parsedDics = []

        # Reads from specified file set in class def
        with open(self.file, "r", encoding="utf8") as f:
            self.config.read_file(f)
            self.config.sections()
            # Change this for more pythonic code like for loop
            for sec in self.config.sections():
                tempDic = {'Name': '',
                           'URL': '',
                           'State': '',
                           'Episode': '',
                           'Score': ''}
                tempDic['Name'] = sec
                # Access the configs num(i) section's URL/STATE/etc.
                tempDic['URL'] = self.config[sec]['URL']
                tempDic['State'] = self.config[sec]['State']
                tempDic['Episode'] = self.config[sec]['Episode']
                tempDic['Score'] = self.config[sec]['Score']

                parsedDics.append(tempDic)

        return parsedDics

    def readFile(self):
        """Will read the contents of the file"""
        testconfig = configparser.ConfigParser()
        print('hi')
        try:
            with open(self.file, 'r', encoding="utf8") as f:
                testconfig.read_file(f)
                testconfig.sections()
                print(testconfig.sections())
        except configparser.Error as err:
            print('[-] Something went wrong')
            raise(err)


def main():

    app = wx.App()
    ex = Watchlist(None)
    ex.Show()
    app.MainLoop()


main()
