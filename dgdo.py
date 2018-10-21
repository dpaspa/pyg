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
import logging
logging.basicConfig(level=logging.DEBUG)
from dgRefRenumber import refRenumber
from dgProperty import setProperty
from dgDataDocument import dataDocument
from dgXL2DB import xl2db

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Generates a document from a configuration spreadsheet and set of document templates')
parser.add_argument('-c','--config', help='Configuration spreadsheet', required=True)
parser.add_argument('-d','--input', help='Input base document template file', required=True)
parser.add_argument('-e','--existingDB', help='Use existing database file', required=False)
parser.add_argument('-f','--dataField', help='Field name containing the record document template file', required=False)
parser.add_argument('-r','--dataRecord', help='Sheet field containing the record document template file', required=False)
parser.add_argument('-k','--key', help='The child document key field name', required=False)
parser.add_argument('-n','--addPageNumbers', help='Add page numbers to the output PDF file', required=False)
parser.add_argument('-o','--output', help='Output for the generated document file', required=True)
parser.add_argument('-s','--scope', help='The document scope', required=True)
parser.add_argument('-t','--type', help='The document type', required=True)
parser.add_argument('-p','--prefix', help='The document reference number prefix', required=False)
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
    # Use the global prefix:                                                   #
    #--------------------------------------------------------------------------#
    global ps
    global sRefPrefix
    ps = trange(1, desc='Initialise', leave=False)

    #--------------------------------------------------------------------------#
    # Get the document scope and type:                                         #
    #--------------------------------------------------------------------------#
    sDocScope = args['scope'].upper()
    sDocType = args['type'].upper()

    #--------------------------------------------------------------------------#
    # Get the input file and output generated document file path and name:     #
    #--------------------------------------------------------------------------#
    sInput = args['input']
    sOutput = args['output']

    #--------------------------------------------------------------------------#
    # Get the reference number prefix if any specified:                        #
    #--------------------------------------------------------------------------#
    sRefPrefix = ''
    if (not args['prefix'] is None):
        sRefPrefix = args['prefix']

    #--------------------------------------------------------------------------#
    # Get the code configuration workbook name and check it exists:            #
    #--------------------------------------------------------------------------#
    wbName = args['config']
    if not os.path.exists(wbName):
        errorHandler(errProc, errorCode.filenotExist, wbName)

    #--------------------------------------------------------------------------#
    # Get the flag for using the existing DB if it exists:                     #
    #--------------------------------------------------------------------------#
    bUseExistingDB = False
    bUseExistingDB = args['existingDB']

    #--------------------------------------------------------------------------#
    # Convert the configuration workbook to SQLite DB and exit if any error:   #
    #--------------------------------------------------------------------------#
    conn = xl2db(wbName, sOutput)
    if (conn is None):
        errorHandler(errProc, errorCode.cannotConnectDB, dbName)
    else:
        #----------------------------------------------------------------------#
        # Create the document and replace the data:                            #
        #----------------------------------------------------------------------#
        dataDocument(d) dgData.py -c $configFile -i $inputFile -o $outputFile -f $tag
        if [ $? -ne 0 ]; then
            echo FAIL $?
            exit 1
        else
            #------------------------------------------------------------------#
            # Renumber any reference tag numbers:                              #
            #------------------------------------------------------------------#
            python dgRefRenumber.py -d $outputFile -p RK
            python dgRefRenumber.py -d $outputFile -p CI
        fi
            . ./dgdo.sh $outputPath/$basename.$db $inputFile $outputPath/IT-DBA-2008.docx IT-DBA-2008
    if [ $? -ne 0 ]; then
        echo FAIL $?
        exit 1
    fi

    #--------------------------------------------------------------------------#
    # Create the remaining documents. No need to check any more errors         #
    # because if the first one worked then they all probably will:             #
    #--------------------------------------------------------------------------#
    . ./dgdo.sh $outputPath/$basename.$db $inputFile $outputPath/IT-DBA-2008.docx IT-DBA-2008 #N 1
    . ./dgdo.sh $outputPath/$basename.$db $inputFile $outputPath/ML-PWS-41.docx ML-PWS-41 #N 3
    . ./dgdo.sh $outputPath/$basename.$db $inputFile $outputPath/PM-C1-FIT-001.docx PM-C1-FIT-001 # Y 3
    . ./dgdo.sh $outputPath/$basename.$db $inputFile $outputPath/PM-P4-ACM-001.docx PM-P4-ACM-001 # N 4
    . ./dgdo.sh $outputPath/$basename.$db $inputFile $outputPath/PM-P2-PRD-001.docx PM-P2-PRD-001 # Y 4
    . ./dgdo.sh $outputPath/$basename.$db $inputFile $outputPath/IT-SYS-RMWH.docx IT-SYS-RMWH # Y 5
    . ./dgdo.sh $outputPath/$basename.$db $inputFile $outputPath/PM-F2-GIA-001.docx PM-F2-GIA-001 # Y 5
fi
