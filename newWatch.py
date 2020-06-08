import wx
import configparser


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
        # Create a func later that writes to file
        self.writeFile()


# Holy shit I'm dumb could've just made it a child class FUCK ME
class watchListGUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        """Main GUI for the watchlist.

        """
        super(watchListGUI, self).__init__(*args, **kwargs)

        self.conf = confCtrl("config.ini")
        self.SetTitle("Watchlist")
        self.SetSizer(512, 512)
        self.Center()
        self.InitUI()

    def InitUI(self):
        pass


hi = confCtrl()

print(hi.currConf)
