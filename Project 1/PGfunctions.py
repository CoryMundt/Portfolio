import coinbase
from coinbase.rest import RESTClient
import json
from MarketDataTables import MarketDataTable
import time
import re
from datetime import datetime
import pytz


def readData():
    global data
    try:
        #will only fail first run when json file is empty
        with open('Sdata.json', 'r') as file:
            data = json.load(file)
        return data
    except:
        with open('Sdata.json', 'w') as file:
            json.dump({}, file, indent=4)
        with open('Sdata.json', 'r') as file:
            data = json.load(file)
        return data
def writeData():
    global data
    with open('Sdata.json', 'w') as file:
        json.dump(data, file, indent=4)


def readConfig():
    global config
    try:
        # will only fail first run when json file is empty
        with open('config.json', 'r') as file:
            config = json.load(file)
        return config
    except:
        with open('config.json', 'w') as file:
            json.dump({"checkpoint": None, "lastStartDate": "",  "runs": -1, "backupRun": 50}, file, indent=4)
        with open('config.json', 'r') as file:
            config = json.load(file)
    return config

def writeConfig():
    global config
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)
### ignore not used in portfolio code
def get30past():
    dtime = datetime.now()
    Unix_TDPtime = time.mktime(dtime.timetuple()) - 2592000
    TDPtime = datetime.fromtimestamp(Unix_TDPtime)
    print("Date and Time Defaulted to : " + str(TDPtime))
    return TDPtime
### ignore not used in portfolio code
def getmidnight():
    dnow = datetime.now()
    dtime = datetime(dnow.year, dnow.month, dnow.day, 0,0,0)
    Unix_TDPtime = time.mktime(dtime.timetuple())
    TDPtime = datetime.fromtimestamp(Unix_TDPtime)
    print("Date and Time Defaulted to : " + str(TDPtime))
    return TDPtime
def getnumbers(userinput):
    return re.sub("[^0-9^.]", "", userinput)

# gets rid of 0 when inputting date like 05 for may or day 5 of whatever month
def checkfrontzero(timevar):
    if timevar.startswith("0"):
        timevar = int(timevar[1])
    else:
        timevar = int(timevar)
    return timevar
### ignore not used in portfolio code
def getdatetimerange(acronym):
    #note to self to update zero date to fetch first row of acronym 15 min canlde table, get unix, and convert that to datetime object to get zero date
    zerodate = datetime(2009, 1, 3)
    noneentered = False
    while True:
        while True:
            # Get Start Date
            try:
                Sinputdate = input("Enter Start date as MM-DD-YYYY, or press Enter to default the starting time to 30 days prior from now: ")
                if len(Sinputdate) < 1:
                    Sdatetime = get30past()
                    Sdate = datetime(Sdatetime.year, Sdatetime.month, Sdatetime.day)
                    noneentered = True
                    break
                elif Sinputdate == '/':
                    Sdatetime = getmidnight()
                    Sdate = datetime(Sdatetime.year, Sdatetime.month, Sdatetime.day)
                    noneentered = True
                    break
                else:
                    Sinputdate = getnumbers(Sinputdate)
                    Syear = int(Sinputdate[4:])
                    Smonth = Sinputdate[0:2]
                    Sday = Sinputdate[2:4]
                    Smonth = checkfrontzero(Smonth)
                    Sday = checkfrontzero(Sday)
                    Sdate = datetime(Syear, Smonth, Sday)
                    if Sdate < zerodate:
                        print("Error: Date Entered must be later than 01/03/2009")
                        continue
                    break
            except (ValueError, IndexError):
                print("Error: Invalid Date Entered")
                continue
        while True:
            if noneentered is True:
                noneentered = False
                break
            # Get Start time
            try:
                Sinputtime = input("Enter starting time as HH:MM (In 24hr format), if no time is entered, the starting time will default to midnight:")
                if len(Sinputtime) < 1:
                    Sdatetime = Sdate
                    break
                elif len(Sinputtime) > 5:
                    print("Error: Invalid Time Entered")
                    continue
                else:
                    Sinputtime = getnumbers(Sinputtime)
                    Shour = checkfrontzero(Sinputtime[0:2])
                    Sdatetime = datetime(Sdate.year, Sdate.month, Sdate.day, Shour, int(Sinputtime[2:]))
                    if Sdatetime > datetime.now():
                        print("Error: Starting time must be at least 1 minute before current time")
                        continue
                    print("Starting Date and Time: " + str(Sdatetime))
                    break
            except (ValueError, IndexError):
                print("Error: Invalid Time Entered")
                continue

        while True:
            try:
                #Get End Date
                Einputdate = input("Enter End date as MM-DD-YYYY, or press Enter to default to current date and time: ")
                if len(Einputdate) < 1:
                    Edatetime = datetime.now()
                    noneentered = True
                    break
                else:
                    Einputdate = getnumbers(Einputdate)
                    Eyear = int(Einputdate[4:])
                    Emonth = Einputdate[0:2]
                    Eday = Einputdate[2:4]
                    Emonth = checkfrontzero(Emonth)
                    Eday = checkfrontzero(Eday)
                    Edate = datetime(Eyear, Emonth, Eday)
                    if Edate < Sdate:
                        print("Error: End date must be the same or after Start date")
                        continue
                    break
            except (ValueError, IndexError):
                print("Error: Invalid Date Entered")
                continue
        while True:
            if noneentered is True:
                noneentered = False
                break
            try:
                #Get End Time
                Einputtime = input("Enter Ending time as HH:MM (In 24hr format), if no time is entered, the Ending time will default to 11:59:")
                if len(Einputtime) < 1:
                    Edatetime = datetime(Edate.year, Edate.month, Edate.day, 23, 59)
                    break
                elif len(Einputtime) > 5:
                    print("Error: Invalid Time Entered")
                    continue
                else:
                    Einputtime = getnumbers(Einputtime)
                    Ehour = checkfrontzero(Einputtime[0:2])
                    Edatetime = datetime(Edate.year, Edate.month, Edate.day, Ehour, int(Einputtime[2:]))
                    if Sdatetime >= Edatetime > datetime.now():
                        print("Error: Ending time must be after starting time and not after current time: ")
                        continue
                    print("Ending Date and Time: " + str(Edatetime))
                    break
            except (ValueError, IndexError):
                print("Error: Invalid Time Entered")
                continue
        break
    print("Starting Date and Time: " + str(Sdatetime) + " Ending Date and Time: " + str(Edatetime))
    return (int(Sdatetime.timestamp()), int(Edatetime.timestamp()), Sdatetime.replace(tzinfo=pytz.UTC).timestamp(), Edatetime.replace(tzinfo=pytz.UTC).timestamp())

### this function gets the start date for the data tables from the user when creating a new crypto in the Data base as all
def getStartTime():
    #get unix timestamp of now
    Ctime = int(time.mktime(datetime.now().timetuple()))
    ### 189345600 is 6 years worth of seconds
    zerodate = Ctime - 157680000
    start = None
    config = readConfig()
    while True:
        # Get Start Date
        try:
            Sinput = input("Enter Start date as MM-DD-YYYY, press Enter to default to last date used:")
            if len(Sinput) < 1:
                Sinput = config["lastStartDate"]
                if len(Sinput) < 1:
                    print("Error: No prior start date exists")
                    continue
                Sinputdate = getnumbers(Sinput)
                Syear = int(Sinputdate[4:])
                Smonth = Sinputdate[0:2]
                Sday = Sinputdate[2:4]
                Smonth = checkfrontzero(Smonth)
                Sday = checkfrontzero(Sday)
                Sdate = datetime(Syear, Smonth, Sday)
                if int(time.mktime(Sdate.timetuple())) < zerodate:
                    print("Error: Date Entered must be within 5 years prior")
                    continue
                start = int(Sdate.timestamp())
                config["lastStartDate"] = Sinput
                writeConfig()
                return start, Sinput
            else:
                Sinputdate = getnumbers(Sinput)
                Syear = int(Sinputdate[4:])
                Smonth = Sinputdate[0:2]
                Sday = Sinputdate[2:4]
                Smonth = checkfrontzero(Smonth)
                Sday = checkfrontzero(Sday)
                Sdate = datetime(Syear, Smonth, Sday)
                if int(time.mktime(Sdate.timetuple())) < zerodate:
                    print("Error: Date Entered must be within 6 years prior")
                    continue
                start = int(Sdate.timestamp())
                config["lastStartDate"] = Sinput
                writeConfig()
                return start, Sinput
        except (ValueError, IndexError):
            print("Error: Invalid Date Entered")
            continue

### goes with update15minCandles, fetches 350 candles of data from coinbase api
def getCoinbaseMarketData(RestClient, crypto_market, Start, End, Timeunit, cursor, connection):
    def insertBatch():
        cursor.executemany(f'INSERT OR IGNORE INTO {table} (Unix, Low, High, Open, Close, Volume) VALUES(?, ?, ?, ?, ?, ?)', batch)
        connection.commit()
        batch.clear()
    MarketData = coinbase.rest.RESTClient.get_candles(RestClient, crypto_market, Start, End, Timeunit)
    table = f'{crypto_market.replace('-', '_')}_FIFTEEN_MINUTE_CANDLES'
    i = 0
    batch = []
    for item in reversed(MarketData['candles']):
        batch.append((item['start'], item['low'], item['high'], item['open'], item['close'], str(int(float(item['volume'])))))
        i += 1
        if i == 50:
            insertBatch()
            i = 0
    insertBatch()
def update15minCandles(acronym, client, cursor, connection):
    end = None
    start = None
    global data, config
    table = from_dict(data[acronym]["tables"]["15min"])
    ### The program fetches each 15 minute candle, the last candle is rarely a full 15 min
    ### this deletes the last candle of prev run to fetch the complete candle this run
    if data[acronym]['gotData']:
        cursor.executescript(f'''
                DELETE FROM {table.name} WHERE Id = (SELECT max(Id) FROM {table.name});
                UPDATE sqlite_sequence SET seq = (SELECT max(Id) FROM {table.name}) WHERE name = "{table.name}";''')
    else:
        temp = getStartTime()
        print('Getting data.....this may take a few minutes depending on start date set')
        start = str(temp[0])
        end = str(int(start) + 315000)
        config['lastStartDate'] = temp[1]
        writeConfig()
    print(f"Updating.... {table.name}")
    timeunit = 'FIFTEEN_MINUTE'
    cryptoMarket = acronym + '-USD'

    ### api only allows 350 candles to be fetched at one time also deletes previous created tables for bad acronym
    while True:
        if data[acronym]['gotData']:
            break
        try:
            getCoinbaseMarketData(client, cryptoMarket, start, end, timeunit, cursor, connection)
            data[acronym]['gotData'] = True
            data[acronym]['prevStart'] = start
            writeData()
            break
        except Exception as a:
            print(f"An error occurred: {a}")
            connection.rollback()
            quit()

    prevStart = int(data[acronym]['prevStart'])
    Ctime = int(time.mktime(datetime.now().timetuple()))
    ### coinbase get_candles requires unix time integers in the form of strings
    while True:
        try:
            cursor.execute(f'SELECT Unix FROM {table.name} WHERE Id = (SELECT max(Id) FROM {table.name})')
            row = cursor.fetchone()[0]
            start = str(int(row) + 1)
            #31500 = the ammount of seconds in 350 15 min candles
            end = str(int(start) + 315000)
            if int(end) > Ctime:
                end = str(Ctime)
                getCoinbaseMarketData(client, cryptoMarket, start, end, timeunit, cursor, connection)
                data[acronym]['prevStart'] = start
                print("Success!")
                break
            getCoinbaseMarketData(client, cryptoMarket, start, end, timeunit, cursor, connection)
            data[acronym]['prevStart'] = start
            prevStart = start
            continue
        except KeyboardInterrupt:
            print('Program interrupted by user...')
            connection.rollback()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
    writeData()

### turns MarketDataTable Object Into Dict before storing in json file in specific format so that it may be converted back
def to_dict(self):
    return {
        "acronym" : self.acronym,
        "timeunit": self.timeunit,
        "denomination": self.denomination,
        "name": self.name,
     }
### Converts dictionary back to MarketDataTable object
def from_dict(self):
    return MarketDataTable(
        acronym = self["acronym"],
        timeunit = self["timeunit"],
        denomination = self["denomination"],
        name = self["name"]
    )

# google variable names for functions in this case
def createDefaultCandleTables(acronym, cursor):
    tables = ["15min", "30min", "1hour", "6hour", "12hour", "1day", "7day", "14day", "30day", "60day", "90day"]
    newTables = dict()
    for table in tables:
        denom = int(re.sub(r'\D+', '', table))
        timeunit = re.sub(r'\d+', '', table)
        newDataTable = MarketDataTable(acronym, timeunit, denom)
        name = newDataTable.name
        newDataTable = to_dict(newDataTable)
        newTables[table] = newDataTable
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
    return newTables




### update all other tables besides 15 minutes, as all other tables are derived from the 15 min table
def updateOtherTable(acronym, sourceTable, table, cursor, connection, iRowLimit=2):
    def maxRow(anyTable):
        cursor.execute(f'SELECT * FROM {anyTable} WHERE Id = (SELECT max(Id) FROM {anyTable})')
        row = cursor.fetchone()
        try:
            maxRow = row[0]
        except TypeError:
            maxRow = 0
        return maxRow
    def getRow(i):
        cursor.execute(f'SELECT * FROM {sourceTable} WHERE Id = ?', (i,))
        row = cursor.fetchone()
        return row
    def insertBatch():
        cursor.executemany(f'INSERT OR IGNORE INTO {table} (Unix, Low, High, Open, Close, Volume) VALUES(?, ?, ?, ?, ?, ?)', batch)
        connection.commit()
        batch.clear()
    print(f"Updating.... {table}")
    #save cursorrent starting row in case user wants to cancel
    cursor.executescript(f'''
            DELETE FROM {table} WHERE Id = (SELECT max(Id) FROM {table});
            UPDATE sqlite_sequence SET seq = (SELECT max(Id) FROM {table}) WHERE name = "{table}"
        ''')
    ### ensures program picks up where it left off, even in case of unintended interruption
    startRow = maxRow(table)

    if startRow == 0:
        i = 0
    else:
        i = startRow * iRowLimit
    lastRow = maxRow(sourceTable)
    batch = []
    n = 0
    try:
        ### the loop is for condensing candles into a single candle of longer time period
        while True:
            i += 1
            n+=1
            if i > lastRow:
                break
            ### Unix and Open Values are always taken from 1st row in iteration, the rest will be updated
            row = getRow(i)
            Unix = row[1]
            Low = row[2]
            High = row[3]
            Open = row[4]
            Close = row[5]
            Volume = row[6]
            r = 1
            ### iRowLimit is how many candles from the source table fits into that time period
            ### e.g. 15 min candle source table into 30 min source table, iRowLimit = 2
            while r < iRowLimit:
                if i == lastRow:
                    batch.append((Unix, Low, High, Open,- Close, Volume))
                    break
                i += 1
                n+=1
                row = getRow(i)
                Low2 = row[2]
                High2 = row[3]
                if High2 > High:
                    High = High2
                if Low2 < Low:
                    Low = Low2
                Volume = Volume + row[6]
                Close = row[5]
                r += 1
            batch.append((Unix, Low, High, Open, Close, Volume))
            if n >= 50:
                n = 0
                insertBatch()
        insertBatch()
        print("Success!")
    except KeyboardInterrupt:
        print('Program interrupted by user....')
        cursor.execute(f"DELETE FROM TABLE {table} WHERE Id >= {startRow + 1}")
        connection.commit()

