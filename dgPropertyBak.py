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
import argparse
import re
from enum import Enum
from docx import Document
import os.path
import sys
import traceback

import logging
logging.basicConfig(level=logging.DEBUG)

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
appTitle = 'Document Generator - Set document property'
appVersion = '1'
parser = argparse.ArgumentParser(description='Renumbers the reference numbers in a RefNum document')
parser.add_argument('-d','--document', help='Input document to renumber', required=True)
parser.add_argument('-p','--property', help='The document property to update', required=True)
parser.add_argument('-v','--value', help='The document property value to set', required=True)
args = vars(parser.parse_args())

#------------------------------------------------------------------------------#
# Declare global program variables:                                            #
#------------------------------------------------------------------------------#
sValue = ''

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
# Function main                                                                #
#                                                                              #
# Description:                                                                 #
# The main entry point for the program.                                        #
#------------------------------------------------------------------------------#
# Calling Attributes:                                                          #
# gDoc                  The generic document object.                           #
#------------------------------------------------------------------------------#
def setProperty(gDoc):
    #--------------------------------------------------------------------------#
    # Define the procedure name:                                               #
    #--------------------------------------------------------------------------#
    errProc = setProperty.__name__

    #--------------------------------------------------------------------------#
    # Use the global value:                                                    #
    #--------------------------------------------------------------------------#
    global sValue

    #--------------------------------------------------------------------------#
    # Get the calling arguments:                                               #
    #--------------------------------------------------------------------------#
    sDocument = args['document']
    sProperty = args['property']
    sValue = args['value']

    #--------------------------------------------------------------------------#
    # Open the document object:                                                #
    #--------------------------------------------------------------------------#
    d = gDoc(sDocument)

    #--------------------------------------------------------------------------#
    # Set the document property:                                               #
    #--------------------------------------------------------------------------#
    d.setProperty(sProperty)

    #--------------------------------------------------------------------------#
    # Save the document:                                                       #
    #--------------------------------------------------------------------------#
    d.document.save(d.inputFile)

    #--------------------------------------------------------------------------#
    # Output a success message:                                                #
    #--------------------------------------------------------------------------#
    print('Congratulations! Document property ' + sProperty + ' successfully set to ' + sValue)

#------------------------------------------------------------------------------#
# Class: gDoc                                                                  #
#                                                                              #
# Description:                                                                 #
# Opens the specified document as an object.                                   #
#------------------------------------------------------------------------------#
# Calling Attributes:                                                          #
# inputFile             The input template file name to use for the document.  #
#------------------------------------------------------------------------------#
class gDoc(object):
    #--------------------------------------------------------------------------#
    # Constructor:                                                             #
    #--------------------------------------------------------------------------#
    def __init__(self, inputFile):
        #----------------------------------------------------------------------#
        # Define the procedure name:                                           #
        #----------------------------------------------------------------------#
        self.errProc = 'gDoc'

        #----------------------------------------------------------------------#
        # Make sure the input document file exists:                            #
        #----------------------------------------------------------------------#
        if not os.path.exists(inputFile):
            errorHandler(self.errProc, errorCode.fileNotExist, inputFile)

        #----------------------------------------------------------------------#
        # Set the instance attributes:                                         #
        #----------------------------------------------------------------------#
        self.inputFile = inputFile

        #----------------------------------------------------------------------#
        # Open the input document:                                             #
        #----------------------------------------------------------------------#
        self.document = Document(self.inputFile)

    #--------------------------------------------------------------------------#
    # Function: setProperty                                                    #
    #                                                                          #
    # Description:                                                             #
    # Sets the core document property.                                         #
    #--------------------------------------------------------------------------#
    def comments(self):
        global sValue
        self.document.core_properties.comments = sValue

    def subject(self):
        global sValue
        self.document.core_properties.subject = sValue

    def title(self):
        global sValue
        self.document.core_properties.title = sValue

    def setProperty(self, argument):
        switcher = {
            "comments": self.comments,
            "subject": self.subject,
            "title": self.title
        }

        # Get the function from switcher dictionary
        func = switcher.get(argument, lambda: "Invalid property")

        # Execute the function
        func()

#------------------------------------------------------------------------------#
# Call the main function:                                                      #
#------------------------------------------------------------------------------#
setProperty()
