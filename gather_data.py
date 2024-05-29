import pandas as pd
import matplotlib.pyplot as plt
import boto3

IEX_API_Key = 'pk_77401b8c03794a8fbb944022f00f46de'
tickers =[
			'JPM',
			'BAC',
			'C',
			'WFC',
			'GS',
         ]

#save the data as string

ticker_string=''

for ticker in tickers:
   ticker_string += ticker
   ticker_string += ','
   
ticker_string = ticker_string [: -1]

#Create the endpoint and years strings
endpoints = 'chart'
years = '10'

#Interpolate the endpoint strings into the HTTP_request string
HTTP_request = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={ticker_string}&types={endpoints}&range={years}y&token={IEX_API_Key}'

#import bank data to pandas data frame

bank_data =pd.read_json(HTTP_request)
"""
print(bank_data)
print(bank_data['JPM'])
print(bank_data['JPM']['chart'])
pandas_dataframe=pd.DataFrame(bank_data['JPM']['chart'])
print(pandas_dataframe)
"""
pd.DataFrame(bank_data['JPM']['chart'])

#for ticker in tickers:
#    series_dict.update({ticker : pd.DataFrame(bank_data[ticker]['chart']['close'])})

series_list=[]

for ticker in tickers:
    series_list.append(pd.DataFrame(bank_data[ticker]['chart'])['close'])
    
series_list.append(pd.DataFrame(bank_data['JPM']['chart'])['date'])

column_names=tickers.copy()
column_names.append('Date')

bank_data = pd.concat(series_list, axis=1)
bank_data.columns = column_names

bank_data.set_index('Date', inplace = True)
#print(bank_data)



plt.subplot(2,2,1)
#plt.figure(figsize=(10, 6))
plt.boxplot([bank_data[col] for col in bank_data.columns])
plt.title('Bank stocks', fontsize=10)
plt.xlabel('Bank', fontsize=5)
plt.ylabel('Stock price', fontsize=5)
ticks = range(1, len(bank_data.columns) + 1)
labels = list(bank_data.columns)
plt.xticks(ticks, labels)


plt.subplot(2,2,2)
dates=bank_data.index.to_series()
dates=[pd.to_datetime(d) for d in dates]
well_fargos_data=bank_data['WFC']
plt.scatter(dates,well_fargos_data)
plt.title('WFC Scatter Graph', fontsize=10)
plt.xlabel('Years',fontsize=5)
plt.ylabel('Stock price',fontsize=5)


plt.subplot(2,2,3)
dates=bank_data.index.to_series()
dates=[pd.to_datetime(d) for d in dates]
well_fargos_data=bank_data['JPM']
plt.scatter(dates,well_fargos_data)
plt.title('JPM Scatter Graph', fontsize=10)
plt.xlabel('Years',fontsize=5)
plt.ylabel('Stock price',fontsize=5)


plt.subplot(2,2,4)
plt.hist(bank_data.transpose(),bins=50)
#plt.legend(bank_data.columns,fontsize=20)
plt.title("A Histogram of Banks", fontsize = 10)
plt.ylabel("Observations", fontsize = 5)
plt.xlabel("Stock Prices", fontsize = 5)


plt.tight_layout()
plt.savefig('bank_data.png')


#s3 = boto3.resource('s3')
#s3.meta.client.upload_file('bank_data.png', 'stock-analysis-of-banks', 'bank_data.png', ExtraArgs={'ACL':'public-read'})

plt.show()