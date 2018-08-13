#------------------------------------------------------------------------------#
#                   Copyright 2018 complianceSHORTCUTS.com                     #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file contains the shell script which creates a document from a sqlite   #
# database by searching and replacing the table field names as @@name@@ data   #
# placeholders within the document.                                            #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      30-Jul-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#------------------------------------------------------------------------------#
configFile=$1
inputFile=$2
outputPath=$3

#------------------------------------------------------------------------------#
# Output document file name:                                                   #
#------------------------------------------------------------------------------#
#outputPath=${outputFile%/*}
s=${configFile##*/}
basename=${s%.*}

#------------------------------------------------------------------------------#
# File extensions:                                                             #
#------------------------------------------------------------------------------#
xlsx='xlsx'
db='db'

#------------------------------------------------------------------------------#
# Convert the configuration workbook to SQLite DB and exit if any error:       #
#------------------------------------------------------------------------------#
python dgXL2DB.py -c $configFile.$xlsx -o $outputPath
if [ $? -ne 0 ]; then
    echo FAIL $?
    exit 1
else
    #--------------------------------------------------------------------------#
    # Create the first document and exit if any error:                         #
    #--------------------------------------------------------------------------#
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
