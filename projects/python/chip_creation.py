# line 23 username :: to
# line 2014 username :: from
# line 2015 email password for username :: from

import ctypes, arcpy, os, sys, time, subprocess, collections, datetime, smtplib, glob, shutil, errno, mimetypes
from arcpy import env
from datetime import datetime
from subprocess import Popen
from distutils.dir_util import copy_tree
from os.path import join
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

arcpy.env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = "250%" 
from_directory = r"G:\Products\Garmin\Garmin_Master_Misc\template\temp"
script_starttime = datetime.now()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#	Set Variables

state = "NH"
toaddr = "***"   #Where notification email will be sent
product = "Premium"
version = "19.0"
year = "2019"
map_tiles = "200"
ResumeTime = datetime(2013, 3, 18, 19, 00, 00)
					#year, month, day(no leading zero), hour(24 hour clock), minute(double digit), second(double digit)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#	Set state specific data layers 
#	Enter state specific directory exactly as it appears in G:/Data_State directory
Layer_1 = "WalkIn"
Layer_2 = "Fences"
Layer_3 = "Guzzlers"
Layer_4 = "Travel_Mgmt_Areas"
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

AdminValues = ["0x11", "0x1c", "0x1d", "0x27"]
BathyValues = ["0x23"]
GMUValues = ["0x10", "0x0b00", "0x0b", "0x12", "0x13", "0x0501"]
GNISValues = ["0x01", "0x02", "0x03", "0x0305", "0x04", "0x0405", "0x05", "0x06", "0x07", "0x08", "0x0801", "0x0b00", "0x0d00", "0x10", 
						"0x2c05", "0x3002", "0x4100" , "0x4101", 
						"0x4200", "0x4201", "0x4202", "0x4203", "0x4204", "0x4205", "0x4206", "0x4207", "0x4210",
						"0x4801", "0x47", "0x4700", "0x4701", "0x4703", "0x48", "0x4800", "0x4801", "0x4802", "0x4803", "0x4804", 
						"0x4805", "0x4806", "0x4807", "0x4808", "0x4809", "0x52", "0x5200", "0x5201", "0x5202", "0x5203", "0x5204", "0x5205", "0x5206",
						"0x5300", "0x5301", "0x6001", "0x6002", "0x6005", "0x6007", "0x6010", "0x6016", "0x6017", "0x6018", "0x6019", "0x600b", "0x600c", "0x6100",
						"0x6103", "0x6104", "0x6105", "0x6106", "0x6107", "0x6108", "0x6109", "0x610a", "0x610b", "0x610e", "0x610f", "0x6110", "0x6111", "0x6115",
						"0x6118", "0x6402", "0x6403", "0x6404", "0x640a", "0x640c", "0x640e", "0x6414", "0x6415", "0x6509", "0x6e00", "0x6601", "0x6608", 
						"0x660f", "0x7001", "0x7002", "0x7003", "0x7004", "0x7005", "0x7006", "0x7008", "0x700a", "0x700b", "0x700e", "0x7010", "0x7016"]
ParkValues = ["0x610e", "0x4801", "0x4802", "0x4803", "0x4804", "0x4805", "0x4806", "0x6001", "0x6018"]
ParcelAreaValues = ["0x03", "0x06", "0x0d", "0x0e", "0x14", "0x15", "0x16", "0x17", "0x18", "0x19", "0x1f", "0x20", "0x21", "0x22",
						"0x23", "0x24", "0x25", "0x26", "0x27", "0x29", "0x2a", "0x2b", "0x2c", "0x2d", "0x2e", "0x2f", "0x30",
						"0x31", "0x32", "0x33", "0x35", "0x37", "0x38", "0x39", "0x52"]
ParcelInsideLinesValues = ["0x1e"]
ParcelLinesValues = ["0x0b", "0x15", "0x19", "0x1a", "0x2a"]
ParcelPointValues = ["0x6001"]
RecreationPointsValues = ["0x0d01", "0x11", "0x1c01", "0x1c09", "0x1c10", "0x2e", 
									"0x2f00", "0x2f01", "0x2f02", "0x2f03", "0x2f04", "0x2f05", "0x2f06", "0x2f07", "0x2f08", "0x2f09", "0x2f10", "0x2f11", "0x2f12", "0x3003", 
									"0x4100", "0x4101", "0x4700", "0x4701", 
									"0x4c00", "0x4c01",
									"0x4702", "0x4703", "0x4800", "0x4801", "0x4803", "0x4804", "0x4807", "0x4802", "0x4808", "0x4809", "0x4c00", "0x4c01", "0x4c02",
									"0x5200", "0x5201", "0x5202", "0x5203", "0x5204", "0x5205", "0x5206", "0x5300", "0x5301", "0x5900", "0x5901", "0x5902", "0x5903", 
									"0x5904", "0x5905", "0x5906", "0x5907", "0x5908", "0x5909", "0x6001", "0x6002", "0x6004", "0x6005", "0x6007", 
									"0x6008", "0x6009", "0x600a", "0x600b", "0x600c", "0x600d", "0x600e", "0x600f", "0x6010", "0x6011", "0x6013", "0x6014", "0x6015", 
									"0x6016", "0x6017", "0x6018", "0x6019", "0x601a", "0x601b", "0x601c", "0x601d", "0x6100", "0x6101", "0x6102", 
									"0x6103", "0x6104", "0x6106", "0x6107", "0x6108", "0x6109", "0x610a", "0x610b", "0x610c", 
									"0x610d", "0x610e", "0x610f", "0x6110", "0x6111", "0x6112", "0x6115", "0x6116", "0x6117", "0x6118", "0x6119", 
									"0x4200", "0x4201", "0x4202", "0x4203", "0x4204", "0x4205", "0x4206", "0x4207", "0x4208", "0x4209", "0x4210", "0x4211", "0x4212", "0x4213", "0x4214", "0x4215", "0x28",
									"0x6401", "0x6402", "0x6406", "0x640a", "0x640c", "0x640e", "0x6414", "0x6415", "0x6417", 
									"0x6418", "0x6419", "0x6509", "0x6e00", "0x6f00", "0x6f01", "0x7002", "0x7004", "0x7005", 
									"0x7006", "0x7007", "0x7008", "0x7009", "0x700a", "0x700b", "0x700c", "0x700d", "0x700e", "0x7010", "0x7016"]
SectionsValues = ["0x11", "0x0d00", "0x0d"]
WaterValues = ["0x6009", "0x6012", "0x6100", "0x6104", "0x6118", "0x6414", "0x6509", "0x13", "0x28", "0x3c", "0x40", "0x41", "0x42", "0x43", "0x44",
						"0x46", "0x47", "0x48", "0x49", "0x4c", "0x4d", "0x51", "0x53", "0x0c", "0x18", "0x1f", "0x25", "0x26", "0x28", "0x6118", "0x4e", "0x4f",
						"0x2b", "0x32", "0x33"]
WildernessValues = ["0x1b", "0x3a"]
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
directory = "G:/Products/Garmin/" + product + "/" + state
to_directory = "C:/Users/mapmaker/HUNT_" + state
logFile = open("GarminProductCreation.log", 'a+')
logFile.writelines("Garmin Product Creation Script has been initialized at " + str(script_starttime) + "\n")
logFile.flush()
print("Garmin Product Creation Script has been initialized.")
temp_folder = directory + "/temp"
large_dir = to_directory + "/temp/"
huge_dir = large_dir + "big/"
large_dir2 = large_dir + "/big2/"
huge_dir2 = large_dir + "huge2/"
dict = {'AK' : 'Alaska', 'AL' : 'Alabama', 'AR' : 'Arkansas', 'AZ' : 'Arizona', 'CA' : 'California', 'CO' : 'Colorado', 'CT' : 'Connecticut', 'DE' : 'Delaware', 'FL' : 'Florida', 'GA' : 'Georgia', 'HI' : 'Hawaii', 'IA' : 'Iowa' , 'ID' : 'Idaho', 
				'IL' : 'Illinois',  'IN' : 'Indiana', 'KS' : 'Kansas', 'KY' : 'Kentucky', 'LA' : 'Louisiana', 'MA' : 'Massachusetts', 'MD' : 'Maryland', 'ME' : 'Maine', 'MI': 'Michigan', 'MN' : 'Minnesota', 'MO' : 'Missouri', 'MS' : 'Mississippi', 
				'MT' : 'Montana', 'NC' : 'NorthCarolina', 'ND' : 'NorthDakota', 'NE' : 'Nebraska', 'NH' : 'NewHampshire', 'NJ' : 'NewJersey', 'NM' : 'NewMexico', 'NV' : 'Nevada', 'NY' : 'NewYork', 'OH' : 'Ohio', 'OK' : 'Oklahoma', 'OR' : 'Oregon', 
				'PA' : 'Pennsylvania', 'RI' : 'RhodeIsland', 'SC' : 'SouthCarolina', 'SD' : 'SouthDakota', 'TN' : 'Tennessee', 'TX' : 'Texas', 'UT' : 'Utah', 'VA' : 'Virginia', 'VT' : 'Vermont', 'WA' : 'Washington', 'WI' : 'Wisconsin', 'WV' : 'WestVirginia', 'WY' : 'Wyoming'}

FID_dict = {'AK' : '1652', 'AL' : '1651', 'AR' : '1654', 'AZ' : '1653', 'CA' : '1655', 'CO' : '1656', 'CT' : '1657', 'DE' : '1658', 'FL' : '1659', 'GA' : '1660', 'HI' : '1661', 'ID' : '1662', 'IL' : '1663', 'IN' : '1664', 'IA' : '1665', 'KS' : '1666',
				 'KY' : '1667', 'LA' : '1668', 'ME' : '1669', 'MD' : '1670', 'MA' : '1671', 'MI' : '1672', 'MN' : '1673', 'MS' : '1674', 'MO' : '1675', 'MT' : '1626', 'NE' : '1677', 'NV' : '1678', 'NH' : '1679', 'NJ' : '1680', 'NM' : '1681', 'NY' : '1682',
				 'NC' : '1683', 'ND' : '1684', 'OH' : '1685', 'OK' : '1686', 'OR' : '1687', 'PA' : '1688', 'RI' : '1676', 'SC' : '1690', 'SD' : '1691', 'TN' : '1692', 'TX' : '1693', 'UT' : '1694', 'VT' : '1695', 'VA' : '1696', 'WA' : '1697', 'WV' : '1698', 'WI' : '1699', 'WY' : '1650'} 

MPdictionary = directory + "/RELEASEv" + version + "/dict-SMAv28_" + str(FID_dict[state]) + ".mp"

GarminTemplateDictionary = '''
[IMG ID]
ID=
Name=
DrawPriority=31
LBLcoding=6
Codepage=0
Marine=N
Elevation=f
Copyright=2019 onXmaps, Inc.
Preprocess=F
POIIndex=Y

TreSize=1000
RgnLimit=1024
Levels=6
Level0=24
Level1=22
Level2=21
Level3=20
Level4=19
Level5=18
Level6=17
Zoom0=1
Zoom1=2
Zoom2=3
Zoom3=4
Zoom4=5
zoom5=6
zoom6=6

Transparent=N

Lock=Y
ProductCode=1
RegionID=1
FID=''' + str(FID_dict[state]) + '''
[END-IMG ID]

[DICTIONARY]
Endlevel=7
;  1  Interstate       23  DON'T USE - WON'T DISPLAY IN MAPSOURCE
;  2  US Highway       24  Stream
;  3  State Highway    25  PARCEL BNDRY
;  4  Arterial Road    26  PARCEL BNDRY
;  5  Street           27  WILDERNESS BNDRY
;  6  Road             28  Political Boundary
;  7  Alley/RD         29  County Boundary
;  8  Ramp             30  Un-Dissolved Parcel
;  9  SKI LIFT         31  River
; 10  Unpaved Road     32  Contour - Minor
; 11  PARCEL<40ACRES   33  Contour - Inter
; 12  Ephemeral Stream 34  Contour - Major
; 13  FENCE            35  Depth Contour - Minor
; 14  ROAD             36  Depth Contour - Inter
; 15  BACKROAD         37  Depth Contour - Major
; 16  GMU BOUNDARY     38  Intermittent River
; 17  SECTION LINE     39  Airport Runway
; 18  ELK GMU          40  Pipeline
; 19  ANTELOPE GMU     41  Powerline
; 20  Railroad         42  Marine Boundary (no line)
; 21  PARCEL BNDRY     43  Marine Hazard (no line)
; 22  Trail			       45  0x2c - DON'T USE - WON'T DISPLAY IN BASECAMP
; 
;*** COULD USE THESE
;
;           0        1         2         3         4         5         6         7         8
;           12345678901234567890123456789012345678901234567890123456789012345678901234567890123
;           0              1               2               3               4                5
;           123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef01234567890abcdef012
Level1RGN40=11111101110011111111111111111010111111111111110000000000000000000000000000000000000
Level2RGN40=11110101110001111111110111111010000100000101010000000000000000000000000000000000000
Level3RGN40=11110101000000011110110010111010000100000101010000000000000000000000000000000000000
Level4RGN40=11100000000000010110000000010000000000000000000000000000000000000000000000000000000
Level5RGN40=11100000000000010000000000010000000000000000000000000000000000000000000000000000000
Level6RGN40=00000000000000000000000000000000000000000000000000000000000000000000000000000000000
;
;
;  1 City              23 City Park         45                     67 Lake
;  2 City              24 Golf              46                     68 Pond
;  3 Corps Rec Area    25 Sport             47                     69 Blue-Unknown
;  4 Military          26 Cemetery          48                     70 River
;  5 Parking Lot       27                   49                     71 River
;  6 Private Underlay  28                   50                     72 River
;  7 Airport           29                   51                     73 River
;  8 Shopping Center   30 State Park        52                     74
;  9 Marina            31 State Park        53                     75 Background
; 10 University        32 State Park        54                     76 Intermittent Water
; 11 Hospital          33                   55                     77 Glacier
; 12 Industrial        34                   56                     78 Orchard
; 13 Reservation       35                   57                     79 Scrub
; 14 Airport Runway    36                   58                     80 Woods
; 15                   37                   59 Blue-Unknown        81 Wetland
; 16                   38                   60 Lake                82 Tundra
; 17                   39                   61 Lake                83 Flats
; 18                   40 Ocean             62 Lake                84 Reef
; 19 Manmade Area      41                   63 Lake                85 Reef
; 20 National Park     42                   64 Lake                86 Reef
; 21 National Park     43                   65 Lake - !Small Lake  
; 22 National Park     44                   66 Estuary             
;
;
;	          0        1         2         3         4         5         6         7         8
;           12345678901234567890123456789012345678901234567890123456789012345678901234567890123456
;           0              1               2               3               4               5
;           123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456
Level1RGN80=11110110000111111111111111111111110111111111111111111111111111111111111110011111111111
Level2RGN80=11110100000010111111111110111111110111111111111111111111111111111100111110011010011111
Level3RGN80=11110000000010111101011110111111110111111111111110111111011111101100111110000010000111
Level4RGN80=11100000000010111101001100111111100001111111111110001001010100000100010000000000000000
Level5RGN80=11100000000010010001001000000111000000100000000000000000000000000100000000000000000000
Level6RGN80=00000000000000000000000000000000000000100000000000000000000000000000000000000000000000
;
; 01-11   Cities/towns
; 59      Airports
; 64      Manmade features (Cemeteris, mines, dams, etc.)
; 65      Water features (Falls, etc.)
; 66      Land features (summits, etc.)
;
;           0              1               2               3               4               5               6               7
;           123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0
Level0RGN10=1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111101
Level1RGN10=1111111111111111100000000001000000001000100000000000000000000000110000110101000001100000100000001100110000000001
Level2RGN10=1111111011110001000000000000000000001000100000000000000000000000100000110100000000100000100000000100110000000001
Level3RGN10=1111100011110001000000000000000000000000100000000000000000000000000000000000000000000000000000000000010000000010
Level4RGN10=1001000011110001000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000
Level5RGN10=1000000011110001000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000
Level6RGN10=0000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000
;
;           0              1               2               3               4               5               6               7
;           123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0
Level0RGN20=1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111101
Level1RGN20=1111111111111111100000000011000000001000100000000000000000000000110000110101000001100000100000001100110000000001
Level2RGN20=1111111011110001000000000010000000001000100000000000000000000000100000110100000000100000100000000100110000000001
Level3RGN20=1111100011110001000000000000000000000000100000000000000000000000000000000000000000000000000000000000010000000010
Level4RGN20=1001000011110001000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000
Level5RGN20=1000000011010001000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000
Level6RGN20=0000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000
[END DICTIONARY]
'''
CompleteAreas_G = "G:/Data_State/" + state + "/Parcels/" + year + "_complete/Complete_Areas"
CompleteAreas_Local = "C:/Users/mapmaker/temp/" + state + "/Complete_Areas"
CompleteAreas_Backup = "G:/Data_State/" + state + "/Parcels/" + year + "_complete/Complete_Areas_Backup"
MB_OKCANCEL = 0x1
MB_YESNO = 0x4
MB_ICONHAND = MB_ICONSTOP = MB_ICONERRPR = 0x10
MB_ICONEXCLAIMATION = 0x30
MB_SETFOREGROUND = 0x10000
MB_TOPMOST = 0x40000
messageBoxFunc = ctypes.windll.user32.MessageBoxA

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def ParcelUpdate():
	env.workspace = in_workspace
	print("Updating " + in_workspace)
	for fc in arcpy.ListFeatureClasses():
		AreaAcres = "AREA_ACRES"
		FieldList = arcpy.ListFields(fc)
		for Field in FieldList:
			if Field.name == AreaAcres:
				logFile.writelines("Updating " + fc + "\n")
				logFile.flush()
				print("Updating " + fc)
				fields = ['MP_TYPE', 'ONX_TYPE', 'NAME']
				WMA = '"ONX_TYPE" = \'WMA\''
				with arcpy.da.UpdateCursor (fc, fields, WMA) as rows:
					for row in rows:
						row[0] = '0x20'
						row[1] = 'WMA'
						rows.updateRow(row)
				LOCAL_temp = '"ONX_TYPE" LIKE \'COUNTY\'' 
				with arcpy.da.UpdateCursor (fc, fields, LOCAL_temp) as rows:
					for row in rows:
						row[0] = '0x26'
						row[1] = 'LOCAL'
						rows.updateRow(row)
    		
						
				NO_OWNER_DATA = '"ONX_TYPE" = \'NO_OWNER_DATA\''
				with arcpy.da.UpdateCursor(fc, fields, NO_OWNER_DATA) as rows:
					for row in rows:
						row[0] = '0x25'
						row[1] = 'NO_OWNER_DATA'
						rows.updateRow(row)
						
				NO_DATA = '"ONX_TYPE" = \'NO_DATA\''
				with arcpy.da.UpdateCursor(fc, fields, NO_DATA) as rows:
					for row in rows:
						row[0] = '0x25'
						row[1] = 'NO_DATA'
						rows.updateRow(row)
    		
				UNDERLAY = '"ONX_TYPE" = \'UNDERLAY\''
				with arcpy.da.UpdateCursor (fc, fields, UNDERLAY) as rows:
					for row in rows:
						row[0] = '0x06'
						row[1] = 'UNDERLAY'
						rows.updateRow(row)
    		
				LOCAL_PARK_FOREST_URBAN = '"ONX_TYPE" = \'LOCAL_PARK_FOREST_URBAN\' OR "ONX_TYPE" = \'LOCAL_FOREST_PARK_URBAN\''
				with arcpy.da.UpdateCursor (fc, fields, LOCAL_PARK_FOREST_URBAN) as rows:
					for row in rows:
						row[0] = '0x16'
						row[1] = 'LOCAL_PARK_FOREST_URBAN'
						rows.updateRow(row)
    		
				
				LOCAL_PARK_FOREST = '"ONX_TYPE" = \'LOCAL_PARK_FOREST\' OR "ONX_TYPE" = \'LOCAL_FOREST_PARK\''
				with arcpy.da.UpdateCursor (fc, fields, LOCAL_PARK_FOREST) as rows:
					for row in rows:
						row[0] = '0x17'
						row[1] = 'LOCAL_PARK_FOREST'
						rows.updateRow(row)
    		
				LOCAL_PARK_FOREST_URBAN = '("ONX_TYPE" = \'LOCAL_PARK_FOREST_URBAN\' OR "ONX_TYPE" = \'LOCAL_FOREST_PARK_URBAN\') AND "AREA_ACRES" > 37'
				with arcpy.da.UpdateCursor (fc, fields, LOCAL_PARK_FOREST_URBAN) as rows:
					for row in rows:
						row[0] = '0x17'
						row[1] = 'LOCAL_PARK_FOREST'
						rows.updateRow(row)
    		
				LOCAL_PARK_FOREST_URBAN = '("ONX_TYPE" = \'LOCAL_PARK_FOREST\' OR "ONX_TYPE" = \'LOCAL_FOREST_PARK\') AND "AREA_ACRES" < 37'
				with arcpy.da.UpdateCursor (fc, fields, LOCAL_PARK_FOREST_URBAN) as rows:
					for row in rows:
						row[0] = '0x16'
						row[1] = 'LOCAL_PARK_FOREST_URBAN'
						rows.updateRow(row)
    		
				LOCAL = '("ONX_TYPE" LIKE \'LOCAL\' OR "ONX_TYPE" = \'LOCAL_SMALL\' OR "ONX_TYPE" = \'LOCAL_XSMALL\') AND "AREA_ACRES" > 37' 
				with arcpy.da.UpdateCursor (fc, fields, LOCAL) as rows:
					for row in rows:
						row[0] = '0x26'
						row[1] = 'LOCAL'
						rows.updateRow(row)
    		
				local_small = '("ONX_TYPE" LIKE \'LOCAL\' OR "ONX_TYPE" = \'LOCAL_SMALL\' OR "ONX_TYPE" = \'LOCAL_XSMALL\') AND "AREA_ACRES" > 1.9 AND "AREA_ACRES" < 37'
				with arcpy.da.UpdateCursor (fc, fields, local_small) as rows:
					for row in rows:
						row[0] = '0x32'
						row[1] = 'LOCAL_SMALL'
						rows.updateRow(row)
    		
				LOCAL_XSMALL = '("ONX_TYPE" LIKE \'LOCAL\' OR "ONX_TYPE" = \'LOCAL_SMALL\' OR "ONX_TYPE" = \'LOCAL_XSMALL\') AND "AREA_ACRES" <= 1.9'
				with arcpy.da.UpdateCursor (fc, fields, LOCAL_XSMALL) as rows:
					for row in rows:
						row[0] = '0x0e'
						row[1] = 'LOCAL_XSMALL'
						rows.updateRow(row)
    		
				COUNTY_EDUCATION = '"ONX_TYPE" = \'COUNTY_EDUCATION\''
				with arcpy.da.UpdateCursor (fc, fields, COUNTY_EDUCATION) as rows:
					for row in rows:
						row[0] = '0x32'
						row[1] = 'COUNTY_EDUCATION'
						rows.updateRow(row)
    		
				EMERGENCY_SERVICES = '"ONX_TYPE" = \'EMERGENCY_SERVICES\''
				with arcpy.da.UpdateCursor (fc, fields, EMERGENCY_SERVICES) as rows:
					for row in rows:
						row[0] = '0x32'
						row[1] = 'EMERGENCY_SERVICES'
						rows.updateRow(row)
    		
				HIGHER_EDUCATION = '"ONX_TYPE" = \'HIGHER_EDUCATION\''
				with arcpy.da.UpdateCursor (fc, fields, HIGHER_EDUCATION) as rows:
					for row in rows:
						row[0] = '0x18'
						row[1] = 'HIGHER_EDUCATION'
						rows.updateRow(row)
					
				STATE = '"ONX_TYPE" = \'STATE\''
				with arcpy.da.UpdateCursor (fc, fields, STATE) as rows:
					for row in rows:
						row[0] = '0x31'
						row[1] = 'STATE'
						rows.updateRow(row)
    		
				STATE_URBAN = '"ONX_TYPE" = \'STATE\' AND "AREA_ACRES" < 37'
				with arcpy.da.UpdateCursor (fc, fields, STATE_URBAN) as rows:
					for row in rows:
						row[0] = '0x15'
						row[1] = 'STATE_URBAN'
						rows.updateRow(row)
    		
				STATE_FOREST = '"ONX_TYPE" = \'STATE_FOREST\''
				with arcpy.da.UpdateCursor (fc, fields, STATE_FOREST) as rows:
					for row in rows:
						row[0] = '0x14'
						row[1] = 'STATE_FOREST'
						rows.updateRow(row)
    		
				STATE_PARK = '"ONX_TYPE" = \'STATE_PARK\''
				with arcpy.da.UpdateCursor (fc, fields, STATE_PARK) as rows:
					for row in rows:
						row[0] = '0x1f'
						row[1] = 'STATE_PARK'
						rows.updateRow(row)
    		
				STATE_DOT = '"ONX_TYPE" = \'STATE_DOT\''
				with arcpy.da.UpdateCursor (fc, fields, STATE_DOT) as rows:
					for row in rows:
						row[0] = '0x32'
						row[1] = 'STATE_DOT'
						rows.updateRow(row)
    		
				STATE_FISH_WILDLIFE = '"ONX_TYPE" = \'STATE_FISH_WILDLIFE\''
				with arcpy.da.UpdateCursor (fc, fields, STATE_FISH_WILDLIFE) as rows:
					for row in rows:
						row[0] = '0x38'
						row[1] = 'STATE_FISH_WILDLIFE'
						rows.updateRow(row)
    		
				USA_UNCLASSIFIED = '"ONX_TYPE" = \'USA_UNCLASSIFIED\''
				with arcpy.da.UpdateCursor (fc, fields, USA_UNCLASSIFIED) as rows:
					for row in rows:
						row[0] = '0x30'
						row[1] = 'USA_UNCLASSIFIED'
						rows.updateRow(row)
    		
				FEDERAL_OTHER = '"ONX_TYPE" = \'FEDERAL_OTHER\''
				with arcpy.da.UpdateCursor (fc, fields, FEDERAL_OTHER)  as rows:
					for row in rows:
						row[0] = '0x30'
						row[1] = 'FEDERAL_OTHER'
						rows.updateRow(row)
    		
				FEDERAL_URBAN = '"ONX_TYPE" = \'FEDERAL_URBAN\' OR (("ONX_TYPE" = \'USA_UNCLASSIFIED\' OR "ONX_TYPE" = \'FEDERAL_OTHER\') AND "AREA_ACRES" < 37)'
				with arcpy.da.UpdateCursor (fc, fields, FEDERAL_URBAN)  as rows:
					for row in rows:
						row[0] = '0x52'
						row[1] = 'FEDERAL_URBAN'
						rows.updateRow(row)
    		
				CORPS = '"ONX_TYPE" = \'CORPS\''
				with arcpy.da.UpdateCursor (fc, fields, CORPS) as rows:
					for row in rows:
						row[0] = '0x0d'
						row[1] = 'CORPS'
						rows.updateRow(row)
						
				CORPS_REC = '"ONX_TYPE" = \'CORPS_REC\''
				with arcpy.da.UpdateCursor (fc, fields, CORPS_REC) as rows:
					for row in rows:
						row[0] = '0x03'
						row[1] = 'CORPS_REC'
						rows.updateRow(row)
    		
				NPS = '"ONX_TYPE" = \'NPS\''
				with arcpy.da.UpdateCursor (fc, fields, NPS) as rows:
					for row in rows:
						row[0] = '0x2b'
						row[1] = 'NPS'
						rows.updateRow(row)
    		
				USFW = '"ONX_TYPE" = \'USFW\''
				with arcpy.da.UpdateCursor (fc, fields, USFW) as rows:
					for row in rows:
						row[0] = '0x2f'
						row[1] = 'USFW'
						rows.updateRow(row)
    		
				USFS = '"ONX_TYPE" = \'USFS\''
				with arcpy.da.UpdateCursor (fc, fields, USFS) as rows:
					for row in rows:
						row[0] = '0x2a'
						row[1] = 'USFS'
						rows.updateRow(row)
    		
				BLM = '"ONX_TYPE" = \'BLM\''
				with arcpy.da.UpdateCursor (fc, fields, BLM) as rows:
					for row in rows:
						row[0] = '0x29'
						row[1] = 'BLM'
						rows.updateRow(row)
    		
				BOR = '"ONX_TYPE" = \'BOR\''
				with arcpy.da.UpdateCursor (fc, fields, BOR) as rows:
					for row in rows:
						row[0] = '0x2d'
						row[1] = 'BOR'
						rows.updateRow(row)
    		
				TVA = '"ONX_TYPE" = \'TVA\''
				with arcpy.da.UpdateCursor (fc, fields, TVA) as rows:
					for row in rows:
						row[0] = '0x2d'
						row[1] = 'TVA'
						rows.updateRow(row)
    		
				NGO = '"ONX_TYPE" = \'NGO\''
				with arcpy.da.UpdateCursor (fc, fields, NGO) as rows:
					for row in rows:
						row[0] = '0x35'
						row[1] = 'NGO'
						rows.updateRow(row)
    		
				DOD = '"ONX_TYPE" = \'DOD\''
				with arcpy.da.UpdateCursor (fc, fields, DOD) as rows:
					for row in rows:
						row[0] = '0x2e'
						row[1] = 'DOD'
						rows.updateRow(row)
    		
				BIA = '"ONX_TYPE" = \'BIA\''
				with arcpy.da.UpdateCursor (fc, fields, BIA) as rows:
					for row in rows:
						row[0] = '0x2c'
						row[1] = 'BIA'
						rows.updateRow(row)
    		
				MISC_ACCESS = '"ONX_TYPE" = \'MISC_ACCESS\''
				with arcpy.da.UpdateCursor (fc, fields, MISC_ACCESS) as rows:
					for row in rows:
						row[0] = '0x33'
						row[1] = 'MISC_ACCESS'
						rows.updateRow(row)
    		
				TIMBER_ACCESS = '"ONX_TYPE" = \'TIMBER_ACCESS\''
				with arcpy.da.UpdateCursor (fc, fields, TIMBER_ACCESS) as rows:
					for row in rows:
						row[0] = '0x21'
						row[1] = 'TIMBER_ACCESS'
						rows.updateRow(row)
    		
				TIMBER_UNKNOWN_ACCESS = ' "ONX_TYPE" = \'TIMBER_UNKNOWN_ACCESS\''
				with arcpy.da.UpdateCursor (fc, fields, TIMBER_UNKNOWN_ACCESS) as rows:
					for row in rows:
						row[0] = '0x22'
						row[1] = 'TIMBER_UNKNOWN_ACCESS'
						rows.updateRow(row)
    		
				private_med = '"ONX_TYPE" LIKE \'PRIVATE%\''
				with arcpy.da.UpdateCursor (fc, fields, private_med) as rows:
					for row in rows:
						row[0] = '0x24'
						row[1] = 'PRIVATE'
						rows.updateRow(row)
    		
				private_small = '"ONX_TYPE" LIKE \'PRIVATE%\' AND "AREA_ACRES" > 1.9 AND "AREA_ACRES" < 37'
				with arcpy.da.UpdateCursor (fc, fields,private_small) as rows:
					for row in rows:
						row[0] = '0x39'
						row[1] = 'PRIVATE_SMALL' 
						rows.updateRow(row)
    		
				private_xsmall = '"ONX_TYPE" LIKE \'PRIVATE%\' AND "AREA_ACRES" <= 1.9'
				with arcpy.da.UpdateCursor (fc, fields,private_xsmall) as rows:
					for row in rows:
						row[0] = '0x23'
						row[1] = 'PRIVATE_XSMALL'
						rows.updateRow(row)
				print(fc + " Updated")
				logFile.writelines(fc + " updated" + "\n")
				logFile.flush()  


def writeTranscodeQ():
	time.sleep(1)
	print("Writing transcodeq.txt file")
	logFile.writelines("Writing transcodeq.txt file" + "\n")
	logFile.flush()
	mpFile = open("C:/Users/mapmaker/HUNT_" + state + "/" + state + "mpfiles.txt", 'w')
	mydir = "C:/Users/mapmaker/HUNT_" + state 
	os.chdir(mydir)
	for file in glob.glob("*.mp"):
		mpFile.writelines(str(mydir + "/" + file) + '\n')
		mpFile.flush()
	print("List of .mp files written. Script complete.")
	logFile.writelines("List of .mp files written. Script complete." + "\n")
	logFile.flush()


def deleteTempFolder(temp_folder):
    if os.path.exists(temp_folder):
        try:
            if os.path.isdir(temp_folder):
                shutil.rmtree(temp_folder, ignore_errors=True)
            else:
                os.remove(temp_folder)
        except:
            print "Exception ",str(sys.exc_info())
    else:
        print "not found ",temp_folder
def compile_img(run):
	subprocess.Popen('C:/Users/mapmaker/HUNT_' + state + '/cgpsrun' + run + '/transcode.bat', cwd='C:/Users/mapmaker/HUNT_' + state + '/cgpsrun' + run)
	print("Starting cgpsrun" + run)
def confirm( buttons=['OK', 'Cancel']):
	title = "MP_TYPE field error check"
	text = "Would you like the script to check " + state + " for MP_TYPE errors?"
	retVal = messageBoxFunc(0, text, title, MB_YESNO | MB_ICONEXCLAIMATION | MB_SETFOREGROUND | MB_TOPMOST)
	if retVal == 6 or len(buttons)==6:
		title = "Run Update Section?"
		text = "Would you like to run the Update Section of the script during the MP_TYPE check?"
		RunUpdateSectionValue = messageBoxFunc(0, text, title, MB_YESNO | MB_ICONEXCLAIMATION | MB_SETFOREGROUND | MB_TOPMOST)

		print("Checking MP_TYPES")
		in_workspace = "G:/Data_State/" + state + "/Administrative_Boundaries/2013_complete"
		starttime = datetime.now()
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = AdminValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		logFile.flush()
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/Bathymetry/complete"
		nullvalues = BathyValues
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/GMU/complete"
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = GMUValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/GNIS/complete"
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = GNISValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		time.sleep(5)
		#
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/Parks/Complete"
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = ParkValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/Parcels/" + year + "_complete/Complete_Areas"
		env.workspace = in_workspace
		if RunUpdateSectionValue == 6:
			print(" Making backup copy of the Complete_Areas folder")
			logFile.writelines("Making backup copy of the Complete_Areas folder" + "\n")
			logFile.flush()
			copy_tree(CompleteAreas_G, CompleteAreas_Backup)
			print("Backup copy of Complete_Areas folder made")
			logFile.writelines("Backup copy of Complete_Areas folder made" + "\n")
			logFile.flush()
			print("Copying Complete_Areas folder locally")
			logFile.writelines("Copying Complete_Areas folder locally" + "\n")
			logFile.flush()
			copy_tree(CompleteAreas_G, CompleteAreas_Local)
			print("Complete_Areas folder copied locally")
			logFile.writelines("Complete_Areas folder copied locally" + "\n")
			logFile.flush()
			in_workspace = CompleteAreas_Local
			ParcelUpdate() 
		elif RunUpdateSectionValue == 7:
			print("Update Section of script skipped.")
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		print("Checking " + in_workspace)
		nullvalues = ParcelAreaValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		time.sleep(5)
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/Parcels/" + year + "_complete/Complete_Inside_Lines"
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = ParcelInsideLinesValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		time.sleep(5)
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/Parcels/" + year + "_complete/Complete_Lines"
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = ParcelLinesValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		time.sleep(5)
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/Parcels/" + year + "_complete/Complete_Points"
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = ParcelPointValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		time.sleep(5)
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/Recreation_Points/complete"
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = RecreationPointsValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/Sections/complete"
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = SectionsValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/Water/complete"
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = WaterValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		starttime = datetime.now()
		in_workspace = "G:/Data_State/" + state + "/Wilderness/complete"
		print("Checking " + in_workspace)
		logFile.writelines("Checking " + in_workspace + "\n")
		logFile.flush()
		nullvalues = WildernessValues
		checkMP(in_workspace, nullvalues)
		runtime = datetime.now() - starttime
		logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
		logFile.flush()
		runtime = datetime.now() - script_starttime
		logFile.writelines("MP field check time was " + str(runtime) + "\n")
		logFile.flush()


		return buttons[0]
	elif retVal == 7:
		return buttons[1]
		print("Cancel")
	else:
		assert False, 'Unexpected return value from MessageBox: %s' % (retVal)
def checkMP(in_workspace, nullvalues):
	logFile = open("GarminProductCreation.log", 'a+')
	arcpy.env.workspace = in_workspace
	field_name_list = ["MP_TYPE"]
	feature_classes = []
	walk = arcpy.da.Walk(in_workspace, datatype='FeatureClass')
	for dirpath, dirnames, filenames in walk:
		for filename in filenames:
			feature_classes.append(os.path.join(dirpath, filename))
	if len(feature_classes) > 0:
		FCs = arcpy.ListFeatureClasses("*")
		for fc in FCs:
			desc = arcpy.Describe(fc)
			print("Checking " + desc.name)
			logFile.writelines(desc.name + "\n")
			logFile.flush()
			fc_path = desc.catalogPath
			lfields = arcpy.ListFields(fc_path)
			for f in lfields:
				#print f.name
				if f.name.upper() in field_name_list:
					rowCount = 0
					with arcpy.da.SearchCursor(fc_path, f.name) as cur:
						for row in cur:
							v = row[0]
							if not(v in nullvalues):
								rowCount += 1
					if rowCount == 0:
						print(f.name, " is correct")
						logFile.writelines(f.name + " is correct." + "\n")
						logFile.flush()
					else:
						print(f.name + " has an error. Ensuring field values are lowercase.")
						logFile.writelines(desc.name + f.name + " has an error. Ensuring field values are lowercase." + "\n")
						if desc.name != nullvalues:
							file = f.name
							arcpy.CalculateField_management(desc.name, "MP_TYPE", '!MP_TYPE!.lower()', 'PYTHON_9.3', '')
							rowCount = 0
							with arcpy.da.SearchCursor(fc_path, f.name) as cur:
								for row in cur:
									v = row[0]
									if not(v in nullvalues):
										rowCount += 1
							if rowCount == 0:
								print f.name, " has been field caculated to lower case and is now correct."
								logFile.writelines(f.name + " has been field caculated to lower case and is now correct." + "\n")
								logFile.flush()
							else:
								print f.name, " ******************************************************  is incorrect!!!!! A value is either missing, incorrect, or the script needs to be updated."
								logFile.writelines(desc.name + f.name + " ********************************** is incorrect!!!!!!!! A value is either missing, incorrect, or the script needs to be updated." + "\n")
								logFile.flush()
								emailfrom = 'script.notification.email@gmail.com'
								emailto = toaddr
								fileToSend = "GarminProductCreation.log"
								username = 'script.notification.email@gmail.com'
								password = 'FishandChips'
								msg = MIMEMultipart()
								msg["From"] = emailfrom
								msg["To"] = emailto
								msg["Subject"] = "There was an error with the MP_TYPE field"
								msg.preamble = "Please see attached logfile to view the error."
								ctype, encoding = mimetypes.guess_type(fileToSend)
								if ctype is None or encoding is not None:
								    ctype = "application/octet-stream"
								maintype, subtype = ctype.split("/", 1)
								if maintype == "text":
								    fp = open(fileToSend)
								    attachment = MIMEText(fp.read(), _subtype=subtype)
								    fp.close()
								elif maintype == "image":
								    fp = open(fileToSend, "rb")
								    attachment = MIMEImage(fp.read(), _subtype=subtype)
								    fp.close()
								elif maintype == "audio":
								    fp = open(fileToSend, "rb")
								    attachment = MIMEAudio(fp.read(), _subtype=subtype)
								    fp.close()
								else:
								    fp = open(fileToSend, "rb")
								    attachment = MIMEBase(maintype, subtype)
								    attachment.set_payload(fp.read())
								    fp.close()
								    encoders.encode_base64(attachment)
								attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
								msg.attach(attachment)
								
								server = smtplib.SMTP("smtp.gmail.com:587")
								server.starttls()
								server.login(username,password)
								server.sendmail(emailfrom, emailto, msg.as_string())
								server.quit()

								time.sleep(1)
						print("")
						logFile.flush()
						time.sleep(1)
	else:
		print("feature classes not found")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Creates working directories
try:
	os.makedirs(large_dir)
	print(large_dir + " made")
except OSError as exception:
	if exception.errno != errno.EEXIST:
		raise
try:
	os.makedirs(huge_dir)
	print(huge_dir + " made")
except OSError as exception:
	if exception.errno != errno.EEXIST:
		raise
try:
	os.makedirs(large_dir2)
	print(large_dir2 + " made")
except OSError as exception:
	if exception.errno != errno.EEXIST:
		raise
try:
	os.makedirs(huge_dir2)
	print(huge_dir2 + " made")
except OSError as exception:
	if exception.errno != errno.EEXIST:
		raise
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Script starts

print("Checking for correct dictionary")
if os.path.isfile(MPdictionary)==False:
	try:
		os.makedirs("G:/Products/Garmin/Premium/" + state + "/RELEASEv" + version)
	except:
		print("Release version folder found")
	Dictionary = open(MPdictionary, 'w')
	Dictionary.writelines(GarminTemplateDictionary + "\n")
	Dictionary.flush()
	Dictionary.close()
	print("Export Dictionary Written")
if os.path.isfile(MPdictionary)==True:
	print("Correct Dictionary Found.")
print("Checking for Complete_Areas_Backup folder on G:")
logFile.writelines("Checking for Complete_Areas_Backup folder on G:" + "\n")
logFile.flush()
print("Checking for old Global Mapper Catalogs, Saved Workspaces, and Transportation Files")
logFile.writelines("Checking for old Global Mapper Catalogs, Saved Workspaces, and Transportation Files" + "\n")
logFile.flush()
PremiumFolder = os.listdir(directory)
for item in PremiumFolder:
	if item.endswith(".MP"):
		os.remove(join(directory, item))
		print("Old transportation file found and removed")
		logFile.writelines("Old transportation file found and removed" + "\n")
		logFile.flush()
	elif item.endswith(".GMC"):
		os.remove(join(directory, item))
		print("Old catalogs found and removed")
		logFile.writelines("Old catalogs found and removed" + "\n")
		logFile.flush()
	elif item.endswith(".GMW"):
		os.remove(join(directory, item))
		print("Old saved workspace found and removed")
		logFile.writelines("Old saved workspace found and removed" + "\n")
		logFile.flush()
	elif item.endswith(".gmw"):
		os.remove(join(directory, item))
		print("Old saved workspace found and removed")
		logFile.writelines("Old saved workspace found and removed" + "\n")
		logFile.flush()
if os.path.isdir(CompleteAreas_Backup)==True:
	text = "WARNING: Complete_Areas_Backup folder already exists. Should I delete this folder?"
	title = "Backup Directory Already Exists!"
	retVal = messageBoxFunc(0, text, title, MB_YESNO | MB_ICONEXCLAIMATION | MB_SETFOREGROUND | MB_TOPMOST)
	if retVal == 6:
		if os.path.exists(CompleteAreas_Backup):
			try:
				if os.path.isdir(CompleteAreas_Backup):
					shutil.rmtree(CompleteAreas_Backup)
				else:
					os.remove(CompleteAreas_Backup)
			except:
				print "Exception ",str(sys.exc_info())
		else:
			print("not found" , CompleteAreas_Backup)
if os.path.isdir(CompleteAreas_Local):
	text = "WARNING:  Local Complete_Areas folder already exists. Should I delete this folder?"
	title = "Local Complete_Areas Directory Already Exists!"
	retVal = messageBoxFunc(0, text, title, MB_YESNO | MB_ICONEXCLAIMATION | MB_SETFOREGROUND | MB_TOPMOST)
	if retVal == 6:
		if os.path.exists(CompleteAreas_Local):
			try:
				if os.path.isdir(CompleteAreas_Local):
					shutil.rmtree(CompleteAreas_Local)
				else:
					os.remove(CompleteAreas_Local)
			except:
				print "Exception ",str(sys.exc_info())
		else:
			print("not found" , CompleteAreas_Local)
	elif retVal == 7:
		print("Folder not deleted")
# Gives option to check for correct MP_TYPE field values
buttons=['OK', 'Cancel']
title = "MP_TYPE field error check"
text = "Would you like the script to check " + state + " for MP_TYPE errors?"
retVal = messageBoxFunc(0, text, title, MB_YESNO | MB_ICONEXCLAIMATION | MB_SETFOREGROUND | MB_TOPMOST)
if retVal == 6 or len(buttons)==6:
	title = "Run Update Section?"
	text = "Would you like to run the Update Section of the script during the MP_TYPE check?"
	RunUpdateSectionValue = messageBoxFunc(0, text, title, MB_YESNO | MB_ICONEXCLAIMATION | MB_SETFOREGROUND | MB_TOPMOST)
	while datetime.now() < ResumeTime:
		print("The script is sleeping")
		time.sleep(10)
	print("Checking MP_TYPES")
	in_workspace = "G:/Data_State/" + state + "/Administrative_Boundaries/2013_complete"
	starttime = datetime.now()
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = AdminValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	logFile.flush()
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/Bathymetry/complete"
	nullvalues = BathyValues
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/GMU/complete"
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = GMUValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/GNIS/complete"
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = GNISValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	time.sleep(5)
	#
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/Parks/Complete"
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = ParkValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	#
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/Parcels/" + year + "_complete/Complete_Areas"
	env.workspace = in_workspace
	if RunUpdateSectionValue == 6:
		print(" Making backup copy of the Complete_Areas folder")
		logFile.writelines("Making backup copy of the Complete_Areas folder")
		logFile.flush()
		copy_tree(CompleteAreas_G, CompleteAreas_Backup)
		print("Backup copy of Complete_Areas folder made")
		logFile.writelines("Backup copy of Complete_Areas folder made")
		logFile.flush()
		print("Copying Complete_Areas folder locally")
		logFile.writelines("Copying Complete_Areas folder locally")
		logFile.flush()
		copy_tree(CompleteAreas_G, CompleteAreas_Local)
		print("Complete_Areas folder copied locally")
		logFile.writelines("Complete_Areas folder copied locally")
		logFile.flush()
		in_workspace = CompleteAreas_Local
		ParcelUpdate() 
	elif RunUpdateSectionValue == 7:
		print("Update Section of script skipped.")
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	print("Checking " + in_workspace)
	nullvalues = ParcelAreaValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	time.sleep(5)
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/Parcels/" + year + "_complete/Complete_Inside_Lines"
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = ParcelInsideLinesValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	time.sleep(5)
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/Parcels/" + year + "_complete/Complete_Lines"
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = ParcelLinesValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	time.sleep(5)
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/Parcels/" + year + "_complete/Complete_Points"
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = ParcelPointValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	time.sleep(5)
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/Recreation_Points/complete"
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = RecreationPointsValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/Sections/complete"
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = SectionsValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/Water/complete"
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = WaterValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	starttime = datetime.now()
	in_workspace = "G:/Data_State/" + state + "/Wilderness/complete"
	print("Checking " + in_workspace)
	logFile.writelines("Checking " + in_workspace + "\n")
	logFile.flush()
	nullvalues = WildernessValues
	checkMP(in_workspace, nullvalues)
	runtime = datetime.now() - starttime
	logFile.writelines(in_workspace + " took " + str(runtime) + "\n")
	logFile.flush()
	runtime = datetime.now() - script_starttime
	logFile.writelines("MP field check time was " + str(runtime) + "\n")
	logFile.flush()

elif retVal == 7:
	print("Cancel")
	RunUpdateSectionValue = 7
else:
	assert False, 'Unexpected return value from MessageBox: %s' % (retVal)

# Creates temp folder to write Global Mapper Scripts, and various other files to 
try:
	os.makedirs(temp_folder)
except OSError as exception:
	if exception.errno != errno.EEXIST:
		raise
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Copies cgps processing folders and contents to Mapbeast. If the state folder on Mapbeast doesn't exist, script will create it.
copy_tree(from_directory, to_directory)
print("Creating TYP file")
template = "G:/Products/Garmin/Garmin_Master_Misc/template/owntypv25.typ"
batfile = "C:/Users/mapmaker/temp/typbatfile.bat"
typname = "hunt" + state.lower() + ".typ"
typfile = "C:/Users/mapmaker/HUNT_" + state + "/cgpsrun1/" + typname
makebatfile = open(batfile, 'w')
makebatfile.writelines('''
cd C:/users/mapmaker
C:/Users/mapmaker/twz -fid=''' + str(FID_dict[state]) + ''' -s=''' + template + ''' -o=''' + typfile + ''' ''' + '\n')
makebatfile.flush()
makebatfile.close()
p= Popen(r'start cmd /c' + batfile, shell=True)
p.wait()
print("TYP file made")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Creates Transportation MP file
logFile.writelines("Writing Transportation MP file." + "\n")
logFile.flush()
Transportation_gdb = "G:/Projects/Activity_Processing/StateTrails_Current.gdb/StateTrails/" + dict[state]
arcpy.FeatureClassToFeatureClass_conversion(Transportation_gdb, "C:/Users/mapmaker/temp", state + "_Trails.shp")
GMscript = temp_folder + "/Transportation_MP_Export.gms"
mpexport = open(GMscript, 'w')
mpexport.writelines('''
GLOBAL_MAPPER_SCRIPT VERSION=1.00
DEFINE_VAR NAME="state" VALUE="''' + state + '''"
DEFINE_VAR NAME="product" VALUE="''' + product + '''"
DEFINE_VAR NAME="FID" VALUE="''' + str(FID_dict[state]) + '''"
DEFINE_VAR NAME="version" VALUE="''' + version + '''"
DEFINE_VAR NAME="template_path" VALUE="G:\Products\Garmin\%product%\%state%\RELEASEv%version%"            
IMPORT FILENAME="G:\Data_State\%state%\Transportation\complete\Bordering_''' + state + '''_OtherTransportation.shp" TYPE=SHAPEFILE
IMPORT FILENAME="G:\Data_State\%state%\Transportation\complete\\''' + state + '''_OtherTransportation.shp" TYPE=SHAPEFILE
IMPORT FILENAME="G:\Data_State\%state%\Transportation\complete\\''' + state + '''_TIGER.shp" TYPE=SHAPEFILE
EDIT_VECTOR DELETE_FEATURES=YES COMPARE_STR="MP_TYPE=0x16"
EDIT_VECTOR DELETE_FEATURES=YES COMPARE_STR="MP_TYPE=0x2d"
IMPORT FILENAME="C:\Users\mapmaker\\temp\\''' + state + '''_Trails.shp" TYPE=SHAPEFILE
EXPORT_VECTOR FILENAME="G:\Products\Garmin\Premium\%state%\%state%_TRANSPORTATION.MP" TYPE=POLISH_MP MAP_NAME=%state%_TRANSPORTATION TEMPLATE_FILENAME="%template_path%\dict-SMAv28_%FID%.mp" MP_EXPORT_TEMPLATE_FILES=NO MP_COPY_ENTIRE_TEMPLATE=NO MP_IMAGE_ID=0
UNLOAD_ALL
''' + '\n')
mpexport.flush()
mpexport.close()
print("Initiating Global Mapper Transportation MP file export.")
p = subprocess.Popen(["C:\Program Files\GlobalMapper18_64bit\global_mapper.exe", GMscript])
p.wait()
for filename in glob.glob("C:/Users/mapmaker/temp/" + state + "_Trails*"):
	os.remove(filename)
print(state + " Tranpsortation MP file written.")
logFile.writelines(state + " Tranpsortation MP file written." + "\n")
logFile.flush()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Removes icons from Transportation MP file
logFile.writelines("Removing tildas from " + state + " Transportation MP file." + "\n")
logFile.flush()
print("Removing tildas from " + state + " Transportation MP file.")
fileToSearch = directory + "/" + state + "_TRANSPORTATION.MP"
replacements = {'~[0x2a]':'', '~[0x2b]':'', '~[0x2c]':'', '~[0x2d]':'', '~[0x2e]':'', '~[0x2f]':'', '~[0x2g]':'', '~[0x2h]':'', '~[0x2A]':'', '~[0x2B]':'', '~[0x2C]':'', '~[0x2D]':'', '~[0x2E]':'', '~[0x2F]':'', '~[0x2G]':'', '~[0x2H]':''}
lines = []
with open(fileToSearch) as infile:
	for line in infile:
		for src, target in replacements.iteritems():
			line = line.replace(src, target)
		lines.append(line)
with open(fileToSearch, 'w') as outfile:
	for line in lines:
		outfile.write(line)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Copy Recreation Points and NPS data to temp directory
if os.path.exists("C:/Users/mapmaker/temp/" + state + "/Recreation_Points"):
	try:
		if os.path.isdir("C:/Users/mapmaker/temp/" + state + "/Recreation_Points"):
			shutil.rmtree("C:/Users/mapmaker/temp/" + state + "/Recreation_Points", ignore_errors=True)
			print(state + " temp folder removed")
		else:
			os.remove("C:/Users/mapmaker/temp/" + state + "/Recreation_Points")
			print(state + " temp folder removed")
	except:
		print "Exception ",str(sys.exc_info())

if os.path.exists("C:/Users/mapmaker/temp/" + state + "_Recreation_Points.gdb"):
	try:
		if os.path.isdir("C:/Users/mapmaker/temp/" + state + "_Recreation_Points.gdb"):
			shutil.rmtree("C:/Users/mapmaker/temp/" + state + "_Recreation_Points.gdb", ignore_errors=True)
			print(state + " temp folder removed")
		else:
			os.remove("C:/Users/mapmaker/temp/" + state + "_Recreation_Points.gdb")
			print(state + " temp folder removed")
	except:
		print "Exception ",str(sys.exc_info())

sr2 = arcpy.SpatialReference(4326)
print("Copying files currently in Recreation_Points/Complete to local temp directory")
copy_tree("G:/Data_State/" + state + "/Recreation_Points/Complete", "C:/Users/mapmaker/temp/" + state + "/Recreation_Points/Complete")
print("Complete directory copied locally")
print("Defining MAPS state")
MAPS_States = open("G:/Data_National/RecreationPoints/Reference/MAPS_States.txt")
MAPS_lines = MAPS_States.read().split("\n")
MAP = MAPS_lines
print("MAPS States defined")
for MAP in MAPS_lines:
	if MAP == state:
		print(state + " is a MAPS ready state!")
		print("Converting for use in Garmin Chip")
		copy_tree("G:/Data_State/" + state + "/Recreation_Points/MAPS/Complete/" + state + "_RecreationPoints.gdb", "C:/Users/mapmaker/temp/Recreation_Points/" + state + "_Recreation_Points.gdb")
		print("		gdb copied locally")
		arcpy.FeatureClassToFeatureClass_conversion("C:/Users/mapmaker/temp/Recreation_Points/" + state + "_Recreation_Points.gdb/RecreationPoints/" + state + "_RecreationPoints", "C:/Users/mapmaker/temp/" + state + "/Recreation_Points/Complete", state + "_RecreationPoints.shp")
		print("		feature class converted to shp file")
NPS_maps = open("G:/Data_National/RecreationPoints/Reference/NPS.txt")
NPS_lines = NPS_maps.read().split("\n")
NPS_MAP = NPS_lines
for NPS_MAP in NPS_lines:
	maps = "G:/Data_National/NPS/NPS_Rec_Data/Complete/" + NPS_MAP + ".gdb"
	print("copying " + maps)
	copy_tree(maps, "C:/Users/mapmaker/temp/" + state + "/Recreation_Points/" + NPS_MAP + ".gdb")
path = "C:/Users/mapmaker/temp/" + state
gdbname = "NPS.gdb"
gdb = path + "/" + gdbname
FD = gdb + "/ToMerge"
print("Making gdb")
arcpy.CreateFileGDB_management(path, gdbname)
print("gdb made")
print("Making feature dataset")
arcpy.CreateFeatureDataset_management(gdb, "ToMerge", sr2)
print("Feature Dataset made")
for path, dirs, files in os.walk("C:/Users/mapmaker/temp/" + state + "/Recreation_Points", topdown=False):
	for d in dirs:
		print(d)
		if d.endswith(".gdb"):
			gdb_path = os.path.join(path, d)
			print("#####################")
			print(gdb_path)
			print("#####################")
			env.workspace = gdb_path
			for fds in arcpy.ListDatasets():
				print(fds)
				all_fcs = arcpy.ListFeatureClasses(gdb_path + "/" + fds)
				for fc in arcpy.ListFeatureClasses('', '', fds):
					print(fc)
					arcpy.FeatureClassToFeatureClass_conversion(fc, FD, fc)
print("Creating another feature dataset")
arcpy.CreateFeatureDataset_management(gdb, "NPS_Merged", sr2)
env.workspace = FD
print("Cleaning up fields for merge")
for fc in arcpy.ListFeatureClasses():
	loop = arcpy.ListFields(fc)
	print("Cleaning up " + fc)
	for field in loop:
		if field.name != "NAME" and field.name != "MP_TYPE" and field.name != "ONxLOCATION" and field.name != "ONxCONDITION" and field.name != "ONxFEATURES" and field.name != "ONxURL" and field.name != "ONxNOTES" and field.name != "TEMPNAME" and field.name != "FID" and field.name != "Object ID" and field.name != "Shape" and field.name != "OBJECTID_1" and field.name != "Name" and field.name != "OBJECTID_12" and field.name != "OBJECTID":
			value = field.name
			arcpy.DeleteField_management(fc, value)
input = arcpy.ListFeatureClasses()
arcpy.Merge_management(input, gdb + "/NPS_Merged/NPS")
print("Merged")
AdminBounds = "G:/Data_National/RecreationPoints/Reference/ClippingAdminBounds/" + dict[state] + ".shp"
print("Clipping by " + state + " Admin Bounds")
arcpy.MakeFeatureLayer_management(gdb + "/NPS_Merged/NPS", "NPS")
arcpy.SelectLayerByLocation_management("NPS", "COMPLETELY_WITHIN", AdminBounds,"#","NEW_SELECTION")
arcpy.CopyFeatures_management("NPS", "C:/Users/mapmaker/temp/" + state + "/Recreation_Points/Complete/" + state + "_NPS_Data.shp")
print("NPS data clipped")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Creates Global Mapper Catalogs
if RunUpdateSectionValue == 6:
	GMscript = temp_folder + "/CatalogCreation.gms"
	catalogcreation = open(GMscript, 'w')
	print("Writing Global Mapper Catalog Creation Script")
	logFile.writelines("Writing Global Mapper Catalog Creation Script" + "\n")
	logFile.flush()
	catalogcreation.writelines('''
	GLOBAL_MAPPER_SCRIPT VERSION=1.00
	DEFINE_PROJ PROJ_NAME="GEO_WGS84"
	Projection     GEOGRAPHIC
	Datum          WGS84
	Zunits         NO
	Units          DD
	Xshift         0.000000
	Yshift         0.000000
	Parameters
	0 0 0.000 /* longitude of center of projection
	END_DEFINE_PROJ
	LOAD_PROJECTION PROJ="GEO_WGS84"
	DEFINE_VAR NAME="state" VALUE="''' + state + '''"
	DEFINE_VAR NAME="year" VALUE="''' + year + '''"
	SET_LOG_FILE FILENAME="G:\Products\Garmin\Premium\%state%\\GarminProductCreationGM.log"
	LOG_MESSAGE <%SCRIPT_FILENAME%> Started at %DATE% %TIME%
	LOG_MESSAGE ----------------------- Preparing to build %state% Admin Bounds Catalog ---------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_Admin_Bounds.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Administrative_Boundaries\\2013_complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_Admin_Bounds.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Administrative_Boundaries\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Admin Bounds Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ----------------------- Preparing to build %state% Bathymetry Catalog ----------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_BATHYMETRY.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Bathymetry\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Bathymetry Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------ Preparing to build %state% GMU Catalog -----------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_GMU.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\GMU\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% GMU Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------ Preparing to build %state% GNIS Catalog -----------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_GNIS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\GNIS\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% GNIS Catalog Created------------------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------ Preparing to build %state% Local Park Point Catalog -------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_Parks.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Parks\Complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ----------------------- %state% Local Park Points added to catalog -----------------------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE -----------------------Preparing to build %state% Parcel Lines Catalog -------------------------------------------
	LOG_MESSAGE ----------------------Adding inside lines to PARCEL_LINES catalog 
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_PARCEL_LINES.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Parcels\%year%_complete\Complete_Inside_Lines\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Inside Parcel lines added to Parcel Lines Catalog ----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------ Adding LINES ---------------------------------------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_PARCEL_LINES.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Parcels\%year%_complete\Complete_Lines\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Parcel Lines added to Parcel Lines Catalog ----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE -----------------------Preparing to build %state% Parcel Points Catalog --------------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_PARCEL_POINTS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Parcels\%year%_complete\Complete_Points\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Parcel Points Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------Preparing to build %state% Parcel Areas Catalog -----------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_PARCEL_AREAS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="C:\Users\mapmaker\\temp\%state%\Complete_Areas\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Parcel Areas Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------ Preparing to build %state% Recreational Points Catalog -----------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_Recreation_Points.GMC" CREATE_IF_EMPTY=YES ADD_FILE="C:\Users\mapmaker\\temp\%state%\Recreation_Points\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Recreational Points Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------Preparing to build %state% Sections Catalog -------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_SECTIONS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Sections\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Sections Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------Preparing to build %state% Transportation Catalog ------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_TRANSPORTATION.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Transportation\complete\Bordering_%state%_Highway_IconShapefile.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_TRANSPORTATION.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Transportation\complete\%state%_Highway_IconShapefile.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_TRANSPORTATION.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Products\Garmin\Premium\%state%\%state%_TRANSPORTATION.MP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ----------------------- Preparing to build %state% state specific catalogs --------------------------------
	LOG_MESSAGE ----------------------- Building ''' + Layer_1 + ''' Catalog ---------------------------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_''' + Layer_1 + '''.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\\''' + Layer_1 + '''\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% ''' + Layer_1 + ''' Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ----------------------- Building ''' + Layer_2 + ''' Catalog ---------------------------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_''' + Layer_2 + '''.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\\''' + Layer_2 + '''\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% ''' + Layer_2 + ''' Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ----------------------- Building %state% ''' + Layer_3 + ''' Catalog --------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_''' + Layer_3 + '''.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\\''' + Layer_3 + '''\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% ''' + Layer_3 + ''' Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ----------------------- Building ''' + Layer_4 + ''' Catalog ---------------------------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_''' + Layer_4 + '''.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\\''' + Layer_4 + '''\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% ''' + Layer_4 + ''' Catalog Created----------------------------------
	LOG_MESSAGE ------------------------ Preparing to build %state% NHD Catalog -------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_NHD.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Water\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% NHD Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------Preparing to build %state% Wilderness Catalog -------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_WILDERNESS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Wilderness\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Wilderness Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ************************************* %state% Catalog Build took %TIME_SINCE_START% ***************************************************
	UNLOAD_ALL
	''' + '\n')
	catalogcreation.flush()     
	catalogcreation.close()
	print("Initiating Global Mapper Catalog Creation Script.")
	logFile.writelines("Initiating Global Mapper Catalog Creation Script." + "\n")
	logFile.flush()
	p = subprocess.Popen(["C:\Program Files\GlobalMapper18_64bit\global_mapper.exe", GMscript])
	p.wait()
	print("Catalogs Created!")
	logFile.writelines("Catalogs Created!" + "\n")
	logFile.flush()    
elif RunUpdateSectionValue == 7:
	GMscript = temp_folder + "/CatalogCreation.gms"
	catalogcreation = open(GMscript, 'w')
	print("Writing Global Mapper Catalog Creation Script")
	logFile.writelines("Writing Global Mapper Catalog Creation Script" + "\n")
	logFile.flush()
	catalogcreation.writelines('''
	GLOBAL_MAPPER_SCRIPT VERSION=1.00
	DEFINE_PROJ PROJ_NAME="GEO_WGS84"
	Projection     GEOGRAPHIC
	Datum          WGS84
	Zunits         NO
	Units          DD
	Xshift         0.000000
	Yshift         0.000000
	Parameters
	0 0 0.000 /* longitude of center of projection
	END_DEFINE_PROJ
	LOAD_PROJECTION PROJ="GEO_WGS84"
	DEFINE_VAR NAME="state" VALUE="''' + state + '''"
	DEFINE_VAR NAME="year" VALUE="''' + year + '''"
	SET_LOG_FILE FILENAME="G:\Products\Garmin\Premium\%state%\\GarminProductCreationGM.log"
	LOG_MESSAGE <%SCRIPT_FILENAME%> Started at %DATE% %TIME%
	LOG_MESSAGE ----------------------- Preparing to build %state% Admin Bounds Catalog ---------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_Admin_Bounds.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Administrative_Boundaries\\2013_complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_Admin_Bounds.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Administrative_Boundaries\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Admin Bounds Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ----------------------- Preparing to build %state% Bathymetry Catalog ----------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_BATHYMETRY.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Bathymetry\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Bathymetry Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------ Preparing to build %state% GMU Catalog -----------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_GMU.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\GMU\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% GMU Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------ Preparing to build %state% GNIS Catalog -----------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_GNIS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\GNIS\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% GNIS Catalog Created------------------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------ Preparing to build %state% Local Park Point Catalog -------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_Parks.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Parks\Complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ----------------------- %state% Local Park Points added to catalog -----------------------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE -----------------------Preparing to build %state% Parcel Lines Catalog -------------------------------------------
	LOG_MESSAGE ----------------------Adding inside lines to PARCEL_LINES catalog 
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_PARCEL_LINES.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Parcels\%year%_complete\Complete_Inside_Lines\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Inside Parcel lines added to Parcel Lines Catalog ----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------ Adding LINES ---------------------------------------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_PARCEL_LINES.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Parcels\%year%_complete\Complete_Lines\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Parcel Lines added to Parcel Lines Catalog ----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE -----------------------Preparing to build %state% Parcel Points Catalog --------------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_PARCEL_POINTS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Parcels\%year%_complete\Complete_Points\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Parcel Points Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------Preparing to build %state% Parcel Areas Catalog -----------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_PARCEL_AREAS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Parcels\%year%_complete\Complete_Areas\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Parcel Areas Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------ Preparing to build %state% Recreational Points Catalog -----------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_REC_PTS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="C:\Users\mapmaker\\temp\%state%\Recreation_Points\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Recreational Points Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------Preparing to build %state% Sections Catalog -------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_SECTIONS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Sections\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Sections Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------Preparing to build %state% Transportation Catalog ------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_TRANSPORTATION.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Transportation\complete\Bordering_%state%_Highway_IconShapefile.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_TRANSPORTATION.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Transportation\complete\%state%_Highway_IconShapefile.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_TRANSPORTATION.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Products\Garmin\Premium\%state%\%state%_TRANSPORTATION.MP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ----------------------- Preparing to build %state% state specific catalogs --------------------------------
	LOG_MESSAGE ----------------------- Building ''' + Layer_1 + ''' Catalog ---------------------------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_''' + Layer_1 + '''.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\\''' + Layer_1 + '''\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% ''' + Layer_1 + ''' Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ----------------------- Building ''' + Layer_2 + ''' Catalog ---------------------------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_''' + Layer_2 + '''.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\\''' + Layer_2 + '''\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% ''' + Layer_2 + ''' Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ----------------------- Building %state% ''' + Layer_3 + ''' Catalog --------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_''' + Layer_3 + '''.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\\''' + Layer_3 + '''\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% ''' + Layer_3 + ''' Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ----------------------- Building ''' + Layer_4 + ''' Catalog ---------------------------------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_''' + Layer_4 + '''.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\\''' + Layer_4 + '''\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% ''' + Layer_4 + ''' Catalog Created----------------------------------
	LOG_MESSAGE ------------------------ Preparing to build %state% NHD Catalog -------------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_NHD.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Water\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% NHD Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ------------------------Preparing to build %state% Wilderness Catalog -------------------------
	EDIT_MAP_CATALOG FILENAME="G:\Products\Garmin\Premium\%state%\%state%_WILDERNESS.GMC" CREATE_IF_EMPTY=YES ADD_FILE="G:\Data_State\%state%\Wilderness\complete\*.SHP" ZOOM_DISPLAY="PERCENT,0.75,0"
	LOG_MESSAGE ------------------------%state% Wilderness Catalog Created----------------------------------
	LOG_MESSAGE ------------------------Import took %TIME_SINCE_LAST_LOG%
	LOG_MESSAGE ************************************* %state% Catalog Build took %TIME_SINCE_START% ***************************************************
	UNLOAD_ALL
	''' + '\n')
	catalogcreation.flush()     
	catalogcreation.close()
	print("Initiating Global Mapper Catalog Creation Script.")
	logFile.writelines("Initiating Global Mapper Catalog Creation Script." + "\n")
	logFile.flush()
	p = subprocess.Popen(["C:\Program Files\GlobalMapper18_64bit\global_mapper.exe", GMscript])
	p.wait()
	print("Catalogs Created!")
	logFile.writelines("Catalogs Created!" + "\n")
	logFile.flush()    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Exports MP files
print("Writing Global Mapper MP Export Script")
logFile.writelines("Writing Global Mapper MP Export Script" + "\n")
logFile.flush()
GMscript = temp_folder + "/MPExport_initial.gms"
mpexport = open(GMscript, 'w')
mpexport.writelines('''
GLOBAL_MAPPER_SCRIPT VERSION=1.00
DEFINE_VAR NAME="state" VALUE="''' + state + '''"
DEFINE_VAR NAME="product" VALUE="''' + product + '''"
SET_LOG_FILE FILENAME="G:\Products\Garmin\%product%\%state%\\GarminProductCreationGM.log"
LOG_MESSAGE %state% variable set
DEFINE_VAR NAME="FID" VALUE="''' + str(FID_dict[state]) + '''"
LOG_MESSAGE %FID% variable set
LOG_MESSAGE %product% variable set
DEFINE_VAR NAME="version" VALUE="''' + version + '''"
LOG_MESSAGE %version% variable set
DEFINE_VAR NAME="template_path" VALUE="G:\Products\Garmin\%product%\%state%\RELEASEv%version%"            
LOG_MESSAGE %template_path% variable set
LOG_MESSAGE <%SCRIPT_FILENAME%> Started at %DATE% %TIME%
LOG_MESSAGE ****************************************************************************Importing Contour gdb***********************************************************************************************************
IMPORT FILENAME="G:\Data_State\%state%\Contours\Complete\%state%_NED_TOPO_Complete.gdb\gdb" 
LOG_MESSAGE ****************************************************************************gdb import finished*************************************************************************************************************
LOG_MESSAGE ****************************************************************************Import took %TIME_SINCE_LAST_LOG%***********************************************************************************************
LOG_MESSAGE ****************************************************************************Importing Global Mapper Catalogs************************************************************************************************
IMPORT_DIR_TREE DIRECTORY="G:\Products\Garmin\%product%\%state%" FILENAME_MASKS="*.GMC"
LOG_MESSAGE ***************************************************************************Global Mapper Catalogs imported**************************************************************************************************
LOG_MESSAGE ****************************************************************************Import took %TIME_SINCE_LAST_LOG%***********************************************************************************************
LOG_MESSAGE ***************************************************************************Saving %state% Workspace*********************************************************************************************************
SAVE_WORKSPACE FILENAME="G:\Products\Garmin\%product%\%state%\\0_HUNT_%state%.gmw"
LOG_MESSAGE ***************************************************************************0_HUNT_%state%.gmw saved*********************************************************************************************************
LOG_MESSAGE ***************************************************************************Initiating MP export*************************************************************************************************************
EXPORT_VECTOR FILENAME="C:\Users\mapmaker\HUNT_%state%\HUNT_%state%_.mp" TYPE=POLISH_MP GRID_TYPE_CELL_SIZE="0.25,0.25" MAP_NAME=%TILE_FNAME_WO_EXT% TEMPLATE_FILENAME="%template_path%\dict-SMAv28_%FID%.mp" MP_EXPORT_TEMPLATE_FILES=NO MP_COPY_ENTIRE_TEMPLATE=NO MP_IMAGE_ID=0 GRID_NAMING=SEPARATE GRID_NAMING_COLS="NUM,1," GRID_NAMING_ROWS="ALPHA,A," GRID_NAMING_SEPARATOR=""
LOG_MESSAGE ****************************************************************************MP export took %TIME_SINCE_LAST_LOG%********************************************************************************************
UNLOAD_ALL
''' + '\n')
mpexport.flush()
mpexport.close()
print("Initiating Global Mapper MP Export Script.")
logFile.writelines("Initiating Global Mapper MP Export Script." + "\n")
logFile.flush()
time.sleep(2)
p = subprocess.Popen(["C:\Program Files\GlobalMapper18_64bit\global_mapper.exe", GMscript])
p.wait()
print( state + " MP tiles exported.")
logFile.writelines( state + " MP tiles exported." + "\n")
logFile.flush()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Clean up temp Recreation Points directories

os.chdir("C:/Users/mapmaker/temp")
if os.path.exists("C:/Users/mapmaker/temp/" + state + "/NPS.gdb"):
	try:
		if os.path.isdir("C:/Users/mapmaker/temp/" + state + "/NPS.gdb"):
			shutil.rmtree("C:/Users/mapmaker/temp/" + state + "/NPS.gdb", ignore_errors=True)
			print(state + " temp folder removed")
		else:
			os.remove("C:/Users/mapmaker/temp/" + state + "/NPS.gdb")
			print(state + " temp folder removed")
	except:
		print "Exception ",str(sys.exc_info())
else:
	print("not found " + "C:/Users/mapmaker/temp/" + state + "/NPS.gdb")
if os.path.exists("C:/Users/mapmaker/temp/" + state + "/Recreation_Points"):
	try:
		if os.path.isdir("C:/Users/mapmaker/temp/" + state + "/Recreation_Points"):
			shutil.rmtree("C:/Users/mapmaker/temp/" + state + "/Recreation_Points", ignore_errors=True)
			print(state + " temp folder removed")
		else:
			os.remove("C:/Users/mapmaker/temp/" + state + "/Recreation_Points")
			print(state + " temp folder removed")
	except:
		print "Exception ",str(sys.exc_info())
else:
	print("not found " + "C:/Users/mapmaker/temp/" + state + "/Recreation_Points")
if os.path.exists("C:/Users/mapmaker/temp/Recreation_Points/" + state + "_Recreation_Points.gdb"):
	try:
		if os.path.isdir("C:/Users/mapmaker/temp/Recreation_Points/" + state + "_Recreation_Points.gdb"):
			shutil.rmtree("C:/Users/mapmaker/temp/Recreation_Points/" + state + "_Recreation_Points.gdb", ignore_errors=True)
		else:
			os.remove("C:/Users/mapmaker/temp/Recreation_Points/" + state + "_Recreation_Points.gdb")
	except:
		print "Exception ",str(sys.exc_info())
else:
	print("not found " + "C:/Users/mapmaker/temp/Recreation_Points/" + state + "_Recreation_Points.gdb")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Deletes empty MP files
print("Writing bat file to delete empty .mp tiles")
logFile.writelines("Removing empty MP tiles" + "\n")
logFile.flush()
batfile = temp_folder + "/deleteemptymptiles.bat"
deleteemptymptiles = open(batfile, 'w')
deleteemptymptiles.writelines('''
@echo off
pushd "C:\Users\mapmaker\HUNT_'''+state+'''
for %%j in (*) do if %%~zj lss 7900 del "%%~j"
popd''' + '\n')
deleteemptymptiles.flush()
deleteemptymptiles.close()
time.sleep(1)
p = Popen(r'start cmd /c ' + batfile, shell=True)
p.wait()
time.sleep(1)
print("All files smaller that 7.90kb have been removed.")
logFile.writelines("All files smaller that 7.90kb have been removed." + "\n")
logFile.flush()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Grab tiles over 120mb and moves them to be split into 4 tiles
os.chdir(to_directory)
for(dirname, dirs, files) in os.walk('.'):
	for filename in files:
		if filename.endswith('.mp'):
			thefile = os.path.join(dirname, filename)
			size = os.path.getsize(thefile)
			if size > 119229440:
				print(filename + " is being moved to " + large_dir)
				logFile.writelines(filename + " is being moved to " + large_dir + "\n")
				logFile.flush()
				try:
					shutil.move(thefile, large_dir + thefile)
				except:
					print("done")
					logFile.writelines("done" + "\n")
					logFile.flush()
# Changes working directory
os.chdir(large_dir)
# Grabs files over 200mb and moves them to be split into 6 tiles
for(dirname, dirs, files) in os.walk('.'):
	for filename in files:
		if filename.endswith('.mp'):
			thefile = os.path.join(dirname, filename)
			size = os.path.getsize(thefile)
			if size > 200358400:
				print(filename + " is being moved to " + huge_dir)
				logFile.writelines(filename + " is being moved to " + huge_dir + "\n")
				logFile.flush()
				try:
					shutil.move(thefile, huge_dir + thefile)
				except:
					print("done")
					logFile.writelines("done" + "\n")
					logFile.flush()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
print("Importing and splitting .mp files in " + large_dir)
logFile.writelines("Importing and splitting .mp files in " + large_dir + "\n")
logFile.flush()

print("Writing Global Mapper MP Export Script")
logFile.writelines("Writing Global Mapper MP Export Script" + "\n")
logFile.flush()
GMscript = temp_folder + "/MPExport_split1.gms"
mpexport = open(GMscript, 'w')
mpexport.writelines('''
GLOBAL_MAPPER_SCRIPT VERSION=1.00
DEFINE_VAR NAME="state" VALUE="''' + state + '''"
DEFINE_VAR NAME="product" VALUE="''' + product + '''"
SET_LOG_FILE FILENAME="G:\Products\Garmin\%product%\%state%\\GarminProductCreationGM.log"
LOAD_STYLE_FILE FILENAME="G:\Products\Garmin\Garmin_Master_Misc\\template\linestyles.gm_style"
LOG_MESSAGE %state% variable set
DEFINE_VAR NAME="FID" VALUE="''' + str(FID_dict[state]) + '''"
LOG_MESSAGE %FID% variable set
LOG_MESSAGE %product% variable set
DEFINE_VAR NAME="version" VALUE="''' + version + '''"
LOG_MESSAGE %version% variable set
DEFINE_VAR NAME="template_path" VALUE="G:\Products\Garmin\%product%\%state%\RELEASEv%version%"            
LOG_MESSAGE %template_path% variable set
LOG_MESSAGE <%SCRIPT_FILENAME%> Started at %DATE% %TIME%
DIR_LOOP_START DIRECTORY="''' + large_dir + '''" FILENAME_MASKS="*.MP" RECURSE_DIR=NO
IMPORT FILENAME="%FNAME_W_DIR%"
EXPORT_VECTOR FILENAME="C:\Users\mapmaker\HUNT_%state%\%FNAME_WO_EXT%_.mp" TYPE=POLISH_MP GRID_TYPE_ROWS_COLS="2,2" MAP_NAME=%TILE_FNAME_WO_EXT% TEMPLATE_FILENAME="%template_path%\dict-SMAv28_%FID%.mp" MP_EXPORT_TEMPLATE_FILES=NO MP_COPY_ENTIRE_TEMPLATE=NO MP_IMAGE_ID=0 GRID_NAMING=SEPARATE GRID_NAMING_COLS="NUM,1," GRID_NAMING_ROWS="ALPHA,A," GRID_NAMING_SEPARATOR=""
UNLOAD_ALL
DIR_LOOP_END
''' + '\n')
mpexport.flush()
mpexport.close()
print("Initiating Global Mapper MP Export Script.")
logFile.writelines("Initiating Global Mapper MP Export Script." + "\n")
logFile.flush()
time.sleep(2)
p = subprocess.Popen(["C:\Program Files\GlobalMapper18_64bit\global_mapper.exe", GMscript])
p.wait()
print( state + " MP tiles exported.")
logFile.writelines( state + " MP tiles exported." + "\n")
logFile.flush()

print("Done with files in " + large_dir)
logFile.writelines("Done with files in " + large_dir + "\n")
logFile.flush()
print("Importing and splitting .mp files in " + huge_dir)
logFile.writelines("Importing and splitting .mp files in " + huge_dir + "\n")
logFile.flush()

print("Writing Global Mapper MP Export Script")
logFile.writelines("Writing Global Mapper MP Export Script" + "\n")
logFile.flush()
GMscript = temp_folder + "/MPExport_split2.gms"
mpexport = open(GMscript, 'w')
mpexport.writelines('''
GLOBAL_MAPPER_SCRIPT VERSION=1.00
DEFINE_VAR NAME="state" VALUE="''' + state + '''"
DEFINE_VAR NAME="product" VALUE="''' + product + '''"
SET_LOG_FILE FILENAME="G:\Products\Garmin\%product%\%state%\\GarminProductCreationGM.log"
LOAD_STYLE_FILE FILENAME="G:\Products\Garmin\Garmin_Master_Misc\\template\linestyles.gm_style"
LOG_MESSAGE %state% variable set
DEFINE_VAR NAME="FID" VALUE="''' + str(FID_dict[state]) + '''"
LOG_MESSAGE %FID% variable set
LOG_MESSAGE %product% variable set
DEFINE_VAR NAME="version" VALUE="''' + version + '''"
LOG_MESSAGE %version% variable set
DEFINE_VAR NAME="template_path" VALUE="G:\Products\Garmin\%product%\%state%\RELEASEv%version%"            
LOG_MESSAGE %template_path% variable set
LOG_MESSAGE <%SCRIPT_FILENAME%> Started at %DATE% %TIME%
DIR_LOOP_START DIRECTORY="''' + huge_dir + '''" FILENAME_MASKS="*.MP" RECURSE_DIR=NO
IMPORT FILENAME="%FNAME_W_DIR%"
EXPORT_VECTOR FILENAME="C:\Users\mapmaker\HUNT_%state%\%FNAME_WO_EXT%_.mp" TYPE=POLISH_MP GRID_TYPE_ROWS_COLS="3,3" MAP_NAME=%TILE_FNAME_WO_EXT% TEMPLATE_FILENAME="%template_path%\dict-SMAv28_%FID%.mp" MP_EXPORT_TEMPLATE_FILES=NO MP_COPY_ENTIRE_TEMPLATE=NO MP_IMAGE_ID=0 GRID_NAMING=SEPARATE GRID_NAMING_COLS="NUM,1," GRID_NAMING_ROWS="ALPHA,A," GRID_NAMING_SEPARATOR=""
UNLOAD_ALL
DIR_LOOP_END
''' + '\n')
mpexport.flush()
mpexport.close()
print("Initiating Global Mapper MP Export Script.")
logFile.writelines("Initiating Global Mapper MP Export Script." + "\n")
logFile.flush()
time.sleep(2)
p = subprocess.Popen(["C:\Program Files\GlobalMapper18_64bit\global_mapper.exe", GMscript])
p.wait()
print( state + " MP tiles exported.")
logFile.writelines( state + " MP tiles exported." + "\n")
logFile.flush()
print("Done with files in " + huge_dir)
logFile.writelines("Done with files in " + huge_dir + "\n")
logFile.flush()
# Changes working directory back to main export folder to check for large tiles again
os.chdir(to_directory)
for(dirname, dirs, files) in os.walk('.'):
	for filename in files:
		if filename.endswith('.mp'):
			thefile = os.path.join(dirname, filename)
			size = os.path.getsize(thefile)
			if size > 119229440:
				print(filename + " is being moved to " + large_dir2)
				logFile.writelines(filename + " is being moved to " + large_dir2 + "\n")
				logFile.flush()
				try:
					shutil.move(thefile, large_dir2 + thefile)
				except:
					print("done")
					logFile.writelines("done" + "\n")
					logFile.flush()
# Changes working directory 
os.chdir(large_dir2)
# Grabs files over 285mb and moves them to be split into 6 tiles
for(dirname, dirs, files) in os.walk('.'):
	for filename in files:
		if filename.endswith('.mp'):
			thefile = os.path.join(dirname, filename)
			size = os.path.getsize(thefile)
			if size > 200358400:
				print(filename + " is being moved to " + huge_dir2)
				logFile.writelines(filename + " is being moved to " + huge_dir2 + "\n")
				logFile.flush()
				try:
					shutil.move(thefile, huge_dir2 + thefile)
				except:
					print("done")
					logFile.writelines("done" + "\n")
					logFile.flush()
time.sleep(.5)
print("Importing and splitting .mp files in " + large_dir2)
logFile.writelines("Importing and splitting .mp files in " + large_dir2 + "\n")
logFile.flush()

print("Writing Global Mapper MP Export Script")
logFile.writelines("Writing Global Mapper MP Export Script" + "\n")
logFile.flush()
GMscript = temp_folder + "/MPExport_split3.gms"
mpexport = open(GMscript, 'w')
mpexport.writelines('''
GLOBAL_MAPPER_SCRIPT VERSION=1.00
DEFINE_VAR NAME="state" VALUE="''' + state + '''"
DEFINE_VAR NAME="product" VALUE="''' + product + '''"
SET_LOG_FILE FILENAME="G:\Products\Garmin\%product%\%state%\\GarminProductCreationGM.log"
LOAD_STYLE_FILE FILENAME="G:\Products\Garmin\Garmin_Master_Misc\\template\linestyles.gm_style"
LOG_MESSAGE %state% variable set
DEFINE_VAR NAME="FID" VALUE="''' + str(FID_dict[state]) + '''"
LOG_MESSAGE %FID% variable set
LOG_MESSAGE %product% variable set
DEFINE_VAR NAME="version" VALUE="''' + version + '''"
LOG_MESSAGE %version% variable set
DEFINE_VAR NAME="template_path" VALUE="G:\Products\Garmin\%product%\%state%\RELEASEv%version%"            
LOG_MESSAGE %template_path% variable set
LOG_MESSAGE <%SCRIPT_FILENAME%> Started at %DATE% %TIME%
DIR_LOOP_START DIRECTORY="''' + large_dir2 + '''" FILENAME_MASKS="*.MP" RECURSE_DIR=NO
IMPORT FILENAME="%FNAME_W_DIR%"
EXPORT_VECTOR FILENAME="C:\Users\mapmaker\HUNT_%state%\%FNAME_WO_EXT%_.mp" TYPE=POLISH_MP GRID_TYPE_ROWS_COLS="2,2" MAP_NAME=%TILE_FNAME_WO_EXT% TEMPLATE_FILENAME="%template_path%\dict-SMAv28_%FID%.mp" MP_EXPORT_TEMPLATE_FILES=NO MP_COPY_ENTIRE_TEMPLATE=NO MP_IMAGE_ID=0 GRID_NAMING=SEPARATE GRID_NAMING_COLS="NUM,1," GRID_NAMING_ROWS="ALPHA,A," GRID_NAMING_SEPARATOR=""
UNLOAD_ALL
DIR_LOOP_END
''' + '\n')
mpexport.flush()
mpexport.close()
print("Initiating Global Mapper MP Export Script.")
logFile.writelines("Initiating Global Mapper MP Export Script." + "\n")
logFile.flush()
time.sleep(2)
p = subprocess.Popen(["C:\Program Files\GlobalMapper18_64bit\global_mapper.exe", GMscript])
p.wait()
print( state + " MP tiles exported.")
logFile.writelines( state + " MP tiles exported." + "\n")
logFile.flush()


print("Done with files in " + large_dir2)
logFile.writelines("Done with files in " + large_dir2 + "\n")
logFile.flush()
print("Importing and splitting .mp files in " + huge_dir2)
logFile.writelines("Importing and splitting .mp files in " + huge_dir2 + "\n")
logFile.flush()

print("Writing Global Mapper MP Export Script")
logFile.writelines("Writing Global Mapper MP Export Script" + "\n")
logFile.flush()
GMscript = temp_folder + "/MPExport_split4.gms"
mpexport = open(GMscript, 'w')
mpexport.writelines('''
GLOBAL_MAPPER_SCRIPT VERSION=1.00
DEFINE_VAR NAME="state" VALUE="''' + state + '''"
DEFINE_VAR NAME="product" VALUE="''' + product + '''"
SET_LOG_FILE FILENAME="G:\Products\Garmin\%product%\%state%\\GarminProductCreationGM.log"
LOAD_STYLE_FILE FILENAME="G:\Products\Garmin\Garmin_Master_Misc\\template\linestyles.gm_style"
LOG_MESSAGE %state% variable set
DEFINE_VAR NAME="FID" VALUE="''' + str(FID_dict[state]) + '''"
LOG_MESSAGE %FID% variable set
LOG_MESSAGE %product% variable set
DEFINE_VAR NAME="version" VALUE="''' + version + '''"
LOG_MESSAGE %version% variable set
DEFINE_VAR NAME="template_path" VALUE="G:\Products\Garmin\%product%\%state%\RELEASEv%version%"            
LOG_MESSAGE %template_path% variable set
LOG_MESSAGE <%SCRIPT_FILENAME%> Started at %DATE% %TIME%
DIR_LOOP_START DIRECTORY="''' + huge_dir2 + '''" FILENAME_MASKS="*.MP" RECURSE_DIR=NO
IMPORT FILENAME="%FNAME_W_DIR%"
EXPORT_VECTOR FILENAME="C:\Users\mapmaker\HUNT_%state%\%FNAME_WO_EXT%_.mp" TYPE=POLISH_MP GRID_TYPE_ROWS_COLS="2,2" MAP_NAME=%TILE_FNAME_WO_EXT% TEMPLATE_FILENAME="%template_path%\dict-SMAv28_%FID%.mp" MP_EXPORT_TEMPLATE_FILES=NO MP_COPY_ENTIRE_TEMPLATE=NO MP_IMAGE_ID=0 GRID_NAMING=SEPARATE GRID_NAMING_COLS="NUM,1," GRID_NAMING_ROWS="ALPHA,A," GRID_NAMING_SEPARATOR=""
UNLOAD_ALL
DIR_LOOP_END
''' + '\n')
mpexport.flush()
mpexport.close()
print("Initiating Global Mapper MP Export Script.")
logFile.writelines("Initiating Global Mapper MP Export Script." + "\n")
logFile.flush()
time.sleep(2)
p = subprocess.Popen(["C:\Program Files\GlobalMapper18_64bit\global_mapper.exe", GMscript])
p.wait()
print( state + " MP tiles exported.")
logFile.writelines( state + " MP tiles exported." + "\n")
logFile.flush()


print("Done with files in " + huge_dir2)
logFile.writelines("Done with files in " + huge_dir2 + "\n")
logFile.flush()
# Writes list of remaining MP files
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Splits MP file list by number specified in Global Variables
print("Writing transcodeq.txt file")
logFile.writelines("Writing transcodeq.txt file" + "\n")
logFile.flush()
mpFile = open("C:/Users/mapmaker/HUNT_" + state + "/" + state + "mpfiles.txt", 'w')
mydir = "C:/Users/mapmaker/HUNT_" + state 
os.chdir(mydir)
for file in glob.glob("*.mp"):
	mpFile.writelines(str(mydir + "/" + file) + '\n')
	mpFile.flush()
print("List of .mp files written. Script complete.")
logFile.writelines("List of .mp files written. Script complete." + "\n")
logFile.flush()

my_file = "C:/Users/mapmaker/HUNT_" + state + "/" + state + "mpfiles.txt"
sorting = True
hold_lines = []
with open(my_file,'r') as text_file:
	for row in text_file:
		hold_lines.append(row)
outer_count = 1
line_count = 0
while sorting:
	count = 0
	increment = (outer_count-1) * int(map_tiles)
	left = len(hold_lines) - increment
	file_name = "G:/Products/Garmin/" + product + "/" + state + "/temp/small_file_" + str(outer_count * int(map_tiles)) + ".txt"
	hold_new_lines = []
	if left < int(map_tiles):
		while count < left:
			hold_new_lines.append(hold_lines[line_count])
			count += 1
			line_count += 1
		sorting = False
	else:
		while count < int(map_tiles):
			hold_new_lines.append(hold_lines[line_count])
			count += 1
			line_count += 1
	outer_count += 1
	with open(file_name,'w') as next_file:
		for row in hold_new_lines:
			next_file.write(row)
try:
	tiles1 = (int(map_tiles) * 1)
	os.rename("G:/Products/Garmin/" + product + "/" + state + "/temp/small_file_" + str(tiles1) + ".txt", "C:/Users/mapmaker/HUNT_" + state + "/cgpsrun1/transcodeq.txt")
	print("transcodeq.txt file created")
except:
	print("file doesn't exsist")
try:
	tiles2 = (int(map_tiles) * 2)
	os.rename("G:/Products/Garmin/" + product + "/" + state + "/temp/small_file_" + str(tiles2) + ".txt", "C:/Users/mapmaker/HUNT_" + state + "/cgpsrun2/transcodeq.txt")
	print("transcodeq.txt file created")
except:
	print("file doesn't exsist")
try:
	tiles3 = (int(map_tiles) * 3)
	os.rename("G:/Products/Garmin/" + product + "/" + state + "/temp/small_file_" + str(tiles3) + ".txt", "C:/Users/mapmaker/HUNT_" + state + "/cgpsrun3/transcodeq.txt")
	print("transcodeq.txt file created")
except:
	print("file doesn't exsist")
try:
	tiles4 = (int(map_tiles) * 4)
	os.rename("G:/Products/Garmin/" + product + "/" + state + "/temp/small_file_" + str(tiles4) + ".txt", "C:/Users/mapmaker/HUNT_" + state + "/cgpsrun4/transcodeq.txt")
	print("transcodeq.txt file created")
except:
	print("file doesn't exsist")
try:
	tiles5 = (int(map_tiles) * 5)
	os.rename("G:/Products/Garmin/" + product + "/" + state + "/temp/small_file_" + str(tiles5) + ".txt", "C:/Users/mapmaker/HUNT_" + state + "/cgpsrun5/transcodeq.txt")
	print("transcodeq.txt file created")
except:
	print("file doesn't exsist")
# Deletes temp folder where Global Mapper Scripts were written
'''
deleteTempFolder(temp_folder)
# Deletes temp folder where large .mp files were moved
deleteTempFolder(large_dir)
'''
# Sends notification email
logFile.writelines("Kicking off cgpsruns." + "\n")
logFile.flush()
# Starts cgps runs
run = "1"
compile_img(run)
time.sleep(1)
run = "2"
compile_img(run)
time.sleep(1.5)
run = "3"
compile_img(run)
time.sleep(1.5)
run = "4"
compile_img(run)
time.sleep(1.5)
run = "5"
compile_img(run)

if RunUpdateSectionValue == 6:
	print("Copying Complete_Areas back to the G:")
	logFile.writelines("Copying Complete_Areas back to the G:" + "\n")
	logFile.flush()
	copy_tree(CompleteAreas_Local, CompleteAreas_G)
	print("Complete_Areas successfully copied back to the G:")
	logFile.writelines("Complete_Areas successfully copied back to the G:" + "\n")
	logFile.flush()
	print("Removing local copy of Complete_Areas")
	logFile.writelines("Removing local copy of Complete_Areas" + "\n")
	logFile.flush()
	temp_folder = CompleteAreas_Local
	#deleteTempFolder(temp_folder)
	#print(temp_folder + " Deleted")
	#logFile.writelines(temp_folder + " Deleted" + "\n")
	#logFile.flush()
	logFile.writelines("Complete_Areas folder copied to the G:" + "\n")
	logFile.flush()

# Sends notification email
usr = '***'
psw = '***'
fromaddr = 'script.notification.email@gmail.com'
print("Sending notification email.")
logFile.writelines("Sending notification email." + "\n")
logFile.flush()
runtime = datetime.now() - script_starttime
server=smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(usr,psw)
senddate=datetime.strftime(datetime.now(), '%Y-%m-%d')
subject= state + " Garmin Product Creator Script is Finished!"
m="Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (senddate, fromaddr, toaddr, subject)
msg='''
  
Garmin Product Creator Script runtime: '''+str(runtime)

server.sendmail(fromaddr, toaddr, m+msg)
server.quit()
logFile.close()
print("End")
