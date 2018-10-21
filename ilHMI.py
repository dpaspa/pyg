#------------------------------------------------------------------------------#
#            Copyright 2018 Rieckermann Engineering Operations                 #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file creates a PDF file of the interlock description.                   #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      27-Jun-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
import argparse
from enum import Enum
import os.path
import sys
from shutil import copyfile
from tqdm import trange
from time import sleep
import sqlite3
import cgSQL
import PyPDF2
import reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

import logging
logging.basicConfig(level=logging.ERROR)

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
appTitle = 'Interlock HMI PDF Generator'
appVersion = '1'
parser = argparse.ArgumentParser(description='Generates a PDF file describing each Interlock for display on the HMI')
parser.add_argument('-d','--database', help='Path and file name of the database', required=True)
parser.add_argument('-o','--output', help='Output for the generated PDF file', required=True)
parser.add_argument('-t','--template', help='The template PDF file to use', required=True)
args = vars(parser.parse_args())

#------------------------------------------------------------------------------#
# Declare global variables:                                                    #
#------------------------------------------------------------------------------#
conn = ''

#------------------------------------------------------------------------------#
# Declare the error handling global variables and procedure:                   #
#------------------------------------------------------------------------------#
def errorHandler(errProc, eCode, *args):
    #--------------------------------------------------------------------------#
    # Get the application specific error message and output the error:         #
    #--------------------------------------------------------------------------#
    sMsg = errorMessage[eCode]

    #--------------------------------------------------------------------------#
    # Close the progress bar:                                                  #
    #--------------------------------------------------------------------------#
    p.close()

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
    cannotCreateOutputSheet            = -1
    cannotOpenWorkbook                 = -2
    cannotQuery                        = -3
    cannotReplace                      = -4
    fileNotExist                       = -5
    instanceNotFound                   = -6
    noMatrixWorksheet                  = -7
    noNamedRange                       = -8

errorMessage = {
    errorCode.cannotCreateOutputSheet  : 'Cannot create output worksheet @1',
    errorCode.cannotOpenWorkbook       : 'Cannot open workbook @1',
    errorCode.cannotQuery              : 'Cannot query with @1.',
    errorCode.cannotReplace            : 'Cannot replace field @1 with value @2.',
    errorCode.fileNotExist             : 'Workbook file @1 does not exist.',
    errorCode.instanceNotFound         : 'Instance @1 does not exist in sheet tblInstance.',
    errorCode.noMatrixWorksheet        : 'Safety matrix worksheet @1 does not exist.',
    errorCode.noNamedRange             : 'Named range @1 does not exist.'
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
    # Declare global and local variables:                                      #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Get the calling parameters and check the database exists:                #
    #--------------------------------------------------------------------------#
    output = args['output']
    dbName = args['database']
    if not os.path.exists(dbName):
        errorHandler(errProc, errorCode.filenotExist, dbName)

    #--------------------------------------------------------------------------#
    # Make the output directories if not already existing:                     #
    #--------------------------------------------------------------------------#
    if not os.path.exists(output + '/CRIL'):
        os.makedirs(output + '/CRIL')
    if not os.path.exists(output + '/NCRIL'):
        os.makedirs(output + '/NCRIL')

    #--------------------------------------------------------------------------#
    # Get the template files and make sure they exist:                         #
    #--------------------------------------------------------------------------#
    templatePDF = args['template']
    if not os.path.exists(templatePDF):
        errorHandler(errProc, errorCode.filenotExist, templatePDF)

    #--------------------------------------------------------------------------#
    # Connect to the new persistent sqlite database file:                      #
    #--------------------------------------------------------------------------#
    try:
        conn = sqlite3.connect(dbName)
        conn.row_factory = sqlite3.Row
    except:
        errorHandler(errProc, errorCode.cannotConnectDB, dbName)

    #--------------------------------------------------------------------------#
    # Get the number of critical interlocked devices:                          #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.CRIL_NUM]
        c.execute(query)
        nData = c.fetchone()
        num = nData['MAXITEM']
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.CRIL_NUM, query)

    #--------------------------------------------------------------------------#
    # Get the critical interlock list:                                         #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.CRIL]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.CRIL, query)

    #--------------------------------------------------------------------------#
    # Process the critical interlocks:                                         #
    #--------------------------------------------------------------------------#
    generateInterlocksPDF(c, 'CRIL', templatePDF, output, num)

    #--------------------------------------------------------------------------#
    # Refresh the critical interlock cursor:                                   #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.CRIL]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.CRIL, query)

    #--------------------------------------------------------------------------#
    # Process the critical interlocks:                                         #
    #--------------------------------------------------------------------------#
    generateInterlocksHTML(c, 'CRIL', output, num)

    #--------------------------------------------------------------------------#
    # Get the number of non critical interlocked devices:                      #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.NCRIL_NUM]
        c.execute(query)
        nData = c.fetchone()
        num = nData['MAXITEM']
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.CRIL_NUM, query)

    #--------------------------------------------------------------------------#
    # Get the non critical interlock list:                                     #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.NCRIL]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.NCRIL, query)

    #--------------------------------------------------------------------------#
    # Process the non-critical interlocks:                                     #
    #--------------------------------------------------------------------------#
    generateInterlocksPDF(c, 'NCRIL', templatePDF, output, num)

    #--------------------------------------------------------------------------#
    # Refresh the non critical interlock cursor:                               #
    #--------------------------------------------------------------------------#
    try:
        c = conn.cursor()
        query = cgSQL.sql[cgSQL.sqlCode.NCRIL]
        c.execute(query)
    except:
        errorHandler(errProc, errorCode.cannotQuery, cgSQL.sqlCode.NCRIL, query)

    #--------------------------------------------------------------------------#
    # Process the non-critical interlocks:                                     #
    #--------------------------------------------------------------------------#
    generateInterlocksHTML(c, 'NCRIL', output, num)

    #--------------------------------------------------------------------------#
    # Output a success message:                                                #
    #--------------------------------------------------------------------------#
    print('Congratulations... interlock HMI template generation successful.')

#------------------------------------------------------------------------------#
# Function: generateInterlocksHTML                                             #
#                                                                              #
# Description:                                                                 #
# Creates a HTML file for display of the interlock list on the HMI for each    #
# interlocked object.                                                          #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# data                  The list of interlocked objects.                       #
# ilName                The instance query name prefix.                        #
# output                The output path for the generated HTML.                #
# num                   The number of interlocked devices for the progress bar.#
#------------------------------------------------------------------------------#
def generateInterlocksHTML(data, ilName, output, num):
    #--------------------------------------------------------------------------#
    # Define the procedure name:                                               #
    #--------------------------------------------------------------------------#
    errProc = generateInterlocksHTML.__name__

    #--------------------------------------------------------------------------#
    # Declare global and local variables:                                      #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Create a progress bar:                                                   #
    #--------------------------------------------------------------------------#
    p = trange(num, desc=ilName, leave=False)

    #--------------------------------------------------------------------------#
    # Process each row in the cursor:                                          #
    #--------------------------------------------------------------------------#
    for row in data:
        #----------------------------------------------------------------------#
        # Update the progress bar:                                             #
        #----------------------------------------------------------------------#
        pc = 100 / num
        p.update(pc)
        p.set_description(row['Instance'])
        p.refresh()
        sleep(0.01)

        #----------------------------------------------------------------------#
        # Get the list of instances for the interlocked device:                #
        #----------------------------------------------------------------------#
        try:
            iData = conn.cursor()
            query = cgSQL.sql[cgSQL.sqlCode[ilName + '_INSTANCE']]
            iData.execute(query, (row['Instance'],))
        except:
            errorHandler(errProc, errorCode.cannotQuery, ilName + '_INSTANCE', query)

        #----------------------------------------------------------------------#
        # Create the HTML content:                                             #
        #----------------------------------------------------------------------#
        outFilename = output + '/' + ilName + '/' + row['Instance'] + '.html'

        sHTML = """ <html>
                        <head>
                        </head>
                        <body>
                            <table border=1> """
        #----------------------------------------------------------------------#
        # Write in the instance interlock descriptions:                        #
        #----------------------------------------------------------------------#
        for r in iData:
            sHTML = sHTML + """
                                <tr>
                                    <td> """ + r['DescriptionIL'] + """
                                    </td>
                                </tr> """

        sHTML = sHTML + """
                        </table>
                    </body>
                </html> """

        #----------------------------------------------------------------------#
        # Create the output HTML file:                                         #
        #----------------------------------------------------------------------#
        outFilename = output + '/' + ilName + '/' + row['Instance'] + '.html'
        fileHTML= open(outFilename, "w")
        fileHTML.write(sHTML)
        fileHTML.close()

    #--------------------------------------------------------------------------#
    # Report completion regardless of error:                                   #
    #--------------------------------------------------------------------------#
    p.set_description(ilName + ' HMI template processing complete')
    p.refresh()
    p.close()

#------------------------------------------------------------------------------#
# Function: generateInterlocksPDF                                              #
#                                                                              #
# Description:                                                                 #
# Creates a PDF file for display of the interlock list on the HMI for each     #
# interlocked object.                                                          #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# data                  The list of interlocked objects.                       #
# ilName                The instance query name prefix.                        #
# template              The template PDF file to use.                          #
# output                The output path for the generated PDF.                 #
# num                   The number of interlocked devices for the progress bar.#
#------------------------------------------------------------------------------#
def generateInterlocksPDF(data, ilName, template, output, num):
    #--------------------------------------------------------------------------#
    # Define the procedure name:                                               #
    #--------------------------------------------------------------------------#
    errProc = generateInterlocksPDF.__name__

    #--------------------------------------------------------------------------#
    # Declare global and local variables:                                      #
    #--------------------------------------------------------------------------#
    global conn

    #--------------------------------------------------------------------------#
    # Create a progress bar:                                                   #
    #--------------------------------------------------------------------------#
    p = trange(num, desc=ilName, leave=False)

    #--------------------------------------------------------------------------#
    # Process each row in the cursor:                                          #
    #--------------------------------------------------------------------------#
    for row in data:
        #----------------------------------------------------------------------#
        # Update the progress bar:                                             #
        #----------------------------------------------------------------------#
        pc = 100 / num
        p.update(pc)
        p.set_description(row['Instance'])
        p.refresh()
        sleep(0.01)

        #----------------------------------------------------------------------#
        # Get the list of instances for the interlocked device:                #
        #----------------------------------------------------------------------#
        try:
            iData = conn.cursor()
            query = cgSQL.sql[cgSQL.sqlCode[ilName + '_INSTANCE']]
            iData.execute(query, (row['Instance'],))
        except:
            errorHandler(errProc, errorCode.cannotQuery, ilName + '_INSTANCE', query)

        #----------------------------------------------------------------------#
        # Create the output PDF file:                                          #
        #----------------------------------------------------------------------#
        tmp = output + '/' + ilName + '/' + row['Instance'] + '.pdf'
        copyfile(template, tmp)

        #----------------------------------------------------------------------#
        # Open the PDf canvas of the output PDF file:                          #
        #----------------------------------------------------------------------#
        c = canvas.Canvas(tmp)
#        c.setPageSize((725, 508))
#        c.setPageSize((2061, 1442))
        c.setPageSize((824, 576))
        c.setFont('Helvetica', 12)
        c.setLineWidth(0.2)
        y = 194

        #----------------------------------------------------------------------#
        # Write in the instance interlock descriptions:                        #
        #----------------------------------------------------------------------#
        for r in iData:
            c.drawString((5)*mm, (y)*mm, r['DescriptionIL'])
            c.line((5)*mm, (y-4)*mm, (285)*mm, (y-4)*mm)
            y = y - 13.3

        #----------------------------------------------------------------------#
        # Save and close the file:                                             #
        #----------------------------------------------------------------------#
        c.save()
        c = None

    #--------------------------------------------------------------------------#
    # Report completion regardless of error:                                   #
    #--------------------------------------------------------------------------#
    p.set_description(ilName + ' HMI template processing complete')
    p.refresh()
    p.close()

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
main()
