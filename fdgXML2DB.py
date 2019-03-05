#------------------------------------------------------------------------------#
#                   Copyright 2018 complianceSHORTCUTS.com                     #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file convert XML to sqlite DB.                                          #
# https://stackoverflow.com/questions/38187781/parsing-hierarchical-information-from-xml-to-sqlite
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      22-Dec-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
import lxml.etree as ET
import sqlite3

def getBatchElementData(element):
    serial = element.find("serial").text
    valDate = element.find("valDate").text
    valTime = element.find("valTime").text
    recipeNumber = element.find("recipeNumber").text
    recipeDescription = element.find("recipeDescription").text
    mx = element.find("mx").text
    smflx = element.find("smflx").text
    svty = element.find("svty").text
    sy = element.find("sy").text
    fz = element.find("fz").text

    return serial, valDate, valTime, recipeNumber, recipeDescription, mx, smflx, svty, sy, fz

#------------------------------------------------------------------------------#
# Function xml2db                                                              #
#                                                                              #
# Description:                                                                 #
# The XML to DB conversion program.                                            #
#------------------------------------------------------------------------------#
# Calling Parameters:                                                          #
# conn                  The sqlite DB connection object.                       #
#------------------------------------------------------------------------------#
def xml2db(conn):
    #--------------------------------------------------------------------------#
    # Create the batch table:                                                  #
    #--------------------------------------------------------------------------#
    curs = conn.cursor()
    curs.execute('CREATE TABLE IF NOT EXISTS batch ('
                        'serial int NOT NULL, '
                        'valDate text NOT NULL, '
                        'valTime text NOT NULL, '
                        'recipeNumber int NOT NULL, '
                        'recipeDescription text NOT NULL, '
                        'mx int NOT NULL, '
                        'smflx int NOT NULL, '
                        'svty int NOT NULL, '
                        'sy int NOT NULL, '
                        'fz int NOT NULL)'
    )
    conn.commit()

    #--------------------------------------------------------------------------#
    # Parse the XMl data:                                                      #
    #--------------------------------------------------------------------------#
    xml = ET.parse("/home/dpaspa/MEGA/Business/Synertec/MPI.SMS/automation/code/hmi/html/serial/serialMaster.xml")
    xslt = ET.parse("fdgXML2DB.xsl")
    transform = ET.XSLT(xslt)
    newdom = transform(xml)
    batch = newdom.xpath("//batch")

    #--------------------------------------------------------------------------#
    # Add the batch elements:                                                  #
    #--------------------------------------------------------------------------#
    curs = conn.cursor()

    for index, element in enumerate(batch):
        serial, valDate, valTime, recipeNumber, recipeDescription, mx, smflx, svty, sy, fz = getBatchElementData(element)
        curs.execute("insert into batch values (?,?,?,?,?,?,?,?,?,?)", (serial, valDate, valTime, recipeNumber, recipeDescription, mx, smflx, svty, sy, fz))

    conn.commit()
