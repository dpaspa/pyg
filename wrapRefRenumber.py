#------------------------------------------------------------------------------#
#                   Copyright 2019 complianceSHORTCUTS.com                     #
#------------------------------------------------------------------------------#
# Wrapper for renumbering reference numbers.                                   #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      23-Jan-2019 NA        Initial design.                   #
#------------------------------------------------------------------------------#
import argparse
import fdgDoc
import fdgRefNumber

#------------------------------------------------------------------------------#
# Process command line arguments:                                              #
#------------------------------------------------------------------------------#
parser = argparse.ArgumentParser(description='Renumbers reference numbers')
parser.add_argument('-i','--inputFile', help='Input document file to renumber', required=True)
parser.add_argument('-p','--prefix', help='The reference number prefixes', required=True)
args = vars(parser.parse_args())
inputFile = args['inputFile']
prefixes = args['prefix']

#------------------------------------------------------------------------------#
# Create a document object and perform the function:                           #
#------------------------------------------------------------------------------#
d = fdgDoc.gDoc(inputFile, inputFile)
fdgRefNumber.refRenumber(d, prefixes, 1)
d.saveDocument()
