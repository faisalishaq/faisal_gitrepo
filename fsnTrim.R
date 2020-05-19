library(readxl)
data<-read_xlsx('Top FSN Pincodes.xlsx',sheet = 'data')
large<-subset(data,data$analytic_super_category %in% c("AirConditioner",
                                                       "CoreEA",
                                                       "HomeEntertainmentLarge",
                                                       "HouseHold",
                                                       "Microwave",
                                                       "PremiumEA",
                                                       "Refrigerator",
                                                       "SeasonalEA",
                                                       "WashingMachineDryer"))
vertgmv<-aggregate(large$gmv,by=list(Vertical=large$analytic_vertical,SCAT=large$analytic_super_category),FUN=sum)


header <- c("FSN","Vertical", "SCAT","GMV")
df <- as.data.frame(matrix(,0,length(header)))
names(df) <- header

Is=vertgmv$Vertical
Js=vertgmv$x

for (i in seq_along(Is)){
  temp<-subset(large,large$analytic_vertical==Is[i])
  agg<-aggregate(temp$gmv,by=list(FSN=temp$product_id,Vertical=temp$analytic_vertical,SCAT=temp$analytic_super_category),FUN=sum)
  agg<-agg[rev(order(agg$x)),]
  sum=0
  n=0
  gmv<-agg$x
  while(sum<0.8*Js[i]){
    n<-n+1
    sum<-sum+gmv[n]
  }
  
  f<-agg[1:n,]
  df<-rbind(df,f)
  
}

header2 <- c("Pincode","FSN","Vertical", "SCAT","GMV")
df2 <- as.data.frame(matrix(,0,length(header2)))
names(df2) <- header2

IIs<-df$FSN
JJs<-df$x

for (i in seq_along(IIs)){
  temp<-subset(large,large$product_id==IIs[i])
  agg<-aggregate(temp$gmv,by=list(Pincode=temp$pincode,FSN=temp$product_id,Vertical=temp$analytic_vertical,SCAT=temp$analytic_super_category),FUN=sum)
  agg<-agg[rev(order(agg$x)),]
  sum=0
  n=0
  gmv<-agg$x
  while(sum<0.8*JJs[i]){
    n<-n+1
    sum<-sum+gmv[n]
  }
  
  f2<-agg[1:n,]
  df2<-rbind(df2,f2)
  
}

write.csv(df,'FSN List.csv',row.names = FALSE)









