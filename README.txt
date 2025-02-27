# Portfolio
GitHub Portfolio for Recruiters

(Project 1)
Description: This code was taken from is a personal project of mine. It just gets data from the coinbase api and builds a database from it.

Technology: Python, JSON, and SQL (sqlite)

Features: 

The biggest feature is efficiency. The application only makes API calls to create to one table of the smallest time period, 15 min. All other tables are derived from the 15 min table by condensing small time period candles into single greater time period candles. Furthermore, it is efficient in that deriviation. For example, the 30 min table will update from the 15min, but the 1 hour will update from the 30 min table, the 6 hour table will update from the 1 hour table, and so on. It is set up to be effiecient even when a user creates or deletes a custom table. 

Which is the second feature in the sample. The user can create custom candle tables, because different types of analysis call for different time periods. 

Lastly the third featur is of course to get candles of time periods not offered in coinbase's limited selection. It is very basic in terms of interface, in  that there is no interface, so all commands go through terminal prompts.

Updates all tables upon running main.py

Setup: First downlaod Python if it is not already installed, make sure to pip install the requirements.txt file. Second you will need to download DB browser from https://sqlitebrowser.org/ or any other sqlite browser, Lastly you will need to download the files for the application of course here on github. When done, run main.py from terminal. If you have your own CoinBase account and want to use it, make sure to update the .env file with your own keys.
