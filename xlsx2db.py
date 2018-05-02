#------------------------------------------------------------------------------#
#                   Copyright 2018 complianceSHORTCUTS.com                     #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file creates document from a sqlite database by searching and replacing #
# the table field names as @@name@@ data placeholders within the document.     #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Rev By               Date        CC        Note                              #
# 1.0 David Paspa      13-Apr-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
import argparse
from enum import Enum
import os.path
from shutil import copyfile
import sys
import traceback
import sqlite3
from xls2db import xls2db

import logging
logging.basicConfig(level=logging.DEBUG)

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
appTitle = 'XLSX 2 SQL Lite DB Converter'
appVersion = '1'
parser = argparse.ArgumentParser(description='Converts an XLSX spreadsheet to SQL Lite database format')
parser.add_argument('-i','--input', help='Input spreadsheet file', required=True)
parser.add_argument('-o','--output', help='Output for the generated database file', required=True)
args = vars(parser.parse_args())

#------------------------------------------------------------------------------#
# Declare the error handling global variables and procedure:                   #
#------------------------------------------------------------------------------#
def errorHandler(errProc, eCode, *args):
    #--------------------------------------------------------------------------#
    # Get the application specific error message and output the error:         #
    #--------------------------------------------------------------------------#
    sMsg = errorMessage[eCode]

    #--------------------------------------------------------------------------#
    # Replace any error parameters:                                            #
    #--------------------------------------------------------------------------#
    i = 1
    for arg in args:
        sMsg = sMsg.replace('@' + str(i), str(arg))
        i = i + 1

    #--------------------------------------------------------------------------#
    # Output the error message and end:                                        #
    #--------------------------------------------------------------------------#
    print('\r\n')
    print(appTitle + ' Version ' + appVersion + '\r\n' + 'ERROR ' +
          str(eCode) + ' in Procedure ' + "'" + errProc + "'" + '\r\n' + '\r\n' + sMsg)
    print('\r\n')
    print(traceback.format_exception(*sys.exc_info()))
    sys.exit()

#------------------------------------------------------------------------------#
# Enumerate the error numbers and map the error messages:                      #
#------------------------------------------------------------------------------#
class errorCode(Enum):
    cannotConvertWorkbook              = -2
    filenotExist                       = -7

errorMessage = {
    errorCode.cannotConvertWorkbook    : 'Cannot convert workbook @1 from xlsx to sqlite db @2',
    errorCode.filenotExist             : 'File @1 does not exist.',
}

#------------------------------------------------------------------------------#
# Function main                                                                #
#                                                                              #
# Description:                                                                 #
# The main entry point for the program.                                        #
#------------------------------------------------------------------------------#
def main():
    #--------------------------------------------------------------------------#
    # Define the procedure name:                                               #
    #--------------------------------------------------------------------------#
    errProc = main.__name__

    #--------------------------------------------------------------------------#
    # Get the code configuration workbook name and check it exists:            #
    #--------------------------------------------------------------------------#
    wbName = args['input']
    if not os.path.exists(wbName):
        errorHandler(errProc, errorCode.filenotExist, wbName)

    #--------------------------------------------------------------------------#
    # Copy it to a new file so the base spreadsheet cannot be affected:        #
    #--------------------------------------------------------------------------#
    wbNameDB = os.path.dirname(wbName) + '/configdb.xlsx'
    copyfile(wbName, wbNameDB)

    #--------------------------------------------------------------------------#
    # Delete the sqlite database file if it already exists so it can be        #
    # created anew with refreshed data:                                        #
    #--------------------------------------------------------------------------#
    dbName = os.path.dirname(wbName) + '/configdb.db'
    try:
        os.remove(dbName)
    except OSError:
        pass

    #--------------------------------------------------------------------------#
    # Convert the configuration workbook from xlsx to sqlite database format:  #
    #--------------------------------------------------------------------------#
    try:
        xls2db(wbNameDB, dbName)
    except:
        errorHandler(errProc, errorCode.cannotConvertWorkbook, wbNameDB, dbName)

    #--------------------------------------------------------------------------#
    # Output a success message:                                                #
    #--------------------------------------------------------------------------#
    print('Congratulations! XLSX to DB successful.')

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
main()
