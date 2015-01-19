# load prediction results
prediction <- read.table("out/unsupervised/train_prediction.csv", 
                         col.names=c("visit_id", "uid", "is_spam"),
                         colClasses="factor")
str(prediction)
table(prediction$is_spam)
prop.table(table(prediction$is_spam))

# check prediction consistency within uids
library(plyr)
predAggUid <- ddply(prediction, .(uid), summarize, 
                 is_spam=as.factor(paste(is_spam,collapse="")))

# check prediction consistency within visits
predAggVisit <- ddply(prediction, .(visit_id), summarize, 
                 is_spam=as.factor(paste(is_spam,collapse="")))



# load spam meta data
nameTypeDataFile  <- "resources/raw_variables.csv"
variableNames <- read.csv(nameTypeDataFile, header=TRUE, stringsAsFactors=FALSE) 
variableNames

# load spam data
spamFile <- "../../data/spam.csv"
spamData <- read.csv(spamFile, stringsAsFactors=FALSE, col.names=variableNames$name, 
                     colClasses=variableNames$type, na.strings=c("NA",""))
spamData$tstamp <- as.POSIXct(spamData$tstamp)

# compare uids
isSpam <- prediction$is_spam=="1"
correctlyIdentified <- intersect(spamData$uid, prediction$uid[isSpam])
length(correctlyIdentified)

missedSpam <- intersect(spamData$uid, prediction$uid[!isSpam])
length(missedSpam)

length(correctlyIdentified) + length(missedSpam)

