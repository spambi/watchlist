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

        self.SetSize(512, 512)
        self.Center()
        self.SetTitle("Watchlist")
        self.panel = wx.Panel(self)
        self.InitUI()

    def InitUI(self):

        test = confCtrl("config.ini")
        shows = test.parseConf()
        currentName = test.getShowNames(shows)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # Use this just so it doesn't have to parse twice
        for i in range(0, len(test.getShowNames(shows))):
            sizer.Add(self.createShowBox(shows, currentName[i], i), flag=wx.EXPAND)
        #sizer.Add(self.createShowBox(shows, currentName[0], 0), flag=wx.EXPAND)

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
        #panel = wx.Panel(self)

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        appendBut = wx.Button(self.panel, label='Add Show')
        sizer.Add(appendBut, flag=wx.EXPAND | wx.BOTTOM, border=5)

        appendBut.Bind(wx.EVT_BUTTON, self.NewShow)

        self.panel.SetSizer(sizer)

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
        with open('config.ini', 'r') as curFile:
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
        with open('config.ini', 'w') as curFile:
            newShowSec.write(curFile)
            print('wrote to file')
            if dia:
                dia.Destroy()

    def createShowBox(self, showDict, showName, iteration):
        """Will create a box of a show from the config file, and
        return it"""
        # Create box sizer
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        # Creates text from show's name dic
        # CURRENT: TYPE ERROR FOR LINE BELOW FUCK THIS PIECE OF SHIT LMAO
        tempName = wx.StaticText(self.panel, label=showDict[iteration]['Name'],
                                 style=wx.ALIGN_LEFT)
        tempURLS = wx.StaticText(self.panel, label=showDict[iteration]['URL'],
                                 style=wx.ALIGN_RIGHT)
        #tempState = wx.StaticText(panel, label=showDict[iteration]['State'])
        #tempEp = wx.StaticText(panel, label=showDict[iteration]['Episode'])
        #tempScore = wx.StaticText(panel, label=showDict[iteration]['Score'])
        # This adds the static text to the boxsizer
        hbox.Add(tempName, flag=wx.RIGHT | wx.EXPAND, border=8)
        hbox.Add(tempURLS, flag=wx.LEFT | wx.EXPAND, border=8)
        #hbox.Add(tempState, flag=wx.EXPAND | wx.EXPAND, border=8)
        #hbox.add(tempep, flag=wx.top | wx.expand, border=8)
        #hbox.Add(tempScore, flag=wx.BOTTOM | wx.EXPAND, border=8)
        # Returns the sizer
        print('returning hbox')
        return hbox

    def OnQuit(self, e):
        self.Close()


class confCtrl():

    config = configparser.ConfigParser()
    #fr = open('config.ini', 'r')
    #fw = open('config.ini', 'w')

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
