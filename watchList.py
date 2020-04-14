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
        showSizer = wx.BoxSizer(wx.VERTICAL)
        # Initial import of show info

        # Menubar
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        appendItem = fileMenu.Append(wx.ID_ANY, 'Add Show', 'Appends Show')
        refreshShows = fileMenu.Append(wx.ID_ANY, 'Refresh Contents',
                                       'Will refresh the show\'s contents')
        clearBox = fileMenu.Append(wx.ID_EXIT, 'Clear', 'clears shit')
        quitGUI = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        menuBar.Append(fileMenu, '&File')
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnQuit, quitGUI)
        self.Bind(wx.EVT_MENU, self.NewShow, appendItem)
        self.Bind(wx.EVT_MENU, self.refreshShowsGUI(showSizer), refreshShows)
        self.Bind(wx.EVT_MENU, lambda evt: self.clearElements(showSizer), clearBox)

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        #appendBut = wx.Button(self.panel, label='Add Show')
        #showSizer.Add(appendBut, flag=wx.EXPAND | wx.BOTTOM, border=5)

        #appendBut.Bind(wx.EVT_BUTTON, self.NewShow)

        self.panel.SetSizer(showSizer)

    def NewShow(self, e):
        """Opens the addShowDialog class"""
        newshowDia = addShowDialog(None, -1, "Add Show", self)
        newshowDia.ShowModal()
        newshowDia.CenterOnScreen()
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

    def clearElements(self, sizer):
        # True for recursive
        try:
            sizer.Clear(True)
            sizer.Destroy(True)
            sizer.Layout()
            print(sizer)
        except:
            pass

    def refreshShowsGUI(self, boxSizer):
        """Will retrieve shows and display them in the show sizer"""
        # Retrieve items needed for config
        conf = confCtrl("config.ini")
        shows = conf.parseConf()
        currentName = conf.getShowNames(shows)
        # Iterate through shows and pipe them into self.createShowBox()
        print("got here")
        for i, ele in enumerate(currentName):

        #for i in range(0, len(conf.getShowNames(shows))):
            boxSizer.Add(self.createShowBox(shows, currentName[i], i),
                         flag=wx.EXPAND)
        pass

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
                                 label=showDict[iteration]['URL'],
                                 style=wx.ALIGN_RIGHT)
        tempState = wx.StaticText(self.panel,
                                  label=showDict[iteration]['State'])
        tempEp = wx.StaticText(self.panel,
                               label=showDict[iteration]['Episode'])
        tempScore = wx.StaticText(self.panel,
                                 label=showDict[iteration]['Score'])
        # This adds the static text to the boxsizer
        hbox.Add(tempName, flag=wx.RIGHT | wx.EXPAND, border=8)
        hbox.Add(tempURLS, flag=wx.LEFT | wx.EXPAND, border=8)
        hbox.Add(tempState, flag=wx.EXPAND | wx.RIGHT, border=8)
        hbox.Add(tempEp, flag=wx.EXPAND | wx.RIGHT, border=8)
        hbox.Add(tempScore, flag=wx.EXPAND | wx.RIGHT, border=8)
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

    def __init__(self, file, **kwargs):
        # self.read_file("config.ini")
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
        with open("config.ini", "r", encoding="utf8") as f:
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


def main():

    app = wx.App()
    ex = Watchlist(None)
    ex.Show()
    app.MainLoop()


main()
