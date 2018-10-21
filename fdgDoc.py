#------------------------------------------------------------------------------#
#                   Copyright 2018 complianceSHORTCUTS.com                     #
#------------------------------------------------------------------------------#
# Class: gDoc                                                                  #
#                                                                              #
# Description:                                                                 #
# Creates a document object for the specified input file.                      #
#------------------------------------------------------------------------------#
# Calling Parameters:                                                          #
# fileInput             The input file to create as a document object.         #
# fileOutput            The output file to save the document to.               #
# docFilter             The document filter for the WHERE clause.              #
# docType               The document type.                                     #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      13-Apr-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
from enum import Enum
import os.path
import sys
from tqdm import trange
from docx import Document
import PyPDF2
import reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import subprocess
from shutil import copyfile
from contextlib import contextmanager
import traceback
import logging

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
    print(traceback.format_exception(*sys.exc_info()))
    sys.exit()

#------------------------------------------------------------------------------#
# Enumerate the error numbers and map the error messages:                      #
#------------------------------------------------------------------------------#
class errorCode(Enum):
    fileNotExist                       = -1
    pathNotExist                       = -2

errorMessage = {
    errorCode.fileNotExist             : 'Parent file @1 does not exist.',
    errorCode.pathNotExist             : 'Path @1 does not exist.'
}

#------------------------------------------------------------------------------#
# Function: silence_stdout                                                     #
#                                                                              #
# Description:                                                                 #
# Silences third party program output at the command line.                     #
#------------------------------------------------------------------------------#
@contextmanager
def silence_stdout():
    new_target = open(os.devnull, "w")
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target

#------------------------------------------------------------------------------#
# Class: gDoc                                                                  #
#------------------------------------------------------------------------------#
class gDoc(object):
    #--------------------------------------------------------------------------#
    # Constructor:                                                             #
    #--------------------------------------------------------------------------#
    def __init__(self, fileInput, fileOutput):
        #----------------------------------------------------------------------#
        # Define the procedure name:                                           #
        #----------------------------------------------------------------------#
        self.errProc = 'gDoc_init'

        #----------------------------------------------------------------------#
        # Make sure the input document file exists:                            #
        #----------------------------------------------------------------------#
        if not os.path.exists(fileInput):
            errorHandler(self.errProc, errorCode.fileNotExist, fileInput)

        #----------------------------------------------------------------------#
        # Create the document object:                                          #
        #----------------------------------------------------------------------#
        self.fileInput = fileInput
        self.fileInputName = os.path.basename(self.fileInput)
        self.fileInputBaseName = os.path.splitext(self.fileInputName)[0]
        self.fileInputDir = os.path.dirname(self.fileInput)
        self.document = Document(self.fileInput)

        #----------------------------------------------------------------------#
        # Set the output file characteristics:                                 #
        #----------------------------------------------------------------------#
        self.fileOutput = fileOutput
        self.fileOutputName = os.path.basename(self.fileOutput)
        self.fileOutputBaseName = os.path.splitext(self.fileOutputName)[0]
        self.fileOutputDir = os.path.dirname(self.fileOutput)
        if not os.path.exists(self.fileOutputDir):
            errorHandler(self.errProc, errorCode.pathNotExist, self.fileOutputDir)

        #----------------------------------------------------------------------#
        # Create the other document attributes:                                #
        #----------------------------------------------------------------------#
        self.cc = None
        self.dataBase = None
        self.dataRow = None
        self.dc = None
        self.docFilter = ''
        self.fileOutputPDF = ''
        self.filterKey = ''
        self.projectName = ''
        self.refNumber = 0
        self.rowCount = 0
        logging.info('Object ' + self.fileInputBaseName + ' created.')

    #--------------------------------------------------------------------------#
    # Function: appendPDF                                                      #
    #                                                                          #
    # Description:                                                             #
    # Appends one PDF file to the end of another.                              #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # dChild                 The child document object.                        #
    #--------------------------------------------------------------------------#
    def appendPDF(self, dChild):
        #----------------------------------------------------------------------#
        # Open the parent and child PDF documents:                             #
        #----------------------------------------------------------------------#
        pdfParent = open(self.fileOutputPDF, 'rb')
        pdfChild = open(dChild.fileOutputPDF, 'rb')

        #----------------------------------------------------------------------#
        # Create a new PDF file merger object:                                 #
        #----------------------------------------------------------------------#
        merger = PyPDF2.PdfFileMerger()

        #----------------------------------------------------------------------#
        # Append the child PDF content to the parent PDF document and save in  #
        # a new temporary document in the output directory:                    #
        #----------------------------------------------------------------------#
        merger.append(fileobj=pdfParent)
        merger.append(fileobj=pdfChild)
        sOutputPDF = self.fileOutputDir + '/p.pdf'
        merger.write(open(sOutputPDF, 'wb'))

        #----------------------------------------------------------------------#
        # Put the output file back to the main PDF output and delete the child #
        # record and other tepmorary files:                                    #
        #----------------------------------------------------------------------#
        os.remove(self.fileOutputPDF)
        copyfile(sOutputPDF, self.fileOutputPDF)
        os.remove(sOutputPDF)
        os.remove(dChild.fileOutputPDF)

    #--------------------------------------------------------------------------#
    # Function: docxDelete                                                     #
    #                                                                          #
    # Description:                                                             #
    # Deletes the output docx document.                                        #
    #--------------------------------------------------------------------------#
    def docxDelete(self):
        os.remove(self.fileOutput)

    #--------------------------------------------------------------------------#
    # Function: saveDocument                                                   #
    #                                                                          #
    # Description:                                                             #
    # Saves the docx document.                                                 #
    #--------------------------------------------------------------------------#
    def saveDocument(self):
        #----------------------------------------------------------------------#
        # Define the procedure name:                                           #
        #----------------------------------------------------------------------#
        self.errProc = 'saveDocument'

        #----------------------------------------------------------------------#
        # Save the output document:                                            #
        #----------------------------------------------------------------------#
        self.document.save(self.fileOutput)
        logging.info('Document ' + self.fileOutput + ' saved.')

    #--------------------------------------------------------------------------#
    # Function: printPDF                                                       #
    #                                                                          #
    # Description:                                                             #
    # Prints a docx document to a PDF document using libreoffice writer.       #
    #--------------------------------------------------------------------------#
    def printPDF(self):
        #----------------------------------------------------------------------#
        # Save the output document as PDF:                                     #
        #----------------------------------------------------------------------#
        output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf' ,
                                         '--outdir', self.fileOutputDir, self.fileOutput])
        with silence_stdout():
            print(output)
        self.fileOutputPDF = self.fileOutputDir + '/' + self.fileOutputBaseName + '.pdf'

    #--------------------------------------------------------------------------#
    # Function: pdfPageNumbers                                                 #
    #                                                                          #
    # Description:                                                             #
    # Adds page numbers to a PDF document.                                     #
    #--------------------------------------------------------------------------#
    def pdfPageNumbers(self):

        ps = trange(1, desc='Insert PDF page numbers...', leave=False)

        f = 't.pdf'
        os.rename(self.fileOutputPDF, f)
        pdfFile = open(f, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        pdfWriter = PyPDF2.PdfFileWriter()

        tmp = '_tmp.pdf'
        n = pdfReader.numPages

        for i in range(n):
            c = canvas.Canvas(tmp)
            c.setFont('Helvetica', 7)
            c.drawString((180)*mm, (276)*mm, 'Page ' + str(i + 1) + ' of ' + str(n))
            c.drawString((273)*mm, (197.5)*mm, 'Page ' + str(i + 1) + ' of ' + str(n))
            c.showPage()
            c.save()
            pageObj = pdfReader.getPage(i)
            pdfTmp = open(tmp, 'rb')
            pdfTmpReader = PyPDF2.PdfFileReader(pdfTmp)
            pageObj.mergePage(pdfTmpReader.getPage(0))
            os.remove(tmp)
            pdfWriter.addPage(pageObj)

            #----------------------------------------------------------------------#
            # Update the progress bar:                                             #
            #----------------------------------------------------------------------#
            pc = 1.0 / n
            ps.update(pc)
            ps.set_description('Numbering page ' + str(i))
            ps.refresh()

        ps.close()
        pdfOutputFile = open(self.fileOutputPDF, 'wb')
        pdfWriter.write(pdfOutputFile)
        pdfOutputFile.close()
        pdfFile.close()
        os.remove(f)
