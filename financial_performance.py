from urllib.request import urlopen
import json
import pandas as pd
import datetime as dt

def get_financial_records(ticker):
    def get_fmp_jsondata(url):
        response = urlopen(url)
        data = response.read().decode('utf-8')
        return json.loads(data)

    income_statement_url = f'https://financialmodelingprep.com/api/v3/financials/income-statement/{ticker}'
    balance_sheet_url = f'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{ticker}'
    cash_flow_url = f'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/{ticker}'
    enterprise_values_url = f'https://financialmodelingprep.com/api/v3/enterprise-value/{ticker}'
    price_url = f'https://financialmodelingprep.com/api/v3/stock/real-time-price/{ticker}'

    try:
        income_statement = get_fmp_jsondata(income_statement_url)
        balance_sheet = get_fmp_jsondata(balance_sheet_url)
        statement_of_cash_flows = get_fmp_jsondata(cash_flow_url)
        enterprise_values = get_fmp_jsondata(enterprise_values_url)
        price = get_fmp_jsondata(price_url)
    except:
        print(f"Could not query for {ticker} on Financial Modeling Prep's API.")

    try:
        income_statement = pd.DataFrame(income_statement['financials']).transpose()
        balance_sheet = pd.DataFrame(balance_sheet['financials']).transpose()
        statement_of_cash_flows = pd.DataFrame(statement_of_cash_flows['financials']).transpose()
        enterprise_values = pd.DataFrame(enterprise_values['enterpriseValues']).transpose()
    except:
        print(f'Unable to process {ticker}.')

    try:
        price = price['price']
    except:
        print(f'Could not process price for {ticker}.')
        price = float('NaN')

    return income_statement, balance_sheet, statement_of_cash_flows, enterprise_values, price


