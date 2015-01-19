# originally from http://research.stowers-institute.org/efg/R/Math/VennDiagram.htm
require(limma)

getTrue <- function(universe, set) {
  sapply(intersect(universe, set), FUN=function(x){ which(universe==x) })
}


Venn2 <- function(set1, set2, setnames, title) {
  #example: Venn2(predictLevels, trainLevels, c("predict", "train"), "myVariable")   
  stopifnot(length(setnames) == 2)
  universe <- sort( unique( c(set1, set2) ) )
  Counts <- matrix(NA, nrow=length(universe), ncol=2)
  colnames(Counts) <- setnames
  
  trueSet1 <- getTrue(universe, set1)
  Counts[trueSet1,1] <- TRUE
  Counts[-trueSet1,1] <- FALSE
  
  trueSet2 <- getTrue(universe, set2)
  Counts[trueSet2,2] <- TRUE
  Counts[-trueSet2,2] <- FALSE
  
  vc <- vennCounts(Counts)
  vc[1,] <- rep(NA,3)
  vennDiagram(vc, circle.col=c("orange1", "blue3"), mar=rep(0,4), cex=c(3.5,3,2))
  text(0, 3, title, cex=4)
}