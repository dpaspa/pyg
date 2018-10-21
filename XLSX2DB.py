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
appTitle = 'XLSX SQLite DB Converter'
appVersion = '1'
parser = argparse.ArgumentParser(description='Generates a SQLite database from an XLSX workbook')
parser.add_argument('-c','--config', help='Configuration spreadsheet', required=True)
parser.add_argument('-o','--output', help='Output for the generated document file', required=False)
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
    sys.exit()

#------------------------------------------------------------------------------#
# Enumerate the error numbers and map the error messages:                      #
#------------------------------------------------------------------------------#
class errorCode(Enum):
    cannotConvertWorkbook              = -1
    cannotConnectDB                    = -2
    fileNotExist                       = -3
    pathNotExist                       = -4

errorMessage = {
    errorCode.cannotConvertWorkbook    : 'Cannot convert workbook @1 from xlsx to sqlite db @2',
    errorCode.cannotConnectDB          : 'Cannot connect to sqlite database @1',
    errorCode.fileNotExist             : 'Parent file @1 does not exist.',
    errorCode.pathNotExist             : 'Path @1 does not exist.'
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
    wbName = args['config']
    if not os.path.exists(wbName):
        errorHandler(errProc, errorCode.fileNotExist, wbName)

    #--------------------------------------------------------------------------#
    # Get the base file name and path of the input workbook:                   #
    #--------------------------------------------------------------------------#
    wbFileName = os.path.basename(wbName)
    wbBaseName = os.path.splitext(wbFileName)[0]
    wbDir = os.path.dirname(wbName)

    #--------------------------------------------------------------------------#
    # Get the output path if specified. If not specified then use same path:   #
    #--------------------------------------------------------------------------#
    if (args['output'] is None):
        wbDirDB = wbDir
    else:
        wbDirDB = args['output']
        if not os.path.exists(wbDirDB):
            errorHandler(errProc, errorCode.pathNotExist, wbDirDB)

    #--------------------------------------------------------------------------#
    # Copy the configuration workbook to a new file so the base spreadsheet    #
    # cannot be affected:                                                      #
    #--------------------------------------------------------------------------#
    wbNameWorking = wbDirDB + '/' + wbBaseName + 'db.xlsx'
    copyfile(wbName, wbNameWorking)

    #--------------------------------------------------------------------------#
    # Delete the sqlite database file if it already exists so it can be        #
    # created anew with refreshed data:                                        #
    #--------------------------------------------------------------------------#
    dbName = wbDirDB + '/' + wbBaseName + '.db'
    try:
        os.remove(dbName)
    except OSError:
        pass

    #--------------------------------------------------------------------------#
    # Convert the configuration workbook from xlsx to sqlite database format:  #
    #--------------------------------------------------------------------------#
    try:
        xls2db(wbNameWorking, dbName)
    except:
        errorHandler(errProc, errorCode.cannotConvertWorkbook, wbNameWorking, dbName)

    #--------------------------------------------------------------------------#
    # Connect to the new persistent sqlite database file to confirm it was     #
    # successfully created:                                                    #
    #--------------------------------------------------------------------------#
    conn = ''
    try:
        conn = sqlite3.connect(dbName)
        conn.row_factory = sqlite3.Row
    except:
        errorHandler(errProc, errorCode.cannotConnectDB, dbName)

    #--------------------------------------------------------------------------#
    # Delete the working workbook file:                                        #
    #--------------------------------------------------------------------------#
    os.remove(wbNameWorking)

    #--------------------------------------------------------------------------#
    # Close the connection and output a success message:                       #
    #--------------------------------------------------------------------------#
    conn.close()
    print('Congratulations! Database ' + dbName + ' generated successfully.')

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
main()
