import sys
import yfinance as yf
from financial_performance import *
from tabulate import tabulate as tb

def target_share_prices(ticker):
    print(ticker)
    income_statement, balance_sheet, statement_of_cash_flows, enterprise_values, price = get_financial_records(ticker)
    #Get Shares Outstanding
    try:
        shares_outstanding = int(float(enterprise_values[0]['Number of Shares']))
    except ValueError:
        print(f'---Could not get shares outstanding query for {ticker} from Financial Modeling Prep. Trying Yahoo Finance...')
        shares_outstanding = yf.Ticker(ticker).info['sharesOutstanding']
    except:
        print('---Could not get number of outstanding shares from Yahoo Finance...')
        shares_outstanding = float('NaN')

    def tc_price(income_statement, balance_sheet, statement_of_cash_flows, shares_outstanding):
        try:
            net_income = float(income_statement[0]['Net Income'])
            net_receivables = float(balance_sheet[0]['Receivables'])-float(balance_sheet[1]['Receivables'])
            net_payables = float(balance_sheet[0]['Payables'])-float(balance_sheet[1]['Payables'])
            income_tax = (float(income_statement[0]['Income Tax Expense']))
            capex = (float(statement_of_cash_flows[0]['Capital Expenditure']))
        except:
            print('---Unable to calculate Ten Cap price.')

        try:
            ten_cap_price = net_income + net_receivables + net_payables + income_tax + capex
            ten_cap_price = round((ten_cap_price*10)/shares_outstanding,2)
        except:
            ten_cap_price = float('NaN')
        return ten_cap_price


    def pbt_price(statement_of_cash_flows, shares_outstanding):
        try:
            pbt_price = round(float(statement_of_cash_flows[0]['Free Cash Flow'])*(1.16*8)/float(enterprise_values[0]['Number of Shares']),2)
        except:
            print('---Unable to calculate Payback Time price.')
            pbt_price = float('NaN')
        return pbt_price

    ten_cap_price = tc_price(income_statement, balance_sheet, statement_of_cash_flows, shares_outstanding)
    payback_time_price = pbt_price(statement_of_cash_flows, shares_outstanding)

    return price, ten_cap_price, payback_time_price

tickers = open("watchlist.txt", "r")
tickers = tickers.read().splitlines()

stock_prices = []
for ticker in tickers:
    prices = target_share_prices(ticker)
    stock_prices.append({'Company': ticker, 'Price': prices[0], 'Ten Cap Price': prices[1], 'Payback Time Price': prices[2]})
    print(ticker)
stock_prices = pd.DataFrame(stock_prices)

print(target_share_prices.to_string())