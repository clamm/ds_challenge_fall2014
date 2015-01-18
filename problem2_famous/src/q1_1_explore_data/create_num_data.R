# rm(list=setdiff(ls(),"webData"))   #clear memory

# ------------------------
# ------------------------ define functions
# ------------------------

writeLevelMappingToFile <- function(df, variable, file) {
  varIdx <- which(names(df)==variable)  
  uniqueValues <- unique(df[,varIdx])
  tmp <- unclass(uniqueValues[!is.na(uniqueValues)])
  mapping <- data.frame(numericLevel=tmp, characterLevel=levels(tmp))
  write.csv(mapping, file=file, row.names=FALSE)
}


getMapFileName <- function(variableName, type) {
  paste("out/",type,"_level_map_",variableName,".csv", sep="")
}


imputeNA <- function(df, variable) {
  varIdx <- which(names(df)==variable) 
  varIsNa <- is.na(df[,varIdx])
  actualValues <- df[!varIsNa,c(1,varIdx)]
  naVisits <- df[varIsNa,1]
  l <- length(naVisits)
  for (i in 1:l) {
    if (i %% 1000 == 0) print(paste(variable, i, l,))
    visit <- naVisits[i]
    value <- actualValues[actualValues[,1]==visit,2]
    visitIdx <- which(df[,1]==visit) 
    df[visitIdx,varIdx] <- value
    
  }
  return(df)
}




# load meta data
nameTypeDataFile  <- "resources/raw_variables.csv"
variableNames <- read.csv(nameTypeDataFile, header=TRUE, stringsAsFactors=FALSE) 
variableNames
factorIdx <- which(variableNames$type=="factor")
factorNames <- variableNames$name[factorIdx]

# ------------------------
# ------------------------ web starts here
# ------------------------

# read the web.log data
webFile <- "../../data/web.csv"
webData <- read.csv(webFile, stringsAsFactors=FALSE, col.names=variableNames$name, 
                    colClasses=variableNames$type, na.strings=c("NA",""))
webData$tstamp <- as.POSIXct(webData$tstamp)
str(webData)

# write-web-numeric
numericWebId <- data.frame(visit_id=webData$visit_id, uid=webData$uid)
head(numericWebId)
write.table(numericWebId, file="out/web_numeric_id.csv", row.names=FALSE, 
            col.names=TRUE, quote=FALSE)

webData <- imputeNA(webData, "campaign")
webData <- imputeNA(webData, "query")
numericWeb <- data.frame(campaign=unclass(webData$campaign), 
                         action=unclass(webData$action),
                         query=unclass(webData$query),
                         tstamp=unclass(webData$tstamp))
head(numericWeb)
write.table(numericWeb, file="out/web_numeric.csv", row.names=FALSE, 
            col.names=FALSE, quote=FALSE)
  
# also write the level mapping in to files:
writeLevelMappingToFile(webData, "campaign", getMapFileName("campaign","web"))
writeLevelMappingToFile(webData, "action", getMapFileName("action","web"))
writeLevelMappingToFile(webData, "query", getMapFileName("query","web"))
  
  
  
# ------------------------
# ------------------------ spam starts here
# ------------------------
  
# read spam data:
spamFile <- "../../data/spam.csv"
spamData <- read.csv(spamFile, stringsAsFactors=FALSE, col.names=variableNames$name, 
                     colClasses=variableNames$type, na.strings=c("NA",""))
spamData$tstamp <- as.POSIXct(spamData$tstamp)
str(spamData)
  
# write-spam-numeric
numericSpamId <- data.frame(visit_id=spamData$visit_id, uid=spamData$uid)
head(numericSpamId)
write.table(numericSpamId, file="out/spam_numeric_id.csv", row.names=FALSE, 
            col.names=TRUE, quote=FALSE)

spamData <- imputeNA(spamData, "campaign")
spamData <- imputeNA(spamData, "query")
numericSpam <- data.frame(campaign=unclass(spamData$campaign), 
                         action=unclass(spamData$action),
                         query=unclass(spamData$query),
                         tstamp=unclass(spamData$tstamp))
head(numericSpam)
write.table(numericSpam, file="out/spam_numeric.csv", row.names=FALSE, 
            col.names=FALSE, quote=FALSE)

# also write the level mapping in to files:
writeLevelMappingToFile(spamData, "uid", getMapFileName("uid","spam"))
writeLevelMappingToFile(spamData, "campaign", getMapFileName("campaign","spam"))
writeLevelMappingToFile(spamData, "actions", getMapFileName("actions","spam"))
writeLevelMappingToFile(spamData, "queries", getMapFileName("queries","spam"))
