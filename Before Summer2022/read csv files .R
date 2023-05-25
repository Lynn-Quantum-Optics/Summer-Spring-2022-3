

#For reading off the coincidence counts and error in a file with many (many) .csv files!

indexvalcolumn <- 1 
indexvalrow <-1
column1 <- 11
row1 <- 26
column2 <- 12
row2 <- 26 #row and column indices in each csv file
countstable <- matrix(data=NA,nrow=21,ncol=21,byrow=TRUE,dimnames=NULL)
errortable <- matrix(data=NA,nrow=21,ncol=21,byrow=TRUE,dimnames=NULL) #tables we want
degreesbob <- seq(0,100,5) 
degreesalice <- seq(0,100,5) 
for (bob in degreesbob){
  for (alice in degreesalice){
    temp <- read.csv(file=paste("C:\\Users\\lynnlab\\Desktop\\summer2018\\measurements\\steering2dmap\\State 2\\UV HWP 22 QP base 5 vert 3bar PCC 45_5\\BHWP and AHWP 2d steering sweep BHWP at ", bob, "_0deg AHWP at ",alice, "_0.csv", sep=""),sep=",")
    countstable[indexvalrow,indexvalcolumn] <- temp$C4[row1]
    errortable[indexvalrow,indexvalcolumn] <- temp$C4.uncertainty[row2]
    indexvalcolumn = indexvalcolumn + 1
  }
  indexvalcolumn = 1
  indexvalrow = indexvalrow + 1
}
write.csv(countstable, file = "C:\\Users\\lynnlab\\Desktop\\summer2018\\measurements\\steering2dmap\\State 2\\Coincidence_counts_onewaysteering_2dmap_state2.csv",row.names=degreesbob)
write.csv(errortable, file = "C:\\Users\\lynnlab\\Desktop\\summer2018\\measurements\\steering2dmap\\State 2\\Coincidence_error_onewaysteering_2dmap_state2.csv",row.names=degreesbob)
