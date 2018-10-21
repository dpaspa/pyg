#------------------------------------------------------------------------------#
#                   Copyright 2018 complianceSHORTCUTS.com                     #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file contains the python script which creates a document from a sqlite  #
# database by searching and replacing the table field names as @@name@@ data   #
# placeholders within the document.                                            #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      21-Sep-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
import argparse
import collections
from enum import Enum
import os.path
import sys
from tqdm import trange
from fdgBlobData import blobData
from fdgDataDocument import dataDocument
from fdgDoc import gDoc
from fdgProperty import setProperty
from fdgRefRenumber import refRenumber
from fdgCSV2XLSX import csv2xlsx
from fdgXLSX2DB import xlsx2db

import logging
logging.basicConfig(filename='fdg.log',level=logging.DEBUG)

#------------------------------------------------------------------------------#
# Declare global variables:                                                    #
#------------------------------------------------------------------------------#
ps = None

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Generates a document from a configuration spreadsheet and set of document templates')
parser.add_argument('-c','--config', help='Configuration spreadsheet', required=True)
parser.add_argument('-f','--docFilter', help='The document data filter for the WHERE clause', required=False)
parser.add_argument('-i','--input', help='The input file path for the document templates', required=False)
parser.add_argument('-n','--projectName', help='The document project name', required=True)
parser.add_argument('-o','--output', help='The ouput file path to save to', required=True)
parser.add_argument('-r','--report', help='Print to PDF if a report', required=True)
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
    # Use global variables:                                                    #
    #--------------------------------------------------------------------------#
    global ps

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
    ps.close()
    sys.exit()

#------------------------------------------------------------------------------#
# Enumerate the error numbers and map the error messages:                      #
#------------------------------------------------------------------------------#
class errorCode(Enum):
    cannotConnectDB                    = -1
    cannotConvertWorkbook              = -2
    cannotQuery                        = -3
    fileNotExist                       = -4
    noDocInfo                          = -5
    pathNotExist                       = -6

errorMessage = {
    errorCode.cannotConnectDB          : 'Cannot connect to sqlite database @1',
    errorCode.cannotConvertWorkbook    : 'Cannot convert workbook @1 to sqlite database @2',
    errorCode.cannotQuery              : 'Query cannot execute using SQL expression @1',
    errorCode.fileNotExist             : 'Parent file @1 does not exist.',
    errorCode.noDocInfo                : 'No document information defined for name @1 with filter @2',
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
    # Use global variables:                                                    #
    #--------------------------------------------------------------------------#
    global ps

    #--------------------------------------------------------------------------#
    # Create a progress bar:                                                   #
    #--------------------------------------------------------------------------#
    ps = trange(1, desc='Document generator...', leave=False)

    #--------------------------------------------------------------------------#
    # Get the document filters:                                                #
    #--------------------------------------------------------------------------#
    docFilter = ''
    if (not args['docFilter'] is None):
        docFilter = args['docFilter']
    projectName = args['projectName']

    #--------------------------------------------------------------------------#
    # Determine if a PDF report:                                               #
    #--------------------------------------------------------------------------#
    s = args['report']
    if (s.upper() == 'Y' or s.upper() == 'YES'):
        isReport = True
    else:
        isReport = False

    #--------------------------------------------------------------------------#
    # Get the output path:                                                     #
    #--------------------------------------------------------------------------#
    pathOutput = args['output']
    if not os.path.exists(pathOutput):
        errorHandler(errProc, errorCode.pathNotExist, pathOutput)

    #--------------------------------------------------------------------------#
    # Get the input path:                                                      #
    #--------------------------------------------------------------------------#
    pathInput = ''
    if (not args['input'] is None):
        pathInput = args['input']
        if not os.path.exists(pathInput):
            errorHandler(errProc, errorCode.pathNotExist, pathInput)

    #--------------------------------------------------------------------------#
    # Get the configuration workbook name and check it exists:                 #
    #--------------------------------------------------------------------------#
    wbName = args['config']
    if not os.path.exists(wbName):
        errorHandler(errProc, errorCode.fileNotExist, wbName)

    #--------------------------------------------------------------------------#
    # Get the configuration workbook as a sqlite database:                     #
    #--------------------------------------------------------------------------#
    logging.info('Document generator')
    logging.info('config: ' + wbName)
    logging.info('output: ' + pathOutput)
    logging.info('docFilter: ' + docFilter)
    logging.info('projectName: ' + projectName)
    logging.info('report: ' + str(isReport))
    conn = xlsx2db(wbName, pathOutput)

    #--------------------------------------------------------------------------#
    # Get the data connections from the configuration database:                #
    #--------------------------------------------------------------------------#
    query = 'SELECT * FROM dataConnections WHERE projectName = ?'
    try:
        c = conn.cursor()
        c.execute(query, (projectName,))
    except:
        errorHandler(errProc, errorCode.cannotQuery, query)

    #--------------------------------------------------------------------------#
    # Process each row of returned data. Add the data sources to a list with   #
    # a connection to the converted SQLite database:                           #
    #--------------------------------------------------------------------------#
    data = c.fetchall()
    for row in data:
        #----------------------------------------------------------------------#
        # Get the data source filename:                                        #
        #----------------------------------------------------------------------#
        s = row['fileInputData']
        if (len(pathInput) > 0):
            fileName = pathInput + '/' + s
        else:
            fileName = row['pathInputData'] + '/' + s

        #----------------------------------------------------------------------#
        # Get the data connections:                                            #
        #----------------------------------------------------------------------#
        dc = getData(conn, fileName, projectName, row['connectionName'], pathOutput, row['dbOutputName'])

    #--------------------------------------------------------------------------#
    # Get the parent documents from the configuration database:                #
    #--------------------------------------------------------------------------#
    query = 'SELECT * FROM docParent WHERE projectName = ?'
    try:
        c = conn.cursor()
        c.execute(query, (projectName,))
    except:
        errorHandler(errProc, errorCode.cannotQuery, query)

    #--------------------------------------------------------------------------#
    # Process each row in the documents table:                                 #
    #--------------------------------------------------------------------------#
    data = c.fetchall()
    iRefNumber = 1
    for rowParent in data:
        #----------------------------------------------------------------------#
        # Get the document information from the configuration database:        #
        #----------------------------------------------------------------------#
        query = 'SELECT * FROM docInfo WHERE projectName = ? and docFilter = ?'
        try:
            c = conn.cursor()
            c.execute(query, (projectName, docFilter))
        except:
            errorHandler(errProc, errorCode.cannotQuery, query)

        #----------------------------------------------------------------------#
        # Process each row of returned data. Add the data sources to a list    #
        # with  a connection to the converted SQLite database:                 #
        #----------------------------------------------------------------------#
        docInfo = c.fetchone()
        if (docInfo is None):
            errorHandler(errProc, errorCode.noDocInfo, projectName, docFilter)

        #----------------------------------------------------------------------#
        # Create the document object:                                          #
        #----------------------------------------------------------------------#
        fileInput = rowParent['fileInput']
        fileOutput = pathOutput + '/' + rowParent['nameOutput'] + '_' + docFilter + '.docx'
        d = createDocument(fileInput, fileOutput, conn, dc,
                           docFilter, rowParent['parentKey'], projectName,
                           docInfo['propertyComments'], docInfo['propertyKeywords'],
                           docInfo['propertySubject'], docInfo['propertyTitle'],
                           rowParent['refNumPrefix'], 1, '', isReport)

        #----------------------------------------------------------------------#
        # Get the parent documents from the configuration database:            #
        #----------------------------------------------------------------------#
        query = 'SELECT * FROM docChild WHERE projectName = ?'
        try:
            c = conn.cursor()
            c.execute(query, (d.projectName, ))
        except:
            errorHandler(errProc, errorCode.cannotQuery, query)

        #----------------------------------------------------------------------#
        # Get any child document. There should be only one:                    #
        #----------------------------------------------------------------------#
        hasChild = False
        rowChild = c.fetchone()
        if (rowChild is not None):
            #------------------------------------------------------------------#
            # Process each row in the parent document database:                #
            #------------------------------------------------------------------#
            for row in d.dataBase:
                #--------------------------------------------------------------#
                # Get the child properties. If an input file is specified for  #
                # the child then it overrides the field lookup properties:     #
                #--------------------------------------------------------------#
                fileInput = rowChild['fileInput']
                fileOutput = d.fileOutputDir + '/t.docx'
                hasChild = True

                #--------------------------------------------------------------#
                # If no input file name then use parent data child field name: #
                #--------------------------------------------------------------#
                if (len(fileInput) == 0):
                    s = str(rowChild['childField'])
                    sChildFileName = row[s]
                    fileInput = d.fileInputDir + '/' + sChildFileName + '.docx'
                    if (sChildFileName.upper() == 'NONE'):
                        hasChild = False

                    elif not os.path.exists(fileInput):
                        errorHandler(errProc, errorCode.fileNotExist, fileInput)

                #--------------------------------------------------------------#
                # Check if a child document filename is defined:               #
                #--------------------------------------------------------------#
                if (hasChild):
                    #----------------------------------------------------------#
                    # Update the progress bar:                                 #
                    #----------------------------------------------------------#
                    pc = 1.0 / d.rowCount
                    ps.update(pc)
                    s = str(rowChild['childKey'])
                    sChildKey = row[s]
                    ps.set_description('Child ' + sChildKey)
                    ps.refresh()

                    #----------------------------------------------------------#
                    # Create the child document object:                        #
                    #----------------------------------------------------------#
                    dChild = createDocument(fileInput, fileOutput, conn, dc,
                                            docFilter, sChildKey, projectName,
                                            docInfo['propertyComments'], docInfo['propertyKeywords'],
                                            docInfo['propertySubject'], docInfo['propertyTitle'],
                                            rowChild['refNumPrefix'], d.refNumber, row, isReport)

                    #----------------------------------------------------------#
                    # Save the maximum reference number reached in the parent: #
                    #----------------------------------------------------------#
                    d.refNumber = dChild.refNumber

                    #----------------------------------------------------------#
                    # Append the child record document PDF to the base parent  #
                    # document PDF:                                            #
                    #----------------------------------------------------------#
                    if (isReport):
                        d.appendPDF(dChild)

        #----------------------------------------------------------------------#
        # Add the page numbers to the output document if a PDF report with     #
        # children:                                                            #
        #----------------------------------------------------------------------#
        if (isReport and hasChild):
            d.pdfPageNumbers()
        ps.close()

#------------------------------------------------------------------------------#
# Function: createDocument                                                     #
#                                                                              #
# Description:                                                                 #
# Creates the document and populates it with any data.                         #
#------------------------------------------------------------------------------#
# Calling Parameters:                                                          #
# fileInput             The input document file.                               #
# fileOutput            The output document file to save to.                   #
# cc                    The configuration database sqlite connection.          #
# dc                    The array of sqlite database connections.              #
# docFilter             The source data FILTER filter.                         #
# filterKey             The source data KEY filter.                            #
# projectName               The configuration file project filter.             #
# propertyComments      The in-built property for Comments.                    #
# propertyKeywords      The in-built property for Keywords.                    #
# propertySubject       The in-built property for Subject.                     #
# propertyTitle         The in-built property for Title.                       #
# refNumPrefix          The reference number alphabetic prefix string.         #
# iRefNumberStart       The reference starting number.                         #
# dataRow               The data row to populate the document with.            #
# isReport              Create a PDF report if true.                           #
#------------------------------------------------------------------------------#
def createDocument(fileInput, fileOutput, cc, dc,
                   docFilter, filterKey, projectName,
                   propertyComments, propertyKeywords, propertySubject, propertyTitle,
                   refNumPrefix, iRefNumberStart, dataRow, isReport):
    #--------------------------------------------------------------------------#
    # Define the procedure name:                                               #
    #--------------------------------------------------------------------------#
    errProc = createDocument.__name__

    #--------------------------------------------------------------------------#
    # Create the document object:                                              #
    #--------------------------------------------------------------------------#
    d = gDoc(fileInput, fileOutput)

    #--------------------------------------------------------------------------#
    # Set the other document object properties:                                #
    #--------------------------------------------------------------------------#
    d.cc = cc
    d.dataRow = dataRow
    d.dc = dc
    d.filterKey = filterKey
    d.docFilter = docFilter
    d.projectName = projectName
    d.refNumber = iRefNumberStart

    #--------------------------------------------------------------------------#
    # Set the internal document properties:                                    #
    #--------------------------------------------------------------------------#
    if (len(propertyComments) > 0):
        setProperty(d, 'COMMENTS', propertyComments)

    if (len(propertyKeywords) > 0):
        setProperty(d, 'KEYWORDS', propertyKeywords)

    if (len(propertySubject) > 0):
        setProperty(d, 'SUBJECT', propertySubject)

    if (len(propertyTitle) > 0):
        setProperty(d, 'TITLE', propertyTitle)

    #--------------------------------------------------------------------------#
    # Update the document data:                                                #
    #--------------------------------------------------------------------------#
    dataDocument(d)

    #--------------------------------------------------------------------------#
    # Update any reference numbers:                                            #
    #--------------------------------------------------------------------------#
    if (len(refNumPrefix) > 0):
        d.refNumber = refRenumber(d, refNumPrefix, d.refNumber)

    #--------------------------------------------------------------------------#
    # Save the document:                                                       #
    #--------------------------------------------------------------------------#
    d.saveDocument()

    #--------------------------------------------------------------------------#
    # Print the base document to PDF:                                          #
    #--------------------------------------------------------------------------#
    if (isReport):
        d.printPDF()
        d.docxDelete()

    #--------------------------------------------------------------------------#
    # Return the document object reference:                                    #
    #--------------------------------------------------------------------------#
    return d

#------------------------------------------------------------------------------#
# Function: getData                                                            #
#                                                                              #
# Description:                                                                 #
# Creates the sqlite database and provides a connector.                        #
#------------------------------------------------------------------------------#
# Calling Parameters:                                                          #
# conn                  The configuration file data connection.                #
# fileInput             The input source data file.                            #
# projectName         The project filter.                                    #
# connectionName        The data connection name in the project.               #
# pathOutput            The output path.                                       #
# fileOutputName        The output file name for the sqlite database.          #
#------------------------------------------------------------------------------#
def getData(conn, fileInput, projectName, connectionName, pathOutput, fileOutputName):
    #--------------------------------------------------------------------------#
    # Define the procedure name:                                               #
    #--------------------------------------------------------------------------#
    errProc = getData.__name__

    #--------------------------------------------------------------------------#
    # Get the data connections from the configuration database:                #
    #--------------------------------------------------------------------------#
    dc = []
    objData = collections.namedtuple('objData', 'name file conn')
    query = 'SELECT * FROM dataMarkers WHERE [projectName] = ? AND [connectionName] = ?'
    try:
        c = conn.cursor()
        c.execute(query, (projectName, connectionName))
    except:
        errorHandler(errProc, errorCode.cannotQuery, query)

    #--------------------------------------------------------------------------#
    # Check if any data markers defined for the connection:                    #
    #--------------------------------------------------------------------------#
    data = c.fetchall()
    if (len(data) == 0):
        #----------------------------------------------------------------------#
        # No data markers. Just use the entire file as is:                     #
        #----------------------------------------------------------------------#
        f, ext = os.path.splitext(fileInput)
        fileInputName = os.path.basename(fileInput)
        fileInputBaseName = os.path.splitext(fileInputName)[0]
        if (ext.upper() == '.CSV'):
            fileInput = csv2xlsx(fileInput, pathOutput, fileOutputName)

        dataConn = xlsx2db(fileInput, pathOutput)
        t = objData(name=connectionName, file=fileInput, conn=dataConn)
        dc.append(t)
    else:
        #----------------------------------------------------------------------#
        # Process each row in the data markers table:                          #
        #----------------------------------------------------------------------#
        for row in data:
            #------------------------------------------------------------------#
            # Get the file data based on the markers:                          #
            #------------------------------------------------------------------#
            marker = row['markerName']
            b = blobData(fileInput)
            if (marker == 'docFilter'):
                pass

            elif (marker == 'time'):
                pass

            #------------------------------------------------------------------#
            # Get the input file data:                                         #
            #------------------------------------------------------------------#
            f, ext = os.path.splitext(fileInput)
            fileInputName = os.path.basename(fileInput)
            fileInputBaseName = os.path.splitext(fileInputName)[0]
            if (ext.upper() == '.CSV'):
                fileInput = csv2xlsx(fileInput, pathOutput, fileOutputName)

            dataConn = xlsx2db(fileInput, pathOutput)
            t = objData(name=connectionName, file=fileInput, conn=dataConn)
            dc.append(t)

    #--------------------------------------------------------------------------#
    # Return the data connections array:                                       #
    #--------------------------------------------------------------------------#
    return dc

#------------------------------------------------------------------------------#
# Function: createVersionHistory                                               #
#                                                                              #
# Description:                                                                 #
# Creates the version history table.                                           #
#------------------------------------------------------------------------------#
# Calling Parameters:                                                          #
# conn                  The configuration file data connection.                #
# fileInput             The input source data file.                            #
# projectName         The project filter.                                    #
# connectionName        The data connection name in the project.               #
# pathOutput            The output path.                                       #
# fileOutputName        The output file name for the sqlite database.          #
#------------------------------------------------------------------------------#
#def createVersionHistory(conn, fileInput, projectName, connectionName, pathOutput, fileOutputName):
    #--------------------------------------------------------------------------#
    # Define the procedure name:                                               #
    #--------------------------------------------------------------------------#
#    errProc = createVersionHistory.__name__

    #--------------------------------------------------------------------------#
    # Get the data connections from the configuration database:                #
    #--------------------------------------------------------------------------#
#    query = 'SELECT printf("%d",V.Ver) AS Ver, V.ChangedBy, substr("00"||printf("%d",V.D), -2, 2) || "-" || substr("00"||printf("%d",V.M), -2, 2) || "-" || printf("%d",V.Y) AS ChangedDate, V.ChangeNumber, V.Description FROM tblRevisionHistory AS V WHERE upper(V.KeyName) = @@DOCTYPE@@ AND V.KeyValue = @@SCOPE@@ ORDER BY V.Ver DESC'

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
main()
