import configparser

config = configparser.ConfigParser()


tempDic = {'Name': 'NekoPara',
           'URL': 'aha',
           'State': 'UW',
           'Episode': '1',
           'Score': '10'}

with open("config.ini", "r", encoding="utf8") as file:
    config.read_file(file)
    for i, sec in enumerate(config.sections()):
        print(tempDic['Name'])