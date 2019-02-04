rm(list = ls())

getFinancialStatements <- function(tickerSymbol){
  #rvest package
  if ("rvest" %in% installed.packages()) {
    library(rvest)
  }
  else{
    install.packages("rvest")
    library(rvest)
  }

  #Scrape figures for balance sheet, income statement, and statement of cash flows from yahoo finance
  for (i in 1:length(tickerSymbol)) {
    tryCatch(
      {
        #Balance Sheet
        url <- "https://finance.yahoo.com/quote/"
        url <- paste0(url,tickerSymbol[i],"/balance-sheet?p=",tickerSymbol[i])
        wahis.session <- html_session(url)
        p <- wahis.session %>%
          html_nodes(xpath = '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/table') %>%
          html_table(fill = TRUE)
        
        balanceSheet <- p[[1]]
        colnames(balanceSheet) <- balanceSheet[1,]
        balanceSheet <- balanceSheet[-c(1,2,17,28),]
        names_row <- balanceSheet[,1]
        balanceSheet <- balanceSheet[,-1] 
        balanceSheet <- apply(balanceSheet,2,function(x){gsub(",","",x)})
        balanceSheet <- suppressWarnings(as.data.frame(apply(balanceSheet,2,as.numeric))) 
        rownames(balanceSheet) <- paste(names_row)
        df1 <- balanceSheet
        
        #Income Statement
        url <- "https://finance.yahoo.com/quote/"
        url <- paste0(url,tickerSymbol[i],"/financials?p=",tickerSymbol[i])
        wahis.session <- html_session(url)                                
        p <- wahis.session %>%
          html_nodes(xpath = '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/table') %>%
          html_table(fill = TRUE)
        
        incomeStatement <- p[[1]]
        colnames(incomeStatement) <- paste(incomeStatement[1,])
        incomeStatement <- incomeStatement[-c(1,5,12,20,25),]
        names_row <- paste(incomeStatement[,1])
        incomeStatement <- incomeStatement[,-1]
        incomeStatement <- apply(incomeStatement,2,function(x){gsub(",","",x)})
        incomeStatement <- suppressWarnings(as.data.frame(apply(incomeStatement,2,as.numeric))) #suppress coercion warnings
        rownames(incomeStatement) <- paste(names_row)
        df2 <- incomeStatement
  
        #Statement of Cash Flows
        url <- "https://finance.yahoo.com/quote/"
        url <- paste0(url,tickerSymbol[i],"/cash-flow?p=",tickerSymbol[i])
        wahis.session <- html_session(url)
        p <- wahis.session %>%
          html_nodes(xpath = '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/table') %>%
          html_table(fill = TRUE)
        
        cashFlow <- p[[1]]
        colnames(cashFlow) <- cashFlow[1,]
        cashFlow <- cashFlow[-c(1,3,11,16),]
        names_row <- cashFlow[,1]
        cashFlow <- cashFlow[,-1] 
        cashFlow <- apply(cashFlow,2,function(x){gsub(",","",x)})
        cashFlow <- suppressWarnings(as.data.frame(apply(cashFlow,2,as.numeric)))
        rownames(cashFlow) <- paste(names_row)
        df3 <- cashFlow
        
        #Create list from temp data.frames
        assign(paste0(tickerSymbol[i],'-financials'),value = list(BalanceSheet= df1,IncomeStatement = df2,CashFlow = df3),envir = parent.frame())
      },
      error = function(cond){
        message(tickerSymbol[i], "gives ",cond)
      }
    )
  }
}

