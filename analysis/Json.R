install.packages("rjson")
library(rjson)
library(data.table)
library(ggplot2)
library(xlsx)
getwd()
JsonData <- fromJSON(file= "Python_Hackathon/withdrawal_count.json" )
View(JsonData)

data <- setNames(data.table(matrix(nrow = 1095, ncol = 2)), c("Date", "NumberWithdrawals"))


for (i in 1:1095) {
  data$Date[[i]] = names(JsonData)[[i]]
  data$NumberWithdrawals[[i]] = JsonData[[i]][[1]]
}    

data = transform(data, Date = as.Date(Date, "%m/%d/%Y"))
View(data)

hist(data$NumberWithdrawals, 
     main = "Histogram of Withdrawals Per Day",
     xlab = "# of Withdrawals",
     ylab = "Frequency",
     border = "blue",
     col = "green",
     xlim = c(0, 1000),
     ylim = c(0, 300),
     las = 1,
     breaks = 90)

ggplot(data=data)+
  ggtitle("Withdrawal Trends Past 3 Years")+
  aes(x=Date, y=NumberWithdrawals) + #x axis & y-axis
  geom_point()+ #plot every point
  theme_bw()+ #black and white theme
  labs(x="Date", y="Total Number of Withdrawals")



news_data = read.csv("Downloads/daily_country.csv")
View(news_data)
news = setNames(data.table(matrix(nrow = 365, ncol = 2)), c("Date", "NumberArticles"))

names(news_data)[[1]] <- "Date"
names(news_data)[[2]] <- "Country"
names(news_data)[[3]] <- "Count"
newdata <- news_data[-c(1:2073456), ] 
View(newdata)

b<-365

while (b<366) {
  if (newdata$Country[[b]]=="US") {
    b = b+1
  }
  else {
    newdata <- newdata[-c(b), ]
  }
}

write.xlsx(newdata, "Downloads/newdata.xlsx")

newdata2 <- read.csv("Downloads/newdata.csv")
View(newdata2)

ggplot(data=newdata2)+
  ggtitle("US Articles")+
  aes(x=Date, y=Count) + #x axis & y-axis
  theme_bw()+ #black and white theme
  geom_point()+
  labs(x="Date", y="Total Articles")
