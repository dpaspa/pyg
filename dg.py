#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
import argparse
import logging
logging.basicConfig(level=logging.DEBUG)

from dgRefRenumber import refRenumber
from dgProperty import setProperty

#------------------------------------------------------------------------------#
# Declare the application title and calling arguments help:                    #
#------------------------------------------------------------------------------#
appTitle = 'Document Generator'
appVersion = '1'
parser = argparse.ArgumentParser(description='Generates a document from a configuration spreadsheet and set of document templates')
parser.add_argument('-c','--config', help='Configuration spreadsheet', required=True)
parser.add_argument('-d','--input', help='Input base document template file', required=True)
