import os
from dotenv import find_dotenv, load_dotenv
from coinbase.rest import RESTClient
import sqlite3
from PGfunctions import update15minCandles, readData, updateOtherTable, from_dict, to_dict, readConfig, writeConfig
import shutil

conn = sqlite3.connect('MarketData.sqlite')
cur = conn.cursor()
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

api_key = os.getenv("api_key")
secret_key = os.getenv("api_secret")
client = RESTClient(api_key=api_key, api_secret=secret_key, timeout=5)

data = readData()
config = readConfig()
# checkpoint is the last completed/updated table saved in config.json in case program is interrupted
checkpoint = config['checkpoint']
runs = config['runs']


try:
    resume = False
    ### checkpoint is None means the last run completed
    if checkpoint is None:
        resume = True
    for crypto in data:
        #see Sdata.json file for dict format
        try: tables = data[crypto]['tables']
        except: quit()
        for key, table in tables.items():
            table = from_dict(table)
            if not resume:
                if table != checkpoint:
                    continue
                else:
                    resume = True
                    continue
            else:
                ###these are the first tables of their respected time units and therfore are special cases
                if key == "15min":
                    update15minCandles(crypto, client, cur, conn)
                    checkpoint = to_dict(table)
                    continue
                if key == "1hour":
                    sourceTable = from_dict(data[crypto]['tables']['30min'])
                    updateOtherTable(crypto, sourceTable.name, table.name, cur, conn)
                    checkpoint = to_dict(table)
                    continue
                if key == "1day":
                    sourceTable = from_dict(data[crypto]['tables']['12hour'])
                    updateOtherTable(crypto, sourceTable.name, table.name, cur, conn)
                    checkpoint = to_dict(table)
                    continue
                else:
                    ### looks for source table starting at the end of the dict, that has the same time unit and
                    ### the table with the least rows, and therefore the table that requires the least compuations,
                    ### ensuring  efficiency if a user adds or deletes tables
                    for item_key, item in reversed(tables.items()):
                        item = from_dict(item)
                        if item.timeunit == table.timeunit:
                            if table.denomination % item.denomination == 0:
                                ### ensure table's source table is not itself
                                if table.denomination / item.denomination > 1:
                                    sourceTable = item
                                    iRows = table.denomination / sourceTable.denomination
                                    cur.execute(f'SELECT max(Id) FROM {sourceTable.name}')
                                    last_row = cur.fetchone()[0]
                                    updateOtherTable(crypto, sourceTable.name, table.name, cur, conn, iRows)
                                    checkpoint = to_dict(table)
                                    break
    checkpoint = None
except KeyboardInterrupt:
    pass
except SyntaxError as e:
    print(e)
    shutil.copy('MarketDataBackup.sqlite', 'MarketData.sqlite')
    checkpoint = None
finally:
    config['checkpoint'] = checkpoint
    config['runs'] += 1
    writeConfig()

print('Done')
conn.close()
