#------------------------------------------------------------------------------#
#                   Copyright 2018 complianceSHORTCUTS.com                     #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file creates document from a sqlite database by searching and replacing #
# the table field names as @@name@@ data placeholders within the document.     #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 2   David Paspa      27-Jul-2018 NA        Split from document generator     #
#                                            into separate module. Added       #
#                                            multiple prefix handling.         #
# 1   David Paspa      13-Apr-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
from enum import Enum
import sys
from docx import Document
import traceback
import logging
logging.basicConfig(filename='fdg.log',level=logging.DEBUG)

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
    print('ERROR ' + str(eCode) + ' in Procedure ' + "'" + errProc + "'" + '\r\n' + '\r\n' + sMsg)
    print('\r\n')
#    print(traceback.format_exception(*sys.exc_info()))
    sys.exit()

#------------------------------------------------------------------------------#
# Enumerate the error numbers and map the error messages:                      #
#------------------------------------------------------------------------------#
class errorCode(Enum):
    fileNotExist                       = -1
    noPrefixFound                      = -2
    pathNotExist                       = -3

errorMessage = {
    errorCode.fileNotExist             : 'Document file @1 does not exist.',
    errorCode.noPrefixFound            : 'No reference numbers found with the specified prefix @1.',
    errorCode.pathNotExist             : 'Path @1 does not exist.'
}

#------------------------------------------------------------------------------#
# Named functions to set the individual core document property value:          #
#------------------------------------------------------------------------------#
def comments(d, sValue):
    d.document.core_properties.comments = sValue

def keywords(d, sValue):
    d.document.core_properties.keywords = sValue

def subject(d, sValue):
    d.document.core_properties.subject = sValue

def title(d, sValue):
    d.document.core_properties.title = sValue

#------------------------------------------------------------------------------#
# Function: setProperty                                                        #
#                                                                              #
# Description:                                                                 #
# The main entry point for the program.                                        #
#------------------------------------------------------------------------------#
# Calling Parameters:                                                          #
# d                     The generic document object.                           #
# sProperty             The property name to set.                              #
# sValue                The value to set the property to.                      #
#------------------------------------------------------------------------------#
def setProperty(d, sProperty, sValue):
    #--------------------------------------------------------------------------#
    # Define the procedure name:                                               #
    #--------------------------------------------------------------------------#
    errProc = setProperty.__name__

    #--------------------------------------------------------------------------#
    # Define the function switcher for the property name:                      #
    #--------------------------------------------------------------------------#
    switcher = {
        "COMMENTS": comments,
        "KEYWORDS": keywords,
        "SUBJECT": subject,
        "TITLE": title
    }

    #--------------------------------------------------------------------------#
    # Get the function name from switcher dictionary:                          #
    #--------------------------------------------------------------------------#
    func = switcher.get(sProperty, lambda: "Invalid property")

    #--------------------------------------------------------------------------#
    # Execute the function:                                                    #
    #--------------------------------------------------------------------------#
    func(d, sValue)

    #--------------------------------------------------------------------------#
    # Output a success message:                                                #
    #--------------------------------------------------------------------------#
    logging.info('Document property ' + sProperty + ' set to ' + sValue)
