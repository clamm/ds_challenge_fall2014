# originally from http://research.stowers-institute.org/efg/R/Math/VennDiagram.htm
require(limma)
Venn2 <- function(set1, set2, setnames, title) {
  #example: Venn2(predictLevels, trainLevels, c("predict", "train"), "myVariable")   
  stopifnot(length(setnames) == 2)
  universe <- sort( unique( c(set1, set2) ) )
  Counts <- matrix(NA, nrow=length(universe), ncol=2)
  colnames(Counts) <- setnames
  for (i in 1:length(universe))
  {
    Counts[i,1] <- universe[i] %in% set1
    Counts[i,2] <- universe[i] %in% set2
  }
  vc <- vennCounts(Counts)
  vc[1,] <- rep(NA,3)
  vennDiagram(vc, circle.col=c("orange1", "blue3"), mar=rep(0,4), cex=c(3.5,3,2))
  text(0, 3, title, cex=4)
}