#------------------------------------------------------------------------------#
#                   Copyright 2018 complianceSHORTCUTS.com                     #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file generates S88 PLC code from a configuration spreadsheet and set of #
# code templates.                                                              #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 2   David Paspa      07-Apr-2018 NA        Ported from MS Access.            #
# 1   David Paspa      09-Jan-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
import argparse
from enum import Enum
import openpyxl
import os.path
import sys
from shutil import copyfile
import traceback
from tqdm import trange
from time import sleep
import sqlite3
from xls2db import xls2db
import cgSQL

import logging
logging.basicConfig(level=logging.DEBUG)

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
appTitle = 'Code Generator'
appVersion = '1'
parser = argparse.ArgumentParser(description='Generates PLC code from a configuration spreadsheet and set of code templates')
parser.add_argument('-c','--config', help='Configuration spreadsheet', required=True)
parser.add_argument('-i','--input', help='Input path of code template files', required=True)
parser.add_argument('-o','--output', help='Output path for the generated code files', required=True)
parser.add_argument('-p','--parent', help='Parent object to generate code files for', required=True)
args = vars(parser.parse_args())

#------------------------------------------------------------------------------#
# Declare global variables:                                                    #
#------------------------------------------------------------------------------#
c = 1
iAdd = 0
iAddMax = 0
iCountAttr = 0
iCountAttrMax = 0
iCountFile = 0
iCountFileMax = 0
iCountTemplate = 0
iCountTemplateMax = 0
iEventConfirmNo = 1
iEventConfirmYes = 1
iEventPrompt = 1
iEventLogMsg = 1
iEventLogReal = 1
iEventLogTime = 1
iEventDataReal = 1
iEventDataTime = 1
iSync = 1
gAlias = ''
gChildClass = ''
gClass = ''
gClassDescription = ''
gCommand = ''
gFile = ''
gInstance = ''
#gILTable = ''
gLevel = ''
gParent = ''
gChildParameter = ''
gRecipeClass = ''
gSelectParameter = ''
gSelectSelection = ''
gSFC = ''
gState = ''
pathOutput = ''
pathTemplates = ''

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
    # Close the progress bar:                                                  #
    #--------------------------------------------------------------------------#
    p.close()

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
    cannotCommit                       = -1
    cannotConvertWorkbook              = -2
    cannotConnectDB                    = -3
    cannotCreateTable                  = -4
    cannotInsertTable                  = -5
    cannotUpdateTable                  = -6
    cannotGetSQL                       = -7
    cannotQuery                        = -8
    filenotExist                       = -9
    invalidAdder                       = -10
    invalidChildData                   = -14
    invalidChildField                  = -15
    invalidChildTag                    = -16
    invalidClassData                   = -17
    invalidCounter                     = -18
    invalidDefaultData                 = -19
    invalidFileData                    = -20
    invalidLevelData                   = -21
    invalidPCellData                   = -22
    invalidPCellRecords                = -23
    noClassDBSheet                     = -24
    noBeginPlaceholder                 = -35
    noEndPlaceholder                   = -36
    noCodeTemplateFile                 = -37
    nonASCIICharacter                  = -38
    nonASCIITemplate                   = -39
    unknownAttribute                   = -40

errorMessage = {
    errorCode.cannotCommit             : 'Cannot commit changes to sqlite database',
    errorCode.cannotConvertWorkbook    : 'Cannot convert workbook @1 from xlsx to sqlite db @2',
    errorCode.cannotConnectDB          : 'Cannot connect to sqlite database @1',
    errorCode.cannotCreateTable        : 'Cannot create table @1 in sqlite database',
    errorCode.cannotInsertTable        : 'Cannot insert data into table @1',
    errorCode.cannotUpdateTable        : 'Cannot update data in table @1',
    errorCode.cannotGetSQL             : 'Cannot retrieve SQL query expression for attribute @1',
    errorCode.cannotQuery              : 'Query element @1 cannot execute using SQL expression @2 using parameters @3',
    errorCode.invalidAdder             : 'Adder template @1 is not numeric!',
    errorCode.filenotExist             : 'File @1 does not exist.',
    errorCode.invalidChildData         : 'Class @1 has no children defined!',
    errorCode.invalidChildField        : 'Class @1 child field @2 is null!',
    errorCode.invalidChildTag          : 'Class @1 has no child tag for alias @2.',
    errorCode.invalidClassData         : 'Class @1 has no records for @2!',
    errorCode.invalidCounter           : 'Counter template @1 is not numeric!',
    errorCode.invalidDefaultData       : 'Default parameter data for Process Cell @1 invalid.',
    errorCode.invalidFileData          : 'Output file list data invalid.',
    errorCode.invalidLevelData         : 'Class level @1 has no records!',
    errorCode.invalidPCellData         : 'PCell @1 has no initial code data!',
    errorCode.invalidPCellRecords      : 'PCell @1 initial code data does not have one record!',
    errorCode.noBeginPlaceholder       : 'No valid BEGIN placholder in @1.',
    errorCode.noEndPlaceholder         : 'No valid END placholder for attribute @1 in @2.',
    errorCode.noClassDBSheet           : 'idb Template Worksheet does not include a template called @1.',
    errorCode.noCodeTemplateFile       : 'Code template file @1 does not exist!',
    errorCode.nonASCIICharacter        : 'Query element @1 using SQL expression @2 and parameters @3 returned a non ascii-encoded unicode string',
    errorCode.nonASCIITemplate         : 'Template @1 contains a non ascii-encoded unicode string: @2',
    errorCode.unknownAttribute         : 'Attribute @1 is unknown.',
}

#------------------------------------------------------------------------------#
# Create a progress bar:                                                       #
#------------------------------------------------------------------------------#
p = trange(100, desc='Starting...', leave=False)

#------------------------------------------------------------------------------#
# Function to determine if a value is numeric:                                 #
#------------------------------------------------------------------------------#
def isnumeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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
    # Declare global and local variables:                                      #
    #--------------------------------------------------------------------------#
    global conn
    global gLevel
    global pathOutput
    global pathTemplates
    global gParent

    #--------------------------------------------------------------------------#
    # Get the parent object in the hierarchy:                                  #
    #--------------------------------------------------------------------------#
    sParent = args['parent']
    gParent = sParent

    #--------------------------------------------------------------------------#
    # Get the input code template path:                                        #
    #--------------------------------------------------------------------------#
    pathTemplates = args['input']

    #--------------------------------------------------------------------------#
    # Get the output code module path:                                         #
    #--------------------------------------------------------------------------#
    pathOutput = args['output']

    #--------------------------------------------------------------------------#
    # Get the code configuration workbook name and check it exists:            #
    #--------------------------------------------------------------------------#
    wbName = args['config']
    if not os.path.exists(wbName):
        errorHandler(errProc, errorCode.filenotExist, wbName)

    #--------------------------------------------------------------------------#
    # Delete the sqlite database file if it already exists so it can be        #
    # created anew with refreshed data:                                        #
    #--------------------------------------------------------------------------#
    dbName = os.path.dirname(wbName) + '/config.db'
    try:
        os.remove(dbName)
    except OSError:
        pass

    #--------------------------------------------------------------------------#
    # Convert the configuration workbook from xlsx to sqlite database format:  #
    #--------------------------------------------------------------------------#
    try:
        xls2db(wbName, dbName)
    except:
        errorHandler(errProc, errorCode.cannotConvertWorkbook, wbName, dbName)

    #--------------------------------------------------------------------------#
    # Connect to the new persistent sqlite database file:                      #
    #--------------------------------------------------------------------------#
    try:
        conn = sqlite3.connect(dbName)
        conn.row_factory = sqlite3.Row
    except:
        errorHandler(errProc, errorCode.cannotConnectDB, dbName)

    #--------------------------------------------------------------------------#
    # Create the global parameters table:                                      #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.tblCreateGlobalParameter]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotCreateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Create the eventPrompt table:                                            #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.tblCreateEventPrompt]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotCreateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Create the eventConfirmNo table:                                         #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.tblCreateEventConfirmNo]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotCreateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Create the eventConfirmYes table:                                        #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.tblCreateEventConfirmYes]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotCreateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Create the eventLogMsg table:                                            #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.tblCreateEventLogMsg]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotCreateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Create the eventLogReal table:                                           #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.tblCreateEventLogReal]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotCreateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Create the eventLogTime table:                                           #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.tblCreateEventLogTime]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotCreateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Get the progress weighting:                                              #
    #--------------------------------------------------------------------------#
    pbChunks = 39.0

    #--------------------------------------------------------------------------#
    # Process the EM SFC parameters for the selected parent:                   #
    #--------------------------------------------------------------------------#
    gLevel = 'EM'
    processSFC(sParent, gLevel, 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the UN SFC parameters for the selected parent:                   #
    #--------------------------------------------------------------------------#
    gLevel = 'UN'
    processSFC(sParent, gLevel, 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the PC SFC parameters for the selected parent:                   #
    #--------------------------------------------------------------------------#
    gLevel = 'PC'
    processSFC(sParent, gLevel, 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Add the block level parameters from the tblClass_Parameters list. Only   #
    # add those parameters not already added in the SFCs:                      #
    #--------------------------------------------------------------------------#
    addParameterClass()

    #--------------------------------------------------------------------------#
    # Populate the eventPrompt table:                                          #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.insertEventPrompt]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotInsertTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Update the index in the eventPrompt table:                               #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.updateEventPrompt]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotUpdateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Populate the eventPrompt Confirm Yes table:                              #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.insertEventConfirmYes]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotInsertTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Update the index in the eventPrompt Confirm Yes table:                   #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.updateEventConfirmYes]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotUpdateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Populate the eventPrompt Confirm No table:                               #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.insertEventConfirmNo]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotInsertTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Update the index in the eventPrompt Confirm No table:                    #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.updateEventConfirmNo]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotUpdateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Populate the eventLogMsg table:                                          #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.insertEventLogMsg]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotInsertTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Update the index in the eventLogMsg table:                               #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.updateEventLogMsg]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotUpdateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Populate the eventLogReal table:                                         #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.insertEventLogReal]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotInsertTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Update the index in the eventLogReal table:                              #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.updateEventLogReal]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotUpdateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Populate the eventLogTime table:                                         #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.insertEventLogTime]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotInsertTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Update the index in the eventLogTime table:                              #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.updateEventLogTime]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotUpdateTable, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Create the overall program files:                                        #
    #--------------------------------------------------------------------------#
    createProgramFiles(sParent, 'PG', 100 * 1 / pbChunks)

    #--------------------------------------------------------------------------#
    # Create the remainder of the program block related files:                 #
    #--------------------------------------------------------------------------#
    createProgramFiles(sParent, 'CM', 100 * 1 / pbChunks)
    createProgramFiles(sParent, 'EM', 100 * 1 / pbChunks)
    createProgramFiles(sParent, 'UN', 100 * 1 / pbChunks)
    createProgramFiles(sParent, 'PC', 100 * 1 / pbChunks)
    createProgramFiles(sParent, 'IL', 100 * 1 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Interlocks for the selected parent:                          #
    #--------------------------------------------------------------------------#
    gLevel = 'IL'
    processLevel(sParent, gLevel, 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected parent:                     #
    #--------------------------------------------------------------------------#
    gLevel = 'CM'
    processLevel(sParent, gLevel, 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected parent:                     #
    #--------------------------------------------------------------------------#
    gLevel = 'EM'
    processLevel(sParent, gLevel, 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected parent:                     #
    #--------------------------------------------------------------------------#
    gLevel = 'UN'
    processLevel(sParent, gLevel, 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected parent:                     #
    #--------------------------------------------------------------------------#
    gLevel = 'PC'
    processLevel(sParent, gLevel, 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Finally create any program files that need all blocks defined:           #
    #--------------------------------------------------------------------------#
    createProgramFiles(sParent, 'BLK', 100 * 1 / pbChunks)

    #--------------------------------------------------------------------------#
    # Commit the changes to the database and close the connection:             #
    #--------------------------------------------------------------------------#
    conn.commit()
    conn.close()

    #--------------------------------------------------------------------------#
    # Report completion regardless of error:                                   #
    #--------------------------------------------------------------------------#
    p.set_description(sParent + ': Processing complete')
    p.refresh()
    p.close()

    #--------------------------------------------------------------------------#
    # Output a success message:                                                #
    #--------------------------------------------------------------------------#
    print('Congratulations... ' + gParent + ' code generation successful.')

#------------------------------------------------------------------------------#
# Function: processLevel                                                       #
#                                                                              #
# Description:                                                                 #
# This processes the selected level for the class.                             #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sParent               The parent tree object to generate code for.           #
# sLevel                The level to process, either CM, EM, UN or PC.         #
# pbwt                  The % weight of the procedure for the progress bar.    #
#------------------------------------------------------------------------------#
def processLevel(sParent, sLevel, pbwt):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = processLevel.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the number of classes:                                               #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.processLevelCount]
        c.execute(query, (sLevel.upper(),))
        r = c.fetchone()
        num = r['num']
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.processLevelCount, query, sLevel.upper())

    #--------------------------------------------------------------------------#
    # Get the list of classes:                                                 #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.processLevel]
        c.execute(query, (sLevel.upper(),))
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.processLevel, query, sLevel.upper())

    #--------------------------------------------------------------------------#
    # Process each row in the list of classes:                                 #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Update the progress bar:                                             #
        #----------------------------------------------------------------------#
        sClass = row['Class']
        logging.info(sClass)
        pc = pbwt * 1.0 / num
        p.update(pc)
        p.set_description(sParent + ': ' + sClass)
        p.refresh()
        sleep(0.01)

        #----------------------------------------------------------------------#
        # Add the child parameters if a block level module:                    #
        #----------------------------------------------------------------------#
        gClass = sClass
        if (sLevel == 'EM' or sLevel == 'UN' or sLevel == 'PC'):
            addParametersChild(sClass)
            addParametersChildCMD(sClass)
#            addParametersDefer(sClass)

        #----------------------------------------------------------------------#
        # Create the instance FB (ifb) of the class:                           #
        #----------------------------------------------------------------------#
        sPrefix = 'ifb'
        createClass(sLevel, sParent, sClass, row['Description'],
                    sPrefix, row['inheritsInstance'], 'awl', row['nameInstance'], 'awl', True)

        #----------------------------------------------------------------------#
        # Create PLC communications transfer function for each class:          #
        #----------------------------------------------------------------------#
        sPrefix = 'fbx'
        if (sLevel == 'CM' or sLevel == 'EM' or sLevel == 'UN' or sLevel == 'PC'):
            createClass(sLevel, sParent, sClass, row['Description'],
                        sPrefix, '', 'awl', sClass, 'awl', True)

#        elif (sLevel == 'IL'):
#            createClass(sLevel, sParent, sClass, row['Description'],
#                        sPrefix, row['inheritsInstance'], row['nameInstance'], True)

        #----------------------------------------------------------------------#
        # Create the function block class file:                                #
        #----------------------------------------------------------------------#
        sPrefix = row['functionClass']
        if (sPrefix != 'DEL'):
            gClass = sClass
            createClass(sLevel, sParent, sClass, row['Description'],
                        sPrefix, row['inheritsClass'], 'awl', row['nameClass'], 'awl', True)

        #----------------------------------------------------------------------#
        # Update the progress message:                                         #
        #----------------------------------------------------------------------#
        p.set_description(sParent + ': ' + sClass + ' complete')
        p.refresh()

    #--------------------------------------------------------------------------#
    # Check if an interlock class. The interlocks are called directly from the #
    # Main routine OB1:                                                        #
    #--------------------------------------------------------------------------#
    if (sLevel == 'IL'):
        #----------------------------------------------------------------------#
        # Create the critical interlock instance DB:                           #
        #----------------------------------------------------------------------#
        createClass(sLevel, sParent, '', '', '', 'idbIL', 'awl', 'idb' + sLevel + 's', 'awl', False)
#        createClass(sLevel, sParent, '', '', '', 'dbxIL', 'dbx' + sLevel + 's', False)
    else:
        #----------------------------------------------------------------------#
        # Must be a functional level and not an interlock class. Create the    #
        # instance DBs for the functional levels:                              #
        #----------------------------------------------------------------------#
        createClass(sLevel, sParent, '', '', '', 'dbi', 'awl', 'idb' + sLevel + 's', 'awl', False)

        #----------------------------------------------------------------------#
        # Create fcCall to be called from OB1 and scan each instance:          #
        #----------------------------------------------------------------------#
        createClass(sLevel, sParent, '', '', '', 'fcCall', 'awl', 'fcCall' + sLevel + 's', 'awl', False)

        #----------------------------------------------------------------------#
        # Create the transfer call instance DBs and calls:                     #
        #----------------------------------------------------------------------#
        if (sLevel == 'CM' or sLevel == 'EM' or sLevel == 'UN'):
            createClass(sLevel, sParent, '', '', '', 'dbx', 'awl', 'dbx' + sLevel + 's', 'awl', False)
            createClass(sLevel, sParent, '', '', '', 'fcCallx', 'awl', 'fcCallx' + sLevel + 's', 'awl', False)

    #--------------------------------------------------------------------------#
    # Update the progress message:                                             #
    #--------------------------------------------------------------------------#
    p.set_description(sParent + ': Level ' + sLevel + ' complete')
    p.refresh()

#------------------------------------------------------------------------------#
# Function: processSFC                                                         #
#                                                                              #
# Description:                                                                 #
# This processes the SFC parameters.                                           #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sParent               The parent tree object to generate code for.           #
# sLevel                The level to process, either CM, EM, UN or PC.         #
# pbwt                  The % weight of the procedure for the progress bar.    #
#------------------------------------------------------------------------------#
def processSFC(sParent, sLevel, pbwt):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = processSFC.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the number of classes:                                               #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.processLevelCount]
        c.execute(query, (sLevel.upper(),))
        r = c.fetchone()
        num = r['num']
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.processLevelCount, query, sLevel.upper())

    #--------------------------------------------------------------------------#
    # Get the list of classes:                                                 #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.processLevel]
        c.execute(query, (sLevel.upper(),))
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.processLevel, query, sLevel.upper())

    #--------------------------------------------------------------------------#
    # Process each row in the list of classes:                                 #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Update the progress bar:                                             #
        #----------------------------------------------------------------------#
        sClass = row['Class']
        logging.info(sClass)
        pc = pbwt * 1.0 / num
        p.update(pc)
        p.set_description(sParent + ': SFC ' + sClass)
        p.refresh()
        sleep(0.01)

        #----------------------------------------------------------------------#
        # Add the SFC and child parameters to the parameter list:              #
        #----------------------------------------------------------------------#
        addParametersSFC(sClass)

        #----------------------------------------------------------------------#
        # Update the progress message:                                         #
        #----------------------------------------------------------------------#
        p.set_description(sParent + ': ' + sClass + ' SFC parameters complete')
        p.refresh()

    #--------------------------------------------------------------------------#
    # Update the progress message:                                             #
    #--------------------------------------------------------------------------#
    p.set_description(sParent + ': Level ' + sLevel + ' SFC parameters complete')
    p.refresh()

#------------------------------------------------------------------------------#
# Function: createProgramFiles                                                 #
#                                                                              #
# Description:                                                                 #
# Creates the overall program files.                                           #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sParent               The parent tree object which owns the instances.       #
# sLevel                The Class level to create.                             #
# pbwt                  The % weight of the procedure for the progress bar.    #
#------------------------------------------------------------------------------#
def createProgramFiles(sParent, sLevel, pbwt):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = createProgramFiles.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the number of non S88 program code files:                            #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.createProgramFilesCount]
        c.execute(query, (sLevel.upper(),))
        r = c.fetchone()
        num = r['num']
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.createProgramFilesCount, query, sLevel.upper())

    #--------------------------------------------------------------------------#
    # Now get the list of non S88 files:                                       #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.createProgramFiles]
        c.execute(query, (sLevel.upper(),))
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.createProgramFiles, query, sLevel.upper())

    #--------------------------------------------------------------------------#
    # Process each row in the list of files:                                   #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Update the progress bar:                                             #
        #----------------------------------------------------------------------#
        pc = pbwt * 1.0 / num
        p.update(pc)
        p.set_description(sParent + ': ' + row['File'])
        p.refresh()
        sleep(0.01)

        #----------------------------------------------------------------------#
        # Create the output file from the input awl source:                    #
        #----------------------------------------------------------------------#
        createClass(sLevel, sParent, '', '', '', row['File'], row['extInput'], row['File'], row['extOutput'], False)

    #--------------------------------------------------------------------------#
    # Update the progress message:                                             #
    #--------------------------------------------------------------------------#
    p.set_description(sParent + ': ' + sLevel + ' files complete')
    p.refresh()

#------------------------------------------------------------------------------#
# Function: createClass                                                        #
#                                                                              #
# Description:                                                                 #
# Creates Class based STL files, such as instance FBs (ifb) and instance       #
# FCs (ifc) for all of the class instances of the specified in the Process     #
# Cell.                                                                        #
# If bOne then creates files with all instances of the specified level.        #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sLevel                The Class level to create.                             #
# sParent               The parent tree object to generate classes for.        #
# sClass                The class to process the instances for.                #
# sClassDescription     The class description.                                 #
# sPrefix               The file prefix.                                       #
# sTemplate             The code template file name.                           #
# sEXtIn                The input file extension.                              #
# sNameOutput           The output file name after the prefix.                 #
# sEXtOut               The output file extension.                             #
# bOne                  Create output file just the specified class.           #
#------------------------------------------------------------------------------#
def createClass(sLevel, sParent, sClass, sClassDescription,
                sPrefix, sTemplate, sExtIn, sNameOutput, sExtOut, bOne):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = createClass.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global iCountFile
    global iCountTemplateMax
    global conn
    global gClass
    global gFile
#    global gILTable
    global pathOutput
    global pathTemplates

    #--------------------------------------------------------------------------#
    # Get a connection to the database:                                        #
    #--------------------------------------------------------------------------#
    c = conn.cursor()
    try:
        query = cgSQL.sql[cgSQL.sqlCode.createClassNone]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.createClassNone, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Get the list of instances for the template if there are any:             #
    #--------------------------------------------------------------------------#
    gClass = sClass
    if (sPrefix == 'fbx'):
        try:
            query = cgSQL.sql[cgSQL.sqlCode.xferInstancesGlobal]
            c.execute(query, (sClass, ))
        except:
            errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.xferInstancesGlobal, query, sClass)

    elif (len(sClass) > 0 and sLevel != 'IL'):
        try:
            query = cgSQL.sql[cgSQL.sqlCode.createInstancesGlobal]
            c.execute(query, (sClass, ))
        except:
            errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.createInstancesGlobal, query, sClass)
    else:
        try:
            query = cgSQL.sql[cgSQL.sqlCode.createClassNone]
            c.execute(query)
        except:
            errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.createClassNone, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Check to see if the cursor contains any data:                            #
    #--------------------------------------------------------------------------#
    data = c.fetchall()
    if (len(data) != 0):
        #----------------------------------------------------------------------#
        # Get the code template file name and check that it exists:            #
        #----------------------------------------------------------------------#
        sFileNameIn = pathTemplates + '/' + sPrefix + sTemplate + '.' + sExtIn
        logging.info(sFileNameIn)
        if not os.path.exists(sFileNameIn):
            errorHandler(errProc, errorCode.filenotExist, sFileNameIn)

        #----------------------------------------------------------------------#
        # Open the template file for reading and parse each line:              #
        #----------------------------------------------------------------------#
        iCountFile = 0
        file = open(sFileNameIn, 'r')
        bSkipLine = False
        bTemplateBegin = False
        bTemplateEnd = False
        sQuery = ''
        txtData = ''
        txtTemplate = ''
        for sBuffer in file:
            #------------------------------------------------------------------#
            # Check if a blank line:                                           #
            #------------------------------------------------------------------#
            if (sBuffer is None):
                if (bTemplateBegin and not bTemplateEnd):
                    if (ord(txtTemplate[-1:]) == 13):
                        txtTemplate = txtTemplate + '\n'
                    else:
                        txtTemplate = txtTemplate + '\r\n'
                else:
                    txtData = txtData + '\r\n'
                    if (ord(txtData[-1:]) == 13):
                        txtData = txtData + '\n'
                    else:
                        txtData = txtData + '\r\n'
            else:
                #--------------------------------------------------------------#
                # Check if the start of a new instance template:               #
                #--------------------------------------------------------------#
                if (sBuffer.find('@@TEMPLATE_BEGIN') >= 0):
                    bTemplateBegin = True
                    bSkipLine = True

                    #----------------------------------------------------------#
                    # Check if there is a new query:                           #
                    #----------------------------------------------------------#
                    if (sBuffer.find('@@TEMPLATE_BEGIN|') >= 0):
                        #------------------------------------------------------#
                        # Get the new query data:                              #
                        #------------------------------------------------------#
                        iQueryBegin = sBuffer.find('@@TEMPLATE_BEGIN|')
                        iQueryEnd = sBuffer.find('@@', iQueryBegin + 17)
                        sQuery = sBuffer[iQueryBegin + 17:iQueryEnd]
                        data = getNamedQueryData(sQuery)

                #--------------------------------------------------------------#
                # Check if the end of the current instance template:           #
                #--------------------------------------------------------------#
                elif (sBuffer.find('@@TEMPLATE_END@@') >= 0):
                    bTemplateEnd = True

                #--------------------------------------------------------------#
                # Build the instance template text if within an instance       #
                # template:                                                    #
                #--------------------------------------------------------------#
                if (bTemplateBegin and not bTemplateEnd):
                    if (bSkipLine):
                        bSkipLine = False
                    else:
                        txtTemplate = txtTemplate + sBuffer

                #--------------------------------------------------------------#
                # Check if not in a template:                                  #
                #--------------------------------------------------------------#
                elif (not bTemplateBegin):
                    #----------------------------------------------------------#
                    # Build the output text with the base file data:           #
                    #----------------------------------------------------------#
                    txtData = txtData + sBuffer

                #--------------------------------------------------------------#
                # Rehhhce the fields in the instance template if the template  #
                # is finished:                                                 #
                #--------------------------------------------------------------#
                elif (bTemplateBegin and bTemplateEnd):
                    #----------------------------------------------------------#
                    # Replace the fields in the instance template:             #
                    #----------------------------------------------------------#
                    gFile = sPrefix + sTemplate + '.' + sExtIn
                    p.set_description(sParent + ': ' + sClass + ': ' + gFile + ': ' + sQuery)
                    p.refresh()
                    txtData = processTemplate(data, txtTemplate, txtData, bOne)
                    txtTemplate = ''
                    bTemplateBegin = False
                    bTemplateEnd = False

        #----------------------------------------------------------------------#
        # Close the input file:                                                #
        #----------------------------------------------------------------------#
        file.close()

        #----------------------------------------------------------------------#
        # Replace any default parameters:                                      #
        #----------------------------------------------------------------------#
        txtData = defaultParameters(sParent, txtData)

        #----------------------------------------------------------------------#
        # Replace the class information in the entire file if just one class:  #
        #----------------------------------------------------------------------#
        if (bOne):
            txtData = txtData.replace('@@CLASS@@', gClass)
            txtData = txtData.replace('@@CLASSDESCRIPTION@@', gClassDescription)

        #----------------------------------------------------------------------#
        # Replace any maximum counter value:                                   #
        #----------------------------------------------------------------------#
        txtData = txtData.replace('@@COUNTERTEMPLATEMAX@@', str(iCountTemplateMax))
        txtData = txtData.replace('@@COUNTERTEMPLATENEXT@@', str(iCountTemplateMax + 1))

        #----------------------------------------------------------------------#
        # Write the output instance file:                                      #
        #----------------------------------------------------------------------#
        if (bOne or sClass == 'IL' or sTemplate == 'fcCall' or sTemplate == 'fcCallx' or sTemplate == 'dbi' or sTemplate == 'dbx'):
            sFileNameOut = pathOutput + '/' + sPrefix + sNameOutput + '.' + sExtOut
        else:
            sFileNameOut = pathOutput + '/' + sTemplate + '.' + sExtOut
        file = open(sFileNameOut, 'w')
        file.write(txtData)
        file.close()

#        if (sLevel == 'CM'):
#            addCodeFileParameters(sLevel, sClass, sClass, sClass, txtData, False)

#------------------------------------------------------------------------------#
# Function: processTemplate                                                    #
#                                                                              #
# Description:                                                                 #
# Updates the placeholder fields in the text template.                         #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# c                     The cursor with the instance data.                     #
# txtTemplate           The template string to look through.                   #
# txtData               The running instance data string.                      #
# bOne                  Create output file just the specified class.           #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtData               The output data string with the new instance data.     #
#------------------------------------------------------------------------------#
def processTemplate(c, txtTemplate, txtData, bOne):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = processTemplate.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global iCountTemplate
    global gClass
    global gClassDescription
    global gInstance
    global gLevel
    global gParent

    #--------------------------------------------------------------------------#
    # Enter a loop to process each instance:                                   #
    #--------------------------------------------------------------------------#
    iCountTemplate = 0
    iCounterBase = 0
    txtInstance = ''
    for row in c:
        #----------------------------------------------------------------------#
        # Enter a loop to process all of the fields in the instance record:    #
        #----------------------------------------------------------------------#
        sClass = ''
        sClassDescription = ''
        sInstance = ''
        txtInstance = txtTemplate
        for fld in row.keys():
            #------------------------------------------------------------------#
            # Replace the field placeholders:                                  #
            #------------------------------------------------------------------#
            if not row[fld] is None:
                sValue = str(row[fld])
                txtInstance = txtInstance.replace('@@' + fld.upper() + '@@', sValue)

                #--------------------------------------------------------------#
                # Get the class and instance names:                            #
                #--------------------------------------------------------------#
                if (fld.upper() == 'CLASS'):
                    sClass = row[fld]
                    gClass = sClass

                elif (fld.upper() == 'CLASSDESCRIPTION'):
                    gClassDescription = row[fld]

                elif (fld.upper() == 'INSTANCE'):
                    sInstance = row[fld]
                    gInstance = sInstance

                elif (fld.upper() == 'LEVEL'):
                    gLevel = row[fld]

        #----------------------------------------------------------------------#
        # Check if there are child attribute aliases in the template:          #
        #----------------------------------------------------------------------#
        if (txtInstance.find('ATTR_BEGIN') >= 0):
            #------------------------------------------------------------------#
            # Process the attribute data:                                      #
            #------------------------------------------------------------------#
            txtInstance = insertAttributeData(sClass, sInstance, txtInstance, 0)

        #----------------------------------------------------------------------#
        # Replace any counters and adders:                                     #
        #----------------------------------------------------------------------#
        txtInstance = replaceCounterFile(txtInstance)
        txtInstance = replaceCounterTemplate(txtInstance)
        txtInstance = replaceAdderAttr(txtInstance)

        #----------------------------------------------------------------------#
        # Add the instance data to the output file:                            #
        #----------------------------------------------------------------------#
        txtData = txtData + txtInstance

    #--------------------------------------------------------------------------#
    # Return the template now it is filled with instance data:                 #
    #--------------------------------------------------------------------------#
    return txtData

#------------------------------------------------------------------------------#
# Function: insertAttributeData                                                #
#                                                                              #
# Description:                                                                 #
# Inserts any template attributes data.                                        #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sClass                The class to process children for.                     #
# sInstance             The instance tag number.                               #
# txtInstance           The instance data string.                              #
# rl                    Recursion level.                                       #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtInstance           The updated instance data string with the new data.    #
#------------------------------------------------------------------------------#
def insertAttributeData(sClass, sInstance, txtInstance, rl):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = insertAttributeData.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object and other variables:      #
    #--------------------------------------------------------------------------#
    global iCountAttr
    global iCountAttrMax
    global gAlias
    global gChildClass
    global gClass
    global gCommand
    global gFile
    global gInstance
    global gLevel
    global gParent
    global gChildParameter
    global gRecipeClass
    global gSelectParameter
    global gSelectSelection
    global gSFC
    global gState

    #--------------------------------------------------------------------------#
    # Process all of the attributes in the template:                           #
    #--------------------------------------------------------------------------#
    while (txtInstance.find('@@ATTR_BEGIN|') >= 0):
        #----------------------------------------------------------------------#
        # Get the attribute name from the template. It must be enclosed in     #
        # the format:                                                          #
        #   @@ATTR_BEGIN|<attr>@@                                              #
        #   @@ATTR_END|<attr>@@                                                #
        #----------------------------------------------------------------------#
        iCountAttr = 0
        iCounterBase = 0
        txtRecordData = ''
        iTagBegin = txtInstance.find('@@ATTR_BEGIN|')
        iTagEnd = txtInstance.find('@@', iTagBegin + 13)
        if (iTagBegin > iTagEnd):
            errorHandler(errProc, errorCode.noBeginPlaceholder, txtInstance)
        else:
            #------------------------------------------------------------------#
            # Get the template text between the BEGIN and END tags. Error if   #
            # no end tag:                                                      #
            #------------------------------------------------------------------#
            sTemplateAttrName = txtInstance[iTagBegin + 13:iTagEnd]
            iTagAttrEnd = txtInstance.find('@@ATTR_END|' + sTemplateAttrName + '@@')
            if (iTagAttrEnd == -1):
                errorHandler(errProc, errorCode.noEndPlaceholder, sTemplateAttrName, txtInstance)

            #------------------------------------------------------------------#
            # Get the instance file text before and after the template:        #
            #------------------------------------------------------------------#
            txtTemplate = txtInstance[iTagEnd + 2:iTagAttrEnd]
            txtInstanceBegin = txtInstance[:iTagBegin]
            txtInstanceEnd = txtInstance[iTagAttrEnd + 11 + len(sTemplateAttrName) + 4:]

            #------------------------------------------------------------------#
            # Strip out the extra carriage returns from the template text:     #
            #------------------------------------------------------------------#
            try:
                if (ord(txtTemplate[-2:-1]) == 13):
                    txtTemplate = txtTemplate[2:-1]
                else:
                    txtTemplate = txtTemplate[2:]
            except:
                errorHandler(errProc, errorCode.nonASCIITemplate, sTemplateAttrName, txtTemplate)

            #------------------------------------------------------------------#
            # Get any Default template definition tags:                        #
            #------------------------------------------------------------------#
            iDefaultBegin = txtTemplate.find('@@ATTR_DEFAULT_BEGIN@@')
            iDefaultEnd = txtTemplate.find('@@ATTR_DEFAULT_END@@')

            #------------------------------------------------------------------#
            # Check to see if the cursor contains any data:                    #
            #------------------------------------------------------------------#
            p.set_description(gParent + ': ' + gClass + ': ' + gFile + ': ' + sTemplateAttrName)
            p.refresh()
            data = getNamedQueryData(sTemplateAttrName)
            if (len(data) == 0):
                #--------------------------------------------------------------#
                # No data so leave any default value:                          #
                #--------------------------------------------------------------#
                if (iDefaultBegin >= 0):
                    txtRecordData = txtTemplate[iDefaultBegin + 24:iDefaultEnd]
                else:
                    #----------------------------------------------------------#
                    # Not even a default value. Blank the template:            #
                    #----------------------------------------------------------#
                    txtRecordData = ''
            else:
                #--------------------------------------------------------------#
                # There is data so erase any default data:                     #
                #--------------------------------------------------------------#
                if (iDefaultBegin >= 0):
                    txtTemplate = txtTemplate[:iDefaultBegin] + txtTemplate[iDefaultEnd + 22:]

                #--------------------------------------------------------------#
                # If special LINK template then don't refresh the record       #
                # template in the loop below:                                  #
                #--------------------------------------------------------------#
                if (sTemplateAttrName == 'LINK'):
                    txtRecord = txtTemplate

                #--------------------------------------------------------------#
                # Enter a loop to replace the attribute field names:           #
                #--------------------------------------------------------------#
                for row in data:
                    #----------------------------------------------------------#
                    # If not a LINK template then each row of the cursor is a  #
                    # different record in the file:                            #
                    #----------------------------------------------------------#
                    if (sTemplateAttrName != 'LINK'):
                        txtRecord = txtTemplate

                    #----------------------------------------------------------#
                    # Enter a loop to process all of the fields in the         #
                    # instance record:                                         #
                    #----------------------------------------------------------#
                    for fld in row.keys():
                        #------------------------------------------------------#
                        # Set a null placeholder if no data:                   #
                        #------------------------------------------------------#
                        if row[fld] is None:
                            txtRecord = txtRecord.replace('@@' + fld.upper() + '@@', '##NULL##')
                        else:
                            #--------------------------------------------------#
                            # Replace the placeholder with the db value:       #
                            #--------------------------------------------------#
                            if (isnumeric(row[fld])):
                                sValue = str(row[fld])
                            else:
                                try:
                                    row[fld].decode('ascii')
                                    sValue = str(row[fld])
                                except:
#                                except UnicodeDecodeError:
                                    s = ''
                                    for i in range(len(qparms)):
                                        if (len(s) > 0):
                                            s = s + ', '
                                        s = s + qparms[i]
                                    errorHandler(errProc, errorCode.nonASCIICharacter,
                                                 cgSQL.sqlCode[sTemplateAttrName], query, s)

                            #--------------------------------------------------#
                            # Update the field name and save the field data    #
                            # for iterative calls:                             #
                            #--------------------------------------------------#
                            if (sTemplateAttrName == 'LINK'):
                                sLink = row['LINK']
                            else:
                                sLink = ''

                            txtRecord = txtRecord.replace('@@' + sLink + fld.upper() + '@@', sValue)

                            if (fld.upper() == 'CHILDPARAMETERALIAS'):
                                gAlias = sValue

                            if (fld.upper() == 'CHILDALIASCLASS' or fld.upper() == 'CHILDPARAMETERCLASS'):
                                gChildClass = sValue

                            elif (fld.upper() == 'CLASS'):
                                gClass = sValue

                            if (fld.upper() == 'TRUECOMMAND' or fld.upper() == 'FALSECOMMAND'):
                                gCommand = sValue

                            elif (fld.upper() == 'INSTANCE'):
                                gInstance = sValue

                            elif (fld.upper() == 'CHILDPARAMETER'):
                                gChildParameter = sValue

                            if (fld.upper() == 'RECIPECLASS'):
                                gRecipeClass = sValue

                            elif (fld.upper() == 'SFC'):
                                gSFC = sValue

                            elif (fld.upper() == 'STATE'):
                                gState = sValue

                            if (sTemplateAttrName.upper() == 'SELECT'):
                                if (fld.upper() == 'PARAMETER'):
                                    gSelectParameter = sValue

                                elif (fld.upper() == 'SELECTION'):
                                    gSelectSelection = sValue

                    #----------------------------------------------------------#
                    # Process any further template child attribute tags:       #
                    #----------------------------------------------------------#
                    if (txtRecord.find('ATTR_BEGIN') >= 0):
                        txtRecord = insertAttributeData(gClass, gInstance, txtRecord, rl + 1)

                    #----------------------------------------------------------#
                    # Replace any counters:                                    #
                    #----------------------------------------------------------#
                    txtRecord = replaceCounterAttr(txtRecord)
                    txtRecord = replaceCounterFile(txtRecord)
                    txtRecord = replaceAdderAttr(txtRecord)

                    #----------------------------------------------------------#
                    # Build the attribute record string if not a LINK:         #
                    #----------------------------------------------------------#
                    if (sTemplateAttrName != 'LINK'):
                        if (len(txtRecord) > 2):
                            if (ord(txtRecord[-2:-1]) == 13):
                                txtRecordData = txtRecordData + txtRecord[:-1] + '\n'

                            elif (ord(txtRecord[-1:]) == 13):
                                txtRecordData = txtRecordData + txtRecord + '\n'
                            else:
                                txtRecordData = txtRecordData + txtRecord + '\r\n'

            #------------------------------------------------------------------#
            # Build the attribute record string if not a LINK:                 #
            #------------------------------------------------------------------#
            if (sTemplateAttrName == 'LINK' and len(data) != 0):
                if (len(txtRecord) > 2):
                    if (ord(txtRecord[-2:-1]) == 13):
                        txtRecordData = txtRecordData + txtRecord[:-1] + '\n'

                    elif (ord(txtRecord[-1:]) == 13):
                        txtRecordData = txtRecordData + txtRecord + '\n'
                    else:
                        txtRecordData = txtRecordData + txtRecord + '\r\n'

            #------------------------------------------------------------------#
            # Exclude the tag markers from the code template string:           #
            #------------------------------------------------------------------#
            txtInstance = txtInstanceBegin + txtRecordData + txtInstanceEnd

            #------------------------------------------------------------------#
            # Replace any maximum or next counter values:                      #
            #------------------------------------------------------------------#
            txtInstance = txtInstance.replace('@@COUNTERATTRMAX@@', str(iCountAttrMax))
            txtInstance = txtInstance.replace('@@COUNTERATTRNEXT@@', str(iCountAttrMax + 1))

    #--------------------------------------------------------------------------#
    # Return the template now it is filled with instance data:                 #
    #--------------------------------------------------------------------------#
    if (rl > 0 and len(txtInstance) > 1 and ord(txtInstance[-1:]) == 13):
        txtInstance = txtInstance[:-1]
        if (len(txtInstance) > 1 and ord(txtInstance[-1:]) == 13):
            txtInstance = txtInstance[:-1]
    return txtInstance

#------------------------------------------------------------------------------#
# Function: getNamedQueryData                                                  #
#                                                                              #
# Description:                                                                 #
# Returns the data for the named query.                                        #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# nameQuery             The name of the query to execute.                      #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# data                  The cursor with the query data.                        #
#------------------------------------------------------------------------------#
def getNamedQueryData(namedQuery):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = getNamedQueryData.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object and other variables:      #
    #--------------------------------------------------------------------------#
    global conn
    global gClass
    global gInstance
    global gLevel
    global gParent
    global gChildParameter
    global gRecipeClass
    global gSelectParameter
    global gSelectSelection
    global gSFC
    global gState

    #--------------------------------------------------------------------------#
    # Set the query based on the attribute name:                               #
    #--------------------------------------------------------------------------#
    parms = []
    qparms = []
    try:
        query = cgSQL.sql[cgSQL.sqlCode[namedQuery]]
        parms = cgSQL.prm[cgSQL.sqlCode[namedQuery]]
    except:
        errorHandler(errProc, errorCode.cannotGetSQL, namedQuery)

    #--------------------------------------------------------------------------#
    # Copy the list locally and replace the parameters with their current      #
    # global values:                                                           #
    #--------------------------------------------------------------------------#
    qparms = list(parms)
    for i in range(len(qparms)):
        if (qparms[i] == 'gAlias'):
            qparms[i] = gAlias
        elif (qparms[i] == 'gChildClass'):
            qparms[i] = gChildClass
        elif (qparms[i] == 'gClass'):
            qparms[i] = gClass
        elif (qparms[i] == 'gCommand'):
            qparms[i] = gCommand
#        elif (qparms[i] == 'gILTable'):
#            qparms[i] = gILTable
        elif (qparms[i] == 'gInstance'):
            qparms[i] = gInstance
        elif (qparms[i] == 'gLevel'):
            qparms[i] = gLevel
        elif (qparms[i] == 'gParent'):
            qparms[i] = gParent
        elif (qparms[i] == 'gChildParameter'):
            qparms[i] = gChildParameter
        elif (qparms[i] == 'gRecipeClass'):
            qparms[i] = gRecipeClass
        elif (qparms[i] == 'gSelectParameter'):
            qparms[i] = gSelectParameter
        elif (qparms[i] == 'gSelectSelection'):
            qparms[i] = gSelectSelection
        elif (qparms[i] == 'gSFC'):
            qparms[i] = gSFC
        elif (qparms[i] == 'gState'):
            qparms[i] = gState

#            for i in range(len(qparms)):
#                print(qparms[i])

    #--------------------------------------------------------------------------#
    # Query the sqlite database:                                               #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        c.execute(query, qparms)
    except:
        s = ''
        for i in range(len(qparms)):
            if (len(s) > 0):
                s = s + ', '
            s = s + qparms[i]
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode[namedQuery], query, s)

    #--------------------------------------------------------------------------#
    # Return the cursor:                                                       #
    #--------------------------------------------------------------------------#
    data = c.fetchall()
    return data

#------------------------------------------------------------------------------#
# Function: replaceAdderAttr                                                   #
#                                                                              #
# Description:                                                                 #
# Sets attribute adder values to count up by multiples.                        #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtRecord             The template text.                                     #
#------------------------------------------------------------------------------#
def replaceAdderAttr(txtRecord):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = replaceAdderAttr.__name__

    #--------------------------------------------------------------------------#
    # Define global variables:                                                 #
    #--------------------------------------------------------------------------#
    global iAdd
    global iAddMax

    #--------------------------------------------------------------------------#
    # Check if any adder placeholders:                                         #
    #--------------------------------------------------------------------------#
    iAdderIncr = 0
    if (txtRecord.find('@@ADDER') >= 0):
        #----------------------------------------------------------------------#
        # Check if a adder base starting value defined:                        #
        #----------------------------------------------------------------------#
        iAdderBase = 0
        sAdderBase = ''
        sAdderIncr = ''
        if (txtRecord.find('@@ADDER|') >= 0):
            #------------------------------------------------------------------#
            # Reset the adder first if requested:                              #
            #------------------------------------------------------------------#
            if (txtRecord.find('@@ADDERRESET@@') >= 0 and
                txtRecord.find('@@ADDERRESET@@') < txtRecord.find('@@ADDER|')):
                iAdd = 0
                txtRecord = txtRecord.replace('@@ADDERRESET@@\r\n', '', 1)

            #------------------------------------------------------------------#
            # Get the adder base starting value:                               #
            #------------------------------------------------------------------#
            iAdderBegin = txtRecord.find('@@ADDER|')
            iAdderEnd = txtRecord.find('|', iAdderBegin + 8)
            sAdderBase = txtRecord[iAdderBegin + 8:iAdderEnd]

            #------------------------------------------------------------------#
            # Get the adder increment value:                                   #
            #------------------------------------------------------------------#
            iAdderBegin = iAdderEnd + 1
            iAdderEnd = txtRecord.find('@@', iAdderBegin)
            sAdderIncr = txtRecord[iAdderBegin:iAdderEnd]

            #------------------------------------------------------------------#
            # Check if a numeric starting value:                               #
            #------------------------------------------------------------------#
            if (isnumeric(sAdderBase)):
                iAdderBase = int(sAdderBase)
                txtRecord = txtRecord.replace('@@ADDER|' + sAdderBase + '@@', str(iAdd + iAdderBase))
            else:
                #--------------------------------------------------------------#
                # Invalid default parameter value:                             #
                #--------------------------------------------------------------#
                errorHandler(errProc, errorCode.invalidAdder, sAdderBase)

            #------------------------------------------------------------------#
            # Check if a numeric increment value:                              #
            #------------------------------------------------------------------#
            if (isnumeric(sAdderIncr)):
                iAdderIncr = int(sAdderIncr)
                txtRecord = txtRecord.replace('@@ADDER|' + sAdderBase + '@@', str(iAdd + iAdderBase))
            else:
                #--------------------------------------------------------------#
                # Invalid default parameter value:                             #
                #--------------------------------------------------------------#
                errorHandler(errProc, errorCode.invalidAdder, sAdderIncr)

        #----------------------------------------------------------------------#
        # Replace the base adder placeholder to kick things off:               #
        #----------------------------------------------------------------------#
        txtRecord = txtRecord.replace('@@ADDER|' + sAdderBase + '|' + sAdderIncr + '@@', str(iAdd + iAdderBase))
        iAddMax = iAdd + iAdderBase

        #----------------------------------------------------------------------#
        # Replace any additional adder placeholders:                           #
        #----------------------------------------------------------------------#
        while (txtRecord.find('@@ADDER') >= 0):
            if (txtRecord.find('@@ADDERRESET@@') >= 0 and
                txtRecord.find('@@ADDERRESET@@') < txtRecord.find('@@ADDER@@')):
                iAdd = 0
                txtRecord = txtRecord.replace('@@ADDERRESET@@\r\n', '', 1)

            if (txtRecord.find('@@ADDERINCR@@') >= 0 and
                txtRecord.find('@@ADDERINCR@@') < txtRecord.find('@@ADDER@@')):
                iAdd = iAdd + iAdderIncr
                txtRecord = txtRecord.replace('@@ADDERINCR@@\r\n', '', 1)

            txtRecord = txtRecord.replace('@@ADDER@@', str(iAdd + iAdderBase), 1)
            iAddMax = iAdd + iAdderBase

    #--------------------------------------------------------------------------#
    # Increment the adder for next occurrence:                                 #
    #--------------------------------------------------------------------------#
    iAdd = iAdd + iAdderIncr

    #--------------------------------------------------------------------------#
    # Return the record now it is filled with adder data:                      #
    #--------------------------------------------------------------------------#
    return txtRecord

#------------------------------------------------------------------------------#
# Function: replaceCounterAttr                                                 #
#                                                                              #
# Description:                                                                 #
# Sets attribute counter values.                                               #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtRecord             The template text.                                     #
#------------------------------------------------------------------------------#
def replaceCounterAttr(txtRecord):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = replaceCounterAttr.__name__

    #--------------------------------------------------------------------------#
    # Define global variables:                                                 #
    #--------------------------------------------------------------------------#
    global iCountAttr
    global iCountAttrMax

    #--------------------------------------------------------------------------#
    # Check if any counter placeholders:                                       #
    #--------------------------------------------------------------------------#
    if (txtRecord.find('@@COUNTERATTR') >= 0):
        #----------------------------------------------------------------------#
        # Check if a counter base starting value defined:                      #
        #----------------------------------------------------------------------#
        iCounterBase = 0
        sCounterBase = ''
        if (txtRecord.find('@@COUNTERATTR|') >= 0):
            #------------------------------------------------------------------#
            # Reset the counter first if requested:                            #
            #------------------------------------------------------------------#
            if (txtRecord.find('@@COUNTERATTRRESET@@') >= 0 and
                txtRecord.find('@@COUNTERATTRRESET@@') < txtRecord.find('@@COUNTERATTR|')):
                iCountAttr = 0
                txtRecord = txtRecord.replace('@@COUNTERATTRRESET@@\r\n', '', 1)

            #------------------------------------------------------------------#
            # Get the counter base starting value:                             #
            #------------------------------------------------------------------#
            iCounterBegin = txtRecord.find('@@COUNTERATTR|')
            iCounterEnd = txtRecord.find('@@', iCounterBegin + 14)
            sCounterBase = txtRecord[iCounterBegin + 14:iCounterEnd]

            #------------------------------------------------------------------#
            # Check if a numeric starting value:                               #
            #------------------------------------------------------------------#
            if (isnumeric(sCounterBase)):
                iCounterBase = int(sCounterBase)
                txtRecord = txtRecord.replace('@@COUNTERATTR|' + sCounterBase + '@@', str(iCountAttr + iCounterBase))
            else:
                #--------------------------------------------------------------#
                # Invalid default parameter value:                             #
                #--------------------------------------------------------------#
                errorHandler(errProc, errorCode.invalidCounter, sCounterBase)

        #----------------------------------------------------------------------#
        # Replace the base counter placeholder to kick things off:             #
        #----------------------------------------------------------------------#
        txtRecord = txtRecord.replace('@@COUNTERATTR|' + sCounterBase + '@@', str(iCountAttr + iCounterBase))
        iCountAttrMax = iCountAttr + iCounterBase

        #----------------------------------------------------------------------#
        # Replace any additional counter placeholders:                         #
        #----------------------------------------------------------------------#
        while (txtRecord.find('@@COUNTERATTR') >= 0):
            if (txtRecord.find('@@COUNTERATTRRESET@@') >= 0 and
                txtRecord.find('@@COUNTERATTRRESET@@') < txtRecord.find('@@COUNTERATTR@@')):
                iCountAttr = 0
                txtRecord = txtRecord.replace('@@COUNTERATTRRESET@@\r\n', '', 1)

            if (txtRecord.find('@@COUNTERATTRINCR@@') >= 0 and
                txtRecord.find('@@COUNTERATTRINCR@@') < txtRecord.find('@@COUNTERATTR@@')):
                iCountAttr = iCountAttr + 1
                txtRecord = txtRecord.replace('@@COUNTERATTRINCR@@\r\n', '', 1)

            txtRecord = txtRecord.replace('@@COUNTERATTR@@', str(iCountAttr + iCounterBase), 1)
            iCountAttrMax = iCountAttr + iCounterBase

    #--------------------------------------------------------------------------#
    # Increment the counter for next occurrence:                               #
    #--------------------------------------------------------------------------#
    iCountAttr = iCountAttr + 1

    #--------------------------------------------------------------------------#
    # Return the record now it is filled with counter data:                    #
    #--------------------------------------------------------------------------#
    return txtRecord

#------------------------------------------------------------------------------#
# Function: replaceCounterFile                                                 #
#                                                                              #
# Description:                                                                 #
# Sets attribute counter values.                                               #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtRecord             The template text.                                     #
#------------------------------------------------------------------------------#
def replaceCounterFile(txtRecord):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = replaceCounterFile.__name__

    #--------------------------------------------------------------------------#
    # Define global variables:                                                 #
    #--------------------------------------------------------------------------#
    global iCountFile
    global iCountFileMax

    #--------------------------------------------------------------------------#
    # Check if any counter placeholders:                                       #
    #--------------------------------------------------------------------------#
    if (txtRecord.find('@@COUNTERFILE') >= 0):
        #----------------------------------------------------------------------#
        # Check if a counter base starting value defined:                      #
        #----------------------------------------------------------------------#
        iCounterBase = 0
        sCounterBase = ''
        if (txtRecord.find('@@COUNTERFILE|') >= 0):
            #------------------------------------------------------------------#
            # Reset the counter first if requested:                            #
            #------------------------------------------------------------------#
            if (txtRecord.find('@@COUNTERFILERESET@@') >= 0 and
                txtRecord.find('@@COUNTERFILERESET@@') < txtRecord.find('@@COUNTERFILE|')):
                iCountFile = 0
                txtRecord = txtRecord.replace('@@COUNTERFILERESET@@\r\n', '', 1)

            #------------------------------------------------------------------#
            # Get the counter base starting value:                             #
            #------------------------------------------------------------------#
            iCounterBegin = txtRecord.find('@@COUNTERFILE|')
            iCounterEnd = txtRecord.find('@@', iCounterBegin + 14)
            sCounterBase = txtRecord[iCounterBegin + 14:iCounterEnd]

            #------------------------------------------------------------------#
            # Check if a numeric starting value:                               #
            #------------------------------------------------------------------#
            if (isnumeric(sCounterBase)):
                iCounterBase = int(sCounterBase)
                txtRecord = txtRecord.replace('@@COUNTERFILE|' + sCounterBase + '@@', str(iCountFile + iCounterBase))
            else:
                #--------------------------------------------------------------#
                # Invalid default parameter value:                             #
                #--------------------------------------------------------------#
                errorHandler(errProc, errorCode.invalidCounter, sCounterBase)

        #----------------------------------------------------------------------#
        # Replace the base counter placeholder to kick things off:             #
        #----------------------------------------------------------------------#
        txtRecord = txtRecord.replace('@@COUNTERFILE|' + sCounterBase + '@@', str(iCountFile + iCounterBase))
        iCountFileMax = iCountFile + iCounterBase

        #----------------------------------------------------------------------#
        # Replace any additional counter placeholders:                         #
        #----------------------------------------------------------------------#
        while (txtRecord.find('@@COUNTERFILE') >= 0):
            if (txtRecord.find('@@COUNTERFILERESET@@') >= 0 and
                txtRecord.find('@@COUNTERFILERESET@@') < txtRecord.find('@@COUNTERFILE@@')):
                iCountFile = 0
                txtRecord = txtRecord.replace('@@COUNTERFILERESET@@\r\n', '', 1)

            if (txtRecord.find('@@COUNTERFILEINCR@@') >= 0 and
                txtRecord.find('@@COUNTERFILEINCR@@') < txtRecord.find('@@COUNTERFILE@@')):
                iCountFile = iCountFile + 1
                txtRecord = txtRecord.replace('@@COUNTERFILEINCR@@\r\n', '', 1)

            elif (txtRecord.find('@@COUNTERFILEINCR@@') >= 0):
                iCountFile = iCountFile + 1
                txtRecord = txtRecord.replace('@@COUNTERFILEINCR@@\r\n', '', 1)

            txtRecord = txtRecord.replace('@@COUNTERFILE@@', str(iCountFile + iCounterBase), 1)
            iCountFileMax = iCountFile + iCounterBase

    #--------------------------------------------------------------------------#
    # Increment the counter for next occurrence:                               #
    #--------------------------------------------------------------------------#
    iCountFile = iCountFile + 1

    #--------------------------------------------------------------------------#
    # Return the record now it is filled with counter data:                    #
    #--------------------------------------------------------------------------#
    return txtRecord

#------------------------------------------------------------------------------#
# Function: replaceCounterTemplate                                             #
#                                                                              #
# Description:                                                                 #
# Sets attribute counter values.                                               #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtRecord             The template text.                                     #
#------------------------------------------------------------------------------#
def replaceCounterTemplate(txtRecord):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = replaceCounterTemplate.__name__

    #--------------------------------------------------------------------------#
    # Define global variables:                                                 #
    #--------------------------------------------------------------------------#
    global iCountTemplate
    global iCountTemplateMax

    #--------------------------------------------------------------------------#
    # Check if any counter placeholders:                                       #
    #--------------------------------------------------------------------------#
    if (txtRecord.find('@@COUNTERTEMPLATE') >= 0):
        #----------------------------------------------------------------------#
        # Check if a counter base starting value defined:                      #
        #----------------------------------------------------------------------#
        iCounterBase = 0
        sCounterBase = ''
        if (txtRecord.find('@@COUNTERTEMPLATE|') >= 0):
            #------------------------------------------------------------------#
            # Reset the counter first if requested:                            #
            #------------------------------------------------------------------#
            if (txtRecord.find('@@COUNTERTEMPLATERESET@@') >= 0 and
                txtRecord.find('@@COUNTERTEMPLATERESET@@') < txtRecord.find('@@COUNTERTEMPLATE|')):
                iCountTemplate = 0
                txtRecord = txtRecord.replace('@@COUNTERTEMPLATERESET@@\r\n', '', 1)

            #------------------------------------------------------------------#
            # Get the counter base starting value:                             #
            #------------------------------------------------------------------#
            iCounterBegin = txtRecord.find('@@COUNTERTEMPLATE|')
            iCounterEnd = txtRecord.find('@@', iCounterBegin + 18)
            sCounterBase = txtRecord[iCounterBegin + 18:iCounterEnd]

            #------------------------------------------------------------------#
            # Check if a numeric starting value:                               #
            #------------------------------------------------------------------#
            if (isnumeric(sCounterBase)):
                iCounterBase = int(sCounterBase)
                txtRecord = txtRecord.replace('@@COUNTERTEMPLATE|' + sCounterBase + '@@', str(iCountTemplate + iCounterBase))
            else:
                #--------------------------------------------------------------#
                # Invalid default parameter value:                             #
                #--------------------------------------------------------------#
                errorHandler(errProc, errorCode.invalidCounter, sCounterBase)

        #----------------------------------------------------------------------#
        # Replace the base counter placeholder to kick things off:             #
        #----------------------------------------------------------------------#
        txtRecord = txtRecord.replace('@@COUNTERTEMPLATE|' + sCounterBase + '@@', str(iCountTemplate + iCounterBase))
        iCountTemplateMax = iCountTemplate + iCounterBase

        #----------------------------------------------------------------------#
        # Replace any additional counter placeholders:                         #
        #----------------------------------------------------------------------#
        while (txtRecord.find('@@COUNTERTEMPLATE') >= 0):
            if (txtRecord.find('@@COUNTERTEMPLATERESET@@') >= 0 and
                txtRecord.find('@@COUNTERTEMPLATERESET@@') < txtRecord.find('@@COUNTERTEMPLATE@@')):
                iCountTemplate = 0
                txtRecord = txtRecord.replace('@@COUNTERTEMPLATERESET@@\r\n', '', 1)

            if (txtRecord.find('@@COUNTERTEMPLATEINCR@@') >= 0 and
                txtRecord.find('@@COUNTERTEMPLATEINCR@@') < txtRecord.find('@@COUNTERTEMPLATE@@')):
                iCountTemplate = iCountTemplate + 1
                txtRecord = txtRecord.replace('@@COUNTERTEMPLATEINCR@@\r\n', '', 1)

            txtRecord = txtRecord.replace('@@COUNTERTEMPLATE@@', str(iCountTemplate + iCounterBase), 1)
            iCountTemplateMax = iCountTemplate + iCounterBase

    #--------------------------------------------------------------------------#
    # Increment the counter for next occurrence:                               #
    #--------------------------------------------------------------------------#
    iCountTemplate = iCountTemplate + 1

    #--------------------------------------------------------------------------#
    # Return the record now it is filled with counter data:                    #
    #--------------------------------------------------------------------------#
    return txtRecord

#------------------------------------------------------------------------------#
# Function: defaultParameters                                                  #
#                                                                              #
# Description:                                                                 #
# Sets any default parameter values.                                           #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sParent               The parent tree object which owns the instances.       #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtInstance           The updated instance template text.                    #
#------------------------------------------------------------------------------#
def defaultParameters(sParent, txtInstance):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = defaultParameters.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the initial tag index value for the selected Process Cell:           #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.defaultParameters]
        c.execute(query, (sParent, ))
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.defaultParameters, query, sParent)

    #--------------------------------------------------------------------------#
    # Process each row in the list of classes:                                 #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Replace the field placeholders:                                      #
        #----------------------------------------------------------------------#
        if (row['Parameter'] is None):
            errorHandler(errProc, errorCode.invalidDefaultData, sParent)

        elif (row['defaultValue'] is None):
            errorHandler(errProc, errorCode.invalidDefaultData, sParent)
        else:
            p = row['Parameter']
#            r = row['defaultValue']
            old = '@@' + p.upper() + '@@'
            new = row['defaultValue']
#            new = '{:10.1f}'.format(r)
            txtInstance = txtInstance.replace(old, new)

    #--------------------------------------------------------------------------#
    # Return the template now it is filled with default parameter data:        #
    #--------------------------------------------------------------------------#
    return txtInstance

#------------------------------------------------------------------------------#
# Function: addParameterClass                                                  #
#                                                                              #
# Description:                                                                 #
# Adds the class parameters from the parameters list tblClass_Parameters.      #
#------------------------------------------------------------------------------#
def addParameterClass():
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = addParameterClass.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the list of parameters from tblClass_Parameter:                      #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.addParametersClass]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.addParametersClass, query, 'no parameters')

    #--------------------------------------------------------------------------#
    # Process each row in the list of parameters:                              #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Get the parameter data:                                              #
        #----------------------------------------------------------------------#
        sLevel = row['Level']
        sClass = row['parameterClass']
        sSource = 'CLASS'
        sState = ''
        sParameterType = 'VAR_IN_OUT'
        iParameterIndex = 0
        sParameter = row['childParameter']
        sParameterBlock = row['blockParameter']
        sParameterDataType = row['parameterDataType']
        sParameterDataType = sParameterDataType.upper()
        sValue = ''
        sValue = row['parameterValue']
        sParameterDescription = row['parameterDescription']
        sChildParameterAlias = ''
        sChildParameterClass = ''
        sChildParameterAttribute = ''
        sOperation = row['parameterOperation']

        #----------------------------------------------------------------------#
        # Add the parameter to the global list:                                #
        #----------------------------------------------------------------------#
        addParameterData(sLevel, sClass, sSource, sState, sParameterType, iParameterIndex,
                         sParameter, sChildParameterClass, sParameterBlock, sParameterDataType,
                         sValue, sParameterDescription,
                         sChildParameterAlias, sChildParameterAttribute, False, sOperation)

#------------------------------------------------------------------------------#
# Function: addParametersChild                                                 #
#                                                                              #
# Description:                                                                 #
# Adds the user parameters from the child function blocks code files.          #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sClass                The parent class to process the code files for.        #
#------------------------------------------------------------------------------#
def addParametersChild(sClass):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = addParametersChild.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the list of child devices for the class:                             #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.getClassChildren]
        c.execute(query, (sClass,))
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.getClassChildren, query, sClass)

    #--------------------------------------------------------------------------#
    # Process each row in the list of child devices:                           #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Get the list of child parameters for the child class from the table  #
        # tblClass_Parameter:                                                  #
        #----------------------------------------------------------------------#
        sChildParameterClass = row['childAliasClass']
        sChildParameterAlias = row['childParameterAlias']
        try:
            cp = conn.cursor()
            query = cgSQL.sql[cgSQL.sqlCode.getChildParameters]
            cp.execute(query, (sChildParameterClass,))
        except:
            errorHandler(errProc, errorCode.cannotQuery,
                         cgSQL.sqlCode.getChildParameters, query, sChildParameterClass)

        #----------------------------------------------------------------------#
        # Process each child device parameter row:                             #
        #----------------------------------------------------------------------#
        for rowp in cp:
            #------------------------------------------------------------------#
            # Get the child parameter data:                                    #
            #------------------------------------------------------------------#
            sLevel = rowp['Level']
            sSource = 'CHILD'
            sState = ''
            sParameterType = 'VAR_IN_OUT'
            iParameterIndex = 0
            sParameter = ''
            sParameterBlock = sChildParameterAlias + '_' + rowp['blockParameter']
            sParameterDataType = rowp['parameterDataType']
            sParameterDataType = sParameterDataType.upper()
            sValue = ''
            sValue = rowp['parameterValue']
            sParameterDescription = rowp['parameterDescription']
            sChildParameterAttribute = rowp['blockParameter']
            sOperation = rowp['parameterOperation']

            #------------------------------------------------------------------#
            # Add the parameter to the global list:                            #
            #------------------------------------------------------------------#
            addParameterData(gLevel, sClass, sSource, '', sParameterType, iParameterIndex,
                             sParameter, sChildParameterClass,
                             sParameterBlock, sParameterDataType,
                             sValue, sParameterDescription, sChildParameterAlias,
                             sChildParameterAttribute, False, sOperation)

            #------------------------------------------------------------------#
            # Add the parent parameter to the global list:                     #
            #------------------------------------------------------------------#
#            sSource = 'PARENT'
#            sParameterBlock = rowp['blockParameter']
#            addParameterData(gLevel, sClass, sSource, '', sParameterType, iParameterIndex,
#                             sParameter, '',
#                             sParameterBlock, sParameterDataType,
#                             sValue, sParameterDescription, '',
#                             '', False, sOperation)

#------------------------------------------------------------------------------#
# Function: addParametersChildCMD                                              #
#                                                                              #
# Description:                                                                 #
# Adds the CMD attribute for all child devices.                                #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sClass                The parent class to process the children for.          #
#------------------------------------------------------------------------------#
def addParametersChildCMD(sClass):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = addParametersChildCMD.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the list of child devices for the class:                             #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.getClassChildren]
        c.execute(query, (sClass,))
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.getClassChildren, query, sClass)

    #--------------------------------------------------------------------------#
    # Process each row in the list of child devices:                           #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Get the list of child parameters for the child class from the table  #
        # tblClass_Child:                                                      #
        #----------------------------------------------------------------------#
        sChildParameterClass = row['childAliasClass']
        sChildParameterAlias = row['childParameterAlias']

        #----------------------------------------------------------------------#
        # Get the child parameter data:                                        #
        #----------------------------------------------------------------------#
        sLevel = row['Level']
        sSource = 'CHILDCMD'
        sState = ''
        sParameterType = 'VAR_IN_OUT'
        iParameterIndex = 0
        sParameter = ''
        sParameterBlock = sChildParameterAlias + '_CMD'
        sParameterDataType = 'INT'
        sValue = 0
        sParameterDescription = row['childAliasDescription'] + ' command'
        sChildParameterAttribute = 'CMD'
        sOperation = 'write'

        #----------------------------------------------------------------------#
        # Add the parameter to the global list:                                #
        #----------------------------------------------------------------------#
        addParameterData(gLevel, sClass, sSource, '', sParameterType, iParameterIndex,
                         sParameter, sChildParameterClass,
                         sParameterBlock, sParameterDataType,
                         sValue, sParameterDescription, sChildParameterAlias,
                         sChildParameterAttribute, False, sOperation)

#------------------------------------------------------------------------------#
# Function: addParametersDefer                                                 #
#                                                                              #
# Description:                                                                 #
# Adds the child calling parameters.                                           #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sClass                The parent class to process the code files for.        #
#------------------------------------------------------------------------------#
def addParametersDefer(sClass):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = addParametersDefer.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the list of child devices for the class:                             #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.getClassChildren]
        c.execute(query, (sClass,))
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.getClassChildren, query, sClass)

    #--------------------------------------------------------------------------#
    # Process each row in the list of child devices:                           #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Get the list of child parameters for the child class:                #
        #----------------------------------------------------------------------#
        sChildParameterClass = row['childAliasClass']
        sChildParameterAlias = row['childParameterAlias']
        try:
            cp = conn.cursor()
            query = cgSQL.sql[cgSQL.sqlCode.getDeferredParameters]
            cp.execute(query, (sChildParameterClass,))
        except:
            errorHandler(errProc, errorCode.cannotQuery,
                         cgSQL.sqlCode.getDeferredParameters, query, sChildParameterClass)

        #----------------------------------------------------------------------#
        # Process each child device parameter row:                             #
        #----------------------------------------------------------------------#
        for rowp in cp:
            #------------------------------------------------------------------#
            # Get the child parameter data:                                    #
            #------------------------------------------------------------------#
            sSource = 'DEFER'
            sParameterType = rowp['parameterType']
            iParameterOrder = rowp['parameterOrder']
            sParameter = rowp['childParameter']
            sParameterBlock = rowp['blockParameter']
            sParameterDataType = rowp['parameterDataType']
            sParameterDataType = sParameterDataType.upper()
            sValue = ''
            sValue = rowp['parameterValue']
            sParameterDescription = rowp['parameterDescription']
            sChildParameterAttribute = rowp['blockParameter']
            sOperation = rowp['operation']
            bIsChild = rowp['isChild']

            #------------------------------------------------------------------#
            # Add the parameter to the global list:                            #
            #------------------------------------------------------------------#
            addParameterData(gLevel, sClass, sSource, '', sParameterType, iParameterOrder,
                             sParameter, sChildParameterClass,
                             sParameterBlock, sParameterDataType,
                             sValue, sParameterDescription, sChildParameterAlias,
                             sChildParameterAttribute, False, sOperation)

#------------------------------------------------------------------------------#
# Function: addParametersSFC                                                   #
#                                                                              #
# Description:                                                                 #
# Adds the user SFC parameters from the SFC function block code files for a    #
# specified module class.                                                      #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sClass                The class to process the SFC class code files for.     #
#------------------------------------------------------------------------------#
def addParametersSFC(sClass):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = addParametersSFC.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the list of running substates for the class:                         #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.addParametersSFC]
        c.execute(query, (sClass, 'NONE'))
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.addParametersSFC, query, sClass + ', ' + 'NONE')

    #--------------------------------------------------------------------------#
    # Process each row in the list of classes:                                 #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Get the SFC file name and extract the user parameters:               #
        #----------------------------------------------------------------------#
        sSource = row['SFC']
        sState = row['State']
        sFileNameIn = pathTemplates + '/sfc/fb' + sSource + '.AWL'

        #----------------------------------------------------------------------#
        # Make sure the file exists before processing it:                      #
        #----------------------------------------------------------------------#
        logging.info(sFileNameIn)
        if not os.path.exists(sFileNameIn):
            errorHandler(errProc, errorCode.filenotExist, sFileNameIn)

        #----------------------------------------------------------------------#
        # Read in the entire contents of the file:                             #
        #----------------------------------------------------------------------#
        with open(sFileNameIn, 'r') as content_file:
            txtData = content_file.read()
            addCodeFileParameters(gLevel, sClass, sSource, sState, txtData, True)

#------------------------------------------------------------------------------#
# Function: addCodeFileParameters                                              #
#                                                                              #
# Description:                                                                 #
# Updates the internal table pGlobal with parameters from the awl code file.   #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sLevel                The level of the parameter object.                     #
# sClass                The class to process the instances for.                #
# sSource               The source file name of the block class module.        #
# sState                The state for the parameters.                          #
# txtData               The file content to get the parameters from.           #
# bIsSFC                TRUE if a an SFC parameter.                            #
#------------------------------------------------------------------------------#
def addCodeFileParameters(sLevel, sClass, sSource, sState, txtData, bIsSFC):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = addCodeFileParameters.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn
    bStruct = False

    #--------------------------------------------------------------------------#
    # Create a new cursor object for the SFC parameters:                       #
    #--------------------------------------------------------------------------#
    c = conn.cursor()

    #--------------------------------------------------------------------------#
    # Open the code file for reading:                                          #
    #--------------------------------------------------------------------------#
    sParameterType = ''
    for sBuffer in txtData.split('\n'):
        #----------------------------------------------------------------------#
        # Read the next line in the file:                                      #
        #----------------------------------------------------------------------#
        sBuffer = sBuffer.replace('\t', ' ')
        sBuffer = sBuffer.strip()

        #----------------------------------------------------------------------#
        # Check if the start of each parameter data type:                      #
        #----------------------------------------------------------------------#
        if (sBuffer == 'VAR_INPUT'):
            sParameterType = 'VAR_INPUT'
            iParameterOrder = 1
            sOperation = 'write'

        elif (sBuffer == 'VAR_OUTPUT'):
            sParameterType = 'VAR_OUTPUT'
            iParameterOrder = 2
            sOperation = 'read'

        elif (sBuffer == 'VAR_IN_OUT'):
            sParameterType = 'VAR_IN_OUT'
            iParameterOrder = 3
            sOperation = 'write'

        elif (sBuffer == 'VAR'):
            sParameterType = 'VAR'
            iParameterOrder = 4
            sOperation = 'read'

        elif (sBuffer == 'BEGIN'):
            sParameterType = 'DONE'

        #----------------------------------------------------------------------#
        # Check if not reached the parameter definition section:               #
        #----------------------------------------------------------------------#
        if (sParameterType is None):
            pass

        #----------------------------------------------------------------------#
        # Check if all parameter data types processed:                         #
        #----------------------------------------------------------------------#
        elif (sParameterType.upper() == 'DONE'):
            #------------------------------------------------------------------#
            # Don't need the rest of the file. Exit the loop:                  #
            #------------------------------------------------------------------#
            break

        #----------------------------------------------------------------------#
        # Check if a structure variable. Ignore those:                         #
        #----------------------------------------------------------------------#
        elif (sBuffer.find('Struct') >= 0):
            bStruct = True

        #----------------------------------------------------------------------#
        # Check if the structure variable is finished:                         #
        #----------------------------------------------------------------------#
        elif (sBuffer.find('END_STRUCT') >= 0):
            bStruct = False

        #----------------------------------------------------------------------#
        # Ignore structure variables:                                          #
        #----------------------------------------------------------------------#
        elif (bStruct):
            pass

        #----------------------------------------------------------------------#
        # Check if a a user defined parameter:                                 #
        #----------------------------------------------------------------------#
        elif (sBuffer[:1] == '_'):
            #------------------------------------------------------------------#
            # Get the parameter data based on the definition code, for example:#
            # _flowpath_WFI :BOOL ;   //flowpath_WFI/CS_WFI:                   #
            #------------------------------------------------------------------#
            sParameter = sBuffer[:sBuffer.find(':') - 1]
            sParameter = sParameter.strip()
            sParameterBlock = sParameter.upper()[1:]
            sParameterDataType = sBuffer[sBuffer.find(':') + 1:sBuffer.find(';')]
            sParameterDataType = sParameterDataType.strip()
            sParameterDescription = sBuffer[-len(sBuffer) + sBuffer.find('/') + 2:]
            sParameterDescription = sParameterDescription.strip()

            #------------------------------------------------------------------#
            # Set the code data type based on the actual data type:            #
            #------------------------------------------------------------------#
            if (sParameterDataType.upper() == 'BOOL'):
                sValue = 'FALSE'

            elif (sParameterDataType.upper() == 'INT'):
                sValue = '0'

            elif (sParameterDataType.upper() == 'REAL'):
                sValue = '0.0'

            elif (sParameterDataType.upper() == 'TIME'):
                sValue = 'T#0s'

            #------------------------------------------------------------------#
            # Add the parameter to the global list:                            #
            #------------------------------------------------------------------#
            addParameterData(sLevel, sClass, sSource, sState, sParameterType, iParameterOrder,
                             sParameter, '', sParameterBlock, sParameterDataType,
                             sValue, sParameterDescription, '', '', bIsSFC, sOperation)

#------------------------------------------------------------------------------#
# Function: addParameterData                                                   #
#                                                                              #
# Description:                                                                 #
# Adds the parameter to the internal table pGlobal.                            #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sLevel                The level of the parameter object.                     #
# sClass                The class to process the instances for.                #
# sSource               The source SFC file name of the block class module.    #
# sState                The parent block state name.                           #
# sParameterType        The VAR type of the parameter.                         #
# iParameterOrder       The order of the parameter in the output code file.    #
# sParameter            The parameter name.                                    #
# sChildParameterClass  The parameter class.                                   #
# sParameterBlock       The capitalised parameter name in block letters.       #
# sParameterDataType    The primitive data type of the parameter.              #
# sValue                The parameter value.                                   #
# sParameterDescription The description of the parameter.                      #
# sChildParameterAlias  Any child device alias.                                #
# sChildParameterAttribute  Any child device attribute.                        #
# bIsSFC                TRUE if an SFC parameter.                              #
# sOperation            The read or write operation.                           #
#------------------------------------------------------------------------------#
def addParameterData(sLevel, sClass, sSource, sState,
                     sParameterType, iParameterOrder,
                     sParameter, sChildParameterClass,
                     sParameterBlock, sParameterDataType,
                     sValue, sParameterDescription, sChildParameterAlias,
                     sChildParameterAttribute, bIsSFC, sOperation):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = addParameterData.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn
    global iEventConfirmNo
    global iEventConfirmYes
    global iEventPrompt
    global iEventLogMsg
    global iEventLogReal
    global iEventLogTime
    global iEventDataReal
    global iEventDataTime
    global iSync

    #--------------------------------------------------------------------------#
    # Create a new cursor object for the parameters:                           #
    #--------------------------------------------------------------------------#
    c = conn.cursor()
    c1 = conn.cursor()

    #--------------------------------------------------------------------------#
    # Initialise granchild parameters:                                         #
    #--------------------------------------------------------------------------#
    bIsGrandchild = False
    sGrandchildParameterClass = ''
    sGrandchildParameterAlias = ''
    sGrandchildParameterAttribute = ''

    #--------------------------------------------------------------------------#
    # Check if the parameter is a writeable calling parameter:                 #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.checkIfClassParameter]
        c.execute(query, (sClass, sParameterBlock))
        data = c.fetchone()
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.checkIfClassParameter, query, sClass + ', ' + sParameterBlock)

    #--------------------------------------------------------------------------#
    # Calling parameter if exists:                                             #
    #--------------------------------------------------------------------------#
    if (data is not None):
        sOperation = data['parameterOperation']

    #--------------------------------------------------------------------------#
    # Check if the parameter is a child device:                                #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.checkIfChildParameter]
        c.execute(query, (sClass, sParameterBlock))
        data = c.fetchone()
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.checkIfChildParameter, query, sClass + ', ' + sParameterBlock + '%')

    #--------------------------------------------------------------------------#
    # Child device if exists as a child alias:                                 #
    #--------------------------------------------------------------------------#
    iChildIndex = 0
    if (data is None):
        bIsChild = False
    else:
        #----------------------------------------------------------------------#
        # Set the child parameter alias and attribute:                         #
        #----------------------------------------------------------------------#
        bIsChild = True
        sChildParameterClass = data['childAliasClass']
        if (len(sChildParameterAlias) == 0):
            sChildParameterAlias = data['childParameterAlias']
#            sChildParameterAlias = sChildParameterAlias[1:]
            sChildParameterAlias = sChildParameterAlias.upper()
            sChildParameterAttribute = sParameter[len(sChildParameterAlias) + 2:]
            sChildParameterAttribute = sChildParameterAttribute.upper()

        #----------------------------------------------------------------------#
        # Get the child index value from the child values list:                #
        #----------------------------------------------------------------------#
        try:
            query = cgSQL.sql[cgSQL.sqlCode.getChildIndex]
            c.execute(query, (sSource, sChildParameterAlias))
            data = c.fetchone()
            if (data is None):
                iChildIndex = 0
            else:
                iChildIndex = data['childIndex']
        except:
            errorHandler(errProc, errorCode.cannotQuery,
                         cgSQL.sqlCode.getChildIndex, query, sSource + ', ' + sChildParameterAlias + '%')

        #----------------------------------------------------------------------#
        # Check if the child parameter itself is a grandchild device:          #
        #----------------------------------------------------------------------#
        try:
            query = cgSQL.sql[cgSQL.sqlCode.checkIfChildParameter]
            c.execute(query, (sChildParameterClass, sChildParameterAttribute))
            data = c.fetchone()
        except:
            errorHandler(errProc, errorCode.cannotQuery,
                         cgSQL.sqlCode.checkIfChildParameter, query, sChildParameterClass + ', ' + sChildParameterAttribute)

        #----------------------------------------------------------------------#
        # Check if a grandchild was found:                                     #
        #----------------------------------------------------------------------#
        if (data is None):
            bIsGrandchild = False
        else:
            bIsGrandchild = True
            sGrandchildParameterClass = data['childAliasClass']
            sGrandchildParameterAlias = data['childParameterAlias']
            sGrandchildParameterAlias = sGrandchildParameterAlias.upper()
            sGrandchildParameterAttribute = sChildParameterAttribute[len(sGrandchildParameterAlias) + 1:]
            sGrandchildParameterAttribute = sGrandchildParameterAttribute.upper()

    #--------------------------------------------------------------------------#
    # Check if a calling parameter:                                            #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.checkIfCallingParameter]
        c.execute(query, (sClass, sParameterBlock))
        data = c.fetchone()
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.checkIfCallingParameter, query, sClass + ', ' + sParameterBlock + '%')

    #--------------------------------------------------------------------------#
    # Selection device if exists:                                              #
    #--------------------------------------------------------------------------#
    if (data is None):
        bIsCalling = False
    else:
        bIsCalling = True

    #--------------------------------------------------------------------------#
    # Check if the parameter is a child selection:                             #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.checkIfSelectionParameter]
        c.execute(query, (sClass, sParameterBlock))
        data = c.fetchone()
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.checkIfSelectionParameter, query, sClass + ', ' + sParameterBlock + '%')

    #--------------------------------------------------------------------------#
    # Selection device if exists:                                              #
    #--------------------------------------------------------------------------#
    if (data is None):
        bIsSelection = False
    else:
        bIsSelection = True
        sChildParameterClass = data['childClass']
        if (len(sChildParameterAlias) == 0):
            sChildParameterAlias = data['linkParameterAlias']
            sChildParameterAlias = sChildParameterAlias.upper()
            sChildParameterAttribute = sParameter[len(sChildParameterAlias) + 2:]
            sChildParameterAttribute = sChildParameterAttribute.upper()

    #--------------------------------------------------------------------------#
    # Check if the parameter is a linked device, i.e. another device           #
    # parameter attribute other than a child device:                           #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.checkIfLinkParameter]
        c.execute(query, (sClass, sParameterBlock))
        data = c.fetchone()
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.checkIfLinkParameter, query, sClass + ', ' + sParameterBlock + '%')

    #--------------------------------------------------------------------------#
    # Link device if exists as a child alias for another class:                #
    #--------------------------------------------------------------------------#
    if (data is None or bIsChild or bIsSelection):
        bIsLink = False
    else:
        bIsLink = True
        sChildParameterClass = data['childAliasClass']
        if (len(sChildParameterAlias) == 0):
            sChildParameterAlias = data['childParameterAlias']
#            sChildParameterAlias = sChildParameterAlias[1:]
            sChildParameterAlias = sChildParameterAlias.upper()
            sChildParameterAttribute = sParameter[len(sChildParameterAlias) + 2:]
            sChildParameterAttribute = sChildParameterAttribute.upper()

    #--------------------------------------------------------------------------#
    # Check if the child attribute is in the mode and command structure,       #
    # regardless of whether in the read or write block:                        #
    #--------------------------------------------------------------------------#
    bIsMC = False
    if (sChildParameterAttribute == 'ME'or
        sChildParameterAttribute == 'CMD_SAFE' or
        sChildParameterAttribute == 'STATE' or
        sChildParameterAttribute == 'INTERLOCK' or
        sChildParameterAttribute == 'CRIL' or
        sChildParameterAttribute == 'NCRIL' or
        sChildParameterAttribute == 'isRead' or
        sChildParameterAttribute == 'modeAUTO' or
        sChildParameterAttribute == 'modeMANUAL' or
        sChildParameterAttribute == 'modeOOS' or
        sChildParameterAttribute == 'isAvailable' or
        sChildParameterAttribute == 'isBatch'):
        bIsMC = True
        sOperation = 'read'

    elif (sChildParameterAttribute == 'CMD' or
        sChildParameterAttribute == 'MODE' or
        sChildParameterAttribute == 'HYGIENE' or
        sChildParameterAttribute == 'OWNER' or
        sChildParameterAttribute == 'RECIPE' or
        sChildParameterAttribute == 'SERIALNUM' or
        sChildParameterAttribute == 'SUBS' or
        sChildParameterAttribute == 'MAN_OVERRIDE'):
        bIsMC = True
        sOperation = 'write'

    #--------------------------------------------------------------------------#
    # Change the other known attribute types:                                  #
    #--------------------------------------------------------------------------#
    if (sChildParameterAttribute == 'PV' or
        sChildParameterAttribute == 'STATE_PEER'):
        sOperation = 'read'

    #--------------------------------------------------------------------------#
    # Check if the parameter is an SFC event parameter of either Prompt,       #
    # Confirm or Log:                                                          #
    #--------------------------------------------------------------------------#
    idx = 1
    isEventConfirmNo = False
    isEventConfirmYes = False
    isEventPrompt = False
    isEventLogMsg = False
    isEventLogReal = False
    isEventLogTime = False
    isEventDataReal = False
    isEventDataTime = False
    isSync = False
    if (sParameterBlock[:7] == 'PROMPT_'):
        if (sParameterBlock.find('CONFIRM_NO') >= 0):
            isEventConfirmNo = True
            idx = iEventConfirmNo
            iEventConfirmNo = iEventConfirmNo + 1

        elif (sParameterBlock.find('CONFIRM_YES') >= 0):
            isEventConfirmYes = True
            idx = iEventConfirmYes
            iEventConfirmYes = iEventConfirmYes + 1
        else:
            isEventPrompt = True
            idx = iEventPrompt
            iEventPrompt = iEventPrompt + 1

    elif (sParameterBlock[:7] == 'LOG_MSG'):
        isEventLogMsg = True
        idx = iEventLogMsg
        iEventLogMsg = iEventLogMsg + 1

    elif (sParameterBlock[:8] == 'LOG_REAL'):
        isEventLogReal = True
        idx = iEventLogReal
        iEventLogReal = iEventLogReal + 1

    elif (sParameterBlock[:5] == 'REAL_'):
        isEventDataReal = True
        idx = iEventDataReal
        iEventDataReal = iEventDataReal + 1

    elif (sParameterBlock[:8] == 'LOG_TIME'):
        isEventLogTime = True
        idx = iEventLogTime
        iEventLogTime = iEventLogTime + 1

    elif (sParameterBlock[:5] == 'TIME_'):
        isEventDataTime = True
        idx = iEventDataTime
        iEventDataTime = iEventDataTime + 1

    elif (sParameterBlock[:5] == 'SYNC_'):
        isSync = True
        idx = iSync
        iSync = iSync + 1
#        if (sParameterBlock[5:10] == 'WRITE'):
#            sOperation = 'write'
#        else:
#            sOperation = 'read'

    #--------------------------------------------------------------------------#
    # Check if a recipe parameter:                                             #
    #--------------------------------------------------------------------------#
    if (sParameterBlock[:2] == 'R_'):
        bIsRecipe = True
        sRecipeClass = ''
        sOperation = 'write'
    else:
        bIsRecipe= False
        sRecipeClass = ''

    #--------------------------------------------------------------------------#
    # Deferred parameter cannot be linked parameters:                          #
    #--------------------------------------------------------------------------#
    if (sSource == 'DEFER'):
        bIsLink = False

    #--------------------------------------------------------------------------#
    # Check if the parameter already exists:                                   #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.checkGlobalParameterExists]
        c.execute(query, (sClass, sParameterBlock))
        data = c.fetchone()
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.checkGlobalParameterExists,
                     query, sClass + ', ' + sParameterBlock)

    #--------------------------------------------------------------------------#
    # Add the parameter to the descendants parameter table if it does not      #
    # already exist. If an SFC parameter just add it:                          #
    #--------------------------------------------------------------------------#
    if (bIsSFC or data is None):
        #----------------------------------------------------------------------#
        # Set the default parameter value if it doesn't have one already:      #
        #----------------------------------------------------------------------#
#        if (len(sValue) > 0):
#            pass
#
#        elif (sParameterDataType.upper() == 'BOOL'):
#            sValue = 'FALSE'
#
#        elif (sParameterDataType.upper() == 'INT'):
#            sValue = '0'
#
#        elif (sParameterDataType.upper() == 'REAL'):
#            sValue = '0.0'
#
#        elif (sParameterDataType.upper() == 'TIME'):
#            sValue = 'T#0s'

        #----------------------------------------------------------------------#
        # Add the parameter to the global parameters table:                    #
        #----------------------------------------------------------------------#
        try:
            query = cgSQL.sql[cgSQL.sqlCode.insertGlobalParameters]
            c.execute(query, (sLevel, sClass, sSource, sState, sParameterType, iParameterOrder,
                               sParameter, sParameterBlock,
                               sChildParameterAlias, sChildParameterClass, sChildParameterAttribute,
                               sGrandchildParameterAlias, sGrandchildParameterClass, sGrandchildParameterAttribute,
                               sParameterDataType, sValue, sParameterDescription, sOperation,
                               bIsSFC, bIsChild, bIsGrandchild, bIsLink, bIsSelection, bIsCalling,
                               bIsMC, iChildIndex,
                               bIsRecipe, sRecipeClass, idx,
                               isEventConfirmNo, isEventConfirmYes, isEventPrompt, isEventLogMsg,
                               isEventLogReal, isEventLogTime,
                               isEventDataReal, isEventDataTime, isSync))
        except:
            errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.insertGlobalParameters, query,
                         sLevel + ', ' + sClass + ', ' +
                         sSource + ', ' + sState + ', ' + sParameterType + ', ' +
                         str(iParameterOrder) + ', ' + sParameter + ', ' +
                         sParameterBlock + ', ' +
                         sChildParameterAlias + ', ' + sChildParameterClass + ', ' +
                         sChildParameterAttribute + ', ' + sParameterDataType + ', ' +
                         sGrandchildParameterAlias + ', ' + sGrandchildParameterClass + ', ' +
                         sGrandchildParameterAttribute + ', ' + str(sValue) + ', ' +
                         sParameterDescription + ', ' + sOperation + ', ' +
                         str(bIsSFC) + ', ' +
                         str(bIsChild) + ', ' + str(bIsGrandchild) + ', ' +
                         str(bIsLink) + ', ' + str(bIsSelection) + ', ' +
                         str(bIsCalling) + ', ' +
                         str(bIsMC) + ', ' + str(iChildIndex) + ', ' +
                         str(bIsRecipe) + ', ' + sRecipeClass + ', ' +
                         str(idx) + ', ' +
                         str(isEventConfirmNo) + ', ' + str(isEventConfirmYes) + ', ' +
                         str(isEventPrompt) + ', ' + str(isEventLogMsg) + ', ' +
                         str(isEventLogReal) + ', ' + str(isEventLogTime) + ', ' +
                         str(isEventDataReal) + ', ' + str(isEventDataTime) + ', ' +
                         str(isSync))

    else:
        #----------------------------------------------------------------------#
        # The parameter exists. Update the read write status with the new      #
        # value to override any SFC value which may be wrong if VAR_IN_OUT:    #
        #----------------------------------------------------------------------#
        try:
            query = cgSQL.sql[cgSQL.sqlCode.updateParameterOperation]
            c.execute(query, (sOperation, sValue, sClass, sParameterBlock))
        except:
            errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.updateParameterOperation, query,
                         sOperation + ', ' + sClass + ', ' + sParameterBlock)

    #--------------------------------------------------------------------------#
    # Commit the changes the database:                                         #
    #--------------------------------------------------------------------------#
    try:
        conn.commit()
    except:
        errorHandler(errProc, errorCode.cannotCommit, query)

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
main()
