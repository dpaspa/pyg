#------------------------------------------------------------------------------#
#                   Copyright 2018 complianceSHORTCUTS.com                     #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file converts an Excel XLSX workbook to sqlite database.                #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      13-Apr-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
from enum import Enum
import os.path
from shutil import copyfile
import sys
import traceback
import sqlite3
from xls2db import xls2db

import logging
logging.basicConfig(filename='fdg.log',level=logging.DEBUG)

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
    print('ERROR ' + str(eCode) + ' in Procedure ' + "'" + errProc + "'" + '\r\n' + '\r\n' + sMsg)
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
# Function xlsx2db                                                             #
#                                                                              #
# Description:                                                                 #
# The XLSX to DB conversion program.                                           #
#------------------------------------------------------------------------------#
# Calling Parameters:                                                          #
# fileXLSX              The xlsx spreadsheet file.                             #
# pathOut               The output path. If blank then use the same path.      #
#------------------------------------------------------------------------------#
def xlsx2db(fileXLSX, pathOut):
    #--------------------------------------------------------------------------#
    # Define the procedure name:                                               #
    #--------------------------------------------------------------------------#
    errProc = xlsx2db.__name__

    #--------------------------------------------------------------------------#
    # Get the code configuration workbook name and check it exists:            #
    #--------------------------------------------------------------------------#
    if not os.path.exists(fileXLSX):
        errorHandler(errProc, errorCode.fileNotExist, fileXLSX)

    #--------------------------------------------------------------------------#
    # Get the base file name and path of the input workbook:                   #
    #--------------------------------------------------------------------------#
    wbFileName = os.path.basename(fileXLSX)
    wbBaseName = os.path.splitext(wbFileName)[0]
    wbDir = os.path.dirname(fileXLSX)

    #--------------------------------------------------------------------------#
    # Get the output path if specified. If not specified then use same path:   #
    #--------------------------------------------------------------------------#
    if (pathOut == ''):
        wbDirDB = wbDir
    else:
        wbDirDB = pathOut
        if not os.path.exists(wbDirDB):
            errorHandler(errProc, errorCode.pathNotExist, wbDirDB)

    #--------------------------------------------------------------------------#
    # Copy the configuration workbook to a new file so the base spreadsheet    #
    # cannot be affected:                                                      #
    #--------------------------------------------------------------------------#
    wbNameWorking = wbDirDB + '/' + wbBaseName + 'db.xlsx'
    copyfile(fileXLSX, wbNameWorking)

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
    # Delete the working workbook file and return the connection:              #
    #--------------------------------------------------------------------------#
    os.remove(wbNameWorking)
    dbFileName = os.path.basename(dbName)
    dbBaseFileName = os.path.splitext(dbFileName)[0]
    logging.info('Database ' + dbBaseFileName + '.db created.')
    return conn
