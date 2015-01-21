# define function to index vector for a pattern in a factor's levels

getPatternIndex <- function(column, pattern) {
  # parameters:
  #   column:  a factor column of a data.frame
  #   pattern: a pattern to look for in the column's levels
  # returns:
  #   Index vector that indicates the rows in which the pattern was found in the column
  values <- names(unlist(sapply(levels(column), FUN=grep, pattern=pattern)))
  cat(paste("Concerned pattern levels are", paste(values, collapse=", ")))
  idx <- c()
  for (l in values) {
    idx <- c(idx, which(column == l))
  }
  return(sort(idx))
}