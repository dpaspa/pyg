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
gClass = ''
gClassDescription = ''
gInstance = ''
gILTable = ''
gParent = ''
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
    cannotGetSQL                       = -5
    cannotQuery                        = -6
    filenotExist                       = -7
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
    unknownAttribute                   = -39

errorMessage = {
    errorCode.cannotCommit             : 'Cannot commit changes to sqlite database',
    errorCode.cannotConvertWorkbook    : 'Cannot convert workbook @1 from xlsx to sqlite db @2',
    errorCode.cannotConnectDB          : 'Cannot connect to sqlite database @1',
    errorCode.cannotCreateTable        : 'Cannot insert table @1 into sqlite database',
    errorCode.cannotGetSQL             : 'Cannot retrieve SQL query expression for attribute @1',
    errorCode.cannotQuery              : 'Query element @1 cannot execute using SQL expression @2 using parameters @3',
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
    global pathOutput
    global pathTemplates
    global gParent

    #--------------------------------------------------------------------------#
    # Get the input code template path:                                        #
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
    # Create the SFC Parameters table:                                         #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.createParameterSFC]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotCreateTable, query)

    #--------------------------------------------------------------------------#
    # Get the progress weighting:                                              #
    #--------------------------------------------------------------------------#
    pbChunks = 27.0

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
    processLevel(sParent, 'IL', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected parent:                     #
    #--------------------------------------------------------------------------#
    processLevel(sParent, 'CM', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected parent:                     #
    #--------------------------------------------------------------------------#
    processLevel(sParent, 'EM', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected parent:                     #
    #--------------------------------------------------------------------------#
    processLevel(sParent, 'UN', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected parent:                     #
    #--------------------------------------------------------------------------#
    processLevel(sParent, 'PC', 100 * 4 / pbChunks)

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
        # Create the instance FB (ifb) of the class:                           #
        #----------------------------------------------------------------------#
        sPrefix = 'ifb'
        createClass(sLevel, sParent, sClass, row['Description'],
                    sPrefix, row['inheritsInstance'], row['nameInstance'], True)

        #----------------------------------------------------------------------#
        # Update the SFC parameters in the database if not interlocks:         #
        #----------------------------------------------------------------------#
        if (sLevel == 'EM' or sLevel == 'UN' or sLevel == 'PC'):
            populateSFCParameters(sClass)

        #----------------------------------------------------------------------#
        # Create the function block class file:                                #
        #----------------------------------------------------------------------#
        sPrefix = 'fb'
        createClass(sLevel, sParent, sClass, row['Description'],
                    sPrefix, row['inheritsClass'], row['nameClass'], True)

        #----------------------------------------------------------------------#
        # Update the progress message:                                         #
        #----------------------------------------------------------------------#
        p.set_description(sParent + ': ' + sClass + ' complete')
        p.refresh()

    #--------------------------------------------------------------------------#
    # Update the progress message:                                             #
    #--------------------------------------------------------------------------#
    p.set_description(sParent + ': Level ' + sLevel + ' complete')
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
        createClass(sLevel, sParent, '', '', '', row['File'], row['File'], False)

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
# sNameOutput           The output file name after the prefix.                 #
# bOne                  Create output file just the specified class.           #
#------------------------------------------------------------------------------#
def createClass(sLevel, sParent, sClass, sClassDescription,
                sPrefix, sTemplate, sNameOutput, bOne):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = createClass.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn
    global gILTable
    global pathOutput
    global pathTemplates

    #--------------------------------------------------------------------------#
    # Get a connection to the database:                                        #
    #--------------------------------------------------------------------------#
    c = conn.cursor()

    #--------------------------------------------------------------------------#
    # Get the list of instances for the template:                              #
    #--------------------------------------------------------------------------#
    if (sClass == 'IL'):
        gILTable = sNameOutput
        if (gILTable == 'CRIL' or gILTable == 'IL'):
            try:
                query = cgSQL.sql[cgSQL.sqlCode.CRIL]
                c.execute(query)
            except:
                errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.CRIL)

        elif (gILTable == 'NCRIL'):
            try:
                query = cgSQL.sql[cgSQL.sqlCode.NCRIL]
                c.execute(query)
            except:
                errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.NCRIL)

    elif (bOne):
        try:
            query = cgSQL.sql[cgSQL.sqlCode.createClassOne]
            c.execute(query, ('RM', sClass, sParent, sParent, sParent, sParent, sParent))
        except:
            errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.createClassOne, query, 'RM' + ', ' + sClass + ', ' + sParent + ', ' + sParent + ', ' + sParent + ', ' + sParent)

    elif (sLevel == 'PG' or sLevel == 'BLK'):
        try:
            query = cgSQL.sql[cgSQL.sqlCode.createClassNone]
            c.execute(query)
        except:
            errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.createClassNone, query, 'no parameters')
    else:
        try:
            query = cgSQL.sql[cgSQL.sqlCode.createClassAll]
            c.execute(query, (sLevel.upper(),))
        except:
            errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.createClassAll, query, sLevel.upper())

    #--------------------------------------------------------------------------#
    # Check to see if the cursor contains any data:                            #
    #--------------------------------------------------------------------------#
    data = c.fetchall()
    if (len(data) != 0):
        #----------------------------------------------------------------------#
        # Get the code template file name and check that it exists:            #
        #----------------------------------------------------------------------#
        sFileNameIn = pathTemplates + '/' + sPrefix + sTemplate + '.awl'
        logging.info(sFileNameIn)
        if not os.path.exists(sFileNameIn):
            errorHandler(errProc, errorCode.filenotExist, sFileNameIn)

        #----------------------------------------------------------------------#
        # Open the template file for reading and parse each line:              #
        #----------------------------------------------------------------------#
        file = open(sFileNameIn, 'r')
        bSkipFirstLine = False
        bTemplateBegin = False
        bTemplateEnd = False
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
                if (sBuffer.find('@@TEMPLATE_BEGIN@@') >= 0):
                    bTemplateBegin = True
                    bSkipFirstLine = True

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
                    if (bSkipFirstLine):
                        bSkipFirstLine = False
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
        # Write the output instance file:                                      #
        #----------------------------------------------------------------------#
        if (bOne or sClass == 'IL'):
            sFileNameOut = pathOutput + '/' + sPrefix + sNameOutput + '.awl'
        else:
            sFileNameOut = pathOutput + '/' + sTemplate + '.awl'
        file = open(sFileNameOut, 'w')
        file.write(txtData)
        file.close()

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
    global gClass
    global gClassDescription
    global gInstance
    global gParent

    #--------------------------------------------------------------------------#
    # Enter a loop to process each instance:                                   #
    #--------------------------------------------------------------------------#
    iRow = 0
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
            if row[fld]:
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

                elif (fld.upper() == 'INSTANCE' or fld.upper() == 'TARGET'):
                    sInstance = row[fld]
                    gInstance = sInstance

        #----------------------------------------------------------------------#
        # Check if there are child attribute aliases in the template:          #
        #----------------------------------------------------------------------#
        if (txtInstance.find('ATTR_BEGIN') >= 0):
            #------------------------------------------------------------------#
            # Process the attribute data:                                      #
            #------------------------------------------------------------------#
            txtInstance = insertAttributeData(sClass, sInstance, txtInstance, 0)

            #------------------------------------------------------------------#
            # Replace any counters:                                            #
            #------------------------------------------------------------------#
            txtInstance = replaceCounter(iRow, txtInstance)
            iRow = iRow + 1

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
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn
    global gClass
    global gInstance
    global gParent
    global gSelectParameter
    global gSelectSelection
    global gSFC
    global gState

    #--------------------------------------------------------------------------#
    # Process all of the attributes in the template:                           #
    #--------------------------------------------------------------------------#
    iRow = 0
    iCounterBase = 0
    while (txtInstance.find('@@ATTR_BEGIN|') >= 0):
        #----------------------------------------------------------------------#
        # Get the attribute name from the template. It must be enclosed in     #
        # the format:                                                          #
        #   @@ATTR_BEGIN|<attr>@@                                              #
        #   @@ATTR_END|<attr>@@                                                #
        #----------------------------------------------------------------------#
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
            iTagAttrEnd = txtInstance.find('@@ATTR_END|' + sTemplateAttrName)
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
            if (ord(txtTemplate[-2:-1]) == 13):
                txtTemplate = txtTemplate[2:-1]
            else:
                txtTemplate = txtTemplate[2:]

            #------------------------------------------------------------------#
            # Get any Default template definition tags:                        #
            #------------------------------------------------------------------#
            iDefaultBegin = txtTemplate.find('@@ATTR_DEFAULT_BEGIN@@')
            iDefaultEnd = txtTemplate.find('@@ATTR_DEFAULT_END@@')

            #------------------------------------------------------------------#
            # Set the query based on the attribute name:                       #
            #------------------------------------------------------------------#
            parms = []
            qparms = []
            try:
                query = cgSQL.sql[cgSQL.sqlCode[sTemplateAttrName]]
                parms = cgSQL.prm[cgSQL.sqlCode[sTemplateAttrName]]
            except:
                errorHandler(errProc, errorCode.cannotGetSQL, sTemplateAttrName)

            #------------------------------------------------------------------#
            # Copy the list locally and replace the parameters with their      #
            # current global values:                                           #
            #------------------------------------------------------------------#
            qparms = list(parms)
            for i in range(len(qparms)):
                if (qparms[i] == 'gClass'):
                    qparms[i] = gClass
                elif (qparms[i] == 'gILTable'):
                    qparms[i] = gILTable
                elif (qparms[i] == 'gInstance'):
                    qparms[i] = gInstance
                elif (qparms[i] == 'gParent'):
                    qparms[i] = gParent
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

            #------------------------------------------------------------------#
            # Query the sqlite database:                                       #
            #------------------------------------------------------------------#
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
                             cgSQL.sqlCode[sTemplateAttrName], query, s)

            #------------------------------------------------------------------#
            # Check to see if the cursor contains any data:                    #
            #------------------------------------------------------------------#
            data = c.fetchall()
            if (len(data) == 0):
                #--------------------------------------------------------------#
                # No data so leave any default value:                          #
                #--------------------------------------------------------------#
                if (iDefaultBegin >= 0):
                    txtRecordData = txtTemplate[iDefaultBegin + 22:iDefaultEnd]
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
                    txtTemplate = txtTemplate[:iDefaultBegin] + txtTemplate[iDefaultEnd + 20:]

                #--------------------------------------------------------------#
                # Enter a loop to replace the attribute field names:           #
                #--------------------------------------------------------------#
                for row in data:
                    #----------------------------------------------------------#
                    # Enter a loop to process all of the fields in the         #
                    # instance record:                                         #
                    #----------------------------------------------------------#
                    txtRecord = txtTemplate
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
                            txtRecord = txtRecord.replace('@@' + fld.upper() + '@@', sValue)
                            if (fld.upper() == 'CLASS'):
                                gClass = sValue

                            elif (fld.upper() == 'INSTANCE' or fld.upper() == 'TARGET'):
                                gInstance = sValue

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
                    txtRecord = replaceCounter(iRow, txtRecord)
                    iRow = iRow + 1

                    #----------------------------------------------------------#
                    # Build the attribute record string:                       #
                    #----------------------------------------------------------#
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
            # Replace any maximum counter value:                               #
            #------------------------------------------------------------------#
            txtInstance = txtInstance.replace('@@COUNTERMAX@@', str(iRow + iCounterBase))

    #--------------------------------------------------------------------------#
    # Return the template now it is filled with instance data:                 #
    #--------------------------------------------------------------------------#
    if (rl > 0 and len(txtInstance) > 1 and ord(txtInstance[-1:]) == 13):
        txtInstance = txtInstance[:-1]
        if (len(txtInstance) > 1 and ord(txtInstance[-1:]) == 13):
            txtInstance = txtInstance[:-1]
    return txtInstance

#------------------------------------------------------------------------------#
# Function: replaceCounter                                                     #
#                                                                              #
# Description:                                                                 #
# Sets any default parameter values.                                           #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# iRecordCount          The record count number.                               #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtRecord             The template text.                                     #
#------------------------------------------------------------------------------#
def replaceCounter(iRecordCount, txtRecord):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = replaceCounter.__name__

    #--------------------------------------------------------------------------#
    # Check if any counter placeholders:                                       #
    #--------------------------------------------------------------------------#
    if (txtRecord.find('@@COUNTER') >= 0):
        #----------------------------------------------------------------------#
        # Check if a counter base starting value defined:                      #
        #----------------------------------------------------------------------#
        iCounterBase = 0
        if (txtRecord.find('@@COUNTER|') >= 0):
            #------------------------------------------------------------------#
            # Get the counter base starting value:                             #
            #------------------------------------------------------------------#
            iCounterBegin = txtRecord.find('@@COUNTER|')
            iCounterEnd = txtRecord.find('@@', iCounterBegin + 10)
            sCounterBase = txtRecord[iCounterBegin + 10:iCounterEnd]

            #------------------------------------------------------------------#
            # Check if a numeric starting value:                               #
            #------------------------------------------------------------------#
            if (isnumeric(sCounterBase)):
                iCounterBase = int(sCounterBase)
                txtRecord = txtRecord.replace('@@COUNTER|' + sCounterBase + '@@', str(iRecordCount + iCounterBase))
            else:
                #--------------------------------------------------------------#
                # Invalid default parameter value:                             #
                #--------------------------------------------------------------#
                errorHandler(errProc, errorCode.invalidCounter, sCounterBase)

        #----------------------------------------------------------------------#
        # Replace any additional counter placeholders:                         #
        #----------------------------------------------------------------------#
        txtRecord = txtRecord.replace('@@COUNTER|' + sCounterBase + '@@', str(iRecordCount + iCounterBase))
        txtRecord = txtRecord.replace('@@COUNTER@@', str(iRecordCount + iCounterBase))
        txtRecord = txtRecord.replace('@@COUNTERNEXT@@', str(iRecordCount + iCounterBase + 1))

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
        c.execute(query)
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

        elif (row['Default'] is None):
            errorHandler(errProc, errorCode.invalidDefaultData, sParent)
        else:
            p = row['Parameter']
            r = row['Default']
            old = '@@' + p.upper() + '@@'
            new = '{:10.1f}'.format(r)
            txtInstance = txtInstance.replace(old, new)

    #--------------------------------------------------------------------------#
    # Return the template now it is filled with default parameter data:        #
    #--------------------------------------------------------------------------#
    return txtInstance

#------------------------------------------------------------------------------#
# Function: populateSFCParameters                                              #
#                                                                              #
# Description:                                                                 #
# Updates the internal table tblParameter_SFC with SFC parameters from the     #
# Visio generated sfc awl files for each SFC.                                  #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sClass                The class to process the instances for.                #
#------------------------------------------------------------------------------#
def populateSFCParameters(sClass):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = populateSFCParameters.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the list of running substates for the class:                         #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.populateSFCParmsSubstate]
        c.execute(query, (sClass, 'NONE'))
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.populateSFCParmsSubstate, query, sClass + ', ' + 'NONE')

    #--------------------------------------------------------------------------#
    # Create a new cursor object for the SFC parameters:                       #
    #--------------------------------------------------------------------------#
    c1 = conn.cursor()

    #--------------------------------------------------------------------------#
    # Process each row in the list of classes:                                 #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Check if the FB template file for the SFC does not exist. It must be #
        # generated from Visio:                                                #
        #----------------------------------------------------------------------#
        sSFC = row['SFC']
        sFileNameIn = pathTemplates + '/sfc/fb' + sSFC + '.AWL'
        logging.info(sFileNameIn)
        if not os.path.exists(sFileNameIn):
            errorHandler(errProc, errorCode.filenotExist, sFileNameIn)

        #----------------------------------------------------------------------#
        # Open the SFC file for reading:                                       #
        #----------------------------------------------------------------------#
        sParameterType = ''
        file = open(sFileNameIn, 'r')
        for sBuffer in file:
            #------------------------------------------------------------------#
            # Read the next line in the file:                                  #
            #------------------------------------------------------------------#
            sBuffer = sBuffer.replace('\t', ' ')
            sBuffer = sBuffer.strip()

            #------------------------------------------------------------------#
            # Check if the start of each parameter data type:                  #
            #------------------------------------------------------------------#
            if (sBuffer == 'VAR_INPUT'):
                sParameterType = 'VAR_INPUT'

            elif (sBuffer == 'VAR_OUTPUT'):
                sParameterType = 'VAR_OUTPUT'

            elif (sBuffer == 'VAR_IN_OUT'):
                sParameterType = 'VAR_IN_OUT'

            elif (sBuffer == 'VAR'):
                sParameterType = 'VAR'

            elif (sBuffer == 'BEGIN'):
                sParameterType = 'DONE'

            #------------------------------------------------------------------#
            # Check if not reached the parameter definition                    #
            # section:                                                         #
            #------------------------------------------------------------------#
            if (sParameterType is None):
                pass

            #------------------------------------------------------------------#
            # Check if all parameter data types processed:                     #
            #------------------------------------------------------------------#
            elif (sParameterType.upper() == 'DONE'):
                #--------------------------------------------------------------#
                # Don't need the rest of the file. Exit the loop:              #
                #--------------------------------------------------------------#
                break

            #------------------------------------------------------------------#
            # Check if a a user defined sequence parameter:                    #
            #------------------------------------------------------------------#
            elif (sBuffer[:1] == '_'):
                #--------------------------------------------------------------#
                # Get the parameter data based on the definition code,         #
                # for example...                                               #
                # _flowpath_WFI :BOOL ;   //flowpath_WFI/CS_WFI:               #
                #--------------------------------------------------------------#
                sParameter = sBuffer[:sBuffer.find(' ')]
                sParameterBlock = sParameter.upper()[1:]
                sParameterDataType = sBuffer[sBuffer.find(':') + 1:
                                             sBuffer.find(':') + 1 +
                                             sBuffer.find(';', sBuffer.find(':') + 1) - 1 - sBuffer.find(':') - 1]
                sParameterDescription = sBuffer[-len(sBuffer) + sBuffer.find('/') + 2:]

                #--------------------------------------------------------------#
                # Set the code data type based on the actual data type:        #
                #--------------------------------------------------------------#
                if (sParameterDataType.upper() == 'BOOL'):
                    sValue = 'FALSE'

                elif (sParameterDataType.upper() == 'INT'):
                    sValue = '0'

                elif (sParameterDataType.upper() == 'REAL'):
                    sValue = '0.0'

                elif (sParameterDataType.upper() == 'TIME'):
                    sValue = 'T#0ms'

                #--------------------------------------------------------------#
                # Check if the parameter is a child device:                    #
                #--------------------------------------------------------------#
                try:
                    query = cgSQL.sql[cgSQL.sqlCode.populateSFCParmsChild]
                    c1.execute(query, (sClass, sParameter))
                    data = c1.fetchone()
                except:
                    errorHandler(errProc, errorCode.cannotQuery,
                                 cgSQL.sqlCode.populateSFCParmsChild, query, sClass + ', ' + '_' + sParameter + '%')

                if (data is None):
                    bIsChild = False
                else:
                    bIsChild = True

                #--------------------------------------------------------------#
                # Add the parameter to the SFC parameter table:                #
                #--------------------------------------------------------------#
                try:
                    query = cgSQL.sql[cgSQL.sqlCode.populateSFCParmsInsert]
                    c1.execute(query, (sClass, sSFC, sParameterType, sParameter,
                                      sParameterBlock, sParameterDataType,
                                      sValue, sParameterDescription, bIsChild))
                except:
                    errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.populateSFCParmsInsert, query,
                                 sClass + ', ' + sSFC + ', ' + sParameterType + ', ' + sParameter + ', ' +
                                 sParameterBlock + ', ' + sParameterDataType + ', ' +
                                 sValue + ', ' + sParameterDescription + ', ' + bIsChild)

                #--------------------------------------------------------------#
                # Commit the changes the database:                             #
                #--------------------------------------------------------------#
                try:
                    conn.commit()
                except:
                    errorHandler(errProc, errorCode.cannotCommit, query)

        #----------------------------------------------------------------------#
        # Finished with the data import. Close the file:                       #
        #----------------------------------------------------------------------#
        file.close()

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
main()
