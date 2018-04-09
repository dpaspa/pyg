#------------------------------------------------------------------------------#
#            Copyright 2018 Rieckermann Engineering Operations                 #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file creates a list of interlocks from a safety matrix.                 #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      05-Apr-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
import argparse
from enum import Enum
import logging
import openpyxl
import os.path
import sys
from tqdm import trange
from time import sleep

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
appTitle = 'Interlock Generator'
appVersion = '1'
parser = argparse.ArgumentParser(description='Generates a list of Interlocks from a Safety Matrix worksheet')
parser.add_argument('-i','--input', help='Path and file name of the input safety matrix worksheet file', required=True)
parser.add_argument('-s','--sheet', help='Name of the safety matrix worksheet', required=True)
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
    cannotCreateOutputSheet            = -1
    cannotOpenWorkbook                 = -2
    cannotReplace                      = -3
    fileNotExist                       = -4
    noMatrixWorksheet                  = -5
    noNamedRange                       = -6

errorMessage = {
    errorCode.cannotCreateOutputSheet  : 'Cannot create output worksheet @1',
    errorCode.cannotOpenWorkbook       : 'Cannot open workbook @1',
    errorCode.cannotReplace            : 'Cannot replace field @1 with value @2.',
    errorCode.fileNotExist             : 'Workbook file @1 does not exist.',
    errorCode.noMatrixWorksheet        : 'Safety matrix worksheet @1 does not exist.',
    errorCode.noNamedRange             : 'Named range @1 does not exist.'
}

#------------------------------------------------------------------------------#
# Create a progress bar:                                                       #
#------------------------------------------------------------------------------#
p = trange(100, desc='Starting...', leave=False)
#TQDMCallback(metric_format="{name}: {value:0.2f}")

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
    # Get the interlock configuration workbook name and check it exists:       #
    #--------------------------------------------------------------------------#
    wbName = args['input']
    if not os.path.exists(wbName):
        errorHandler(errorCode.fileNotExist, wbName)

    #--------------------------------------------------------------------------#
    # Open the workbook:                                                       #
    #--------------------------------------------------------------------------#
    try:
        wb = openpyxl.load_workbook(wbName, data_only=True)
    except:
        errorHandler(errorCode.cannotOpenWorkbook, wbName)

    #--------------------------------------------------------------------------#
    # Get the input safety matrix worksheet:                                   #
    #--------------------------------------------------------------------------#
    wsName = args['sheet']
    try:
        wsi = wb[wsName]
    except:
        errorHandler(errorCode.noMatrixWorksheet, wsName)

    #--------------------------------------------------------------------------#
    # Process the critical interlocks:                                         #
    #--------------------------------------------------------------------------#
    generateInterlocks(wb, wsi, 'X', 'tblInterlockCR', 50)

    #--------------------------------------------------------------------------#
    # Process the non-critical interlocks:                                     #
    #--------------------------------------------------------------------------#
    generateInterlocks(wb, wsi, 'M', 'tblInterlockNCR', 50)

    #--------------------------------------------------------------------------#
    # Save the changes if no error:                                            #
    #--------------------------------------------------------------------------#
    if (iErr == 0):
        wb.save(wbName)

    #--------------------------------------------------------------------------#
    # Report completion regardless of error:                                   #
    #--------------------------------------------------------------------------#
    p.close()
    reportComplete()

#------------------------------------------------------------------------------#
# Function generateInterlocks                                                  #
#                                                                              #
# Description:                                                                 #
# Creates the interlock worksheet with the safety matrix as an interlock list. #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# wb                    The workbook object.                                   #
# wsi                   The input safety matrix worksheet object.              #
# sILMarker             The interlock marker, either "X" for critical          #
#                       interlocks or "M" for non-critical interlocks          #
#                       which are allowed to be manually overrridden.          #
# sILSheet              The output sheet name.                                 #
# pbwt                  The % weight of the procedure for the progress bar.    #
#------------------------------------------------------------------------------#
def generateInterlocks(wb, wsi, sILMarker, sILSheet, pbwt):
    #--------------------------------------------------------------------------#
    # Define the procedure name:                                               #
    #--------------------------------------------------------------------------#
    global errProc
    errProc = generateInterlocks.__name__

    #--------------------------------------------------------------------------#
    # Delete the output worksheet and create a blank new one:                  #
    #--------------------------------------------------------------------------#
    global p
    try:
        wso = wb[sILSheet]
        wb.remove(wso)
        wb.create_sheet(sILSheet)
        wso = wb[sILSheet]
        logging.info(wso.title)
    except:
        errorHandler(errorCode.cannotCreateOutputSheet, sILSheet)

    #--------------------------------------------------------------------------#
    # Set the new worksheet titles:                                            #
    #--------------------------------------------------------------------------#
    wso.cell(row=1, column=1).value = 'Source'
    wso.cell(row=1, column=2).value = 'Target'
    wso.cell(row=1, column=3).value = 'Interlock'
    iRowOut = 2

    #--------------------------------------------------------------------------#
    # Get the named ranges to orientate the data:                              #
    #--------------------------------------------------------------------------#
    try:
        sNamedRange = 'ILEnd'
        colILEnd = wsi[list(wb.defined_names[sNamedRange].destinations)[0][1]].col_idx
        sNamedRange = 'ILName'
        colILName = wsi[list(wb.defined_names[sNamedRange].destinations)[0][1]].col_idx
        sNamedRange = 'ILCode'
        colILCode = wsi[list(wb.defined_names[sNamedRange].destinations)[0][1]].col_idx
        sNamedRange = 'ILTarget'
        colILTarget = wsi[list(wb.defined_names[sNamedRange].destinations)[0][1]].col_idx
        rowILTarget = wsi[list(wb.defined_names[sNamedRange].destinations)[0][1]].row
        sNamedRange = 'ILSource'
        colILSource = wsi[list(wb.defined_names[sNamedRange].destinations)[0][1]].col_idx
        rowILSource = wsi[list(wb.defined_names[sNamedRange].destinations)[0][1]].row
        sNamedRange = 'ILState'
        colILState = wsi[list(wb.defined_names[sNamedRange].destinations)[0][1]].col_idx
        sNamedRange = 'ILFunction'
        colILFunction = wsi[list(wb.defined_names[sNamedRange].destinations)[0][1]].col_idx
        sNamedRange = 'ILFunctionEnd'
        colILFunctionEnd = wsi[list(wb.defined_names[sNamedRange].destinations)[0][1]].col_idx
    except:
        errorHandler(errorCode.noNamedRange, sNamedRange)

    #--------------------------------------------------------------------------#
    # Enter a loop to process all of the safety interlocks:                    #
    #--------------------------------------------------------------------------#
    iCol = colILSource
    sNamePrevious = ''
    iRowMax = wsi.max_row
    for i in range(rowILSource + 1, iRowMax):
        #----------------------------------------------------------------------#
        # Check if a new interlock:                                            #
        #----------------------------------------------------------------------#
        sName = wsi.cell(row=i, column=colILName).value
        num = iRowMax - rowILSource - 1
        pc = pbwt * 1.0 / num
        p.update(pc)
        p.set_description(sILSheet + ' ' + sName)
        p.refresh()
        sleep(0.01)
        if (sName != sNamePrevious):
            #------------------------------------------------------------------#
            # Enter a loop to process the interlock name set:                  #
            #------------------------------------------------------------------#
            iRow = i
            iRowNext = iRow
            sExpression = ''
            sNameNext = wsi.cell(row=iRowNext, column=colILName).value
            while (sNameNext == sName):
                #--------------------------------------------------------------#
                # Get the source device data:                                  #
                #--------------------------------------------------------------#
                sSource = wsi.cell(row=iRowNext, column=colILSource).value
                sCode = wsi.cell(row=iRowNext, column=colILCode).value
                sFunction = wsi.cell(row=iRowNext, column=colILFunction).value
                sFunctionEnd = wsi.cell(row=iRowNext, column=colILFunctionEnd).value
                sState = wsi.cell(row=iRowNext, column=colILState).value

                #--------------------------------------------------------------#
                # Replace any placeholder text:                                #
                #--------------------------------------------------------------#
                logging.info('Source: ' + sSource)
                sCode = sCode.replace('@@INSTANCE@@', sSource)
                sCode = sCode.replace('@@STATE@@', sState)

                #--------------------------------------------------------------#
                # Build the interlock code:                                    #
                #--------------------------------------------------------------#
                if (not sFunction is None):
                    sExpression = sExpression + sFunction

                sExpression = sExpression + '\r\n' + sCode

                if (not sFunctionEnd is None):
                    sExpression = sExpression + '\r\n' + sFunctionEnd

                #--------------------------------------------------------------#
                # Check the next row:                                          #
                #--------------------------------------------------------------#
                iRowNext = iRowNext + 1
                sNameNext = wsi.cell(row=iRowNext, column=colILName).value
                if (sName == sNameNext):
                    sExpression = sExpression + '\r\n'

            #------------------------------------------------------------------#
            # Enter another loop to process all of the safety interlock data   #
            # in the current row for the current interlock source tag:         #
            #------------------------------------------------------------------#
            iXCol = colILTarget + 1
            while (iXCol < colILEnd):
                #--------------------------------------------------------------#
                # Check if an interlock:                                       #
                #--------------------------------------------------------------#
                sX = wsi.cell(row=iRow, column=iXCol).value
                if (sX == sILMarker):
                    #----------------------------------------------------------#
                    # Add the interlock to the output list:                    #
                    #----------------------------------------------------------#
                    sTarget = wsi.cell(row=rowILTarget, column=iXCol).value
                    logging.info('Target: ' + sTarget)

                    #----------------------------------------------------------#
                    # Add the interlock to the output list:                    #
                    #----------------------------------------------------------#
                    wso.cell(row=iRowOut, column=1).value = sSource
                    wso.cell(row=iRowOut, column=2).value = sTarget
                    wso.cell(row=iRowOut, column=3).value = sExpression
                    iRowOut = iRowOut + 1

                #--------------------------------------------------------------#
                # Process the next column:                                     #
                #--------------------------------------------------------------#
                iXCol = iXCol + 1

            #------------------------------------------------------------------#
            # Process the next interlock source row:                           #
            #------------------------------------------------------------------#
            sNamePrevious = sName

    #--------------------------------------------------------------------------#
    # Return completion status:                                                #
    #--------------------------------------------------------------------------#
    p.set_description('Processing complete')
    p.refresh()
    return iErr

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
