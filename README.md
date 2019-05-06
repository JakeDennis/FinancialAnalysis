Work in progress repository that will utilize r and python to analyze securities for potential investment opportunities.

## Goals
### Watchlist.txt
  * Tracking interesting companies that may be worth owning
  * Will be used to run fundamental and technical analysis functions
### SecularTrendIdeas.md
  * Brainstorming highest areas of growth and disruption in the marketplace
  * Will be used to identify best sectors for portfolio exposure
### Fundamental Analysis
  * ~~Pull SPX tickers from Wikipedia~~
  * ~~Pull financial statements for past 3 years~~
  * Investigate if longer term financials can be imported (5 or 10 years)
  * Calculate leading sectors over 1, 3, 12, 36, 60, 120, 240 months (alpha)
#### Financial Metrics
  * Earnings / Share (EPS)
  * Earnings / Share Growth
  * Current Ratio
  * Working Capital
  * Turnover Ratio
  * Price / Earnings Ratio (P/E)
  * Price / Earnings / Growth Ratio (PEG)
  * Dividend Yield
  * Dividend Payout Ratio
  * Cash Conversion Cycle (CCC)
  * Return on Equity (ROE / Formula for DuPont Model)
    + Net income / Revenue (Net Profit Margin)
    + *(Sales / Average Total Assets (Asset Turnover))
    + *(Average Total Assets / Shareholder's Equity (Financial Leverage))
#### Target Share Price
  ##### Formula for Owner Earnings (Ten Cap Price)
	Net Income
	+Net Change: Accounts Receivable
	+Net Change: Accounts Payable
	+Income Tax
	+Maintenance Capital Expenditures
	___
	Owner Earnings X 10
  ##### Formula for Payback Time (Free Cash Flow / Payback Time)
	Net Cash Provided by Operating Activities
	+Purchase of Property and Equipment
	+Any Other Capital Expenditures for Maintenance and Growth
	___
	Free Cash Flow X (1.16)8
### Technical Analysis
  * Calculate daily, weekly, and monthly moving averages (50, 100, & 200)
  	+ Perform regression tests
	+ Alert when securities are close to 200 week moving average
  * Calculate for outperformance (alpha) against benchmarks over 3, 12, 36, 120, and 240-month timeframes.
  	+ Ticker/SPX
	+ Ticker/Industry ETF
  * Calculate RSI for weekly and monthly timeframes
	+ Find securities with upward trends over extended timeframes
	+ Alert when securities are overbought or oversold
### Options Analysis
  * Calculate greeks for security options contracts
  * Calculate IV for securities
