import pandas as pd
import matplotlib.pyplot as plt
import numpy
from sklearn import linear_model

def create_df(filepath):
    df = pd.read_csv(filepath, na_values=['.'])
    df[filepath[:-4]] = df[filepath[:-4]].astype(float)
    df = df.set_index(df['DATE'])
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    df.drop(columns=['DATE'], inplace=True)
    return df

vix_df = create_df('VIXCLS.csv') #link: https://fred.stlouisfed.org/series/VIXCLS
vix_df = vix_df.resample("M").mean()
vix_df.index = vix_df.index.strftime('%m/%Y')
vix_df = vix_df.drop(index=['09/2021'])
vix_df = vix_df.drop(index=['10/2021'])
vix_df.columns = ['VIX Price']


ten_yr_yield_df = create_df('IRLTLT01USM156N.csv') #link: https://fred.stlouisfed.org/series/IRLTLT01USM156N
ten_yr_yield_df.columns = ['10-Year Treasury Yield']
ten_yr_yield_df.index = ten_yr_yield_df.index.strftime('%m/%Y')
ten_yr_yield_df = ten_yr_yield_df.drop(index=['09/2021'])

#unrate link: https://fred.stlouisfed.org/series/UNRATE
unrate_df = create_df('UNRATE.csv')
unrate_df.columns = ['Unemployment Rate']
unrate_df.index = unrate_df.index.strftime('%m/%Y')
unrate_df = unrate_df.drop(index=['09/2021'])

#fedfunds link: https://fred.stlouisfed.org/series/FEDFUNDS
fedfunds_df = create_df('FEDFUNDS.csv')
fedfunds_df.columns = ['Interest Rate']
fedfunds_df.index = fedfunds_df.index.strftime('%m/%Y')
fedfunds_df = fedfunds_df.drop(index=['09/2021'])

#cpi link: https://fred.stlouisfed.org/series/CPALTT01USM657N
delta_cpi_df = create_df('CPALTT01USM657N.csv')
delta_cpi_df.index = delta_cpi_df.index.strftime('%m/%Y')
delta_cpi_df.columns = ['Change in CPI']

#inflation exp link: https://fred.stlouisfed.org/series/MICH
inf_exp_df = create_df('MICH.csv')
inf_exp_df.index = inf_exp_df.index.strftime('%m/%Y')
inf_exp_df.columns = ['Inflation Expectation']

dfs = [ten_yr_yield_df, unrate_df, fedfunds_df, delta_cpi_df, inf_exp_df]

merged = vix_df
for df in dfs:
    merged = merged.join(df)

x_columns = ['VIX Price', 'Unemployment Rate', 'Interest Rate', 'Change in CPI', 'Inflation Expectation']
X = merged[x_columns]
Y = merged['10-Year Treasury Yield']
reg = linear_model.LinearRegression()
reg.fit(X, Y)
equation = ''
for var in x_columns:
    if reg.coef_[x_columns.index(var)] < 0:
        equation += ' - ' + str(abs(round(reg.coef_[x_columns.index(var)], 2)))
    else:
        equation += ' + ' + str(round(reg.coef_[x_columns.index(var)], 2))
    equation += '(' + var + ')'
print('\nMultiple regression equation:', '\n10-Year Treasury Yield', ' = ', round(reg.intercept_, 2), equation)

vix_v_10y = vix_df
vix_v_10y = vix_v_10y.join(ten_yr_yield_df)
vix_v_10y.index = pd.to_datetime(vix_v_10y.index, format='%m/%Y')
vix_v_10y = vix_v_10y.resample("1Y").mean()
vix_v_10y.index = vix_v_10y.index.strftime('%Y')
ax1 = vix_v_10y['VIX Price'].plot(kind='line', label='VIX Price')
ax2 = vix_v_10y['10-Year Treasury Yield'].plot(kind='line', secondary_y = True, label='Yield')
ax1.set_xlabel('Date', fontweight='bold')
ax1.set_ylabel('VIX Price (in USD)', fontweight='bold')
ax2.set_ylabel('10-Year Treasury Yield (in %)', fontweight='bold')
vix_line, vix_label = ax1.get_legend_handles_labels()
t10y_line, t10y_label = ax2.get_legend_handles_labels()
lines = vix_line + t10y_line
labels = vix_label + t10y_label
ax1.legend(lines, labels)
plt.title('Annual Average VIX Price and 10-Year Treasury Yield Since 1990', fontweight='bold')
#plt.savefig('vix_yield_line.png')
#plt.show()

plt.scatter(vix_df['VIX Price'], ten_yr_yield_df['10-Year Treasury Yield'])
plt.xlabel('VIX Price (in USD)', fontweight='bold')
plt.ylabel('10-Year Treasury Yield (in %)', fontweight='bold')
plt.title('VIX Price vs. 10-Year Treasury Yield', fontweight='bold')
z = numpy.polyfit(vix_df['VIX Price'], ten_yr_yield_df['10-Year Treasury Yield'], 1)
p = numpy.poly1d(z)
plt.plot(vix_df['VIX Price'],p(vix_df['VIX Price']),"r--")
#plt.savefig('vix_vs_yield.png')
print('\nVIX vs. Yield Regression Equation:', "\n10-Year Treasury Yield = %.2f + %.2f(VIX Price)\n"%(z[1],z[0]))
#plt.show()

plt.scatter(merged['Interest Rate'], merged['10-Year Treasury Yield'])
plt.xlabel('Interest Rate (in %)', fontweight='bold')
plt.ylabel('10-Year Treasury Yield (in %)', fontweight='bold')
plt.title('Interest Rate vs. 10-Year Treasury Yield', fontweight='bold')
z = numpy.polyfit(merged['Interest Rate'], merged['10-Year Treasury Yield'], 1)
p = numpy.poly1d(z)
plt.plot(merged['Interest Rate'],p(merged['Interest Rate']),"r--")
#plt.savefig('intrate_vs_yield.png')
print('\nInterest Rate vs. Yield Regression Equation:', "\n10-Year Treasury Yield = %.2f + %.2f(Interest Rate)\n"%(z[1],z[0]))
#plt.show()