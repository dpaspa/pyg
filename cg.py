#------------------------------------------------------------------------------#
#            Copyright 2018 Rieckermann Engineering Operations                 #
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
import logging
import openpyxl
import os.path
import sys
import traceback
from tqdm import trange
from time import sleep
import sqlite3
from xls2db import xls2db
import cgSQL

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
appTitle = 'Code Generator'
appVersion = '1'
parser = argparse.ArgumentParser(description='Generates PLC code from a configuration spreadsheet and set of code templates')
parser.add_argument('-t','--templates', help='Input path of code template files', required=True)
parser.add_argument('-o','--output', help='Output path for the generated code files', required=True)
parser.add_argument('-p','--pcell', help='Process Cell to generate code files for', required=True)
parser.add_argument('-s','--sheet', help='Configuration spreadsheet', required=True)
args = vars(parser.parse_args())

#------------------------------------------------------------------------------#
# Declare global variables:                                                    #
#------------------------------------------------------------------------------#
c = 1
gClass = ''
gInstance = ''
gSelectParameter = ''
gSelectSelection = ''
gSFC = ''
gState = ''
pathOutput = ''
pathTemplates = ''

#------------------------------------------------------------------------------#
# Declare the error handling global variables and procedure:                   #
#------------------------------------------------------------------------------#
iErr = 0
errProc = ''
errParameters = []
def errorHandler(eCode, *args):
    global iErr
    global errParameters

    iErr = eCode
    errParameters = []
    for arg in args:
        errParameters.append(arg)
    reportComplete()

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
    unknownAttribute                   = -38

errorMessage = {
    errorCode.cannotCommit             : 'Cannot commit changes to sqlite database',
    errorCode.cannotConvertWorkbook    : 'Cannot convert workbook @1 from xlsx to sqlite db @2',
    errorCode.cannotConnectDB          : 'Cannot connect to sqlite database @1',
    errorCode.cannotCreateTable        : 'Cannot insert table @1 into sqlite database',
    errorCode.cannotGetSQL             : 'Cannot retrieve SQL query expression for attribute @1',
    errorCode.cannotQuery              : 'Cannot query using SQL expression @1',
    errorCode.filenotExist             : 'Workbook file @1 does not exist.',
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
    global errProc
    errProc = main.__name__
    logging.basicConfig(level=logging.INFO)

    #--------------------------------------------------------------------------#
    # Declare global and local variables:                                      #
    #--------------------------------------------------------------------------#
    global conn
    global pathOutput
    global pathTemplates

    #--------------------------------------------------------------------------#
    # Get the input code template path:                                        #
    #--------------------------------------------------------------------------#
    sPCell = args['pcell']

    #--------------------------------------------------------------------------#
    # Get the input code template path:                                        #
    #--------------------------------------------------------------------------#
    pathTemplates = args['templates']

    #--------------------------------------------------------------------------#
    # Get the output code module path:                                         #
    #--------------------------------------------------------------------------#
    pathOutput = args['output']

    #--------------------------------------------------------------------------#
    # Get the code configuration workbook name and check it exists:            #
    #--------------------------------------------------------------------------#
    wbName = args['sheet']
    if not os.path.exists(wbName):
        errorHandler(errorCode.filenotExist, wbName)

    #--------------------------------------------------------------------------#
    # Delete the sqlite database file if it already exists so it can be        #
    # created anew with refreshed data:                                        #
    #--------------------------------------------------------------------------#
    dbName = 'cg.db'
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
        errorHandler(errorCode.cannotConvertWorkbook, wbName, dbName)

    #--------------------------------------------------------------------------#
    # Connect to the new persistent sqlite database file:                      #
    #--------------------------------------------------------------------------#
    try:
        conn = sqlite3.connect('cg.db')
        conn.row_factory = sqlite3.Row
    except:
        errorHandler(errorCode.cannotConnectDB, 'cg.db')

    #--------------------------------------------------------------------------#
    # Create the SFC Parameters table:                                         #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.createParameterSFC]
        c.execute(query)
    except:
        errorHandler(errorCode.cannotCreateTable, query)

    #--------------------------------------------------------------------------#
    # Get the progress weighting:                                              #
    #--------------------------------------------------------------------------#
    pbChunks = 21.0

    #--------------------------------------------------------------------------#
    # Create the overall program files:                                        #
    #--------------------------------------------------------------------------#
    createProgramFiles(sPCell, 'PG', 100 * 1 / pbChunks)

    #--------------------------------------------------------------------------#
    # Create the remainder of the program block related files:                 #
    #--------------------------------------------------------------------------#
    createProgramFiles(sPCell, 'CM', 100 * 1 / pbChunks)
    createProgramFiles(sPCell, 'EM', 100 * 1 / pbChunks)
    createProgramFiles(sPCell, 'UN', 100 * 1 / pbChunks)
    createProgramFiles(sPCell, 'PC', 100 * 1 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected Process Cell:               #
    #--------------------------------------------------------------------------#
    processLevel(sPCell, 'CM', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected Process Cell:               #
    #--------------------------------------------------------------------------#
    processLevel(sPCell, 'EM', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected Process Cell:               #
    #--------------------------------------------------------------------------#
    processLevel(sPCell, 'UN', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected Process Cell:               #
    #--------------------------------------------------------------------------#
    processLevel(sPCell, 'PC', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Commit the changes to the database if no error and close the connection: #
    #--------------------------------------------------------------------------#
    if (iErr == 0):
        conn.commit()
    conn.close()

    #--------------------------------------------------------------------------#
    # Report completion regardless of error:                                   #
    #--------------------------------------------------------------------------#
    p.set_description('Processing complete')
    p.refresh()
    p.close()
    reportComplete()

#------------------------------------------------------------------------------#
# Function reportComplete                                                      #
#                                                                              #
# Description:                                                                 #
# Reports the completion status of the operation.                              #
#------------------------------------------------------------------------------#
def reportComplete():
    #--------------------------------------------------------------------------#
    # Declare global parameters:                                               #
    #--------------------------------------------------------------------------#
    global iErr
    global errProc
    global errParameters

    #--------------------------------------------------------------------------#
    # Check if successful completion:                                          #
    #--------------------------------------------------------------------------#
    if (iErr == 0):
        #----------------------------------------------------------------------#
        # Output a success message:                                            #
        #----------------------------------------------------------------------#
        print('Congratulations! Operation successful.')
    else:
        #----------------------------------------------------------------------#
        # Get the application specific error message and output the error:     #
        #----------------------------------------------------------------------#
        sMsg = errorMessage[iErr]

        #----------------------------------------------------------------------#
        # Check if there are any error parameters to replace:                  #
        #----------------------------------------------------------------------#
        if (not errParameters is None):
            #------------------------------------------------------------------#
            # Enter a loop to replace each parameter:                          #
            #------------------------------------------------------------------#
            for i in range(0, len(errParameters)):
                sMsg = sMsg.replace('@' + str(i + 1), errParameters[i])

        #----------------------------------------------------------------------#
        # Output the error message and end:                                    #
        #----------------------------------------------------------------------#
        print('\r\n')
        logging.critical(appTitle + ' Version ' + appVersion + '\r\n' + 'ERROR ' +
                         str(iErr) + ' in Procedure ' + "'" + errProc + "'" + '\r\n' + '\r\n' + sMsg)
        print('\r\n')
        print(traceback.format_exception(*sys.exc_info()))
        sys.exit()

#------------------------------------------------------------------------------#
# Function: processLevel                                                       #
#                                                                              #
# Description:                                                                 #
# This processes the selected level for the class.                             #
# for information in an MS Word document.                                      #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sPCell                The process cell to generate code for.                 #
# sLevel                The level to process, either CM, EM, UN or PC.         #
# pbwt                  The % weight of the procedure for the progress bar.    #
#------------------------------------------------------------------------------#
def processLevel(sPCell, sLevel, pbwt):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    global errProc
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
        errorHandler(errorCode.cannotQuery, 'tblClass')

    #--------------------------------------------------------------------------#
    # Get the list of classes:                                                 #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.processLevel]
        c.execute(query, (sLevel.upper(),))
    except:
        errorHandler(errorCode.cannotQuery, 'tblClass')

    #--------------------------------------------------------------------------#
    # Process each row in the list of classes:                                 #
    #--------------------------------------------------------------------------#
    for row in c:
        #------------------------------------------------------------------#
        # Update the progress bar:                                         #
        #------------------------------------------------------------------#
        sClass = row['Class']
        logging.info(sClass)
        pc = pbwt * 1.0 / num
        p.update(pc)
        p.set_description(sClass)
        p.refresh()
        sleep(0.01)

        #----------------------------------------------------------------------#
        # Create the instance FB (ifb) of the class:                           #
        #----------------------------------------------------------------------#
        createOneClass(sPCell, sClass, row['Description'], row['ifb'], 'ifb', '')

        #----------------------------------------------------------------------#
        # Create the instance FCs (ifc) of the class:                          #
        #----------------------------------------------------------------------#
        createOneClass(sPCell, sClass, row['Description'], row['ifc'], 'ifc', '')

        #----------------------------------------------------------------------#
        # Update the SFC parameters in the database:                           #
        #----------------------------------------------------------------------#
        populateSFCParameters(sClass)

        #----------------------------------------------------------------------#
        # Create the block class files:                                        #
        #----------------------------------------------------------------------#
        createOneClass(sPCell, sClass, row['Description'], row['fb'], 'fb', '')

        #----------------------------------------------------------------------#
        # Update the progress message:                                         #
        #----------------------------------------------------------------------#
        p.set_description(sClass + ' complete')
        p.refresh()

    #--------------------------------------------------------------------------#
    # Update the progress message:                                             #
    #--------------------------------------------------------------------------#
    p.set_description('Level ' + sLevel + ' complete')
    p.refresh()

#------------------------------------------------------------------------------#
# Function: createProgramFiles                                                 #
#                                                                              #
# Description:                                                                 #
# Creates the overall program files.                                           #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sPCell                The process cell which owns the instances.             #
# sLevel                The Class level to create.                             #
# pbwt                  The % weight of the procedure for the progress bar.    #
#------------------------------------------------------------------------------#
def createProgramFiles(sPCell, sLevel, pbwt):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    global errProc
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
        errorHandler(errorCode.cannotQuery, query)

    #--------------------------------------------------------------------------#
    # Now get the list of non S88 files:                                       #
    #--------------------------------------------------------------------------#
    try:
        query = cgSQL.sql[cgSQL.sqlCode.createProgramFiles]
        c.execute(query, (sLevel.upper(),))
    except:
        errorHandler(errorCode.cannotQuery, 'tblFile')

    #--------------------------------------------------------------------------#
    # Process each row in the list of files:                                   #
    #--------------------------------------------------------------------------#
    for row in c:
        #------------------------------------------------------------------#
        # Update the progress bar:                                         #
        #------------------------------------------------------------------#
        pc = pbwt * 1.0 / num
        p.update(pc)
        p.set_description(row['File'])
        p.refresh()
        sleep(0.01)

        #----------------------------------------------------------------------#
        # Create the output file from the input awl source:                    #
        #----------------------------------------------------------------------#
        createAllClasses(sPCell, sLevel, row['File'])

    #--------------------------------------------------------------------------#
    # Update the progress message:                                             #
    #--------------------------------------------------------------------------#
    p.set_description(sLevel + ' files complete')
    p.refresh()

#------------------------------------------------------------------------------#
# Function: createAllClasses                                                   #
#                                                                              #
# Description:                                                                 #
# Creates Class based STL files, such as instance FBs (ifb) and instance       #
# FCs (ifc) for all of the class instances of the specified in the Process     #
# Cell.                                                                        #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sPCell                The process cell which owns the instances.             #
# sLevel                The Class level to create.                             #
# sTemplate             The code template file name.                           #
#------------------------------------------------------------------------------#
def createAllClasses(sPCell, sLevel, sTemplate):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    global errProc
    errProc = createAllClasses.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn
    global pathOutput
    global pathTemplates

    #--------------------------------------------------------------------------#
    # Get the code template file name and check that it exists:                #
    #--------------------------------------------------------------------------#
    sFileNameIn = pathTemplates + '/' + sTemplate + '.awl'
    logging.info(sFileNameIn)
    if not os.path.exists(sFileNameIn):
        errorHandler(errorCode.filenotExist, sFileNameIn)

    #--------------------------------------------------------------------------#
    # Get the list of global block classes:                                    #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        if (sLevel == 'PG'):
            query = cgSQL.sql[cgSQL.sqlCode.createAllClasses1]
            c.execute(query)
        else:
            query = cgSQL.sql[cgSQL.sqlCode.createAllClassesAll]
            c.execute(query, (sLevel.upper(),))
    except:
        errorHandler(errorCode.cannotQuery, query)

    #--------------------------------------------------------------------------#
    # Open the template file for reading and parse each line:                  #
    #--------------------------------------------------------------------------#
    file = open(sFileNameIn, 'r')
    bSkipFirstLine = False
    bTemplateBegin = False
    bTemplateEnd = False
    txtData = ''
    txtTemplate = ''
    for sBuffer in file:
        #----------------------------------------------------------------------#
        # Check if a blank line:                                               #
        #----------------------------------------------------------------------#
        if (len(sBuffer) == 0):
            if (bTemplateBegin and not bTemplateEnd):
                txtTemplate = txtTemplate + '\r\n'
            else:
                txtData = txtData + '\r\n'
        else:
            #------------------------------------------------------------------#
            # Check if the start of a new instance template:                   #
            #------------------------------------------------------------------#
            if (sBuffer.find('@@TEMPLATE_BEGIN@@') > 0):
                bTemplateBegin = True
                bSkipFirstLine = True

            #------------------------------------------------------------------#
            # Check if the end of the current instance template:               #
            #------------------------------------------------------------------#
            elif (sBuffer.find('@@TEMPLATE_END@@') > 0):
                bTemplateEnd = True


            #------------------------------------------------------------------#
            # Build the instance template text if within an instance template: #
            #------------------------------------------------------------------#
            if (bTemplateBegin and not bTemplateEnd):
                if (bSkipFirstLine):
                    bSkipFirstLine = False
                else:
                    txtTemplate = txtTemplate + sBuffer# + '\r\n'

            #------------------------------------------------------------------#
            # Check if not in a template:                                      #
            #------------------------------------------------------------------#
            if (not bTemplateBegin):
                #--------------------------------------------------------------#
                # Build the output text with the base file data:               #
                #--------------------------------------------------------------#
                txtData = txtData + sBuffer# + '\r\n'

            #------------------------------------------------------------------#
            # Replace the fields in the instance template if the template is   #
            # finished:                                                        #
            #------------------------------------------------------------------#
            elif (bTemplateBegin and bTemplateEnd):
                txtData = processTemplate(c, txtTemplate, txtData)

            #------------------------------------------------------------------#
            # Reset the instance template flags:                               #
            #------------------------------------------------------------------#
            elif (bTemplateBegin and bTemplateEnd):
                txtTemplate = ''
                bTemplateBegin = False
                bTemplateEnd = False

    #--------------------------------------------------------------------------#
    # Close the input file:                                                    #
    #--------------------------------------------------------------------------#
    file.close()

    #--------------------------------------------------------------------------#
    # Replace any default parameters:                                          #
    #--------------------------------------------------------------------------#
    txtData = defaultParameters(sPCell, txtData)

    #--------------------------------------------------------------------------#
    # Write the output instance file:                                          #
    #--------------------------------------------------------------------------#
    sFileNameOut = pathOutput + '/' + sTemplate + '.awl'
    file = open(sFileNameOut, 'w')
    file.write(txtData)
    file.close()

#------------------------------------------------------------------------------#
# Function: createOneClass                                                     #
#                                                                              #
# Description:                                                                 #
# Creates Class based STL files, such as instance FBs (ifb) and instance       #
# FCs (ifc) for all of the class instances of the specified in the Process     #
# Cell.                                                                        #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sPCell                The process cell which owns the instances.             #
# sClass                The class to process the instances for.                #
# sClassDescription     The class description.                                 #
# sTemplate             The code template file name.                           #
# sOutputPrefix         The output file prefix name.                           #
# sOutputSuffix         The output file suffix name.                           #
#------------------------------------------------------------------------------#
def createOneClass(sPCell, sClass, sClassDescription, sTemplate, sOutputPrefix, sOutputSuffix):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    global errProc
    errProc = createOneClass.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn
    global pathOutput
    global pathTemplates

    #--------------------------------------------------------------------------#
    # Get the code template file name and check that it exists:                #
    #--------------------------------------------------------------------------#
    sFileNameIn = pathTemplates + '/' + sTemplate + '.awl'
    logging.info(sFileNameIn)
    if not os.path.exists(sFileNameIn):
        errorHandler(errorCode.filenotExist, sFileNameIn)

    #--------------------------------------------------------------------------#
    # Get the list of instances:                                               #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.createOneClass]
        c.execute(query, ('RM', sClass, sPCell, sPCell, sPCell))
    except:
        errorHandler(errorCode.cannotQuery, query)

    #--------------------------------------------------------------------------#
    # Open the template file for reading:                                      #
    #--------------------------------------------------------------------------#
    bSkipFirstLine = False
    bTemplateBegin = False
    bTemplateEnd = False
    txtData = ''
    txtTemplate = ''
    file = open(sFileNameIn, 'r')
    for sBuffer in file:
        #----------------------------------------------------------------------#
        # Check if a blank line:                                               #
        #----------------------------------------------------------------------#
        if (len(sBuffer) == 0):
            if (bTemplateBegin and not bTemplateEnd):
                txtTemplate = txtTemplate + '\r\n'
            else:
                txtData = txtData + '\r\n'
        else:
            #------------------------------------------------------------------#
            # Check if the start of a new instance template:                   #
            #------------------------------------------------------------------#
            if (sBuffer.find('@@TEMPLATE_BEGIN@@') >= 0):
                bTemplateBegin = True
                bSkipFirstLine = True

            #------------------------------------------------------------------#
            # Check if the end of the current instance template:               #
            #------------------------------------------------------------------#
            elif (sBuffer.find('@@TEMPLATE_END@@') >= 0):
                bTemplateEnd = True

            #------------------------------------------------------------------#
            # Build the instance template text if within an instance template: #
            #------------------------------------------------------------------#
            if (bTemplateBegin and not bTemplateEnd):
                if (bSkipFirstLine):
                    bSkipFirstLine = False
                else:
                    txtTemplate = txtTemplate + sBuffer# + '\r\n'

            #------------------------------------------------------------------#
            # Check if not in a template:                                      #
            #------------------------------------------------------------------#
            if (not bTemplateBegin):
                #--------------------------------------------------------------#
                # Build the output text with the base file data:               #
                #--------------------------------------------------------------#
                txtData = txtData + sBuffer# + '\r\n'

            #------------------------------------------------------------------#
            # Replace the fields in the instance template if the template is   #
            # finished:                                                        #
            #------------------------------------------------------------------#
            elif (bTemplateBegin and bTemplateEnd):
                txtData = processTemplate(c, txtTemplate, txtData)

            #------------------------------------------------------------------#
            # Reset the instance template flags:                               #
            #------------------------------------------------------------------#
            elif (bTemplateBegin and bTemplateEnd):
                txtTemplate = ''
                bTemplateBegin = False
                bTemplateEnd = False

    #----------------------------------------------------------------------#
    # Close the input file:                                                #
    #----------------------------------------------------------------------#
    file.close()

    #--------------------------------------------------------------------------#
    # Replace the class information in the entire file:                        #
    #--------------------------------------------------------------------------#
    txtData.replace('@@CLASS@@', sClass)
    txtData.replace('@@CLASSDESCRIPTION@@', sClassDescription)

    #--------------------------------------------------------------------------#
    # Replace any default parameters:                                          #
    #--------------------------------------------------------------------------#
    txtData = defaultParameters(sPCell, txtData)

    #--------------------------------------------------------------------------#
    # Write the output instance file:                                          #
    #--------------------------------------------------------------------------#
    sFileNameOut = pathOutput + '/' + sOutputPrefix + sClass + sOutputSuffix + '.awl'
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
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtData               The output data string with the new instance data.     #
#------------------------------------------------------------------------------#
def processTemplate(c, txtTemplate, txtData):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    global errProc
    errProc = processTemplate.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global gClass
    global gInstance

    #--------------------------------------------------------------------------#
    # Enter a loop to process each instance:                                   #
    #--------------------------------------------------------------------------#
    iRow = 0
    iCounterBase = 0
    for row in c:
        #----------------------------------------------------------------------#
        # Enter a loop to process all of the fields in the                     #
        # instance record:                                                     #
        #----------------------------------------------------------------------#
        iRow = iRow + 1
        sClass = ''
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

                elif (fld.upper() == 'INSTANCE'):
                    sInstance = row[fld]

        #----------------------------------------------------------------------#
        # Check if there are child attribute aliases in the template:          #
        #----------------------------------------------------------------------#
        if (txtInstance.find('ATTR') > 0):
            #------------------------------------------------------------------#
            # Process the attribute data:                                      #
            #------------------------------------------------------------------#
            gClass = sClass
            gInstance = sInstance
            txtInstance = insertAttributeData(sClass, sInstance, txtInstance)

            #------------------------------------------------------------------#
            # Replace any counters:                                            #
            #------------------------------------------------------------------#
            txtInstance = replaceCounter(iRow, txtInstance)

        #----------------------------------------------------------------------#
        # Add the instance template to the output data:                        #
        #----------------------------------------------------------------------#
        txtData = txtData + txtInstance
        txtInstance = ''

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
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtInstance           The updated instance data string with the new data.    #
#------------------------------------------------------------------------------#
def insertAttributeData(sClass, sInstance, txtInstance):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    global errProc
    errProc = insertAttributeData.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn
    global gClass
    global gInstance
    global gSelectParameter
    global gSelectSelection
    global gSFC
    global gState

    #--------------------------------------------------------------------------#
    # Process all of the attributes in the template:                           #
    #--------------------------------------------------------------------------#
    iRow = 0
    iCounterBase = 0
    txtRecordData = ''
    while (txtInstance.find('@@ATTR_BEGIN|') > 0):
        #----------------------------------------------------------------------#
        # Get the attribute name from the template. It must be in the          #
        # the enclosed in the format:                                          #
        #   @@ATTR_BEGIN|<attr>@@                                              #
        #   @@ATTR_END|<attr>@@                                                #
        #----------------------------------------------------------------------#
        iTagBegin = txtInstance.find('@@ATTR_BEGIN|')
        iTagEnd = txtInstance.find('@@', iTagBegin + 13)
        if (iTagBegin > iTagEnd):
            errorHandler(errorCode.noBeginPlaceholder, txtInstance)
        else:
            sTemplateAttrName = txtInstance[iTagBegin + 13:iTagEnd]

            #------------------------------------------------------------------#
            # Get the template text between the BEGIN and END tags:            #
            #------------------------------------------------------------------#
            iTagAttrEnd = txtInstance.find('@@ATTR_END|' + sTemplateAttrName)
            if (iTagAttrEnd == 0):
                errorHandler(errorCode.noEndPlaceholder, sTemplateAttrName, txtInstance)
            else:
                txtTemplate = txtInstance[iTagEnd + 3:iTagAttrEnd - 1]

            #------------------------------------------------------------------#
            # Get the instance file text before and after the template:        #
            #------------------------------------------------------------------#
            txtInstanceBegin = txtInstance[:iTagBegin]
            txtInstanceEnd = txtInstance[-(iTagBegin + 14 + len(sTemplateAttrName) + 1 +
                             len(txtTemplate) + 14 + len(sTemplateAttrName) + 2):]

            #------------------------------------------------------------------#
            # Strip out the extra carriage returns from the template text:     #
            #------------------------------------------------------------------#
            txtTemplate = txtTemplate[2:len(txtTemplate) - 1]

            #------------------------------------------------------------------#
            # Get any Default template definition tags:                        #
            #------------------------------------------------------------------#
            iDefaultBegin = txtTemplate.find('@@ATTR_DEFAULT_BEGIN@@')
            iDefaultEnd = txtTemplate.find('@@ATTR_DEFAULT_END@@')

            #------------------------------------------------------------------#
            # Set the query based on the attribute name:                       #
            #------------------------------------------------------------------#
            try:
                query = cgSQL.sql[cgSQL.sqlCode[sTemplateAttrName]]
                parms = cgSQL.prm[cgSQL.sqlCode[sTemplateAttrName]]
            except:
                errorHandler(errorCode.cannotGetSQL, sTemplateAttrName)

            #------------------------------------------------------------------#
            # Replace the parameters with their current values:                #
            #------------------------------------------------------------------#
            for i in range(len(parms)):
                if (parms[i] == 'gClass'):
                    parms[i] = gClass
                elif (parms[i] == 'gInstance'):
                    parms[i] = gInstance
                elif (parms[i] == 'gSelectParameter'):
                    parms[i] = gSelectParameter
                elif (parms[i] == 'gSelectSelection'):
                    parms[i] = gSelectSelection
                elif (parms[i] == 'gSFC'):
                    parms[i] = gSFC
                elif (parms[i] == 'gState'):
                    parms[i] = gState
#            for i in range(len(parms)):
#                print(parms[i])

            #------------------------------------------------------------------#
            # Query the sqlite database:                                       #
            #------------------------------------------------------------------#
            try:
                c = conn.cursor()
                c.execute(query, parms)
            except:
                errorHandler(errorCode.cannotQuery, query)

            #--------------------------------------------------------------#
            # Check to see if the recordset contains any data:             #
            #--------------------------------------------------------------#
            data = c.fetchall()
            if data is None:
                #----------------------------------------------------------#
                # No data so leave any default value:                      #
                #----------------------------------------------------------#
                if (iDefaultBegin > 0):
                    txtRecordData = txtTemplate[iDefaultBegin + 1 + 22:iDefaultEnd]
                else:
                    #------------------------------------------------------#
                    # not even a default value. Blank the template:        #
                    #------------------------------------------------------#
                    txtRecordData = ''
            else:
                #----------------------------------------------------------#
                # There is data so erase any default data:                 #
                #----------------------------------------------------------#
                if (iDefaultBegin > 0):
                    txtTemplate = txtTemplate[:iDefaultBegin - 1] + txtTemplate[:iDefaultEnd + 20]

                #----------------------------------------------------------#
                # Enter a loop to replace the attribute field names:       #
                #----------------------------------------------------------#
                for row in data:
                    #------------------------------------------------------#
                    # Enter a loop to process all of the fields in the     #
                    # instance record:                                     #
                    #------------------------------------------------------#
                    sClassRecursive = sClass
                    txtRecord = txtTemplate
                    iRow = iRow + 1
                    for fld in row.keys():
                        #--------------------------------------------------#
                        # Set a null placeholder if no data:               #
                        #--------------------------------------------------#
                        if row[fld] is None:
                            txtRecord = txtRecord.replace('@@' + fld.upper() + '@@', '##NULL##')
                        else:
                            #----------------------------------------------#
                            # Replace the placeholder with the db value:   #
                            #----------------------------------------------#
                            sValue = str(row[fld])
                            txtRecord = txtRecord.replace('@@' + fld.upper() + '@@', sValue)

                            #----------------------------------------------#
                            # Save the field data for iterative calls:     #
                            #----------------------------------------------#
                            if (fld.upper() == 'CLASS'):
                                gClass = sValue

                            if (fld.upper() == 'INSTANCE'):
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

                    #------------------------------------------------------#
                    # Process any further template child attribute tags:   #
                    #------------------------------------------------------#
                    if (txtRecord.find('ATTR') >= 0):
                        txtRecord = insertAttributeData(gClass, gInstance, txtRecord)

                    #------------------------------------------------------#
                    # Replace any counters:                                #
                    #------------------------------------------------------#
                    txtRecord = replaceCounter(iRow, txtRecord)

                    #------------------------------------------------------#
                    # Build the attribute record string:                   #
                    #------------------------------------------------------#
                    if (len(txtRecord) > 0):
                        txtRecordData = txtRecordData + txtRecord

#                            if (Mid(txtRecordData, len(txtRecordData) - 1, 1) = Chr(13) and _
#                                Mid(txtRecordData, len(txtRecordData), 1) = Chr(10) and _
#                                Mid(txtRecordData, len(txtRecordData) - 3, 1) = Chr(13) and _
#                                Mid(txtRecordData, len(txtRecordData) - 2, 1) = Chr(10)):
#                            else:
#                                txtRecordData = txtRecordData + '\r\n'

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
    global errProc
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
                errorHandler(errorCode.invalidCounter, sCounterBase)

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
# sPCell                The process cell which owns the instances.             #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# txtInstance           The updated instance template text.                    #
#------------------------------------------------------------------------------#
def defaultParameters(sPCell, txtInstance):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    global errProc
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
        c.execute(query, (sPCell,))
    except:
        errorHandler(errorCode.cannotQuery, query)

    #--------------------------------------------------------------------------#
    # Process each row in the list of classes:                                 #
    #--------------------------------------------------------------------------#
    for row in c:
        #----------------------------------------------------------------------#
        # Replace the field placeholders:                                      #
        #----------------------------------------------------------------------#
        if (row['Parameter'] is None):
            errorHandler(errorCode.invalidDefaultData, sPCell)

        elif (row['Default'] is None):
            errorHandler(errorCode.invalidDefaultData, sPCell)
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
    global errProc
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
        errorHandler(errorCode.cannotQuery, query)

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
            errorHandler(errorCode.filenotExist, sFileNameIn)

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
                sParameter = sBuffer[:sBuffer.find(' ') - 1]
                sParameter = sParameter[-len(sParameter) + 1:]
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
                    c1.execute(query, (sClass, '_' + sParameter + '%'))
                    data = c1.fetchone()
                except:
                    errorHandler(errorCode.cannotQuery, query)

                if data is None:
                    bIsChild = False
                else:
                    bIsChild = True

                #--------------------------------------------------------------#
                # Add the parameter to the SFC parameter table:                #
                #--------------------------------------------------------------#
                try:
                    query = cgSQL.sql[cgSQL.sqlCode.populateSFCParmsInsert]
                    c1.execute(query, (sClass, sSFC, sParameterType, sParameter,
                                      sParameter.upper(), sParameterDataType,
                                      sValue, sParameterDescription, bIsChild))
                except:
                    errorHandler(errorCode.cannotQuery, query)

                #--------------------------------------------------------------#
                # Commit the changes the database:                             #
                #--------------------------------------------------------------#
                try:
                    conn.commit()
                except:
                    errorHandler(errorCode.cannotCommit, query)

        #----------------------------------------------------------------------#
        # Finished with the data import. Close the file:                       #
        #----------------------------------------------------------------------#
        file.close()

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
main()
