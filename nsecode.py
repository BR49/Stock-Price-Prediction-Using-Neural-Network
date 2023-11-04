from datetime import date
from nsepy import get_history
import pandas as pd

todays_date = date.today()
sym=input("Enter the symbol :")
sbin = get_history(symbol=sym, start=date(2015,1,1), end=date(todays_date.year,todays_date.month,todays_date.day))
print(type(sbin))
print(sbin)
sbin = pd.DataFrame(sbin)
#sbin.drop(['Series','Prev Close','Last','VWAP','Turnover','Trades','Deliverable Volume','%Deliverble'], axis = 1)
sbin.drop(sbin.columns[[1,2,6,8,10,11,12,13]], axis = 1, inplace = True)
print(sbin)
sbin = sbin[['Open','High','Low','Close','Volume','Symbol']]
sbin = sbin.rename(columns = {'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume', 'Symbol': 'Name','Date':'date'}, inplace = False)
sbin.index.names = ['date']
print(sbin)
print(type(sbin))
sbin.to_csv('./individual_stocks_5yr/NSE_data.csv')
sbin.to_csv('./Stock-Prices-ML-Dashboard\individual_stocks_5yr/NSE_data.csv')
