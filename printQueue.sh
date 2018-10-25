#!/bin/sh
#------------------------------------------------------------------------------#
#             Copyright 2018 Rieckermann Engineering Operations                #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file contains the cron job to check the print queue for queue batch     #
# report jobs every minute.                                                    #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      23-Oct-2018 NA        Initial design.                   #
#------------------------------------------------------------------------------#
# Set the base directory path:                                                 #
#------------------------------------------------------------------------------#
#pathBase='/mnt/dietpi_userdata'
pathBase='/media/dpaspa/dataSMS/dietpi_userdata'
printerName='MX-3640N'

#------------------------------------------------------------------------------#
# Check if any print jobs have been queued:                                    #
#------------------------------------------------------------------------------#
for fileName in $pathBase/queue/*; do
    #--------------------------------------------------------------------------#
    # Read the print queue job data from the file into local variables:        #
    #--------------------------------------------------------------------------#
    unset -v serialNumber procName pathData
    for var in serialNumber procName pathData; do
        IFS= read -r "$var" || break
    done < $fileName

    #--------------------------------------------------------------------------#
    # Get the process name from the index:                                     #
    #--------------------------------------------------------------------------#
    case procName in
        "0")
            procNameString = 'cipsip'
            ;;
        "1")
            procNameString = 'fill'
            ;;
        "2")
            procNameString = 'filter'
            ;;
        "3")
            procNameString = 'make'
            ;;
        *)
            echo 'invalid process index'
    esac

    #--------------------------------------------------------------------------#
    # Run the report:                                                          #
    #--------------------------------------------------------------------------#
    python $pathBase/py/fdg.py -c $pathBase/py/conf.xlsx -o $pathBase/report -i $pathBase/data/$pathData -n $procNameString -r Y -f $serialNumber
    if [ $? -ne 0 ]; then
        echo FAIL $?
        exit 1
    else
        #----------------------------------------------------------------------#
        # Print the report:                                                    #
        #----------------------------------------------------------------------#
        lp -d $printerName $fileName
        if [ $? -ne 0 ]; then
            echo FAIL $?
            exit 1
        else
            #------------------------------------------------------------------#
            # Delete the print queue job file now the report is printed:       #
            #------------------------------------------------------------------#
            rm $fileName
        fi
    fi
done
