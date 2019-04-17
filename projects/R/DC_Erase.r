# Title     : TODO
# Objective : TODO
# Created by: mrohansmith
# Created on: 4/16/2019
library(sp)
library(rgdal)
library(rgeos)
library(tictoc)
library(cleangeo)
library(raster)
tic("Script Started")
print("Script Started")
x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_A1")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_A1")
print("Data Loaded")

print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")

print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_A1", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_A1")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_A1", driver = "ESRI Shapefile")


x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_A2")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_A2")
print("Data Loaded")

print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")

print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_A2", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_A2")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_A2", driver = "ESRI Shapefile")

x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_A3")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_A3")
print("Data Loaded")

print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")

print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_A3", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_A3")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_A3", driver = "ESRI Shapefile")


x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_B1")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_B1")
print("Data Loaded")
print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")
print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_B1", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_B1")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_B1", driver = "ESRI Shapefile")


x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_B2")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_B2")
print("Data Loaded")
print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")
print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_B2", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_B2")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_B2", driver = "ESRI Shapefile")

x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_B3")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_B3")
print("Data Loaded")
print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")
print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_B3", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_B3")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_B3", driver = "ESRI Shapefile")

x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_B4")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_B4")
print("Data Loaded")
print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")
print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_B4", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_B4")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_B4", driver = "ESRI Shapefile")


x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_C2")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_C2")
print("Data Loaded")
print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")
print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_C2", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_C2")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_C2", driver = "ESRI Shapefile")

x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_C3")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_C3")
print("Data Loaded")
print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")
print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_C3", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_C3")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_C3", driver = "ESRI Shapefile")

x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_C4")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_C4")
print("Data Loaded")
print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")
print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_C4", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_C4")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_C4", driver = "ESRI Shapefile")

x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_D2")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_D2")
print("Data Loaded")
print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")
print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_D2", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_D2")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_D2", driver = "ESRI Shapefile")

x <- ""
y <- ""
print("Loadind Data")
x <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "er_DC_D3")
y <- readOGR(dsn = "C:/Data_State/MD/inputs", layer = "DC_D3")
print("Data Loaded")
print("Repairing geometry")
x.clean <- clgeo_Clean(x, print.log = FALSE)
x2 <- x.clean
y.clean <- clgeo_Clean(y, print.log = FALSE)
y2 <- y.clean
print("Geometry repaired")
print("Erasing")
e <- erase(x2, y2)
print("Erase complete")
print("Repairing Geometry again")
e.clean <- clgeo_Clean(e, print.log = FALSE)
e2 <- e.clean
print("Geometry Repaired again")
print("Creating Spatial Data Frame")
e2ddf <-  SpatialPolygonsDataFrame(e2, data = data.frame(e2))
print("Writing to shp file")
writeOGR(e2ddf, dsn = "C:/Data_State/MD/process", layer = "DC_D3", driver = "ESRI Shapefile")
print("Reading shp file")
e4 <- readOGR(dsn = "C:/Data_State/MD/process", layer = "DC_D3")
print("Disaggregating")
e5 <- disaggregate(e4)
print("Writing shp file")
writeOGR(e5, dsn = "C:/Data_State/MD/Complete", layer = "DC_D3", driver = "ESRI Shapefile")


print("Done")
toc()
print("Script Finished")
tic.clear()
