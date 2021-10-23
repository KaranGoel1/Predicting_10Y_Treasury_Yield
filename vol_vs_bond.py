from numpy.core.numeric import NaN
import pandas as pd
import matplotlib.pyplot as plt
from pandas._libs.missing import NA
from pandas.core.dtypes.missing import notnull

vix_df = pd.read_csv('VIXCLS.csv', na_values=['.'])
vix_df['DATE'] = pd.to_datetime(vix_df.DATE, format=('%Y-%m-%d'))
vix_df = vix_df.set_index(vix_df.DATE)
vix_df.drop(columns=['DATE'], inplace=True)
vix_df['VIXCLS'] = vix_df['VIXCLS'].astype(float)
vix_df = vix_df.resample("M").mean()
vix_df.index = vix_df.index.strftime('%m/%Y')
vix_df = vix_df.drop(index=['10/2021'])
vix_df.columns = ['Price']
#print(vix_df)

ten_yr_yield_df = pd.read_csv('IRLTLT01USM156N.csv')
ten_yr_yield_df['DATE'] = pd.to_datetime(ten_yr_yield_df.DATE, format=('%Y-%m-%d'))
ten_yr_yield_df = ten_yr_yield_df.set_index(ten_yr_yield_df.DATE)
ten_yr_yield_df.drop(columns=['DATE'], inplace=True)
ten_yr_yield_df.columns = ['10-Year Treasury Yield']
ten_yr_yield_df['10-Year Treasury Yield'] = ten_yr_yield_df['10-Year Treasury Yield'].astype(float)
ten_yr_yield_df.index = ten_yr_yield_df.index.strftime('%m/%Y')
#print(ten_yr_yield_df)

#vix_chart = vix_df.plot(kind='line', ylabel = 'Price')
#plt.show()

plt.scatter(vix_df['Price'], ten_yr_yield_df['10-Year Treasury Yield'])
plt.xlabel('VIX Price')
plt.ylabel('10-Year Treasury Yield')
plt.title('VIX Price vs. 10-Year Treasury Yield')
plt.show()