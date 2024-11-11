import shutil
from PGfunctions import readConfig, writeConfig
config = readConfig()
while True:
    if config['runs'] == -1:
        backupRun = input("How many times after updating should we create a back up the database? Press Enter to default to 50: ")
        try:
            if len(backupRun) < 1:
                backupRun = 50
                shutil.copy('MarketData.sqlite', 'MarketDataBackup.sqlite')
                shutil.copy('Sdata.json', 'SdataBackup.json')
                shutil.copy('config.json', 'configBackup.json')
            backupRun = int(backupRun)
            config['backupRun'] = backupRun
            if backupRun < 1:
                print("You must create a backup database in case something unexpected happens")
                continue
            config['runs'] = 0
        except TypeError:
            print("Error: Numbers are accepted only")
            continue
    break

if config['runs'] >= config["backupRun"]:
    shutil.copy('MarketData.sqlite', 'MarketDataBackup.sqlite')
    shutil.copy('Sdata.json', 'SdataBackup.json')
    shutil.copy('config.json', 'configBackup.json')
    config['runs'] = 0
    writeConfig()
