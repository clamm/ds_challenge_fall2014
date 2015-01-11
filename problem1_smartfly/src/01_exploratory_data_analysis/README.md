Usage
----

To generate the [exploratory_data_analysis.pdf](exploratory_data_analysis.pdf) with the commands and results of the exploratory data analysis do the following:

1. Open `exploratory_data_analysis.Rnw` in Rstudio
1. (Edit code)
1. On the R command line in RStudio run
		
		library(knitr)
		knit("exploratory_data_analysis.Rnw")

	This creates the file `exploratory_data_analysis.tex`. This might take a few minutes since it loads the 7.3 million data points into R.

1. Open the file `exploratory_data_analysis.tex` in TeXShop and click on Typeset to generate the pdf. On Mac OSX Yosemite I had problems compiling the pdf directly in RStudio since the knitr options were ignored.
