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
import sys
import traceback
from tqdm import trange
from time import sleep
import sqlite3
from xls2db import xls2db
import collections
import datetime
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
parser.add_argument('-i','--input', help='Input document template file', required=True)
parser.add_argument('-o','--output', help='Output for the generated document file', required=True)
parser.add_argument('-p','--parent', help='Parent object to generate document files for', required=True)
parser.add_argument('-l','--level', help='Object hierarchy level to generate document files for', required=True)
args = vars(parser.parse_args())

#------------------------------------------------------------------------------#
# Declare global variables:                                                    #
#------------------------------------------------------------------------------#
c = 1
gClass = ''
gClassDescription = ''
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
    errorCode.noEndPlaceholder         : 'No valid END placholder in query string @1.',
    errorCode.noClassDBSheet           : 'idb Template Worksheet does not include a template called @1.',
    errorCode.noCodeTemplateFile       : 'Code template file @1 does not exist!',
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
    global gLevel
    global gParent
    global pathOutput
    global pathTemplates

    #--------------------------------------------------------------------------#
    # Get the hierarchy level:                                                 #
    #--------------------------------------------------------------------------#
    sLevel = args['level']
    gLevel = sLevel.upper()

    #--------------------------------------------------------------------------#
    # Get the parent object:                                                   #
    #--------------------------------------------------------------------------#
    sParent = args['parent']
    gParent = sParent.upper()

    #--------------------------------------------------------------------------#
    # Get the input document template file path and name and check it exists:  #
    #--------------------------------------------------------------------------#
    sInput = args['input']
    if not os.path.exists(sInput):
        errorHandler(errProc, errorCode.filenotExist, sInput)

    #--------------------------------------------------------------------------#
    # Get the output generated document file path and name:                    #
    #--------------------------------------------------------------------------#
    sOutput = args['output']

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
    dbName = 'dg.db'
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
        conn = sqlite3.connect('dg.db')
        conn.row_factory = sqlite3.Row
    except:
        errorHandler(errProc, errorCode.cannotConnectDB, 'dg.db')

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
    # Create the overall program index file:                                   #
    #--------------------------------------------------------------------------#
#    createIndexFile(sParent, 'PG', 100 * 1 / pbChunks)

    #--------------------------------------------------------------------------#
    # Create the document:                                                     #
    #--------------------------------------------------------------------------#
    createDocument(sParent, sLevel, sInput, sOutput, 100 * 1 / pbChunks)
#    createIndexFile(sParent, 'EM', 100 * 1 / pbChunks)
#    createIndexFile(sParent, 'UN', 100 * 1 / pbChunks)
#    createIndexFile(sParent, 'PC', 100 * 1 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected Parent:                     #
    #--------------------------------------------------------------------------#
#    processLevel(sParent, 'CM', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected Parent:                     #
    #--------------------------------------------------------------------------#
#    processLevel(sParent, 'EM', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected Parent:                     #
    #--------------------------------------------------------------------------#
#    processLevel(sParent, 'UN', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Process the Control Modules for the selected Parent:                     #
    #--------------------------------------------------------------------------#
#    processLevel(sParent, 'PC', 100 * 4 / pbChunks)

    #--------------------------------------------------------------------------#
    # Finally create any program files that need all blocks defined:           #
    #--------------------------------------------------------------------------#
#    createIndexFile(sParent, 'BLK', 100 * 1 / pbChunks)

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

#    def paragraph_replace(self, search, replace):
#        searchre = re.compile(search)
#        for paragraph in self.paragraphs:
#            paragraph_text = paragraph.text
#            if paragraph_text:
#                if searchre.search(paragraph_text):
#                    self.clear_paragraph(paragraph)
#                    paragraph.add_run(re.sub(search, replace, paragraph_text))
#        return paragraph

#    def clear_paragraph(self, paragraph):
#        p_element = paragraph._p
#        p_child_elements = [elm for elm in p_element.iterchildren()]
#        for child_element in p_child_elements:
#            p_element.remove(child_element)


#        document = Document()
#        paragraph = document.add_paragraph('Lorem ipsum dolor sit amet.')
#        prior_paragraph = paragraph.insert_paragraph_before('Lorem ipsum')
#        document.add_heading('The REAL meaning of the universe')
#        document.add_heading('The role of dolphins', level=2)
#        table = document.add_table(rows=2, cols=2)
#        paragraph = document.add_paragraph('Lorem ipsum dolor sit amet.')
#        paragraph.style = 'Normal'
#        document.save('./test.odt')

#table = document.add_table(1, 3)

#------------------------------------------------------------------------------#
# Function: createDocument                                                     #
#                                                                              #
# Description:                                                                 #
# Creates a document using sqlite data and a document template. The document   #
# template must have the query definitions deifned within it. A base query is  #
# defined in the document's "Comments" property and sub-table definitions are  #
# defined in each table as a query string in the first row, followed by a row  #
# of column headings followed by a row of cell data attributes using @@ data   #
# field placeholders.                                                          #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sParent               The parent tree object to generate code for.           #
# sLevel                The level to process, either CM, EM, UN or PC.         #
# sInput                The input document template to use.                    #
# sOutput               The output document to save.                           #
# pbwt                  The % weight of the procedure for the progress bar.    #
#------------------------------------------------------------------------------#
def createDocument(sParent, sLevel, sInput, sOutput, pbwt):
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
    global gClass
    global gDocType
    global gLevel
    global gParent

    #--------------------------------------------------------------------------#
    # Set the global parent and level variables:                               #
    #--------------------------------------------------------------------------#
    gLevel = sLevel

    #--------------------------------------------------------------------------#
    # Open the input document:                                                 #
    #--------------------------------------------------------------------------#
    document = Document(sInput)

    #--------------------------------------------------------------------------#
    # Get the document type from the core properties:                          #
    #--------------------------------------------------------------------------#
    gDocType = document.core_properties.subject

    #--------------------------------------------------------------------------#
    # Get the version history for the document:                                #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.versionHistory]
        c.execute(query, (gDocType.upper(), gLevel))
    except:
        errorHandler(errProc, errorCode.cannotQuery,
                     cgSQL.sqlCode.populateSFCParmsSubstate, query, sClass + ', ' + 'NONE')

    #--------------------------------------------------------------------------#
    # Set the document version information into the core properties:           #
    #--------------------------------------------------------------------------#
    data = c.fetchone()
    if (data is None):
        #----------------------------------------------------------------------#
        # Set the document to version 1:                                       #
        #----------------------------------------------------------------------#
        document.core_properties.category = '1'
        now = datetime.datetime.now()
        document.core_properties.keywords = str(now)
    else:
        #----------------------------------------------------------------------#
        # Set the document version information into the core properties:       #
        #----------------------------------------------------------------------#
        document.core_properties.category = data['Ver']
        document.core_properties.keywords = data['ChangedDate']
#        sDocNum = txtQuery = document.core_properties.company

    #--------------------------------------------------------------------------#
    # Get the base query data for the entire document and other properties:    #
    #--------------------------------------------------------------------------#
    txtQuery = document.core_properties.comments

#    queryDoc = core_properties.comments
    #--------------------------------------------------------------------------#
    # Check for non-ascii characters. Can't be a query string in that case:    #
    #--------------------------------------------------------------------------#
    try:
        txtQuery.decode('ascii')
    except:
        pass
#        errorHandler(errProc, errorCode.nonASCIICharacter)
    else:
        #----------------------------------------------------------------------#
        # Execute the query and get the data:                                  #
        #----------------------------------------------------------------------#
        c = getQueryData(txtQuery)
        if (not c is None):
            #------------------------------------------------------------------#
            # Process each row in the data set:                                #
            #------------------------------------------------------------------#
            data = c.fetchone()
#            for row in c:
            gClass = data['Class']

            #------------------------------------------------------------------#
            # Process each table in the document:                              #
            #------------------------------------------------------------------#
            for table in document.tables:
                #--------------------------------------------------------------#
                # Get the table data source and check it is a valid SQL SELECT #
                # query:                                                       #
                #--------------------------------------------------------------#
                rowSQL = table.rows[0]
                txtQuery = rowSQL.cells[0].text

                #--------------------------------------------------------------#
                # Check for non-ascii characters. Can't be a anchor string in  #
                # that case:                                                   #
                #--------------------------------------------------------------#
                try:
                    txtQuery.decode('ascii')
                except:
                    pass
            #        errorHandler(errProc, errorCode.nonASCIICharacter)
                else:
                    #----------------------------------------------------------#
                    # Check if the base query data table:                      #
                    #----------------------------------------------------------#
                    if (txtQuery[:7].upper() == 'SQLBASE'):
                        #------------------------------------------------------#
                        # Update the data row in the table:                    #
                        #------------------------------------------------------#
                        cells = table.rows[2].cells
                        for i in range(0, len(cells)):
                            #--------------------------------------------------#
                            # Replace the field placeholders in the cell text: #
                            #--------------------------------------------------#
                            s = cells[i].text
                            for fld in data.keys():
                                s = s.replace('@@' + fld.upper() + '@@', str(data[fld]))
                            para = cells[i].paragraphs[0]
                            para.text = ''
                            run = para.add_run(s)
                            para.style = 'NormalTableTitle'

                        #------------------------------------------------------#
                        # Delete the query row:                                #
                        #------------------------------------------------------#
                        remove_row(table, table.rows[0])

                    #----------------------------------------------------------#
                    # Check if an image anchor:                                #
                    #----------------------------------------------------------#
                    elif (txtQuery[:5].upper() == 'IMAGE'):
                        #------------------------------------------------------#
                        # Insert the image:                                    #
                        #------------------------------------------------------#
                        tableInsertImage(rowSQL, txtQuery, data)

                    #----------------------------------------------------------#
                    # Check if an append table rows query:                     #
                    #----------------------------------------------------------#
                    elif (txtQuery[:6].upper() == 'SQLROW'):
                        #------------------------------------------------------#
                        # Must be a valid query. Insert the data:              #
                        #------------------------------------------------------#
                        tableAddRows(rowSQL, txtQuery[8:], table)

                    #----------------------------------------------------------#
                    # Check if a static table query:                           #
                    #----------------------------------------------------------#
                    elif (txtQuery[:9].upper() == 'SQLSTATIC'):
                        #------------------------------------------------------#
                        # Must be a valid query. Insert the data:              #
                        #------------------------------------------------------#
                        tableStaticFields(rowSQL, txtQuery[11:], table)
                    else:
                        #------------------------------------------------------#
                        # Ignore other content:                                #
                        #------------------------------------------------------#
                        pass

        #----------------------------------------------------------------------#
        # Save the output document:                                            #
        #----------------------------------------------------------------------#
        document.save(sOutput)

        #----------------------------------------------------------------------#
        # Update the progress message:                                         #
        #----------------------------------------------------------------------#
    #    srDocument(document, 'replaceme', 'okbaby')
        p.set_description(sLevel + ' files complete')
        p.refresh()

def tableAddRows(rowSQL, txtQuery, table):
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
    c = getQueryData(txtQuery)
    if (not c is None):
        #----------------------------------------------------------------------#
        # Get the column attribute row:                                        #
        #----------------------------------------------------------------------#
        rowAttr = table.rows[2]
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
        remove_row(table, rowSQL)

def tableInsertImage(rowSQL, txtQuery, data):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = tableInsertImage.__name__

    #--------------------------------------------------------------------------#
    # Get the image file:                                                      #
    #--------------------------------------------------------------------------#
    sImage = txtQuery[6:]
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

def tableStaticFields(rowSQL, txtQuery, table):
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
    c = getQueryData(txtQuery)
    row = c.fetchone()
    if (not row is None):
        #----------------------------------------------------------------------#
        # Process each field in the data row:                                  #
        #----------------------------------------------------------------------#
        for fld in row.keys():
            srTable(table, '@@' + fld.upper() + '@@', str(row[fld]))

        #----------------------------------------------------------------------#
        # Clean up the table by deleting the query and attribute rows:         #
        #----------------------------------------------------------------------#
        remove_row(table, rowSQL)

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

def srParagraph(paragraph, txtSearch, txtReplace):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = srParagraph.__name__

    for run in paragraph.runs:
        while (txtSearch in run.text):
            text = run.text.split(txtSearch)
            run.text = text[0] + txtReplace + text[1]

def srDocument(document, txtSearch, txtReplace):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = srDocument.__name__

    for paragraph in document.paragraphs:
        srParagraph(paragraph, txtSearch, txtReplace)

def srTable(table, txtSearch, txtReplace):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = srTable.__name__

    for cell in table.cells:
        for paragraph in cell.paragraphs:
            srParagraph(paragraph, txtSearch, txtReplace)

def remove_row(t, r):
    #--------------------------------------------------------------------------#
    # Define the procedure name and trap any programming errors:               #
    #--------------------------------------------------------------------------#
    errProc = remove_row.__name__

    tbl = t._tbl
    tr = r._tr
    tbl.remove(tr)

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
main()
