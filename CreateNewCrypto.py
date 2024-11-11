import os
from dotenv import find_dotenv, load_dotenv
import coinbase
from coinbase.rest import RESTClient
import sqlite3
from PGfunctions import createDefaultCandleTables,  readData, writeData
import time
from datetime import datetime
import subprocess
import sys
from pathlib import Path

while True:
    run = input("Would you like to create a new crypto in database? Y/N: ")
    if run.upper() not in ('Y', 'N'):
        continue
    else:
        if run == "N":
            quit()
        else:
            break
conn = sqlite3.connect('MarketData.sqlite')
cur = conn.cursor()

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

api_key = os.getenv("api_key")
secret_key = os.getenv("api_secret")
client = RESTClient(api_key=api_key, api_secret=secret_key, timeout=5)

data = readData()
firstLoop = True
while True:
    if not firstLoop:
        run = input("Would you like to create another crypto in database? Y/N: ")
        if run.upper() not in ('Y', 'N'):
            continue
        else:
            if run == "N":
                break
    while True:
        acronym = input('Enter 3 letter Crypto acronym: ')
        acronym = acronym.upper()
        if len(acronym) < 1:
            # for user to quit application
            quit()
        if len(acronym) != 3:
            "Error: Invalid Acronym"
            continue
        if acronym not in data:
            new_crypto = {
                "gotData": False,
                "prevStart": "",
                "tables": createDefaultCandleTables(acronym, cur)
            }
            data[acronym] = new_crypto
        else:
            print("Error: Crypto already Exists")
            continue
        # end: gets the date time of now converts that to unix timestamp, subtracts a day worth of seconds to get start timestamp
        end = str(int(time.mktime(datetime.now().timetuple())))
        start = str(int(end) - 90000)
        try:
            ### get_candles(client, crypto_market, str(int(unixtimestamp)), str(int(unixtimestamp)), per candle time period)
            ### #here I am just checking if the inputs are valid, before adding anything to the data base with a small query to the api
            MarketData = coinbase.rest.RESTClient.get_candles(client, acronym + "-USD", start, end, "ONE_DAY")
            writeData()
            firstLoop = False
            break
        except Exception as e:
            print(e)
            del data[acronym]

venv_python = Path(sys.executable)
subprocess.run([venv_python, "UpdateTables.py"])
conn.close()
