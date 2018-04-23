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
from docx import Document
import openpyxl
import os.path
from shutil import copyfile
import sys
import traceback
from tqdm import trange
from time import sleep
import sqlite3
from xls2db import xls2db
import collections
import datetime
import PyPDF2
#from pyPdf import PdfFileReader, PdfFileWriter
import subprocess
import cgSQL

import logging
logging.basicConfig(level=logging.DEBUG)

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
appTitle = 'Document Generator'
appVersion = '1'
parser = argparse.ArgumentParser(description='Generates PLC code from a configuration spreadsheet and set of code templates')
parser.add_argument('-c','--config', help='Configuration spreadsheet', required=True)
parser.add_argument('-b','--inputBase', help='Input base document template file', required=True)
parser.add_argument('-r','--inputRecord', help='Input record document template file', required=False)
parser.add_argument('-o','--output', help='Output for the generated document file', required=True)
parser.add_argument('-s','--scope', help='The document scope', required=True)
parser.add_argument('-t','--type', help='The document type', required=True)
args = vars(parser.parse_args())

#------------------------------------------------------------------------------#
# Declare global variables:                                                    #
#------------------------------------------------------------------------------#
gcBase = 1
gcQuery = ''
gClass = ''
gClassDescription = ''
gDocScope = ''
gDocType = ''
gInstance = ''
gLevel = ''
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
    noCodeTemplateFile                 = -36
    noEndPlaceholder                   = -37
    noRecordDocument                   = -40
    nonASCIICharacter                  = -41
    unknownAttribute                   = -42

errorMessage = {
    errorCode.cannotCommit             : 'Cannot commit changes to sqlite database',
    errorCode.cannotConvertWorkbook    : 'Cannot convert workbook @1 from xlsx to sqlite db @2',
    errorCode.cannotConnectDB          : 'Cannot connect to sqlite database @1',
    errorCode.cannotCreateTable        : 'Cannot insert table @1 into sqlite database',
    errorCode.cannotGetSQL             : 'Cannot retrieve SQL query expression for attribute @1',
    errorCode.cannotQuery              : 'Query cannot execute using SQL expression @1 with parameters @2',
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
    errorCode.noClassDBSheet           : 'idb Template Worksheet does not include a template called @1.',
    errorCode.noCodeTemplateFile       : 'Code template file @1 does not exist!',
    errorCode.noEndPlaceholder         : 'No valid END placholder in query string @1.',
    errorCode.noRecordDocument         : 'No record document specified with record data.',
    errorCode.nonASCIICharacter        : 'Query expression returned a non ascii-encoded unicode string',
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
    global gDocScope
    global gDocType
    global pathOutput
    global pathTemplates

    #--------------------------------------------------------------------------#
    # Get the document scope and type:                                         #
    #--------------------------------------------------------------------------#
    gDocScope = args['scope'].upper()
    gDocType = args['type'].upper()

    #--------------------------------------------------------------------------#
    # Get the input document template file path and name and check it exists:  #
    #--------------------------------------------------------------------------#
    sInputBase = args['inputBase']
    if not os.path.exists(sInputBase):
        errorHandler(errProc, errorCode.filenotExist, sInputBase)

    #--------------------------------------------------------------------------#
    # Get the output generated document file path and name:                    #
    #--------------------------------------------------------------------------#
    sOutputBase = args['output']

    #--------------------------------------------------------------------------#
    # Get the code configuration workbook name and check it exists:            #
    #--------------------------------------------------------------------------#
    wbName = args['config']
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
    dbName = os.path.dirname(wbName) + '/dg.db'
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
    pbChunks = 1.0

    #--------------------------------------------------------------------------#
    # Create the base document:                                                #
    #--------------------------------------------------------------------------#
    createDocument(sInputBase, sOutputBase, 100 * 1 / pbChunks)

    #--------------------------------------------------------------------------#
    # Print the base document to PDF:                                          #
    #--------------------------------------------------------------------------#
    sBaseName = os.path.basename(sOutputBase)
    sBaseDir = os.path.dirname(sOutputBase)
    printPDF(sOutputBase, sBaseDir)
    sFileName = os.path.splitext(sBaseName)[0]
    sOutputBasePDF = sBaseDir + '/' + sFileName + '.pdf'
    print('sOutputBasePDF = ' + sOutputBasePDF)

    #--------------------------------------------------------------------------#
    # Check if the document has base data for mulitple records:                #
    #--------------------------------------------------------------------------#
    if (not gcBase is None):
        #----------------------------------------------------------------------#
        # Get the input record document template file path and name and check  #
        # it exists:                                                           #
        #----------------------------------------------------------------------#
        if (args['inputRecord'] is None):
            errorHandler(errProc, errorCode.noRecordDocument)

        sInputRecord = args['inputRecord']
        if not os.path.exists(sInputRecord):
            errorHandler(errProc, errorCode.filenotExist, sInputRecord)

        #----------------------------------------------------------------------#
        # Process each row in the cursor to append the new record document:    #
        #----------------------------------------------------------------------#
        for row in gcBase:
            #------------------------------------------------------------------#
            # Define a temporary output document;                              #
            #------------------------------------------------------------------#
            sOutput = os.path.dirname(sOutputBase) + '/t.docx'

            #------------------------------------------------------------------#
            # Create the record document:                                      #
            #------------------------------------------------------------------#
            createDocument(sInputRecord, sOutput, 100 * 1 / pbChunks)

            #------------------------------------------------------------------#
            # Print the document to PDF:                                       #
            #------------------------------------------------------------------#
            printPDF(sOutput, sBaseDir)

            #------------------------------------------------------------------#
            # Append the record document PDF to the base document PDF:         #
            #------------------------------------------------------------------#
            sOutputPDF = sBaseDir + '/t.pdf'
            print('sOutputPDF = ' + sOutputPDF)
            sOutputBaseCopy = sBaseDir + '/p.pdf'
            copyfile(sOutputBasePDF, sOutputBaseCopy)
            appendPDF(sOutputBaseCopy, sOutputPDF, sOutputBasePDF)
#            os.rename(sOutputBase, os.path.dirname(sOutputBase) + '/t.docx')
#            os.remove(sOutputBaseTemp)

    #--------------------------------------------------------------------------#
    # Commit the changes to the database and close the connection:             #
    #--------------------------------------------------------------------------#
    conn.commit()
    conn.close()

    #--------------------------------------------------------------------------#
    # Report completion regardless of error:                                   #
    #--------------------------------------------------------------------------#
    p.set_description('Processing complete')
    p.refresh()
    p.close()

    #--------------------------------------------------------------------------#
    # Output a success message:                                                #
    #--------------------------------------------------------------------------#
    print('Congratulations! Operation successful.')

#------------------------------------------------------------------------------#
# Function: createDocument                                                     #
#                                                                              #
# Description:                                                                 #
# Creates a document using sqlite data and a document template.                #
# The document template must have the query definitions defined within it in   #
# tables with the query string in the first row. Different types of queries    #
# are handled as follows:                                                      #
#                                                                              #
# IMAGE      An image will be inserted in the table cell.                      #
# SQLBASE    Base data for the document, such as document number and title.    #
# SQLRECORD  A sub-document in a multi-record compound document. The first     #
#            document will be the parent header document and each record will  #
#            be appended as a child document.                                  #
# SQLROW     Multi-record table. The table must include a row of column        #
#            headings followed by a row of cell data attributes using @@ data  #
#            field placeholders.                                               #
# SQLSTATIC  A table of any cell arrangement to be populated without changing  #
#            the table structure.                                              #

#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sInput                The input document template to use.                    #
# sOutput               The output document to create.                         #
# pbwt                  The % weight of the procedure for the progress bar.    #
#------------------------------------------------------------------------------#
def createDocument(sInput, sOutput, pbwt):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = createDocument.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object and global parent and     #
    # level variables:                                                         #
    #--------------------------------------------------------------------------#
    c = 1
    global conn
    global gcQuery
    global gClass
    global gDocType
    global gLevel
    global gParent

    #--------------------------------------------------------------------------#
    # Open the input document:                                                 #
    #--------------------------------------------------------------------------#
    document = Document(sInput)

    #--------------------------------------------------------------------------#
    # Get the document properties:                                             #
    #--------------------------------------------------------------------------#
    setDocumentProperties(document)

    #--------------------------------------------------------------------------#
    # Get the latest document version number:                                  #
    #--------------------------------------------------------------------------#
    getVersionNumber(document)

    #--------------------------------------------------------------------------#
    # Process each table in the document:                                      #
    #--------------------------------------------------------------------------#
    for table in document.tables:
        #----------------------------------------------------------------------#
        # Get the table data source and check it is a valid SQL SELECT query:  #
        #----------------------------------------------------------------------#
        rowSQL = table.rows[0]
        txtQuery = rowSQL.cells[0].text

        #----------------------------------------------------------------------#
        # Finished with the query row already so delete it:                    #
        #----------------------------------------------------------------------#
        remove_row(table, rowSQL)

        #----------------------------------------------------------------------#
        # Check for non-ascii characters. Can't be a anchor string in that     #
        # case:                                                                #
        #----------------------------------------------------------------------#
        try:
            txtQuery.decode('ascii')
        except:
            #------------------------------------------------------------------#
            # Just ignore this table:                                          #
            #------------------------------------------------------------------#
            pass
        else:
            #------------------------------------------------------------------#
            # Check if an image anchor:                                        #
            #------------------------------------------------------------------#
            if (txtQuery[:5].upper() == 'IMAGE'):
                #--------------------------------------------------------------#
                # Insert the image:                                            #
                #--------------------------------------------------------------#
                tableInsertImage(txtQuery[6:], data)

            #------------------------------------------------------------------#
            # Check if base query data for the entire document:                #
            #------------------------------------------------------------------#
            elif (txtQuery[:7].upper() == 'SQLBASE'):
                #--------------------------------------------------------------#
                # Get the base data for the document:                          #
                #--------------------------------------------------------------#
                gcQuery = txtQuery[8:]
                getBaseData()

            #------------------------------------------------------------------#
            # Check if a base query record table:                              #
            #------------------------------------------------------------------#
            elif (txtQuery[:9].upper() == 'SQLRECORD'):
                #--------------------------------------------------------------#
                # Must be a valid query. Insert the data:                      #
                #--------------------------------------------------------------#
                tableBaseRecord(table)

            #------------------------------------------------------------------#
            # Check if an append table rows query:                             #
            #------------------------------------------------------------------#
            elif (txtQuery[:6].upper() == 'SQLROW'):
                #--------------------------------------------------------------#
                # Must be a valid query. Insert the data:                      #
                #--------------------------------------------------------------#
                tableAddRows(txtQuery[7:], table)

            #------------------------------------------------------------------#
            # Check if a static table query:                                   #
            #------------------------------------------------------------------#
            elif (txtQuery[:9].upper() == 'SQLSTATIC'):
                #--------------------------------------------------------------#
                # Must be a valid query. Insert the data:                      #
                #--------------------------------------------------------------#
                tableStaticFields(txtQuery[10:], table)
            else:
                #--------------------------------------------------------------#
                # Ignore other content:                                        #
                #--------------------------------------------------------------#
                pass

    #--------------------------------------------------------------------------#
    # Save the output document:                                                #
    #--------------------------------------------------------------------------#
    document.save(sOutput)

    #--------------------------------------------------------------------------#
    # Update the progress message:                                             #
    #--------------------------------------------------------------------------#
    p.set_description(gDocScope + ' files complete')
    p.refresh()

#------------------------------------------------------------------------------#
# Function: getBaseData                                                        #
#                                                                              #
# Description:                                                                 #
# Gets the underlying document cursor for multi-record compound documents.     #
#------------------------------------------------------------------------------#
def getBaseData():
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = getBaseData.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global base data cursor:                              #
    #--------------------------------------------------------------------------#
    global gcBase
    global gcQuery

    #--------------------------------------------------------------------------#
    # Execute the query and get the data:                                      #
    #--------------------------------------------------------------------------#
    gcBase = getQueryData(gcQuery)

#------------------------------------------------------------------------------#
# Function: setDocumentProperties                                              #
#                                                                              #
# Description:                                                                 #
# Sets the core document properties for version number and date and retrieves  #
# the document type.                                                           #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# document              The document to get properties for.                    #
#------------------------------------------------------------------------------#
def setDocumentProperties(document):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = setDocumentProperties.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite connection object:                      #
    #--------------------------------------------------------------------------#
    global conn
    global gDocScope
    global gDocType

    #--------------------------------------------------------------------------#
    # Set the document type from the core properties:                          #
    #--------------------------------------------------------------------------#
    document.core_properties.comments = gDocScope
    document.core_properties.subject = gDocType

    #--------------------------------------------------------------------------#
    # Get the document information:                                            #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.documentInfo]
        c.execute(query, (gDocType.upper(), gDocScope.upper()))
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.documentInfo, query, gDocType + ', ' + gDocScope)

    #--------------------------------------------------------------------------#
    # Set the document number into the core properties:                        #
    #--------------------------------------------------------------------------#
    data = c.fetchone()
    if (data is None):
        pass
    else:
        #----------------------------------------------------------------------#
        # Set the document version information into the core properties:       #
        #----------------------------------------------------------------------#
        document.core_properties.company = data['docNumber']
        document.core_properties.title = data['docTitle']

#------------------------------------------------------------------------------#
# Function: getVersionNumber                                                   #
#                                                                              #
# Description:                                                                 #
# Gets the core document properties for version number and date and retrieves  #
# the document type.                                                           #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# document              The document to get properties for.                    #
#------------------------------------------------------------------------------#
def getVersionNumber(document):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = getVersionNumber.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite connection object:                      #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the version history for the document:                                #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.versionHistory]
        c.execute(query, (gDocType.upper(), gLevel))
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.versionHistory, query, gDocType + ', ' + gLevel)

    #--------------------------------------------------------------------------#
    # Set the document version information into the core properties. The last  #
    # version number is first in the returned descending order cursor:         #
    #--------------------------------------------------------------------------#
    data = c.fetchone()
    if (data is None):
        pass
    else:
        #----------------------------------------------------------------------#
        # Set the document version information into the core properties:       #
        #----------------------------------------------------------------------#
        document.core_properties.category = data['Ver']
        document.core_properties.keywords = data['ChangedDate']

#------------------------------------------------------------------------------#
# Function: tableAddRows                                                       #
#                                                                              #
# Description:                                                                 #
# Adds one table row for each row in the cursor.                               #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# query                 The query string to get the data for.                  #
# table                 The table in the document being processed.             #
#------------------------------------------------------------------------------#
def tableAddRows(query, table):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = tableAddRows.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite connection object:                      #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Execute the query and get the data:                                      #
    #--------------------------------------------------------------------------#
    c = getQueryData(query)
    if (not c is None):
        #----------------------------------------------------------------------#
        # Get the column attribute row:                                        #
        #----------------------------------------------------------------------#
        rowAttr = table.rows[1]
        cellsAttr = rowAttr.cells

        #----------------------------------------------------------------------#
        # Process each row of returned data:                                   #
        #----------------------------------------------------------------------#
        for row in c:
            #------------------------------------------------------------------#
            # Add a new row to the table and enter a loop to process each      #
            # cell:                                                            #
            #------------------------------------------------------------------#
            cellsNew = table.add_row().cells
            for i in range(0, len(cellsAttr)):
                #--------------------------------------------------------------#
                # Replace the field placeholders in the cell text:             #
                #--------------------------------------------------------------#
                s = cellsAttr[i].text
                for fld in row.keys():
                    s = s.replace('@@' + fld.upper() + '@@', str(row[fld]))
                para = cellsNew[i].paragraphs[0]
                para.text = ''
                run = para.add_run(s)
                para.style = 'NormalTable'

        #----------------------------------------------------------------------#
        # Clean up the table by deleting the query and attribute rows:         #
        #----------------------------------------------------------------------#
        remove_row(table, rowAttr)

#------------------------------------------------------------------------------#
# Function: tableBaseRecord                                                    #
#                                                                              #
# Description:                                                                 #
# A table which includes fields from the document base cursor.                 #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# table                 The table in the document being processed.             #
#------------------------------------------------------------------------------#
def tableBaseRecord(table):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = tableBaseRecord.__name__

    #--------------------------------------------------------------------------#
    # Refresh the base data cursor:                                            #
    #--------------------------------------------------------------------------#
    global gcBase
    getBaseData()

    #--------------------------------------------------------------------------#
    # Simply process the table as a static field table with the global data:   #
    #--------------------------------------------------------------------------#
    for row in gcBase:
        for fld in row.keys():
            try:
                srTable(table, '@@' + fld.upper() + '@@', str(row[fld]), 'NormalTableTitle')
            except:
                pass

def tableInsertImage(sImage, data):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = tableInsertImage.__name__

    #--------------------------------------------------------------------------#
    # Get the image file:                                                      #
    #--------------------------------------------------------------------------#
    for fld in data.keys():
        sImage = sImage.replace('@@' + fld.upper() + '@@', str(data[fld]))

    #--------------------------------------------------------------------------#
    # Check if the image exists:                                               #
    #--------------------------------------------------------------------------#
    if not os.path.exists(sImage):
        errorHandler(errProc, errorCode.filenotExist, sImage)

    #--------------------------------------------------------------------------#
    # Insert the image:                                                        #
    #--------------------------------------------------------------------------#
    para = rowSQL.cells[0].paragraphs[0]
    para.text = ''
    run = para.add_run()
    run.add_picture(sImage)
    para.style = 'NormalTableCentre'

def tableStaticFields(query, table):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = tableStaticFields.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite connection object:                      #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Execute the query and get the data:                                      #
    #--------------------------------------------------------------------------#
    c = getQueryData(query)
    row = c.fetchone()
    if (not row is None):
        #----------------------------------------------------------------------#
        # Process each field in the data row:                                  #
        #----------------------------------------------------------------------#
        for fld in row.keys():
            srTable(table, '@@' + fld.upper() + '@@', str(row[fld]), 'NormalTable')

def getQueryData(txtQuery):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = getQueryData.__name__

    #--------------------------------------------------------------------------#
    # Declare use of the global sqlite cursor object:                          #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get any parameters from the query string:                                #
    #--------------------------------------------------------------------------#
    q = getQueryParameters(txtQuery)

    #--------------------------------------------------------------------------#
    # Execute the query:                                                       #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        c.execute(q.query, q.parms)
    except:
        errorHandler(errProc, errorCode.cannotQuery, q.query, q.parms)
    return c

def getQueryParameters(txtQuery):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = getQueryParameters.__name__

    #--------------------------------------------------------------------------#
    # Declare the named tuple for the returned data:                           #
    #--------------------------------------------------------------------------#
    Query = collections.namedtuple('Query', ['query', 'parms'])

    #--------------------------------------------------------------------------#
    # Declare use of the global variables:                                     #
    #--------------------------------------------------------------------------#
    global gClass
    global gDocScope
    global gDocType
    global gInstance
    global gLevel
    global gParent
    global gSelectParameter
    global gSelectSelection
    global gSFC
    global gState

    #--------------------------------------------------------------------------#
    # Declare local parameter list to return:                                  #
    #--------------------------------------------------------------------------#
    parms = []

    #--------------------------------------------------------------------------#
    # Enter a loop to process all of the parameter placeholders in the query:  #
    #--------------------------------------------------------------------------#
    while (txtQuery.find('@@') >= 0):
        #----------------------------------------------------------------------#
        # Search for any parameter placeholders in the query string:           #
        #----------------------------------------------------------------------#
        iTagBegin = txtQuery.find('@@')
        iTagEnd = txtQuery.find('@@', iTagBegin + 2)
        if (iTagBegin == -1):
            #------------------------------------------------------------------#
            # Nothing to do. Return null:                                      #
            #------------------------------------------------------------------#
            return;

        elif (iTagBegin > iTagEnd):
            errorHandler(errProc, errorCode.noEndPlaceholder, txtQuery)
        else:
            #------------------------------------------------------------------#
            # Get the parameter text between the BEGIN and END tags and        #
            # replace the parameter with a question mark. Add the parameter to #
            # the list:                                                        #
            #------------------------------------------------------------------#
            sParameterName = txtQuery[iTagBegin + 2:iTagEnd]
            txtQuery = txtQuery[:iTagBegin] + '?' + txtQuery[iTagEnd + 2:]
            parms.append(sParameterName)

    #--------------------------------------------------------------------------#
    # Replace the parameters with the global variable values:                  #
    #--------------------------------------------------------------------------#
    for i in range(len(parms)):
        if (parms[i].upper() == 'CLASS'):
            parms[i] = gClass
        elif (parms[i].upper() == 'DOCSCOPE'):
            parms[i] = gDocScope.upper()
        elif (parms[i].upper() == 'DOCTYPE'):
            parms[i] = gDocType.upper()
        elif (parms[i].upper() == 'INSTANCE'):
            parms[i] = gInstance
        elif (parms[i].upper() == 'LEVEL'):
            parms[i] = gLevel
        elif (parms[i] == 'PARENT'):
            parms[i] = gParent
        elif (parms[i] == 'SFC'):
            parms[i] = gSFC
        elif (parms[i] == 'STATE'):
            parms[i] = gState

    #--------------------------------------------------------------------------#
    # Return the parameter value list:                                         #
    #--------------------------------------------------------------------------#
    q = Query(query=txtQuery, parms=parms)
    return q;

def srParagraph(paragraph, txtSearch, txtReplace, style):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = srParagraph.__name__

    s = paragraph.text
    s = s.replace(txtSearch, txtReplace)
    paragraph.text = ''
    run = paragraph.add_run(s)
    paragraph.style = style

def srDocument(document, txtSearch, txtReplace, style):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = srDocument.__name__

    for paragraph in document.paragraphs:
        srParagraph(paragraph, txtSearch, txtReplace, style)

def srTable(table, txtSearch, txtReplace, style):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = srTable.__name__

    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                srParagraph(paragraph, txtSearch, txtReplace, style)

def remove_row(t, r):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = remove_row.__name__

    tbl = t._tbl
    tr = r._tr
    tbl.remove(tr)

def appendPDF(sParent, sChild, sOutput):
    pdfParent = open(sParent, 'rb')
    pdfChild = open(sChild, 'rb')

    merger = PyPDF2.PdfFileMerger()

    merger.append(fileobj=pdfParent)
    merger.append(fileobj=pdfChild)
    merger.write(open(sOutput, 'wb'))
#    output = PdfFileWriter()
#    pdfParent = PdfFileReader(file( "out.pdf", "rb"))
#    pdfChild = PdfFileReader(file("out1.pdf", "rb"))

#    output.addPage(pdfParent.getPage(0))
#    output.addPage(pdfChild.getPage(0))

#    outputStream = file(r"output.pdf", "wb")
#    output.write(outputStream)
#    outputStream.close()

def printPDF(sDocument, outDir):
    #--------------------------------------------------------------------------#
    # Save the output document as PDF:                                         #
    #--------------------------------------------------------------------------#
    output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf' , '--outdir', outDir, sDocument])
    print output

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
main()
