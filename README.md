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
  * Asset Ratios
  * Earnings / Share (EPS)
  * Earnings / Share Growth
  * Book Value / Share (BVPS)
  * Cash Flow
    + FCF/Sales
    + FCF/Share
    + Operating CF/Net Income
  * Capital Intensity
    + CapEx/Sales
    + CapEx/Net Income
  * Current Ratio
  * Growth
    + Momentum
      + EPS growth
      + Margins growth
      + Revenue growth
    + Stability
      + BVPS trend
    + Quality
      + EPS growth vs. Revenue growth
      + Leverage
  * Liability Ratios
  * Margins
    + Gross Margin
    + Net Margin
  * Momentum
    + Upward Trends in the Following
      + Margins
      + ROIC
      + Liquidity (Current ratio, quick ratio, & cash ratio)
    + Downward Trends in the Following
      + Debt Loads (Debt/Equity)
      + Cash Conversion Cycle
      + Payout Ratio
      + Inventory / Sales
  * Working Capital
  * Turnover Ratio
  * Price / Earni
  * Price / Earnings / Growth Ratio (PEG)
  * Dividend Yield
  * Dividend Payout Ratio
  * Cash Conversion Cycle (CCC)
  * Cash Return on Invested Capital (CROIC)
  * Return on Assets (ROA)
  * Return on Tangible Assets (ROTA)
    + Net Income / ((Total Assets[0] - Intangible Assets[0] + Total Assets[1] - Intangible Assets[1])/2)
  * Return on Invested Capital (ROIC)
  * Return on Equity (ROE / Formula for DuPont Model)
    + Net income / Revenue (Net Profit Margin)
    + *(Sales / Average Total Assets (Asset Turnover))
    + *(Average Total Assets / Shareholder's Equity (Financial Leverage))
#### Peer Analysis
  * Relative Strength of the Following
    + Debt Load
    + Growth
    + Margins
    + ROIC
#### Target Share Price
  ##### ~~Formula for Owner Earnings (Ten Cap Price)~~
	Net Income
	+Net Change: Accounts Receivable
	+Net Change: Accounts Payable
	+Income Tax
	+Maintenance Capital Expenditures
	___
	Owner Earnings X 10
  ##### ~~Formula for Payback Time (Free Cash Flow / Payback Time)~~
	Net Cash Provided by Operating Activities
	+Purchase of Property and Equipment
	+Any Other Capital Expenditures for Maintenance and Growth
	___
	Free Cash Flow X (1.16)*8
  ##### Discounted Free Cash Flow * Margin of Safety
#### Greenblatt Formula
  * Recursively scan for top companies based on Greenblatt's method. Exclude financial and utility stocks.
    + Calculate company's earnings yield (EBIT / Enterprise Value)
    + Calculate company's return on capital (EBIT/(net fixed assets + working capital))
### Technical Analysis
  * Calculate daily, weekly, and monthly moving averages (50, 100, & 200)
  	+ Perform regression tests
	+ Alert when securities are close to 200 week moving average
	+ Calculate moving volume-weighted average price (MVWAP)
  * Calculate for outperformance (alpha) against benchmarks over 3, 12, 36, 120, and 240-month timeframes.
  	+ Ticker/SPX
	+ Ticker/Industry ETF
  * Calculate RSI for weekly and monthly timeframes
	+ Find securities with upward trends over extended timeframes
	+ Alert when securities are overbought or oversold
### Options Analysis
  * Calculate greeks for security options contracts
  * Calculate IV for securities
