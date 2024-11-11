import sqlite3
from PGfunctions import readData,  from_dict, writeData, to_dict
from MarketDataTables import MarketDataTable
import subprocess
import sys
from pathlib import Path

### this file is for user to create tables not inlcuded in default list
### ["15min", "30min", "1hour", "6hour", "12hour", "1day", "7day", "14day", "30day", "60day", "90day"]
while True:
    run = input("Would you like to create a table not included by default? Y/N: ")
    if run.upper() not in ('Y', 'N'):
        continue
    else:
        if run == "N":
            quit()
        else:
            break

conn = sqlite3.connect('MarketData.sqlite')
cur = conn.cursor()
data = readData()


def createTables():
    global data
    def createCandleTable(acronym, timeunit, denom, cursor):
        global data
        if timeunit.lower() not in ("hour", "day", "min"):
            raise ValueError("Invalid value. Allowed values are min, hour, day")
        newDataTable = MarketDataTable(acronym, timeunit, denom)
        name = newDataTable.name
        newDataTable = to_dict(newDataTable)
        key = str(denom) + timeunit
        data[acronym]["tables"][key] = newDataTable
        cursor.executescript(f'''
                              CREATE TABLE IF NOT EXISTS {name}(
                              Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                              Unix TEXT Unique,
                              Low DECIMAL(4, 6),
                              High DECIMAL(4, 6),
                              Open DECIMAL(4, 6),
                              Close DECIMAL(4, 6),
                              Volume INTEGER
                              );
                              ''')
    while True:
        acronym = input("Enter 3 letter acronym for the crypto you would like to add a table to, if you want to add this table to all cryptos press Enter: ")
        acronym = acronym.upper()
        if len(acronym) < 1:
            break
        if acronym not in data:
            print("Error: Crypto does not exist in database")
            continue
        break
    while True:
        timeunit = input("Enter timeunit for candles, Hour/Day: ")
        if timeunit.lower() not in ('hour', 'day'):
            print('Error: Invalid timeunit')
            continue
        else:
            break
    while True:
        denom = input("Enter how many hours or days a candle should be: ")
        try:
            denom = int(denom)
            if denom % 1 != 0:
                print("Error: Please enter a whole number")
                continue
            break
        except:
            print("Error: Please enter a whole number")
            continue
    key = str(denom) + timeunit

    def checkCreate():
        try:
            from_dict(data[acronym]['tables'][key])
            print('Table already exists')
        except:
            createCandleTable(acronym, timeunit, denom, cur)

    firstLoop = True
    if len(acronym) > 1:
        while True:
            if not firstLoop:
                acronym = input("Would your like to create this same table for another crypto? If so input acronym, if not, press Enter: ")
                acronym = acronym.upper()
                if len(acronym) < 1:
                    break
            checkCreate()
            print("Table Created")
            firstLoop = False
    else:
        for acronym in data:
            print("Creating tables...")
            checkCreate()
            print("Done")
def sortData():
    global data
    def sortKey(item):
        ### MDT means MarketDataTable object
        MDT = from_dict(item[1])
        timeunitPriority = {"min": 0, "hour": 1, "day": 2}
        return (timeunitPriority[MDT.timeunit], MDT.denomination)

    for crypto in data:
        sortedTables = dict(sorted(data[crypto]["tables"].items(), key=sortKey))
        data[crypto]["tables"] = sortedTables
    writeData()

createTables()

while True:
    user = input("Would you like to create another table? Y/N: ")
    if user.upper() == "Y":
        createTables()
    elif user.upper() == "N":
        break
    else:
        print("Enter Y or N")
        continue

sortData()

venv_python = Path(sys.executable)
subprocess.run([venv_python, "UpdateTables.py"])
conn.close()
