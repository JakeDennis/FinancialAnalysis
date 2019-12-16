import json
import numpy as np
import pandas as pd
import sys
import yfinance as yf
from urllib.request import urlopen

ticker = sys.argv[1]

def get_financial_records(ticker):
    #api loader
    def get_fmp_jsondata(url):
        response = urlopen(url)
        data = response.read().decode('utf-8')
        return json.loads(data)
    urls = {
    'income' : f'https://financialmodelingprep.com/api/v3/financials/income-statement/{ticker}',
    'balance_sheet' : f'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{ticker}',
    'cash_flow' : f'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/{ticker}',
    'price' : f'https://financialmodelingprep.com/api/v3/stock/real-time-price/{ticker}',
    }

    #query APIs for statement values
    try:
        income_statement = get_fmp_jsondata(urls['income'])
        balance_sheet = get_fmp_jsondata(urls['balance_sheet'])
        statement_of_cash_flows = get_fmp_jsondata(urls['cash_flow'])
        price = get_fmp_jsondata(urls['price'])
    except Exception as e:
        print(f"Could not query for {ticker} on Financial Modeling Prep's API.")
        print(e)
        raise
    try:
        price = price['price']
    except:
        print(f'Could not process price for {ticker}.')
        price = float('NaN')

    #coerce to pandas dataframes
    try:
        income_statement = pd.DataFrame(income_statement['financials'])
        balance_sheet = pd.DataFrame(balance_sheet['financials'])
        statement_of_cash_flows = pd.DataFrame(statement_of_cash_flows['financials'])
    except:
       print(f'Unable to process {ticker} as pandas dataframe.')

    #replace blank values as numpy NaN
    def replace_null_values(df):
        df.replace('', np.nan, inplace=True)
        return df

    statement_dfs = [income_statement, balance_sheet, statement_of_cash_flows]
    for df in statement_dfs:
        replace_null_values(df)

    #change statement dataframes to datetime and float values
    def coerce_statement_df(df):
        try:
            df['date'] = pd.to_datetime(df['date'])
            df.loc[:, df.columns != 'date'] = df.loc[:, df.columns != 'date'].astype(float)
        except:
            print('Unexpected error:', sys.exc_info()[0])
        return df

    try:
        income_statement = coerce_statement_df(income_statement)
        balance_sheet = coerce_statement_df(balance_sheet)
        statement_of_cash_flows = coerce_statement_df(statement_of_cash_flows)
    except:
        print(f'Could not coerce dataframes to specified values for {ticker}')
        print('Unexpected error:', sys.exc_info()[0])

    #calculate and insert book value per share (BVPS) into balance sheet after equity
    metric = 'Total shareholders equity'
    total_years = balance_sheet.count(axis='rows')[metric]
    index = balance_sheet.columns.get_loc(metric) + 1
    bvps = []
    for year in range(total_years):
        try:
            bvps.append((balance_sheet[metric][year] / income_statement['Weighted Average Shs Out'][year]))
        except KeyError:
            bvps.append(float('NaN'))
    balance_sheet.insert(index, 'Book Value per Share', bvps, False)

    return income_statement, balance_sheet, statement_of_cash_flows, price

def target_share_prices(balance_sheet, income_statement, price, statement_of_cash_flows, ticker):
    try:
        shares_outstanding = income_statement['Weighted Average Shs Out'][0]
    except ValueError:
        print(f'---Could not get shares outstanding query for {ticker} from Financial Modeling Prep. Trying Yahoo Finance...')
        shares_outstanding = yf.Ticker(ticker).info['sharesOutstanding']
    except:
        print('---Could not get number of outstanding shares from Yahoo Finance...')
        shares_outstanding = float('NaN')

    #calculate ten cap price
    def tc_price(income_statement, balance_sheet, statement_of_cash_flows, shares_outstanding):
        try:
            net_income = income_statement['Net Income'][0]
            net_receivables = balance_sheet['Receivables'][0]-balance_sheet['Receivables'][1]
            net_payables = balance_sheet['Payables'][0]-balance_sheet['Payables'][1]
            income_tax = income_statement['Income Tax Expense'][0]
            capex = statement_of_cash_flows['Capital Expenditure'][0]
        except:
            print('---Unable to calculate Ten Cap price.')
        try:
            ten_cap_price = net_income + net_receivables + net_payables + income_tax + capex
            ten_cap_price = round((ten_cap_price*10)/shares_outstanding,2)
        except:
            ten_cap_price = float('NaN')
        return ten_cap_price

    #calculate payback time price (private company value)
    def pbt_price(statement_of_cash_flows, shares_outstanding):
        try:
            pbt_price = round((statement_of_cash_flows['Free Cash Flow'][0]*(1.16*8))/shares_outstanding,2)
        except:
            print('---Unable to calculate Payback Time price.')
            pbt_price = float('NaN')
        return pbt_price

    ten_cap_price = tc_price(income_statement, balance_sheet, statement_of_cash_flows, shares_outstanding)
    payback_time_price = pbt_price(statement_of_cash_flows, shares_outstanding)

    return price, ten_cap_price, payback_time_price

def metric_growth(metric, df):
    total_years = df.count(axis='rows')[metric]
    total_years -= 1
    metric_growth = []
    for year in range(total_years):
        last_year = year + 1
        metric_growth_rate = round(((df[metric][year] - df[metric][last_year]) / df[metric][last_year]), 3)
        metric_growth.append(metric_growth_rate)
    metric_growth.append(float('NaN'))
    index = df.columns.get_loc(metric) + 1

    try:
        df.insert(index, f'{metric} Growth Rate', metric_growth, True)
    except ValueError:
        df.insert(index, f'{metric} Growth Rate', pd.Series(metric_growth), True)
    return df

#Call parent function with ticker and save to dataframes
income_statement, balance_sheet, statement_of_cash_flows, price = get_financial_records(ticker)

print(income_statement, balance_sheet, statement_of_cash_flows)

metric_growth('EPS', income_statement)
metric_growth('Revenue', income_statement)
metric_growth('Operating Income', income_statement)
metric_growth('Cash and cash equivalents', balance_sheet)
metric_growth('Book Value per Share', balance_sheet)
metric_growth('Free Cash Flow', statement_of_cash_flows)

metric_growth_rates = {
    'EPS Growth Rate': income_statement['EPS Growth Rate'],
    'Book Value per Share Growth Rate': balance_sheet['Book Value per Share Growth Rate'],
    'Revenue Growth Rate': income_statement['Revenue Growth Rate'],
    'Operating Income Growth Rate': income_statement['Operating Income Growth Rate'],
    'Free Cash Flow Growth Rate': statement_of_cash_flows['Free Cash Flow Growth Rate'],
    'Cash and cash equivalents Growth Rate': balance_sheet['Cash and cash equivalents Growth Rate']
}

#create new df to display current, ten cap, and private company price
columns = []
prices = target_share_prices(balance_sheet, income_statement, price, statement_of_cash_flows, ticker)
columns.append({'Company' : ticker, 'Current Price' : prices[0], 'Ten Cap Price' : prices[1], 'Payback Time Price' : prices[2]})
price_df = pd.DataFrame(columns)

#create new df to display growth rate metrics
index = 0
growth_df = pd.DataFrame()
for rate in metric_growth_rates:
    growth_df.insert(index, rate, metric_growth_rates[rate], True)
    index += 1

print(price_df)
print(growth_df.transpose())