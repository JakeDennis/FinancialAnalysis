<<<<<<< HEAD
library(rvest)

#Gather S&P 500
spx_wiki<-"https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
spx <- spx_wiki %>%
  read_html() %>%
  html_nodes(xpath='//*[@id="mw-content-text"]/div/table[1]') %>%
  html_table()

#Create table and omit unwanted columns
spx_companies <- spx[[1]]
omit_columns <- c('SEC filings','Date first added[3][4]', 'CIK')
spx_companies[ ,omit_columns]<-list(NULL)
head(spx_companies)


=======
library(rvest)

#Gather S&P 500
spx_wiki<-"https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
spx <- spx_wiki %>%
  read_html() %>%
  html_nodes(xpath='//*[@id="mw-content-text"]/div/table[1]') %>%
  html_table()

#Create table and omit unwanted columns
spx_companies <- spx[[1]]
omit_columns <- c('SEC filings','Date first added[3][4]', 'CIK')
spx_companies[ ,omit_columns]<-list(NULL)
head(spx_companies)


>>>>>>> 116ac8cefa186708d0ad27b27710464202354e9a
