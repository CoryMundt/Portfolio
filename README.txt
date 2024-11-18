# Portfolio
GitHub Portfolio for Recruiters

(Project 1)
Description: The project the code was taken from is a personal project of mine. I have always wanted to create a complex trading bot built on statistical analysis. The sample code is taken from an early version of said project. It basically just gets data from the coinbase api and builds a database from it. It is not the final version because everyone wants an advantage in trading, so I don't want the final version public. One known error in this version is that it does not account for null rows. I also want to add that I chose Coinbase for this project because crpyto is mostly irrational. With stocks real world factors affect it more, and there is a lot of them. They represent tangible businesses and assets, employees of which often like to paint a picture for shareholders. A simple quarterly sales report can upend the stock trajectory. With crypto though, it's mostly just about how useful a coin is and even more so just plain greed. With less external factors affecting crypto, technical analysis is much more viable.

Technology: Python, JSON, and SQL (sqlite)

Features: The biggest feature is efficiency. The application only makes API calls to create to one table of the smallest time period, 15 min. All other tables are derived from the 15 min table by condensing small time period candles into single greater time period candles. Furthermore, it is efficient in that deriviation. For example, the 30 min table will update from the 15min, but the 1 hour will update from the 30 min table, the 6 hour table will update from the 1 hour table, and so on. It set up to be effiecient even when a user creates or deletes a custom table. Which is the second biggest feature in the sample. The user can create custom candle tables, because different types of analysis call for different time periods. Lastly the third featur is of course to get candles of time periods not offered in coinbase's limited selection. It is very basic in terms of interface, in  that there is no interface, so all commands go through terminal prompts.

Setup: First you will need to downlaod Python if it is not already installed, make sure to pip install the requirements.txt file. Second you will need to download DB browser from https://sqlitebrowser.org/. Lastly you will need to download the files for the application of course here on github.  To use the application you will need a coinbase account and then create an API key on your account. To do that I reccommend you watch the "Authenicate with Coinbase" section of this video: https://www.youtube.com/watch?v=kjazNLwZvzU.  You should get two keys, copy those and create a file named ".env" in the same directory as others. 
Set it up like this:
api_key = "the other key here"
api_secret = ""-----BEGIN EC PRIVATE KEY----....."
(the video shows this too)
Then just run main.py either in terminal or an IDE. 
