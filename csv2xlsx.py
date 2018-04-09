#------------------------------------------------------------------------------#
#            Copyright 2018 Rieckermann Engineering Operations                 #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file converts a CSV file to xlsx format.                                #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      07-Apr-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
import argparse
from enum import Enum
import logging
import os.path
import sys
import csv
from openpyxl import Workbook
from tqdm import trange
from time import sleep

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
appTitle = 'CSV 2 XLSX Converter'
appVersion = '1'
parser = argparse.ArgumentParser(description='Converts a CSV file to XLSX format')
parser.add_argument('-i','--input', help='Path and file name of the input CSV file', required=True)
args = vars(parser.parse_args())

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
    cannotCreateCSV                    = -1
    cannotOpenCSV                      = -2
    cannotOpenWorkbook                 = -3
    fileNotExist                       = -4
    pathNotExist                       = -5

errorMessage = {
    errorCode.cannotCreateCSV          : 'Cannot create output worksheet @1',
    errorCode.cannotOpenCSV            : 'Cannot open CSV file @1',
    errorCode.cannotOpenWorkbook       : 'Cannot open workbook @1',
    errorCode.fileNotExist             : 'Workbook file @1 does not exist.',
    errorCode.pathNotExist             : 'Ouput path @1 does not exist.'
}

#------------------------------------------------------------------------------#
# Create a progress bar:                                                       #
#------------------------------------------------------------------------------#
p = trange(100, desc='Starting...', leave=False)

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
    logging.basicConfig(level=logging.ERROR)

    #--------------------------------------------------------------------------#
    # Get the input CSV file name and check it exists:                         #
    #--------------------------------------------------------------------------#
    csvName = args['input']
    if not os.path.exists(csvName):
        errorHandler(errorCode.fileNotExist, csvName)

    #--------------------------------------------------------------------------#
    # Open the CSV file:                                                       #
    #--------------------------------------------------------------------------#
    try:
        f = open(csvName)
    except:
        errorHandler(errorCode.cannotOpenCSV, csvName)

    #--------------------------------------------------------------------------#
    # Define the CSV dialect being used:                                       #
    #--------------------------------------------------------------------------#
    csv.register_dialect('colons', delimiter=':')
    csv.register_dialect('commas', delimiter=',')
    reader = csv.reader(f, dialect='commas')

    #--------------------------------------------------------------------------#
    # Get the number of lines in the file:                                     #
    #--------------------------------------------------------------------------#
    for i, l in enumerate(f):
        pass
    numLines = i + 1

    #--------------------------------------------------------------------------#
    # Create a new workbook file in memory and use the first worksheet:        #
    #--------------------------------------------------------------------------#
    wb = Workbook()
    ws = wb.worksheets[0]
    ws.title = 'PLC Tags'

    #--------------------------------------------------------------------------#
    # Process the critical interlocks:                                         #
    #--------------------------------------------------------------------------#
    f.seek(0)
    for row_index, row in enumerate(reader):
        for column_index, cell in enumerate(row):
            ws.cell(row=row_index + 1, column=column_index + 1).value = cell

        p.update(100 * 1.0 / numLines)
        p.refresh()
        sleep(0.01)

    #--------------------------------------------------------------------------#
    # Save the changes if no error:                                            #
    #--------------------------------------------------------------------------#
    if (iErr == 0):
        wb.save(filename = os.path.splitext(csvName)[0] + '.xlsx')

    #--------------------------------------------------------------------------#
    # Report completion regardless of error:                                   #
    #--------------------------------------------------------------------------#
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
        logging.critical(appTitle + ' Version ' + appVersion + '\r\n' + 'ERROR ' +
                         str(iErr) + ' in Procedure ' + "'" + errProc + "'" + '\r\n' + sMsg)
        sys.exit()

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
main()
