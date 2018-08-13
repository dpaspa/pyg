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
outputFile=$3
tag=$4

#------------------------------------------------------------------------------#
# Create the document and replace the data:                                    #
#------------------------------------------------------------------------------#
python dgData.py -c $configFile -i $inputFile -o $outputFile -f $tag
if [ $? -ne 0 ]; then
    echo FAIL $?
    exit 1
else
    #--------------------------------------------------------------------------#
    # Renumber any reference tag numbers:                                      #
    #--------------------------------------------------------------------------#
    python dgRefRenumber.py -d $outputFile -p RK
    python dgRefRenumber.py -d $outputFile -p CI
fi
