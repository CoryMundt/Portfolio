from num2words import num2words

### a Market Data Table is not the table itself, but information about the table allolwing for easy comparison between tables
### acronym is the 3 letter crypto acronym
### timeunit is min, hour, or day
### denominaiton is the number of timeunit e.g. the 15 in "15min"
### name is the name of the table derived from the previous 3 vairables automatically
class MarketDataTable:
    def __init__(self, acronym, timeunit, denomination, name=None):
        self.acronym = acronym
        if timeunit.lower() not in ["hour", "day", "min"]:
            raise ValueError("Invalid value. Allowed values are min, hour, day")
        self.timeunit = timeunit
        self.denomination = denomination
        if name is not None:
            self.name = name
        elif timeunit == "min":
            self.name = acronym + f'_USD_{num2words(denomination).replace('-', '_').upper()}_MINUTE_CANDLES'
        else:
           self.name = acronym + f'_USD_{num2words(denomination).replace('-', '_').upper()}_{timeunit.upper()}_CANDLES'

    def __str__(self):
        return f"MarketDataTable(acronym={self.acronym}, timeunit={self.timeunit}, denomination={self.denomination}, name={self.name})"

    def __repr__(self):
        return f"<MarketDataTable(acronym={self.acronym}, timeunit={self.timeunit}, denomination={self.denomination}, name={self.name})>"