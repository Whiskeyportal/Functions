# R libraries to install 
# author: Morgan Rohan-Smith
# date: 4/26/2018
closeAllConnections()
rm(list=ls())
# Description: Installs libraries used in my R scripts
p1 <- proc.time()

#######################################################
install.packages("raster") # raster AND vector analysis
install.packages("rgdal") # bindings to GDAL (must have gdal installed).
install.packages("maptools") # provides various mapping functions, BUT I don't recommend using it to read/write files bc it drops projection information. 
install.packages("devtools") # makes creating R packages easier (also allows us to install packages from other locations)
install_github("hadley/ggplot2@v2.2.0") # data visualization package that breaks graphics into component parts (e.g., plot, layers, scales).
install.packages("GGally") # extension of ggplot
devtools::install_github("dgrtwo/gganimate") # create animated ggplot2 plots
install.packages("plotly") # a graphing package for interactive plots
install.packages("data.table") # enhanced version of data.frames. FAST
install.packages("lubridate") # package that facilitates working with dates and times
install.packages("RColorBrewer") # premade color palettes for plots
install.packages("colorRamps") # package to build custom gradient color ramps
install.packages("sf") # simple features
install.packages("tmap") # layer-based approach to building thematic maps
install.packages("rasterVis") # visualization of raster data
install.packages("gdalUtils") # wrappers for GDAL utilities
install.packages("ggmap") # visualize spatial data atop static maps from online sources
install.packages("rgeos") # interfact to GEOS (Geometry Engine - Open Source)
install.packages("dplyr") # A fast set of tools for working with data frame like objects
install.packages("sp")  # working with spatial objects (this package will be installed with raster, but wanted to explicitly recognize it as important)
install.packages("leaflet")  # interactive web mapping using Leaflet
install.packages("rmarkdown") # convert to and from rmarkdown files
install.packages("knitr") # a tool for dynamic report generation in R
install.packages("rlist") # a set of functions for working with lists
install.packages("snow") # simple parallel computing in R
require("devtools")
install_github("eblondel/cleangeo") # Package that repairs Geometry
install.packages("parallel") # another parallel processing package 
install.packages("pryr") # allows you to dig into what R is doing behind the scenes
devtools::install_github("hadley/lineprof")
install.packages("shiny")
install.packages("mapview")
webshot::install_phantomjs()
install.packages("weatherr")
install.packages("RStoolbox")
install.packages("data.table")
install.packages("tidyr")
install.packages("ggplot2")
install.packages("foreign")
#################################
p2 <- proc.time()
p2-p1
