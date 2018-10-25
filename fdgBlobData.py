#------------------------------------------------------------------------------#
#            Copyright 2018 Rieckermann Engineering Operations                 #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file is used to reduce huge ascii files to a manageable size.           #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      04-Oct-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
from enum import Enum
import os.path
import sys

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
    sys.exit()

#------------------------------------------------------------------------------#
# Enumerate the error numbers and map the error messages:                      #
#------------------------------------------------------------------------------#
class errorCode(Enum):
    noSearchTerm                       = -1
    noTimeBegin                        = -2
    noTimeEnd                          = -3

errorMessage = {
    errorCode.noSearchTerm             : 'Search term @1 not found',
    errorCode.noTimeBegin              : 'Begin mark @1 not found',
    errorCode.noTimeEnd                : 'End mark @1 not found'
}

#------------------------------------------------------------------------------#
# Function findnth                                                             #
#                                                                              #
# Description:                                                                 #
# Find the nth occurrence of one string within another string.                 #
#------------------------------------------------------------------------------#
def findnth(string, substring, n):
    parts = string.split(substring, n + 1)
    if (len(parts) <= n + 1):
        return -1
    return len(string) - len(parts[-1]) - len(substring)

#------------------------------------------------------------------------------#
# Class: blobData                                                              #
#------------------------------------------------------------------------------#
class blobData(object):
    #--------------------------------------------------------------------------#
    # Constructor:                                                             #
    #--------------------------------------------------------------------------#
    def __init__(self, fileInput):
        #----------------------------------------------------------------------#
        # Define the procedure name:                                           #
        #----------------------------------------------------------------------#
        self.errProc = 'blobData_init'

        #----------------------------------------------------------------------#
        # Set the marker properties:                                           #
        #----------------------------------------------------------------------#
        self.dataFilter = ''
        self.markerSearchBegin = ''
        self.markerSearchEnd = ''

        #----------------------------------------------------------------------#
        # Make sure the input document file exists:                            #
        #----------------------------------------------------------------------#
        if not os.path.exists(fileInput):
            errorHandler(self.errProc, errorCode.fileNotExist, fileInput)

        #----------------------------------------------------------------------#
        # Load the whole text file in RAM at once. Don't read line by line:    #
        #----------------------------------------------------------------------#
        with open(fileInput, 'r') as fileContent:
            self.content = fileContent.read()

    #--------------------------------------------------------------------------#
    # Function: getTime                                                        #
    #                                                                          #
    # Description:                                                             #
    # Gets the time stampe of the marker search string:                        #
    #--------------------------------------------------------------------------#
    # Calling Parameters:                                                      #
    # markerSearchString    The marker event search string.                    #
    #--------------------------------------------------------------------------#
    def getTime(self, markerSearchString):
        #----------------------------------------------------------------------#
        # Define the procedure name:                                           #
        #----------------------------------------------------------------------#
        self.errProc = 'getTime'

        #----------------------------------------------------------------------#
        # Get the search term position:                                        #
        #----------------------------------------------------------------------#
        s = markerSearchString.replace('@@FILTER@@', str(self.dataFilter))
        posBegin = self.getMarkerPosition(s, True)
        posEnd = self.content.find('\n', posBegin)
        s = self.content[posBegin:posEnd]
        posTime = findnth(s, ',', 13)
        return s[posTime + 1:16]

    #--------------------------------------------------------------------------#
    # Function: setMarker                                                      #
    #                                                                          #
    # Description:                                                             #
    # Sets the marker name and search string:                                  #
    #--------------------------------------------------------------------------#
    # Calling Parameters:                                                      #
    # markerName            The maker name.                                    #
    # markerSearchString    The marker event search string.                    #
    #--------------------------------------------------------------------------#
    def setMarker(self, markerName, markerSearchString):
        #----------------------------------------------------------------------#
        # Define the procedure name:                                           #
        #----------------------------------------------------------------------#
        self.errProc = 'setMarker'

        #----------------------------------------------------------------------#
        # Get the search term position:                                        #
        #----------------------------------------------------------------------#
        if (markerName[:5].upper() == 'BEGIN'):
            self.markerSearchBegin = markerSearchString.replace('@@FILTER@@', str(self.dataFilter))
        else:
            self.markerSearchEnd = markerSearchString.replace('@@FILTER@@', str(self.dataFilter))

    #--------------------------------------------------------------------------#
    # Function: getMarkerPosition                                              #
    #                                                                          #
    # Description:                                                             #
    # Gets a marker string based on a search term and returns the position in  #
    # the file.                                                                #
    #--------------------------------------------------------------------------#
    # Calling Parameters:                                                      #
    # searchMarker          The search term to find the marker.                #
    # bBegin                True if begin marker.                              #
    #--------------------------------------------------------------------------#
    def getMarkerPosition(self, searchMarker, bBegin):
        #----------------------------------------------------------------------#
        # Define the procedure name:                                           #
        #----------------------------------------------------------------------#
        self.errProc = 'getMarkerPosition'

        #----------------------------------------------------------------------#
        # Get the search term position:                                        #
        #----------------------------------------------------------------------#
        posMarker = self.content.find(searchMarker)

        #----------------------------------------------------------------------#
        # Error if search term not found:                                      #
        #----------------------------------------------------------------------#
        if (posMarker == -1):
            errorHandler(self.errProc, errorCode.noSearchTerm, searchMarker)

        #----------------------------------------------------------------------#
        # Check if a begin marker:                                             #
        #----------------------------------------------------------------------#
        elif (bBegin):
            #------------------------------------------------------------------#
            # Update the begin to the start of the found line:                 #
            #------------------------------------------------------------------#
            posMarker = self.content.rfind('\n', 0, posMarker) + 1
        else:
            #------------------------------------------------------------------#
            # Update the end marker to the end of the previous line:           #
            #------------------------------------------------------------------#
            posMarker = self.content.find('\n', posMarker) - 1

        #----------------------------------------------------------------------#
        # Return the found position:                                           #
        #----------------------------------------------------------------------#
        return posMarker

    #--------------------------------------------------------------------------#
    # Function: extractData                                                    #
    #                                                                          #
    # Description:                                                             #
    # Extracts data from an ASCII file between two specified markers.          #
    #--------------------------------------------------------------------------#
    # Calling Parameters:                                                      #
    # fileName              The filename to extract the data to.               #
    #--------------------------------------------------------------------------#
    def extractData(self, fileName):
        #----------------------------------------------------------------------#
        # Define the procedure name:                                           #
        #----------------------------------------------------------------------#
        self.errProc = 'extractData'

        #----------------------------------------------------------------------#
        # Get the begin and end marker positions:                              #
        #----------------------------------------------------------------------#
        posBegin = self.getMarkerPosition(self.markerSearchBegin, True)
        posEnd = self.getMarkerPosition(self.markerSearchEnd, False)

        #----------------------------------------------------------------------#
        # Get the title from the first row:                                    #
        #----------------------------------------------------------------------#
        posMarker = self.content.find('\n', 1)
        titleRow = self.content[:posMarker]

        #----------------------------------------------------------------------#
        # Save the extracted data:                                             #
        #----------------------------------------------------------------------#
        fileOutput = open(fileName, 'w')
        fileOutput.write(titleRow + '\n' + self.content[posBegin:posEnd])
        fileOutput.close()
