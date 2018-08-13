#------------------------------------------------------------------------------#
#            Copyright 2018 Rieckermann Engineering Operations                 #
#------------------------------------------------------------------------------#
# Description:                                                                 #
# This file stores the rather verbose SQL query strings for the code           #
# generator application.                                                       #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Ver By               Date        CC        Note                              #
# 1   David Paspa      08-Apr-2018 NA        Split out from cg.py.             #
#------------------------------------------------------------------------------#
# Import the python libraries:                                                 #
#------------------------------------------------------------------------------#
from enum import Enum

#------------------------------------------------------------------------------#
# Enumerate the SQL query string numbers and map the query strings:            #
#------------------------------------------------------------------------------#
class sqlCode(Enum):
    createIndexFileCount               = -1
    createIndexFile                    = -2
    createClass                        = -3
    createClassesBlock                 = -7434
    createClassesForLevel              = -4
    createClassesGlobal                = -5
    createClassNone                    = -6
    createCM                           = -403
    createEM                           = -404
    createUN                           = -405
    createPC                           = -406
    createInstances                    = -7
    createInstanceAlarmsGlobal         = -8889
    createInstancesAll                 = -1237
    createInstancesForeign             = -8888
    createInstancesGlobal              = -8
    xferInstancesGlobal                = -9
    createSFCGlobal                    = -888
    numInstances                       = -10
    GLOBAL_INSTANCE                    = -11
    createLevel                        = -12
    createLevelsGlobal                 = -13
    createParameterSFC                 = -14
    createProgramFiles                 = -15
    createProgramFilesCount            = -20
    defaultParameters                  = -21
    documentInfo                       = -22
    checkIfClassParameter              = -2323
    checkIfChildParameter              = -23
    checkIfLinkParameter               = -24
    checkIfSelectionParameter          = -2224
    getChildIndex                      = -25
    checkGlobalParameterExists         = -27
    updateParameterOperation           = -3228
    insertGlobalParameters             = -28
    insertEventPrompt                  = -1326
    insertEventLogMsg                  = -1327
    insertEventLogReal                 = -1328
    insertEventLogTime                 = -1329
    updateEventPrompt                  = -1426
    updateEventLogMsg                  = -1427
    updateEventLogReal                 = -1428
    updateEventLogTime                 = -1429
    addParametersClass                 = -29
    getClassChildren                   = -30
    addParametersSFC                   = -31
    getChildParameters                 = -1732
    getDeferredParameters              = -1733
    processLevel                       = -40
    processLevelCount                  = -41
    tblCreateGlobalParameter           = -42
    tblCreateEventPrompt               = -7142
    tblCreateEventLogMsg               = -7143
    tblCreateEventLogReal              = -7144
    tblCreateEventLogTime              = -7145
    tblCreateEventDataReal             = -7146
    tblCreateEventDataTime             = -7147
    versionHistory                     = -43
    VERHIST                            = -44
    ANALOG                             = -45
    ANALOG_EMBED                       = -46
    callList                           = -47
    callListExists                     = -48
    callListExistsGlobal               = -49
    callListExistsCRIL                 = -50
    callListExistsNCRIL                = -60
    callListExistsXfer                 = -61
    CHILD                              = -62
    CHILD_ACQUIRE                      = -63
    CHILD_CASCADE                      = -64
    CHILD_ACQUIRED                     = -65
    CHILD_ACQUIRE_REQ                  = -66
    CHILD_ACQUIRE_NREQ                 = -67
    CHILD_BIND                         = -68
    CHILD_INDEX_MAX                    = -69
    CHILD_INIT_COMMAND_TRUE            = -70
    CHILD_INIT_COMMAND_FALSE           = -71
    CHILD_INSTANCE                     = -72
    CHILD_INSTANCE_BIND                = -73
    CHILD_SELECT                       = -713
    pChildSelect                       = -714
    pChildSelectExists                 = -715
    CRIL                               = -74
    CRIL_EXISTS                        = -75
    CRIL_INSTANCE                      = -76
    CRIL_INSTANCE_NUM                  = -77
    CRIL_NUM                           = -78
    CRIL_TARGET                        = -79
    NCRIL                              = -80
    NCRIL_EXISTS                       = -81
    NCRIL_INSTANCE                     = -82
    NCRIL_INSTANCE_NUM                 = -83
    NCRIL_NUM                          = -84
    NCRIL_TARGET                       = -85
    HYGIENE                            = -86
    FLOWPATH                           = -686
    INSTANCE_ALL                       = -87
    INSTANCE_BLK                       = -88
    INSTANCE_BLK_ALL                   = -7188
    INSTANCE_SFC                       = -89
    ISOWNED                            = -901
    LINK                               = -902
    LINK_BLK                           = -90
    LINK_BLK_Define                    = -91
    pLink                              = -92
    pLinkExists                        = -93
    pLinkInput                         = -94
    pLinkInputMC                       = -95
    pLinkOutput                        = -96
    pLinkOutputMC                      = -97
    UNIQUEID                           = -98
    PARAMETER_INDEX_MAX                = -99
    PARENT                             = -100
    PARENTBLK                          = -101
    PARENTDATA                         = -731
    PARENTEM                           = -102
    PARM_CHILD_VAR_INPUT               = -103
    PARM_CHILD_VAR_OUTPUT              = -104
    PARM_CHILD_VAR_IN_OUT              = -105
    PARM_INSTANCE_VAR_INPUT            = -106
    PARM_INSTANCE_VAR_OUTPUT           = -107
    PARM_INSTANCE_VAR_IN_OUT           = -108
    PARM_INSTANCE_VAR                  = -109
    PARM_CLASS_VAR_INPUT               = -110
    PARM_CLASS_VAR_IN_OUT              = -111
    PARM_CLASS_VAR_OUTPUT              = -120
    RECIPE                             = -121
    RECIPE_CLASS                       = -122
    RECIPE_INSTANCE                    = -123
    RECIPE_PARAMETERS                  = -124
    REQUIREMENT                        = -125
    SCOPE                              = -126
    SELECT                             = -127
    SELVALUE                           = -128
    SFC                                = -129
    SFCExists                          = -230
    STATE                              = -130
    STATE_TIMER                        = -131
    SETPOINT                           = -132
    OUTPUT                             = -133
    TAGS                               = -134
    TAGALARMS                          = -135
    TAGSALT                            = -136
    TIMER                              = -137
    TRANSITION                         = -138
    getSFCBlockParameters              = -139
#    pBLOCK_READ                        = -140
#    pBLOCK_WRITE                       = -141
    pBLOCK_RECIPE                      = -131
    pBLOCK_RECIPE_EXISTS               = -142
#    pCHILD_NotMC                       = -143
    pBlock                             = -144
    pBlockIN                           = -145
    pBlockIN_OUT                       = -146
    pBlockOUT                          = -147
#    pChildDefine                       = -148
#    pChildInput                        = -149
#    pChildOutput                       = -150
#    pChildIN                           = -151
#    pChildIN_OUT                       = -152
#    pChildOUT                          = -153
#    pClass                             = -154
    pClassBlockRead                    = -155
    pClassBlockWrite                   = -156
#    pClassIN                           = -157
#    pClassIN_OUT                       = -158
#    pClassOUT                          = -160
    pClassSFC                          = -161
#    pSFC                               = -162
    pSFCLink                           = -163
#    pSFCLinkOutput                     = -164
    pChildRead                         = -301
    pChildReadBool                     = -302
    pChildReadDefine                   = -303
    pChildWrite                        = -304
    pChildWriteBool                    = -305
    pChildWriteDefine                  = -306
    pParentRead                        = -307
    pParentReadBool                    = -308
    pParentWrite                       = -309
    pParentWriteBool                   = -310
    pSFCChild                          = -311
#    pSFCChildWrite                     = -307
#    pSFCGrandChild                     = -309
    pSFCChildMC                        = -312
#    pSFCChildMCWrite                   = -311
    pSFCChildExists                    = -313
#    pSFCChildWriteExists               = -313
#    pSFCGrandChildExists               = -314
    pSFCChildMCExists                  = -314
#    pSFCChildMCWriteExists             = -316
    pSFCSelectMC                       = -315
#    pSFCSelectMCWrite                  = -318
    pSFCParametersRecipe               = -319
    pSFCParametersRecipeExist          = -320
    pSFCParametersBlock                = -2321
#    pSFCParametersBlockWrite           = -2322
    pEventExists                       = -179
    pEventConfirm                      = -175
    pEventPrompt                       = -176
#    pEventLogMsg                       = -177
    pEventLogReal                      = -180
    pEventLogTime                      = -181
    pEventDataReal                     = -182
    pEventDataTime                     = -183
    pEventConfirmExists                = -184
    pEventPromptExists                 = -185
    pEventLogRealExists                = -187
    pEventLogTimeExists                = -188
    pEventDataRealExists               = -189
    pEventDataTimeExists               = -200
    pEventConfirmNoExists              = -201
    pEventConfirmAll                   = -202
    pEventPromptAll                    = -203
#    pEventLogMsgAll                    = -204
    pEventLogRealAll                   = -205
    pEventLogTimeAll                   = -206
    pEventConfirmNum                   = -209
    pEventPromptNum                    = -220
#    pEventLogMsgNum                    = -221
    pEventLogRealNum                   = -222
    pEventLogTimeNum                   = -223
    pEventDataLogMatch                 = -4223
    pEventDataValueMatch               = -4224
    pSyncRead                          = -5101
    pSyncWrite                         = -5102
    numChildren                        = -8001
    numReadBool                        = -8002
    numReadInt                         = -8003
    numReadReal                        = -8004
    numReadTime                        = -8005
    numWriteBool                       = -8005
    numWriteInt                        = -8007
    numWriteReal                       = -8008
    numWriteTime                       = -8009
    pReadBool                          = -9001
    pReadInt                           = -9002
    pReadReal                          = -9003
    pReadTime                          = -9004
    pWriteBool                         = -9005
    pWriteInt                          = -9006
    pWriteReal                         = -9007
    pWriteTime                         = -9008
    pEventLogMsgClass                  = -7171
    pEventLogMsgExists                 = -7172
    pEventLogMsgInstance               = -7173
    pEventLogMsgMaxClass               = -7174
    pEventLogMsgMaxInstance            = -7175
    pEventLogMsgWordClass              = -7176
    pEventLogMsgWordInstance           = -7177
    pEventLogMsgWordBitClass           = -7178
    pEventLogMsgWordBitInstance        = -7179
    simulateDI1                        = -9701
    simulateDI2                        = -9702
    simulatePOS2                       = -9703
    simulatePOS4                       = -9704
    simulateZSC1                       = -9705
    simulateZSC2                       = -9706

prm = {
    sqlCode.ANALOG                     : ['gInstance'],
    sqlCode.ANALOG_EMBED               : ['gInstance'],
    sqlCode.callList                   : ['gLevel'],
    sqlCode.callListExists             : ['gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.callListExistsGlobal       : ['gClass'],
    sqlCode.callListExistsCRIL         : [],
    sqlCode.callListExistsNCRIL        : [],
    sqlCode.callListExistsXfer         : ['gClass'],
    sqlCode.createClass                : ['gClass'],
    sqlCode.createClassNone            : [],
    sqlCode.createClassesBlock         : [],
    sqlCode.createClassesForLevel      : ['gLevel'],
    sqlCode.createClassesGlobal        : [],
    sqlCode.createCM                   : [],
    sqlCode.createEM                   : [],
    sqlCode.createUN                   : [],
    sqlCode.createPC                   : [],
#    sqlCode.createInstances            : ['gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent', 'gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent', 'gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.createInstances            : ['gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.createInstanceAlarmsGlobal : [],
    sqlCode.createInstancesAll         : [],
    sqlCode.createInstancesForeign     : ['gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.createInstancesGlobal      : ['gClass'],
    sqlCode.xferInstancesGlobal        : ['gClass'],
    sqlCode.createSFCGlobal            : [],
#    sqlCode.numInstances               : ['gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.numInstances               : ['gClass'],
    sqlCode.createLevel                : ['gLevel'],
    sqlCode.createLevelsGlobal         : [],
    sqlCode.CHILD                      : ['gClass', 'gClass', 'gClass'],
    sqlCode.CHILD_ACQUIRE              : ['gClass'],
    sqlCode.CHILD_CASCADE              : ['gClass'],
    sqlCode.CHILD_ACQUIRED             : ['gClass', 'gState'],
    sqlCode.CHILD_ACQUIRE_REQ          : ['gClass', 'gState'],
    sqlCode.CHILD_ACQUIRE_NREQ         : ['gClass', 'gState'],
    sqlCode.CHILD_BIND                 : ['gClass', 'gState'],
    sqlCode.CHILD_INDEX_MAX            : ['gClass'],
    sqlCode.CHILD_INIT_COMMAND_TRUE    : ['gClass', 'gState'],
    sqlCode.CHILD_INIT_COMMAND_FALSE   : ['gClass', 'gState'],
    sqlCode.CHILD_INSTANCE             : ['gInstance', 'gParent', 'gParent', 'gParent', 'gClass', 'gClass'],
    sqlCode.CHILD_INSTANCE_BIND        : ['gInstance', 'gParent', 'gParent', 'gParent', 'gClass', 'gState'],
    sqlCode.CHILD_SELECT               : ['gClass'],
    sqlCode.pChildSelect               : ['gClass'],
    sqlCode.pChildSelectExists         : ['gClass'],
    sqlCode.CRIL                       : [],
    sqlCode.CRIL_EXISTS                : ['gInstance'],
    sqlCode.CRIL_INSTANCE              : ['gInstance'],
    sqlCode.CRIL_INSTANCE_NUM          : ['gInstance'],
    sqlCode.CRIL_NUM                   : [],
    sqlCode.CRIL_TARGET                : ['gInstance'],
    sqlCode.NCRIL                      : [],
    sqlCode.NCRIL_EXISTS               : ['gInstance'],
    sqlCode.NCRIL_INSTANCE             : ['gInstance'],
    sqlCode.NCRIL_INSTANCE_NUM         : ['gInstance'],
    sqlCode.NCRIL_NUM                  : [],
    sqlCode.NCRIL_TARGET               : ['gInstance'],
    sqlCode.GLOBAL_INSTANCE            : ['gClass'],
    sqlCode.FLOWPATH                   : ['gClass'],
    sqlCode.HYGIENE                    : ['gClass'],
    sqlCode.INSTANCE_ALL               : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.INSTANCE_BLK               : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.INSTANCE_BLK_ALL           : [],
    sqlCode.INSTANCE_SFC               : [],
    sqlCode.ISOWNED                    : ['gInstance'],
    sqlCode.LINK                       : ['gInstance'],
    sqlCode.LINK_BLK                   : ['gInstance'],
    sqlCode.LINK_BLK_Define            : ['gClass'],
    sqlCode.pLink                      : ['gClass'],
    sqlCode.pLinkExists                : ['gClass'],
    sqlCode.pLinkInput                 : ['gInstance', 'gState'],
    sqlCode.pLinkInputMC               : ['gInstance', 'gState'],
    sqlCode.pLinkOutput                : ['gInstance', 'gState'],
    sqlCode.pLinkOutputMC              : ['gInstance', 'gState'],
    sqlCode.UNIQUEID                   : [],
    sqlCode.PARAMETER_INDEX_MAX        : ['gClass'],
    sqlCode.PARENT                     : [],
    sqlCode.PARENTBLK                  : [],
    sqlCode.PARENTDATA                 : [],
    sqlCode.PARENTEM                   : [],
    sqlCode.RECIPE                     : [],
    sqlCode.RECIPE_CLASS               : [],
    sqlCode.RECIPE_INSTANCE            : ['gInstance'],
    sqlCode.RECIPE_PARAMETERS          : [],
#    sqlCode.PARM_CLASS_VAR_INPUT             : ['gClass'],
#    sqlCode.PARM_CLASS_VAR_IN_OUT            : ['gClass'],
#    sqlCode.PARM_CLASS_VAR_OUTPUT            : ['gClass'],
#    sqlCode.PARM_INSTANCE_VAR_INPUT    : ['gInstance'],
#    sqlCode.PARM_INSTANCE_VAR_IN_OUT   : ['gInstance'],
#    sqlCode.PARM_INSTANCE_VAR_OUTPUT   : ['gInstance'],
#    sqlCode.PARM_INSTANCE_VAR          : ['gInstance'],
    sqlCode.SELECT                     : ['gClass'],
    sqlCode.SELVALUE                   : ['gClass', 'gSelectParameter', 'gSelectSelection'],
    sqlCode.SFC                        : ['gClass'],
    sqlCode.SFCExists                  : ['gClass'],
    sqlCode.STATE                      : ['gClass'],
    sqlCode.STATE_TIMER                : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.SETPOINT                   : [],
    sqlCode.OUTPUT                     : [],
    sqlCode.TAGS                       : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.TAGALARMS                  : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.TAGSALT                    : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.TIMER                      : ['gClass'],
    sqlCode.pEventExists               : ['gClass'],
    sqlCode.pEventConfirm              : ['gClass'],
    sqlCode.pEventPrompt               : ['gClass', 'gClass'],
#    sqlCode.pEventLogMsg               : ['gClass'],
    sqlCode.pEventLogReal              : ['gClass', 'gClass'],
    sqlCode.pEventLogTime              : ['gClass', 'gClass'],
    sqlCode.pEventDataReal             : ['gClass'],
    sqlCode.pEventDataTime             : ['gClass'],
    sqlCode.pEventConfirmExists        : ['gClass'],
    sqlCode.pEventPromptExists         : ['gClass'],
    sqlCode.pEventLogRealExists        : ['gClass'],
    sqlCode.pEventLogTimeExists        : ['gClass'],
    sqlCode.pEventDataRealExists       : ['gClass'],
    sqlCode.pEventDataTimeExists       : ['gClass'],
    sqlCode.pEventConfirmNoExists      : ['gClass', 'gChildParameter'],
    sqlCode.pEventConfirmAll           : [],
    sqlCode.pEventPromptAll            : [],
#    sqlCode.pEventLogMsgAll            : [],
    sqlCode.pEventLogRealAll           : [],
    sqlCode.pEventLogTimeAll           : [],
    sqlCode.pEventConfirmNum           : [],
    sqlCode.pEventPromptNum            : [],
#    sqlCode.pEventLogMsgNum            : [],
    sqlCode.pEventLogRealNum           : [],
    sqlCode.pEventLogTimeNum           : [],
    sqlCode.pEventDataLogMatch         : ['gSFC', 'gChildParameter'],
    sqlCode.pEventDataValueMatch       : ['gSFC', 'gChildParameter'],
    sqlCode.pSyncRead                  : ['gChildClass', 'gClass', 'gChildClass', 'gChildClass', 'gChildClass'],
    sqlCode.pSyncWrite                 : ['gChildClass', 'gClass', 'gChildClass', 'gChildClass', 'gChildClass'],
#    sqlCode.pChildDefine               : ['gClass'],
#    sqlCode.pChildInput                : ['gClass', 'gAlias'],
#    sqlCode.pChildOutput               : ['gClass', 'gAlias'],
#    sqlCode.pChildIN                   : ['gClass'],
#    sqlCode.pChildIN_OUT               : ['gClass'],
#    sqlCode.pChildOUT                  : ['gClass'],
#    sqlCode.pClass                     : ['gClass'],
    sqlCode.pClassBlockRead            : ['gClass'],
    sqlCode.pClassBlockWrite           : ['gClass'],
#    sqlCode.pClassIN                   : ['gClass'],
#    sqlCode.pClassIN_OUT               : ['gClass'],
#    sqlCode.pClassOUT                  : ['gClass'],
#    sqlCode.pSFCListIN                 : ['gSFC'],
#    sqlCode.pSFCListIN_OUT             : ['gSFC'],
#    sqlCode.pSFCListOUT                : ['gSFC'],
    sqlCode.pClassSFC                  : ['gClass'],
    sqlCode.pChildRead                 : ['gClass', 'gAlias'],
    sqlCode.pChildReadBool             : ['gClass', 'gAlias'],
    sqlCode.pChildWrite                : ['gClass', 'gAlias'],
    sqlCode.pChildWriteBool            : ['gClass', 'gAlias'],
    sqlCode.pChildReadDefine           : ['gClass'],
    sqlCode.pChildWriteDefine          : ['gClass'],
    sqlCode.pParentRead                : ['gClass', 'gAlias', 'gClass'],
    sqlCode.pParentReadBool            : ['gClass', 'gAlias', 'gClass'],
    sqlCode.pParentWrite               : ['gClass', 'gAlias', 'gClass'],
    sqlCode.pParentWriteBool           : ['gClass', 'gAlias', 'gClass'],
#    sqlCode.pSFCCallingIN_OUT          : ['gSFC'],
#    sqlCode.pSFCCallingOUT             : ['gSFC'],
#    sqlCode.pSFC                       : ['gSFC'],
    sqlCode.pSFCLink                   : ['gSFC'],
#    sqlCode.pSFCLinkOutput             : ['gSFC'],
    sqlCode.pSFCChild                  : ['gClass', 'gSFC'],
#    sqlCode.pSFCChildWrite             : ['gClass', 'gSFC'],
#    sqlCode.pSFCGrandChild             : ['gClass', 'gSFC'],
    sqlCode.pSFCChildMC                : ['gClass', 'gSFC'],
#    sqlCode.pSFCChildMCWrite           : ['gClass', 'gSFC'],
    sqlCode.pSFCChildExists            : ['gClass', 'gSFC'],
#    sqlCode.pSFCChildWriteExists       : ['gClass', 'gSFC'],
#    sqlCode.pSFCGrandChildWriteExists  : ['gClass', 'gSFC'],
    sqlCode.pSFCChildMCExists          : ['gClass', 'gSFC'],
#    sqlCode.pSFCChildMCWriteExists     : ['gClass', 'gSFC'],
    sqlCode.pSFCSelectMC               : ['gClass', 'gState'],
#    sqlCode.pSFCSelectMCWrite          : ['gClass', 'gState'],
    sqlCode.pSFCParametersRecipe       : ['gSFC'],
    sqlCode.pSFCParametersRecipeExist  : ['gSFC'],
    sqlCode.pSFCParametersBlock        : ['gSFC'],
#    sqlCode.pSFCParametersBlockWrite   : ['gSFC'],
    sqlCode.getSFCBlockParameters      : ['gClass'],
#    sqlCode.pBLOCK_READ                : ['gClass'],
#    sqlCode.pBLOCK_WRITE               : ['gClass'],
    sqlCode.pBLOCK_RECIPE              : ['gClass'],
    sqlCode.pBLOCK_RECIPE_EXISTS       : ['gClass'],
#    sqlCode.pCHILD_NotMC               : ['gClass'],
    sqlCode.pBlock                     : ['gClass'],
    sqlCode.pBlockIN                   : ['gClass'],
    sqlCode.pBlockIN_OUT               : ['gClass'],
    sqlCode.pBlockOUT                  : ['gClass'],
#    sqlCode.pBLKCallingIN_OUT          : ['gClass'],
#    sqlCode.pBLKCallingOUT             : ['gClass'],
    sqlCode.numChildren                : ['gClass'],
    sqlCode.numReadBool                : ['gClass'],
    sqlCode.numReadInt                 : ['gClass'],
    sqlCode.numReadReal                : ['gClass'],
    sqlCode.numReadTime                : ['gClass'],
    sqlCode.numWriteBool               : ['gClass'],
    sqlCode.numWriteInt                : ['gClass'],
    sqlCode.numWriteReal               : ['gClass'],
    sqlCode.numWriteTime               : ['gClass'],
    sqlCode.pReadBool                  : ['gClass', 'gClass', 'gClass'],
    sqlCode.pReadInt                   : ['gClass', 'gClass', 'gClass'],
    sqlCode.pReadReal                  : ['gClass', 'gClass', 'gClass'],
    sqlCode.pReadTime                  : ['gClass', 'gClass', 'gClass'],
    sqlCode.pWriteBool                 : ['gClass', 'gClass', 'gClass'],
    sqlCode.pWriteInt                  : ['gClass', 'gClass', 'gClass'],
    sqlCode.pWriteReal                 : ['gClass', 'gClass', 'gClass'],
    sqlCode.pWriteTime                 : ['gClass', 'gClass', 'gClass'],
    sqlCode.pEventLogMsgClass          : ['gClass', 'gClass', 'gClass', 'gClass', 'gClass', 'gClass', 'gClass'],
    sqlCode.pEventLogMsgExists         : ['gClass'],
    sqlCode.pEventLogMsgInstance       : ['gInstance', 'gInstance', 'gInstance', 'gInstance', 'gInstance', 'gInstance', 'gInstance'],
    sqlCode.pEventLogMsgMaxClass       : ['gClass', 'gClass'],
    sqlCode.pEventLogMsgMaxInstance    : [],
    sqlCode.pEventLogMsgWordClass      : ['gClass', 'gClass'],
    sqlCode.pEventLogMsgWordInstance   : ['gInstance', 'gInstance'],
    sqlCode.pEventLogMsgWordBitClass   : ['gClass', 'gClass', 'gClass', 'gClass'],
    sqlCode.pEventLogMsgWordBitInstance: ['gInstance'],
    sqlCode.simulateDI1                : ['gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.simulateDI2                : ['gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.simulatePOS2               : ['gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.simulatePOS4               : ['gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.simulateZSC1               : ['gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.simulateZSC2               : ['gParent', 'gParent', 'gParent', 'gParent'],
}

sql = {
    sqlCode.createIndexFileCount       : ('SELECT count(*) AS num '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ?'
                                         ),
    sqlCode.createIndexFile            : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'Description, '
                                                 'sfcMarker, '
                                                 'inheritsInstance '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ?'
                                         ),
    sqlCode.createClass                : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Class]) = ?'
                                         ),
    sqlCode.createClassesBlock         : ('SELECT Level,  '
                                                 'Class, '
                                                 'ID, '
                                                 'Description AS ClassDescription, '
                                                 'substr(Description, 1, 35) AS briefClassDescription '
                                          'FROM tblClass '
                                          'WHERE Level = "EM" OR '
                                                'Level = "UN" OR '
                                                'Level = "PC" '
                                          'ORDER BY [ID]'
                                         ),
    sqlCode.createClassesForLevel      : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY [Class]'
                                         ),
    sqlCode.createClassesGlobal        : ('SELECT Level,  '
                                                 'Class, '
                                                 'ID, '
                                                 'Description AS ClassDescription, '
                                                 'substr(Description, 1, 35) AS briefClassDescription '
                                          'FROM tblClass '
                                          'WHERE Level = "CM" OR '
                                                'Level = "EM" OR '
                                                'Level = "UN" OR '
                                                'Level = "PC" '
                                          'ORDER BY [ID]'
                                         ),
    sqlCode.createClassNone            : ('SELECT 1'
                                         ),
    sqlCode.createCM                   : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Class]) = "CM"'
                                         ),
    sqlCode.createEM                   : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Class]) = "EM"'
                                         ),
    sqlCode.createUN                   : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Class]) = "UN"'
                                         ),
    sqlCode.createPC                   : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Class]) = "PC"'
                                         ),
    sqlCode.createInstances            : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.Recipe, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'CASE '
                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
                                                 'END NC, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I INNER JOIN '
                                                 'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Class] = ? AND '
                                                 '(I.Instance = ? OR '
                                                 'I.Parent = ? OR '
                                                 'I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?) AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance'
                                         ),
    sqlCode.createInstanceAlarmsGlobal: ('SELECT printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.Instance || "-" || A.Mnemonic AS Symbol, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'substr(I.Description, 1, 35) AS briefDescription, '
                                                 '(I.Instance || " - " || A.Mnemonic || " - " || A.Message) AS Message, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'A.Condition, '
                                                 'A.Mnemonic, '
                                                 'A.Priority, '
                                                 'A.idbTag, '
                                                 'printf("%d",A.bitTrigger) AS bitTrigger '
                                          'FROM tblInstance AS I LEFT JOIN '
                                          'tblClass_Alarm AS A ON I.[Class] = A.[Class] '
                                          'WHERE length(I.Class) > 0 AND '
                                                 'length(A.Mnemonic) > 0 AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance, '
                                                 'I.Instance || "-" || A.Mnemonic'
                                         ),
    sqlCode.createInstancesForeign     : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.Recipe, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'CASE '
                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
                                                 'END NC, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I INNER JOIN '
                                                 'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Class] = ? AND '
                                                 '(I.Instance != ? AND '
                                                 'I.Parent != ? AND '
                                                 'I.GParent != ? AND '
                                                 'I.GGParent != ? AND '
                                                 'I.GGGParent != ?) AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance'
                                         ),
    sqlCode.createInstancesGlobal      : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'substr(I.Description, 1, 35) AS briefDescription, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'CASE '
                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
                                                 'END NC, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I INNER JOIN '
                                                  'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Class] = ? AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance'
                                         ),
    sqlCode.createInstancesAll         : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'substr(I.Description, 1, 35) AS briefDescription, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'C.Description AS ClassDescription, '
                                                 'printf("%d",I.xPos) AS xPos, '
                                                 'printf("%d",I.yPos) AS yPos '
                                          'FROM tblInstance AS I INNER JOIN '
                                                  'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE (upper(I.[Level]) == "CM" or '
                                                 'upper(I.[Level]) == "EM" or '
                                                 'upper(I.[Level]) == "UN" or '
                                                 'upper(I.[Level]) == "PC") AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance'
                                         ),
    sqlCode.xferInstancesGlobal        : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'substr(I.Description, 1, 35) AS briefDescription, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'CASE '
                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
                                                 'END NC, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I INNER JOIN '
                                                  'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Class] = ? AND '
                                                 'substr(I.Level, 1, 1) != "V" AND '
                                                 'I.OwnerID = 0 '
                                          'ORDER BY I.Instance'
                                         ),
    sqlCode.createSFCGlobal            : ('SELECT Level,  '
                                                 'Class, '
                                                 'State, '
                                                 'StateDescription, '
                                                 'SFC, '
                                                 'printf("%d",IDX) AS IDX '
                                          'FROM tblClass_State '
                                          'WHERE SFC <> "None" '
                                          'ORDER BY length(IDX), IDX'
                                         ),
#    sqlCode.numInstances               : ('SELECT count(*) - 1 AS MAXITEM '
#                                          'FROM tblInstance AS I INNER JOIN '
#                                                  'tblClass AS C ON I.ClassID = C.ID '
#                                          'WHERE I.[Class] = ? AND '
#                                                 '(I.Instance = ? OR '
#                                                 'I.Parent = ? OR '
#                                                 'I.GParent = ? OR '
#                                                 'I.GGParent = ? OR '
#                                                 'I.GGGParent = ?) AND '
#                                                 'substr(I.Level, 1, 1) != "V"'
#                                         ),
    sqlCode.numInstances               : ('SELECT count(*) - 1 AS MAXITEM '
                                          'FROM tblInstance '
                                          'WHERE [Class] = ? AND '
                                                 'substr(Level, 1, 1) != "V"'
                                         ),
    sqlCode.GLOBAL_INSTANCE            : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'CASE '
                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
                                                 'END NC, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I INNER JOIN '
                                                  'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Class] = ? AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance'
                                         ),
    sqlCode.createLevel                : ('SELECT [Level] '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY [Class] '
                                          'LIMIT 1'
                                         ),
    sqlCode.createLevelsGlobal         : ('SELECT Distinct Level '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) == "CM" or '
                                                'upper([Level]) == "EM" or '
                                                'upper([Level]) == "UN" or '
                                                'upper([Level]) == "PC" '
                                          'ORDER BY [ID]'
                                         ),
    sqlCode.callList                  : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY [Class]'
                                         ),
    sqlCode.callListExists             : ('SELECT ID '
                                          'FROM tblInstance '
                                          'WHERE [Class] = ? AND '
                                                 '(Instance = ? OR '
                                                 'Parent = ? OR '
                                                 'GParent = ? OR '
                                                 'GGParent = ? OR '
                                                 'GGGParent = ?) AND '
                                                 'substr(Level, 1, 1) != "V" '
                                          'LIMIT 1'
                                         ),
    sqlCode.callListExistsGlobal       : ('SELECT ID '
                                          'FROM tblInstance '
                                          'WHERE [Class] = ? AND '
                                                 'substr(Level, 1, 1) != "V" '
                                          'LIMIT 1'
                                         ),
    sqlCode.callListExistsCRIL         : ('SELECT Instance '
                                          'FROM tblInterlockCRIL '
                                          'LIMIT 1'
                                         ),
    sqlCode.callListExistsNCRIL        : ('SELECT Instance '
                                          'FROM tblInterlockNCRIL '
                                          'LIMIT 1'
                                         ),
    sqlCode.callListExistsXfer         : ('SELECT * '
                                          'FROM tblInstance '
                                          'WHERE [Class] = ? AND '
                                                 'substr(Level, 1, 1) != "V" AND '
                                                 'OwnerID = 0 '
                                          'LIMIT 1'
                                         ),
    sqlCode.createProgramFiles         : ('SELECT * '
                                          'FROM tblFile '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY File'
                                         ),
    sqlCode.createProgramFilesCount    : ('SELECT count(*) AS num '
                                          'FROM tblFile '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY File'
                                         ),
    sqlCode.documentInfo               : ('SELECT * '
                                          'FROM tblDocument '
                                          'WHERE upper(docClass) = ? AND '
                                                'upper(docScope) = ?'
                                         ),
    sqlCode.defaultParameters          : ('SELECT Parameter, '
                                                 'UOM, '
                                                 'CASE '
                                                     'WHEN upper(dataType) = "REAL" THEN printf("%.1f", defaultValue) '
                                                     'WHEN upper(dataType) = "INT" THEN printf("%d", defaultValue) '
                                                     'WHEN upper(dataType) = "STRING" THEN defaultValue '
                                                 'END defaultValue '
                                          'FROM tblParameter_Default'
                                         ),
    sqlCode.processLevel               : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY [Class]'
                                         ),
    sqlCode.processLevelCount          : ('SELECT count(*) AS num '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY [Class]'
                                         ),
    sqlCode.versionHistory             : ('SELECT printf("%d",V.Ver) AS Ver, '
                                                  'V.ChangedBy, '
                                                  'substr("00"||printf("%d",V.D), -2, 2) || "-" '
                                                      '|| substr("00"||printf("%d",V.M), -2, 2) || "-" || '
                                                      'printf("%d",V.Y) AS ChangedDate, '
                                                  'V.ChangeNumber, '
                                                  'V.Description '
                                          'FROM tblRevisionHistory AS V '
                                          'WHERE upper(V.KeyName) = ? AND '
                                                'V.KeyValue = ? ORDER BY V.Ver DESC '
                                         ),
    sqlCode.ANALOG                     : ('SELECT printf("%d",T.ID) AS ID, '
                                                 'T.Instance, '
                                                 'T.[Class], '
                                                 'T.Description, '
                                                 'A.Polarity, '
                                                 'A.rangeLow, '
                                                 'A.rangeHigh, '
                                                 'A.limitLL, '
                                                 'A.limitL, '
                                                 'A.limitH, '
                                                 'A.limitHH, '
                                                 'A.enableLL, '
                                                 'A.enableL, '
                                                 'A.enableH, '
                                                 'A.enableHH '
                                          'FROM tblInstance AS T LEFT JOIN '
                                                 'tblClass_Analog AS A ON T.ClassID = A.ClassID '
                                          'WHERE T.Instance = ? AND '
                                                'A.Embedded = "FALSE" AND '
                                                 'substr(T.Level, 1, 1) != "V" '
                                          'ORDER BY T.Parent, T.Instance'
                                         ), # gInstance
    sqlCode.ANALOG_EMBED               : ('SELECT printf("%d",T.ID) AS ID, '
                                                 'T.Instance, '
                                                 'T.[Class], '
                                                 'T.Description, '
                                                 'A.Polarity, '
                                                 'A.rangeLow, '
                                                 'A.rangeHigh, '
                                                 'A.limitLL, '
                                                 'A.limitL, '
                                                 'A.limitH, '
                                                 'A.limitHH, '
                                                 'A.enableLL, '
                                                 'A.enableL, '
                                                 'A.enableH, '
                                                 'A.enableHH '
                                          'FROM tblInstance AS T LEFT JOIN '
                                                 'tblClass_Analog AS A ON T.ClassID = A.ClassID '
                                          'WHERE T.Instance = ? AND '
                                                'A.Embedded = "TRUE" AND '
                                                 'substr(T.Level, 1, 1) != "V" '
                                          'ORDER BY T.Parent, T.Instance'
                                         ), # gInstance
    sqlCode.CHILD                      : ('SELECT C.*, '
                                                 'printf("%d", S.childIndex) AS childIndex, '
                                                 'printf("%d", S.IDX) AS childIDX '
                                          'FROM tblClass_Child AS C '
                                          'INNER JOIN tblClass_ChildStateValues AS S ON '
                                                 'C.childKey = S.childKey '
                                          'WHERE C.Class = ? AND '
                                                 'S.Class = ? AND '
                                          'S.State = (SELECT [State] FROM tblClass_State WHERE Class = ? LIMIT 1) '
                                          'ORDER BY cast(childIndex as Int)'
                                         ), # gClass
    sqlCode.CHILD_ACQUIRE              : ('SELECT childParameterAlias, '
                                                 'childAliasClass, '
                                                 'childAcquireStatement '
                                          'FROM tblClass_Child '
                                          'WHERE [Class] = ? AND '
                                                 'Shared = "TRUE" '
                                          'ORDER BY childParameterAlias'
                                         ), # gClass
    sqlCode.CHILD_CASCADE              : ('SELECT childParameterAlias, '
                                                 'childAliasClass, '
                                                 'childAcquireStatement '
                                          'FROM tblClass_Child '
                                          'WHERE [Class] = ? '
                                          'ORDER BY childParameterAlias'
                                         ), # gClass
    sqlCode.CHILD_ACQUIRED             : ('SELECT childParameterAlias, '
                                                 'childClass AS childAliasClass, '
                                                 'printf("%d", childIndex) AS childIndex, '
                                                 'childAcquireStatement '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND '
                                                 '[State] = ? AND '
                                                 '(childAcquire = "TRUE" OR '
                                                 'childAcquire = "OWNER") '
                                          'ORDER BY childParameterAlias'
                                         ), # gClass, gState
    sqlCode.CHILD_ACQUIRE_REQ          : ('SELECT childParameterAlias, '
                                                 'childClass AS childAliasClass, '
                                                 'printf("%d", childIndex) AS childIndex, '
                                                 'childAcquireStatement '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND '
                                                 '[State] = ? AND '
                                                 'childAcquire = "TRUE" '
                                          'ORDER BY childParameterAlias'
                                         ), # gClass, gState
    sqlCode.CHILD_ACQUIRE_NREQ         : ('SELECT childParameterAlias, '
                                                 'childClass AS childAliasClass, '
                                                 'printf("%d", childIndex) AS childIndex, '
                                                 'childAcquireStatement '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND '
                                                 '[State] = ? AND '
                                                 '(childAcquire = "FALSE" OR '
                                                 'childAcquire = "OWNER") '
                                          'ORDER BY childParameterAlias'
                                         ), # gClass, gState
    sqlCode.CHILD_BIND                 : ('SELECT childParameterAlias, '
                                                 'childClass, '
                                                 'conditionStatement, '
                                                 'printf("%d", childIndex) AS childIndex, '
                                                 'printf("%d", childBind) AS childBindIndex, '
                                                 'childParameterAliasBind '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE Class = ? AND '
                                                 'State = ? AND '
                                                 'length(childBind) > 0 '
                                          'ORDER BY cast(childIndex as Int)'
                                         ), # gInstance
    sqlCode.CHILD_INDEX_MAX            : ('SELECT printf("%d", MAX(childIndex)) AS childIndexMax '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE Class = ?'
                                         ), # gClass
    sqlCode.CHILD_INIT_COMMAND_TRUE    : ('SELECT childParameterAlias, '
                                                 'childClass AS childAliasClass, '
                                                 'printf("%d", childIndex) AS childIndex, '
                                                 'conditionStatement, '
                                                 'trueStatement, '
                                                 'trueCommand, '
                                                 'falseStatement, '
                                                 'falseCommand '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND '
                                                 'State = ? AND '
                                                 '(childAcquire = "TRUE" OR '
                                                 'childAcquire = "OWNER") '
                                          'ORDER BY childParameterAlias'
                                         ), # gClass, gState
    sqlCode.CHILD_INIT_COMMAND_FALSE   : ('SELECT childParameterAlias, '
                                                 'childClass AS childAliasClass, '
                                                 'printf("%d", childIndex) AS childIndex, '
                                                 'conditionStatement, '
                                                 'trueStatement, '
                                                 'trueCommand, '
                                                 'falseStatement, '
                                                 'falseCommand '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND '
                                                 'State = ? AND '
                                                 '(childAcquire = "TRUE" OR '
                                                 'childAcquire = "OWNER") AND '
                                                 'length(falseStatement) > 0'
                                         ), # gClass, gState
    sqlCode.CHILD_INSTANCE             : ('SELECT C.childParameterAlias, '
                                                 'I.Class AS childAliasClass, '
                                                 'printf("%d", C.childIndex) AS childIndex, '
                                                 'printf("%d", I.IDX) AS childIDX, '
                                                 'childClass, '
                                                 'I.Instance AS childInstance, '
                                                 'I.Description AS childDescription '
                                          'FROM tblClass_ChildStateValues AS C '
                                          'INNER JOIN tblInstance AS I ON '
                                                 'C.childKey = I.childKey AND '
                                                 '(I.Parent = ? OR '
                                                 '(I.OwnerID = 0 AND '
                                                 '(I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?))) '
                                          'WHERE C.Class = ? AND '
                                                 'C.State = (SELECT [State] FROM tblClass_State WHERE Class = ? LIMIT 1) '
                                          'ORDER BY cast(childIndex as Int)'
                                         ), # gInstance
    sqlCode.CHILD_INSTANCE_BIND        : ('SELECT C.childParameterAlias, '
                                                 'I.Class AS childAliasClass, '
                                                 'C.conditionStatement, '
                                                 'printf("%d", C.childIndex) AS childIndex, '
                                                 'printf("%d", C.childBind) AS childBindIndex, '
                                                 'C.childParameterAliasBind, '
                                                 'I.Instance AS childInstance '
                                          'FROM tblClass_ChildStateValues AS C '
                                          'INNER JOIN tblInstance AS I ON '
                                                 'C.childKey = I.childKey AND '
                                                 '(I.Parent = ? OR '
                                                 '(I.OwnerID = 0 AND '
                                                 '(I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?))) '
                                          'WHERE C.Class = ? AND '
                                                 'C.State = ? AND '
                                                 'length(C.childBind) > 0 '
                                          'ORDER BY cast(childIndex as Int)'
                                         ), # gInstance
    sqlCode.CHILD_SELECT               : ('SELECT * '
                                          'FROM tblClass_ChildSelection '
                                          'WHERE [Class] = ? '
                                          'ORDER BY childParameterAlias'
                                         ), # gClass
    sqlCode.pChildSelect               : ('SELECT DISTINCT linkParameterAlias, '
                                                 'childClass '
                                          'FROM tblClass_ChildSelection '
                                          'WHERE [Class] = ? '
                                          'ORDER BY linkParameterAlias'
                                         ), # gClass
    sqlCode.pChildSelectExists         : ('SELECT Level '
                                          'FROM tblClass_ChildSelection '
                                          'WHERE [Class] = ? '
                                          'LIMIT 1'
                                         ), # gClass
#    sqlCode.CRIL                       : ('SELECT DISTINCT Instance, Description '
#                                          'FROM tblInterlockCRIL '
#                                          'ORDER BY Instance'
#                                         ),
    sqlCode.CRIL                       : ('SELECT DISTINCT Instance, '
                                                 'Description, '
                                                 'substr(Description, 1, 35) AS briefDescription, '
                                                 '(SELECT COUNT (DISTINCT Instance) '
                                                    'FROM tblInterlockCRIL t2 '
                                                    'WHERE t2.Instance < t1.Instance) '
                                                  '+ '
                                                    '(SELECT COUNT (DISTINCT Instance) '
                                                    'FROM tblInterlockCRIL t3 '
                                                    'WHERE t3.Instance = T1.Instance) - 1 '
                                                  'AS IDX '
                                          'FROM tblInterlockCRIL t1 '
                                          'ORDER BY Instance'
                                         ),
    sqlCode.CRIL_EXISTS                : ('SELECT Instance, IDX '
                                          'FROM tblInterlockCRIL '
                                          'WHERE Instance = ? '
                                          'LIMIT 1'
                                         ), # gInstance
    sqlCode.CRIL_INSTANCE              : ('SELECT * '
                                          'FROM tblInterlockCRIL '
                                          'WHERE Instance = ?'
                                         ), # gInstance
    sqlCode.CRIL_INSTANCE_NUM          : ('SELECT COUNT(Instance) AS NUMIL '
                                          'FROM tblInterlockCRIL '
                                          'WHERE Instance = ?'
                                         ), # gInstance
    sqlCode.CRIL_TARGET                : ('SELECT DISTINCT Instance, '
                                                 'Description, '
                                                 '(SELECT COUNT (DISTINCT Instance) '
                                                    'FROM tblInterlockCRIL t2 '
                                                    'WHERE t2.Instance < t1.Instance) '
                                                  '+ '
                                                    '(SELECT COUNT (DISTINCT Instance) '
                                                    'FROM tblInterlockCRIL t3 '
                                                    'WHERE t3.Instance = T1.Instance) - 1 '
                                                  'AS idxIL, Class, IDX, DescriptionIL, Interlock '
                                          'FROM tblInterlockCRIL t1 '
                                          'WHERE Instance = ? '
                                          'ORDER BY Instance '
                                          'LIMIT 1'
                                         ),
    sqlCode.CRIL_NUM                   : ('SELECT COUNT(Instance) - 1 AS MAXITEM '
                                          'FROM tblInterlockCRIL '
                                          'ORDER BY Instance'
                                         ),
    sqlCode.NCRIL                      : ('SELECT DISTINCT Instance, '
                                                 'Description, '
                                                 'substr(Description, 1, 35) AS briefDescription, '
                                                 '(SELECT COUNT (DISTINCT Instance) '
                                                    'FROM tblInterlockNCRIL t2 '
                                                    'WHERE t2.Instance < t1.Instance) '
                                                  '+ '
                                                    '(SELECT COUNT (DISTINCT Instance) '
                                                    'FROM tblInterlockNCRIL t3 '
                                                    'WHERE t3.Instance = T1.Instance) - 1 '
                                                  'AS IDX '
                                          'FROM tblInterlockNCRIL t1 '
                                          'ORDER BY Instance'
                                         ),
#    sqlCode.NCRIL                      : ('SELECT DISTINCT Instance, Description '
#                                          'FROM tblInterlockNCRIL '
#                                          'ORDER BY Instance'
#                                         ),
    sqlCode.NCRIL_EXISTS               : ('SELECT Instance, IDX '
                                          'FROM tblInterlockNCRIL '
                                          'WHERE Instance = ? '
                                          'LIMIT 1'
                                         ), # gInstance
    sqlCode.NCRIL_INSTANCE             : ('SELECT * '
                                          'FROM tblInterlockNCRIL '
                                          'WHERE Instance = ?'
                                         ), # gInstance
    sqlCode.NCRIL_INSTANCE_NUM         : ('SELECT COUNT(DISTINCT Instance) AS NUMIL '
                                          'FROM tblInterlockNCRIL '
                                          'WHERE Instance = ?'
                                         ), # gInstance
    sqlCode.NCRIL_TARGET               : ('SELECT DISTINCT Instance, '
                                                 'Description, '
                                                 '(SELECT COUNT (DISTINCT Instance) '
                                                    'FROM tblInterlockNCRIL t2 '
                                                    'WHERE t2.Instance < t1.Instance) '
                                                  '+ '
                                                    '(SELECT COUNT (DISTINCT Instance) '
                                                    'FROM tblInterlockNCRIL t3 '
                                                    'WHERE t3.Instance = T1.Instance) - 1 '
                                                  'AS idxIL, Class, IDX, DescriptionIL, Interlock '
                                          'FROM tblInterlockNCRIL t1 '
                                          'WHERE Instance = ? '
                                          'ORDER BY Instance '
                                          'LIMIT 1'
                                         ),
    sqlCode.NCRIL_NUM                  : ('SELECT COUNT(DISTINCT Instance) - 1 AS MAXITEM '
                                          'FROM tblInterlockNCRIL '
                                          'ORDER BY Instance'
                                         ),
    sqlCode.FLOWPATH                   : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE [Class] = ? AND '
                                                 'Flowpath = 1'
                                         ), # gClass
    sqlCode.HYGIENE                    : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE [Class] = ? AND '
                                                 'upper(Hygiene) = "YES"'
                                         ), # gClass
    sqlCode.INSTANCE_ALL               : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'CASE '
                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
                                                 'END NC, '
                                                 'I.instanceChildAlias, '
                                                 'I.instanceChildAliasClass, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I LEFT JOIN '
                                                 'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Level] != "CP" AND '
                                                 '(I.Instance = ? OR '
                                                 'I.Parent = ? OR '
                                                 'I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?) '
                                          'ORDER BY I.[Level], I.Instance'
                                         ),
    sqlCode.INSTANCE_BLK               : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'CASE '
                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
                                                 'END NC, '
                                                 'I.instanceChildAlias, '
                                                 'I.instanceChildAliasClass, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I LEFT JOIN '
                                                 'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Level] != "CM" AND '
                                                 'I.[Level] != "CP" AND '
                                                 '(I.Instance = ? OR '
                                                 'I.Parent = ? OR '
                                                 'I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?) AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.[Level], I.Instance'
                                         ),
    sqlCode.INSTANCE_BLK_ALL           : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'CASE '
                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
                                                 'END NC, '
                                                 'I.instanceChildAlias, '
                                                 'I.instanceChildAliasClass, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I LEFT JOIN '
                                                 'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Level] != "CM" AND '
                                                 'I.[Level] != "CP" AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.[Level], I.Instance'
                                         ),
    sqlCode.INSTANCE_SFC               : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'printf("%d",S.IDX) AS sfcIDX, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'I.Parent, '
                                                 'S.SFC, '
                                                 'S.State, '
                                                 'S.StateDescription '
                                          'FROM tblInstance AS I INNER JOIN '
                                                 'tblClass_State AS S ON '
                                                        'I.Level = S.Level AND '
                                                        'I.ClassID = S.ClassID '
                                          'WHERE S.SFC != "None" AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.[Level], I.Instance, S.SFC'
                                         ),
    sqlCode.ISOWNED                    : ('SELECT Instance '
                                          'FROM tblInstance '
                                          'WHERE Instance = ? AND '
                                                 'OwnerID != 0 AND '
                                                 'substr(Level, 1, 1) != "V" '
                                                 'LIMIT 1'
                                         ), # gInstance
    sqlCode.LINK                       : ('SELECT userInstance, '
                                                 'userClass, '
                                                 'userIndex, '
                                                 'userAlias, '
                                                 'Link, '
                                                 'linkInstance, '
                                                 'linkClass, '
                                                 'printf("%d",linkIDX) AS linkIDX, '
                                                 'linkAttribute, '
                                                 'actualAttribute, '
                                                 'sfcParameter, '
                                                 'linkDataType '
                                          'FROM tblInstance_Link '
                                          'WHERE [userInstance] = ?'
                                         ), # gInstance
#    sqlCode.LINK_BLK                   : ('SELECT userInstance, '
#                                                 'userClass, '
#                                                 'userIndex, '
#                                                 'userAlias, '
#                                                 'Link, '
#                                                 'linkAlias, '
#                                                 'P.blockParameter, '
#                                                 'linkInstance, '
#                                                 'linkClass, '
#                                                 'printf("%d",linkIDX) AS linkIDX, '
#                                                 'linkAttribute, '
#                                                 'actualAttribute, '
#                                                 'sfcParameter, '
#                                                 'linkDataType '
    sqlCode.LINK_BLK                   : ('SELECT DISTINCT linkAlias, '
                                                 'printf("%d",linkIDX) AS linkIDX, '
                                                 'linkClass '
                                          'FROM tblInstance_Link AS L INNER JOIN '
                                                'pGlobal AS P ON L.userClass = P.parameterClass '
                                                'AND L.Link = P.childParameterAlias AND '
                                                'L.linkAttribute = P.childParameterAttribute '
                                          'WHERE [userInstance] = ? AND '
                                                'p.isLink = 1 '
                                          'ORDER BY Link'
                                         ), # gInstance
    sqlCode.LINK_BLK_Define            : ('SELECT DISTINCT blockParameter, '
                                                 'parameterDataType  '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isLink = 1 '
                                          'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pLink                      : ('SELECT DISTINCT childParameterAlias, '
                                                 'childParameterClass '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isLink = 1 '
                                          'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pLinkExists                : ('SELECT Level '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isLink = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pLinkInput                 : ('SELECT userInstance, '
                                                 'userClass, '
                                                 'userIndex, '
                                                 'userAlias, '
                                                 'Link, '
                                                 'linkAlias, '
                                                 'P.blockParameter, '
                                                 'linkInstance, '
                                                 'linkClass, '
                                                 'printf("%d",linkIDX) AS linkIDX, '
                                                 'linkAttribute, '
                                                 'actualAttribute, '
                                                 'sfcParameter, '
                                                 'linkDataType '
                                          'FROM tblInstance_Link AS L INNER JOIN '
                                                 'pGlobal AS P ON L.userClass = P.parameterClass '
                                                 'AND L.Link = P.childParameterAlias AND '
                                                 'L.linkAttribute = P.childParameterAttribute AND '
                                                 'L.isLinkWrite = 0 '
                                          'WHERE userInstance = ? AND '
                                                 'userState = ? AND '
                                                 'p.isMC = 0 AND '
                                                 'p.isLink = 1 '
                                          'ORDER BY Link'
                                         ), # gInstance
    sqlCode.pLinkInputMC               : ('SELECT userInstance, '
                                                 'userClass, '
                                                 'userIndex, '
                                                 'userAlias, '
                                                 'Link, '
                                                 'linkAlias, '
                                                 'P.blockParameter, '
                                                 'linkInstance, '
                                                 'linkClass, '
                                                 'printf("%d",linkIDX) AS linkIDX, '
                                                 'linkAttribute, '
                                                 'actualAttribute, '
                                                 'sfcParameter, '
                                                 'linkDataType '
                                          'FROM tblInstance_Link AS L INNER JOIN '
                                                 'pGlobal AS P ON L.userClass = P.parameterClass '
                                                 'AND L.Link = P.childParameterAlias AND '
                                                 'L.linkAttribute = P.childParameterAttribute AND '
                                                 'L.isLinkWrite = 0 '
                                          'WHERE userInstance = ? AND '
                                                 'userState = ? AND '
                                                 'p.isMC = 1 AND '
                                                 'p.isLink = 1 '
                                          'ORDER BY Link'
                                         ), # gInstance
    sqlCode.pLinkOutput                : ('SELECT userInstance, '
                                                 'userClass, '
                                                 'userIndex, '
                                                 'userAlias, '
                                                 'Link, '
                                                 'linkAlias, '
                                                 'P.blockParameter, '
                                                 'linkInstance, '
                                                 'linkClass, '
                                                 'printf("%d",linkIDX) AS linkIDX, '
                                                 'linkAttribute, '
                                                 'actualAttribute, '
                                                 'sfcParameter, '
                                                 'linkDataType '
                                          'FROM tblInstance_Link AS L INNER JOIN '
                                                 'pGlobal AS P ON L.userClass = P.parameterClass '
                                                 'AND L.Link = P.childParameterAlias AND '
                                                 'L.linkAttribute = P.childParameterAttribute AND '
                                                 'L.isLinkWrite = 1 '
                                          'WHERE userInstance = ? AND '
                                                 'userState = ? AND '
                                                 'p.isMC = 0 AND '
                                                 'p.isLink = 1 '
                                          'ORDER BY Link'
                                         ), # gInstance
    sqlCode.pLinkOutputMC              : ('SELECT userInstance, '
                                                 'userClass, '
                                                 'userIndex, '
                                                 'userAlias, '
                                                 'Link, '
                                                 'linkAlias, '
                                                 'P.blockParameter, '
                                                 'linkInstance, '
                                                 'linkClass, '
                                                 'printf("%d",linkIDX) AS linkIDX, '
                                                 'linkAttribute, '
                                                 'actualAttribute, '
                                                 'sfcParameter, '
                                                 'linkDataType '
                                          'FROM tblInstance_Link AS L INNER JOIN '
                                                 'pGlobal AS P ON L.userClass = P.parameterClass '
                                                 'AND L.Link = P.childParameterAlias AND '
                                                 'L.linkAttribute = P.childParameterAttribute AND '
                                                 'L.isLinkWrite = 1 '
                                          'WHERE userInstance = ? AND '
                                                 'userState = ? AND '
                                                 'p.isMC = 1 AND '
                                                 'p.isLink = 1 '
                                          'ORDER BY Link'
                                         ), # gInstance
    sqlCode.UNIQUEID                   : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.ParentClass, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'CASE '
                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
                                                 'END NC, '
                                                 'I.instanceChildAlias, '
                                                 'I.instanceChildAliasClass, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I INNER JOIN '
                                                 'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.[Level], I.Instance'
                                         ),
    sqlCode.PARAMETER_INDEX_MAX        : ('SELECT printf("%d", MAX(parameterIndex)) AS parameterIndexMax '
                                          'FROM tblClass_Parameter '
                                          'WHERE parameterClass = ?'
                                         ), # gClass
    sqlCode.PARENT                     : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE [Level] = "EM" OR '
                                                 '[Level] = "UN" OR '
                                                 '[Level] = "PC" '
                                          'ORDER BY [ID]'
                                         ),
    sqlCode.PARENTBLK                  : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE [Level] = "UN" OR '
                                                 '[Level] = "PC" '
                                          'ORDER BY [ID]'
                                         ),
    sqlCode.PARENTEM                   : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE [Level] = "EM" '
                                          'ORDER BY [ID]'
                                         ),
    sqlCode.PARENTDATA                 : ('SELECT P.Level, '
                                                 'P.Class, '
                                                 'printf("%d", P.ID) AS IDX, '
                                                 '(SELECT COUNT(C.childAliasTag) '
                                                       'FROM tblClass_Child AS C '
                                                       'WHERE P.Class = C.Class) '
                                                       'AS cntChildren, '
                                                 '(SELECT COUNT(G.childParameterAlias) '
                                                       'FROM pGlobal AS G '
                                                       'WHERE P.Class = G.parameterClass AND '
                                                       'G.parameterType LIKE "VAR_%" AND '
                                                       'length(G.childParameterAlias) = 0) '
                                                       'AS cntParameters '
                                          'FROM tblClass AS P '
                                          'WHERE P.Level = "CM" OR '
                                                 'P.Level = "EM" OR '
                                                 'P.Level = "UN" OR '
                                                 'P.Level = "PC" '
                                          'ORDER BY P.ID'
                                         ),
    sqlCode.RECIPE                     : ('SELECT DISTINCT I.Recipe, I.RecipeClass '
                                          'FROM tblInstance AS I INNER JOIN '
                                                'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE length(I.Recipe) > 0 AND '
                                                'C.Recipe = 1 AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Recipe'
                                         ),
    sqlCode.RECIPE_CLASS               : ('SELECT DISTINCT I.Instance AS RecipeName, '
                                                 'I.RecipeClass '
                                          'FROM tblInstance AS I INNER JOIN '
                                                 'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE length(I.Recipe) > 0 AND '
                                                 'C.Recipe = 1 AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.RecipeClass'
                                         ),
    sqlCode.RECIPE_INSTANCE            : ('SELECT Instance, Recipe, RecipeClass '
                                          'FROM tblInstance '
                                          'WHERE Instance = ? AND '
                                                 'substr(Level, 1, 1) != "V" '
                                         ), # gInstance

    sqlCode.RECIPE_PARAMETERS          : ('SELECT DISTINCT blockParameter, '
                                                 'parameterDataType, '
                                                 'parameterDescription '
                                          'FROM pGlobal '
                                          'WHERE isRecipe = 1 '
                                          'GROUP BY blockParameter '
                                          'ORDER BY blockParameter'
                                         ),
    sqlCode.REQUIREMENT                : ('SELECT printf("%d",C.ID) AS ID, '
                                                 'C.Class, '
                                                 'F.ClassID, '
                                                 'F.ReqRef, '
                                                 'F.Requirement '
                                          'FROM tblClass AS C INNER JOIN '
                                                 'tblClass_Requirement AS F ON C.ID = F.ClassID '
                                          'WHERE F.[Type]="Req" '
                                          'ORDER BY C.Class, F.ReqOrder'
                                         ),
    sqlCode.SCOPE                      : ('SELECT printf("%d",C.ID) AS ID, '
                                                 'C.Class, '
                                                 'F.ClassID, '
                                                 'F.Requirement AS Scope '
                                          'FROM tblClass AS C INNER JOIN '
                                                 'tblClass_Requirement AS F ON C.ID = F.ClassID '
                                          'WHERE F.[Type]="Scope" '
                                          'ORDER BY C.Class'
                                         ),
    sqlCode.SELECT                     : ('SELECT DISTINCT '
                                                 '[Class], '
                                                 'Parameter, '
                                                 'Selection '
                                          'FROM tblClass_Selection '
                                          'WHERE [Class] = ? '
                                          'ORDER BY Parameter'
                                         ), # gClass
    sqlCode.SELVALUE                   : ('SELECT S.Level, '
                                                 'S.Class, '
                                                 'S.Parameter, '
                                                 'S.Selection, '
                                                 'S.Description, '
                                                 'V.selectionIndex, '
                                                 'V.selectionValue '
                                          'FROM tblClass_Selection AS S '
                                          'INNER JOIN tblClass_SelectionValues AS V '
                                          'ON S.Key = V.Key '
                                          'WHERE S.Class = ? AND '
                                                'S.Parameter = ? AND '
                                                'S.Selection = ? '
                                          'ORDER BY S.Level, S.Class, S.Parameter, '
                                                   'V.selectionValue'
                                         ), # gClass, gSelectParameter
#    sqlCode.SELVALUE                   : ('SELECT * '
#                                          'FROM tblClass_Selection '
#                                          'WHERE [Class] = ? AND '
#                                                'Parameter = ? AND '
#                                                'Selection = ? '
#                                          'ORDER BY Parameter, '
#                                                'Selection, '
#                                                'SelectionValue'
#                                          ), # gClass, gSelectParameter , gSelectSelection
    sqlCode.SFC                        : ('SELECT * '
                                          'FROM tblClass_State '
                                          'WHERE [Class] = ? AND '
                                                'hasSFC = "TRUE" '
                                          'ORDER BY State'
                                         ), # gClass
    sqlCode.SFCExists                  : ('SELECT Class '
                                          'FROM tblClass_State '
                                          'WHERE [Class] = ? AND '
                                                'hasSFC = "TRUE" '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.STATE                      : ('SELECT * '
                                          'FROM tblClass_State '
                                          'WHERE [Class] = ? '
                                          'ORDER BY State'
                                         ), # gClass
    sqlCode.STATE_TIMER                : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'I.Parent, '
                                                 'I.ParentID, '
                                                 'I.Parent[Class], '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'CASE '
                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
                                                 'END NC, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I '
                                          'LEFT JOIN tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Level] != "CP" AND '
                                                 '(I.Instance = ? OR '
                                                 'I.Parent = ? OR '
                                                 'I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?) AND '
                                                 'substr(I.Level, 1, 1) != "V" AND '
                                                 'upper(C.timerTransition) = "YES" '
                                          'ORDER BY I.[Level], I.Instance'
                                         ),
    sqlCode.SETPOINT                   : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper(hasSetpoint) = "YES" '
                                          'ORDER BY Class'
                                         ),
    sqlCode.OUTPUT                     : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper(hasOutput) = "YES" '
                                          'ORDER BY Class'
                                         ),
    sqlCode.TAGS                       : ('SELECT I.Instance || "-" || IO.Mnemonic AS Symbol, '
                                                 'I.Instance AS CMTag, '
                                                 'I.Description AS CMDescription, '
                                                 'I.[Class] AS CMClass, '
                                                 'I.Parent, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'IO.Mnemonic, '
                                                 'M.Address,'
                                                 'IO.Description AS IODescription, '
                                                 'IO.Source, '
                                                 'IO.DI, '
                                                 'IO.DO, '
                                                 'IO.AI, '
                                                 'IO.AO, '
                                                 'IO.PDI, '
                                                 'IO.PDO, '
                                                 'IO.PAI, '
                                                 'IO.PAO, '
                                                 'IO.IOClass, '
                                                 'IO.Prefix, '
                                                 'IO.dataType '
                                          'FROM tblInstance AS I '
                                          'LEFT JOIN tblClass_IO AS IO ON I.[Class] = IO.[Class] '
                                          'LEFT JOIN tblIOMaster AS M ON I.Instance || "-" || IO.Mnemonic = M.Symbol '
                                          'WHERE length(I.Class) > 0 AND '
                                                 'length(IO.Mnemonic) > 0 AND '
                                                 '(I.Instance = ? OR '
                                                 'I.Parent = ? OR '
                                                 'I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?) AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY IO.DI DESC , '
                                                 'IO.DO DESC , '
                                                 'IO.AI DESC , '
                                                 'IO.AO DESC , '
                                                 'IO.PDI DESC , '
                                                 'IO.PDO DESC , '
                                                 'IO.PAI DESC , '
                                                 'IO.PAO DESC , '
                                                 'IO.Source DESC , '
                                                 'I.Instance, '
                                                 'I.Instance || "-" || IO.Mnemonic'
                                         ),
    sqlCode.TAGALARMS                  : ('SELECT I.Instance || "-" || A.Mnemonic AS Symbol, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.Instance, '
                                                 'I.Description, '
                                                 'I.[Class], '
                                                 'I.Parent, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 '(I.Instance || " - " || A.Mnemonic || " - " || A.Message) AS Message, '
                                                 'A.Condition, '
                                                 'A.Mnemonic, '
                                                 'A.Priority, '
                                                 'A.idbTag, '
                                                 'A.bitTrigger '
                                          'FROM tblInstance AS I '
                                          'LEFT JOIN tblClass_Alarm AS A ON I.[Class] = A.[Class] '
                                          'WHERE length(I.Class) > 0 AND '
                                                 'length(A.Mnemonic) > 0 AND '
                                                 '(I.Instance = ? OR '
                                                 'I.Parent = ? OR '
                                                 'I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?) AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance, '
                                                 'I.Instance || "-" || A.Mnemonic'
                                         ),
    sqlCode.TAGSALT                    : ('SELECT I.Instance || "-" || IO.Mnemonic AS Symbol, '
                                                 'I.Instance AS CMTag, '
                                                 'I.Description AS CMDescription, '
                                                 'I.[Class] AS CMClass, '
                                                 'I.Parent, '
                                                 'I.GParent, '
                                                 'I.GGParent, '
                                                 'I.GGGParent, '
                                                 'IO.Mnemonic, '
                                                 'CASE '
                                                     'WHEN IO.dataType="Bool" THEN "%M@@COUNTERTEMPLATE|200@@.0" '
                                                     'WHEN IO.dataType="Int" THEN "%MW@@COUNTERTEMPLATE@@" '
                                                     'WHEN IO.dataType="Real" THEN "%MD@@COUNTERTEMPLATE@@" '
                                                 'END Address, '
                                                 'IO.Description AS IODescription, '
                                                 'IO.Source, '
                                                 'IO.DI, '
                                                 'IO.DO, '
                                                 'IO.AI, '
                                                 'IO.AO, '
                                                 'IO.PDI, '
                                                 'IO.PDO, '
                                                 'IO.PAI, '
                                                 'IO.PAO, '
                                                 'IO.IOClass, '
                                                 'IO.Prefix, '
                                                 'IO.dataType '
                                          'FROM tblInstance AS I '
                                          'LEFT JOIN tblClass_IO AS IO ON I.[Class] = IO.[Class] '
                                          'LEFT JOIN tblIOMaster AS M ON I.Instance || "-" || IO.Mnemonic = M.Symbol '
                                          'WHERE length(I.Class) > 0 AND '
                                                 'length(IO.Mnemonic) > 0 AND '
                                                 '(I.Instance != ? AND '
                                                 'I.Parent != ? AND '
                                                 'I.GParent != ? AND '
                                                 'I.GGParent != ? AND '
                                                 'I.GGGParent != ?) AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY IO.DI DESC , '
                                                 'IO.DO DESC , '
                                                 'IO.AI DESC , '
                                                 'IO.AO DESC , '
                                                 'IO.PDI DESC , '
                                                 'IO.PDO DESC , '
                                                 'IO.PAI DESC , '
                                                 'IO.PAO DESC , '
                                                 'IO.Source DESC , '
                                                 'I.Instance, '
                                                 'I.Instance || "-" || IO.Mnemonic'
                                         ),
    sqlCode.TIMER                      : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE [Class] = ? AND '
                                                 'upper(Timer) = "YES"'
                                         ), # gClass
    sqlCode.TRANSITION                 : ('SELECT printf("%d",C.ID) AS ID, '
                                                 'C.Class, '
                                                 'C.Level, '
                                                 'T.ClassID, '
                                                 'T.Transition, '
                                                 'T.Description '
                                          'FROM tblClass AS C INNER JOIN '
                                                 'tblClass_Transition AS T ON C.ID = T.ClassID '
                                          'ORDER BY C.Level, C.Class, T.Transition'
                                         ),
    sqlCode.VERHIST                    : ('SELECT printf("%d",V.Ver) AS Ver, '
                                                 'V.ChangedBy, '
                                                 'substr("00"||printf("%d",V.D), -2, 2) '
                                                 '|| "-" || CASE '
                                                     'WHEN V.M=1 THEN "Jan" '
                                                     'WHEN V.M=2 THEN "Feb" '
                                                     'WHEN V.M=3 THEN "Mar" '
                                                     'WHEN V.M=4 THEN "Apr" '
                                                     'WHEN V.M=5 THEN "May" '
                                                     'WHEN V.M=6 THEN "Jun" '
                                                     'WHEN V.M=7 THEN "Jul" '
                                                     'WHEN V.M=8 THEN "Aug" '
                                                     'WHEN V.M=9 THEN "Sep" '
                                                     'WHEN V.M=10 THEN "Oct" '
                                                     'WHEN V.M=11 THEN "Nov" '
                                                     'WHEN V.M=12 THEN "Dec" '
                                                 'END || "-" || '
                                                 'printf("%d",V.Y) AS ChangedDate, '
                                                 'V.ChangeNumber, '
                                                 'V.Description '
                                          'FROM tblRevisionHistory AS V '
                                          'WHERE upper(V.KeyName) = @@DOCTYPE@@ AND '
                                                'V.KeyValue = @@SCOPE@@ '
                                                'ORDER BY V.Ver DESC'
                                         ),
    sqlCode.checkIfClassParameter      : ('SELECT * '
                                          'FROM tblClass_Parameter '
                                          'WHERE ParameterClass = ? AND '
                                               'blockParameter = ? AND '
                                               'upper(parameterOperation) = "WRITE"'
                                         ), # gClass, sParameter
    sqlCode.checkIfChildParameter      : ('SELECT childParameterAlias, '
                                                 'childAliasClass '
                                          'FROM tblClass_Child '
                                          'WHERE Class = ? AND '
                                               'childParameterAlias || "_" '
                                               'LIKE substr(?, 1, length(childParameterAlias) + 1) || "%"'
                                         ), # gClass, sParameter
#                                               'childLinkAlias || "_" '
#                                               'LIKE substr(?, 1, length(childLinkAlias) + 1) || "%")'
    sqlCode.checkIfLinkParameter       : ('SELECT childParameterAlias, '
                                                 'childAliasClass '
                                          'FROM tblClass_Child '
                                          'WHERE Class != ? '
                                               'AND childParameterAlias || "_" '
                                               'LIKE substr(?, 1, length(childParameterAlias) + 1) || "%"'
                                         ), # gClass, sParameter
    sqlCode.checkIfSelectionParameter  : ('SELECT linkParameterAlias, '
                                                 'childClass '
                                          'FROM tblClass_ChildSelection '
                                          'WHERE Class = ? '
                                               'AND linkParameterAlias || "_" '
                                               'LIKE substr(?, 1, length(linkParameterAlias) + 1) || "%"'
                                         ), # gClass, sParameter
    sqlCode.getChildIndex              : ('SELECT printf("%d", childIndex) AS childIndex '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE SFC = ? AND childParameterAlias = ?'
                                         ), # gSFC, gChild
    sqlCode.checkGlobalParameterExists : ('SELECT * FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'blockParameter = ?'
                                         ), # gClass, sParameter
    sqlCode.updateParameterOperation   : ('UPDATE pGlobal '
                                          'SET operation = ? '
                                          'WHERE parameterClass = ? AND '
                                                'blockParameter = ?'
                                         ),
    sqlCode.insertGlobalParameters     : ('INSERT INTO pGlobal '
                                          'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                                         ),
    sqlCode.insertEventPrompt          : ('INSERT INTO pEventPrompt '
                                                 'SELECT 0, '
                                                 'I.Instance || P.childParameter || "_" || P.parameterState AS pKey, '
                                                 'I.Instance, '
                                                 'printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.Class, '
                                                 'I.Description, '
                                                 'I.instanceChildAlias, '
                                                 'I.instanceChildSFCAlias, '
                                                 'P.parameterSource, '
                                                 'P.parameterState, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.parameterDataType, '
                                                 'p.parameterDescription '
                                          'FROM tblInstance AS I '
                                                 'INNER JOIN pGlobal AS P '
                                                 'ON I.Class = P.parameterClass '
                                          'WHERE P.isSFC = 1 AND '
                                                 'P.isEventPrompt = 1 AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance, '
                                                 'P.parameterState, '
                                                 'P.childParameter'
                                         ),
    sqlCode.insertEventLogMsg          : ('INSERT INTO pEventLogMsg '
                                                 'SELECT 0, '
                                                 'I.Instance || P.childParameter || "_" || P.parameterState AS pKey, '
                                                 'I.Instance, '
                                                 'printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.Class, '
                                                 'I.Description, '
                                                 'I.instanceChildAlias, '
                                                 'I.instanceChildSFCAlias, '
                                                 'P.parameterSource, '
                                                 'P.parameterState, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.parameterDataType, '
                                                 'p.parameterDescription '
                                          'FROM tblInstance AS I '
                                                 'INNER JOIN pGlobal AS P '
                                                 'ON I.Class = P.parameterClass '
                                          'WHERE P.isSFC = 1 AND '
                                                 'P.isEventLogMsg = 1 AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance, '
                                                 'P.parameterState, '
                                                 'P.childParameter'
                                         ),
    sqlCode.insertEventLogReal         : ('INSERT INTO pEventLogReal '
                                                 'SELECT 0, '
                                                 'I.Instance || P.childParameter || "_" || P.parameterState AS pKey, '
                                                 'I.Instance, '
                                                 'printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.Class, '
                                                 'I.Description, '
                                                 'I.instanceChildAlias, '
                                                 'I.instanceChildSFCAlias, '
                                                 'P.parameterSource, '
                                                 'P.parameterState, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.parameterDataType, '
                                                 'p.parameterDescription '
                                          'FROM tblInstance AS I '
                                                 'INNER JOIN pGlobal AS P '
                                                 'ON I.Class = P.parameterClass '
                                          'WHERE P.isSFC = 1 AND '
                                                 'P.isEventLogReal = 1 AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance, '
                                                 'P.parameterState, '
                                                 'P.childParameter'
                                         ),
    sqlCode.insertEventLogTime         : ('INSERT INTO pEventLogTime '
                                                 'SELECT 0, '
                                                 'I.Instance || P.childParameter || "_" || P.parameterState AS pKey, '
                                                 'I.Instance, '
                                                 'printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.Class, '
                                                 'I.Description, '
                                                 'I.instanceChildAlias, '
                                                 'I.instanceChildSFCAlias, '
                                                 'P.parameterSource, '
                                                 'P.parameterState, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.parameterDataType, '
                                                 'p.parameterDescription '
                                          'FROM tblInstance AS I '
                                                 'INNER JOIN pGlobal AS P '
                                                 'ON I.Class = P.parameterClass '
                                          'WHERE P.isSFC = 1 AND '
                                                 'P.isEventLogTime = 1 AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance, '
                                                 'P.parameterState, '
                                                 'P.childParameter'
                                         ),
    sqlCode.updateEventPrompt          : ('UPDATE pEventPrompt '
                                          'SET idxEvent = ('
                                                 'SELECT keyEvent FROM '
                                                    '(SELECT '
                                                      '(SELECT '
                                                        '(SELECT COUNT(pKey) '
                                                         'FROM pEventPrompt t2 '
                                                         'WHERE t2.pKey < t1.pKey) '
                                                        '+ '
                                                        '(SELECT COUNT(pKey) '
                                                         'FROM pEventPrompt t3 '
                                                         'WHERE t3.pKey = T1.pKey) '
                                                       ') '
                                                    'AS keyEvent, '
                                                    'pKey AS keyName '
                                                    'FROM pEventPrompt t1) '
                                                 'WHERE keyName=pKey)'
                                         ),
    sqlCode.updateEventLogMsg          : ('UPDATE pEventLogMsg '
                                          'SET idxEvent = ('
                                                 'SELECT keyEvent FROM '
                                                    '(SELECT '
                                                      '(SELECT '
                                                        '(SELECT COUNT(pKey) '
                                                         'FROM pEventLogMsg t2 '
                                                         'WHERE t2.pKey < t1.pKey) '
                                                        '+ '
                                                        '(SELECT COUNT(pKey) '
                                                         'FROM pEventLogMsg t3 '
                                                         'WHERE t3.pKey = T1.pKey) '
                                                       ') '
                                                    'AS keyEvent, '
                                                    'pKey AS keyName '
                                                    'FROM pEventLogMsg t1) '
                                                 'WHERE keyName=pKey)'
                                         ),
    sqlCode.updateEventLogReal         : ('UPDATE pEventLogReal '
                                          'SET idxEvent = ('
                                                 'SELECT keyEvent FROM '
                                                    '(SELECT '
                                                      '(SELECT '
                                                        '(SELECT COUNT(pKey) '
                                                         'FROM pEventLogReal t2 '
                                                         'WHERE t2.pKey < t1.pKey) '
                                                        '+ '
                                                        '(SELECT COUNT(pKey) '
                                                         'FROM pEventLogReal t3 '
                                                         'WHERE t3.pKey = T1.pKey) '
                                                       ') '
                                                    'AS keyEvent, '
                                                    'pKey AS keyName '
                                                    'FROM pEventLogReal t1) '
                                                 'WHERE keyName=pKey)'
                                         ),
    sqlCode.updateEventLogTime         : ('UPDATE pEventLogTime '
                                          'SET idxEvent = ('
                                                 'SELECT keyEvent FROM '
                                                    '(SELECT '
                                                      '(SELECT '
                                                        '(SELECT COUNT(pKey) '
                                                         'FROM pEventLogTime t2 '
                                                         'WHERE t2.pKey < t1.pKey) '
                                                        '+ '
                                                        '(SELECT COUNT(pKey) '
                                                         'FROM pEventLogTime t3 '
                                                         'WHERE t3.pKey = T1.pKey) '
                                                       ') '
                                                    'AS keyEvent, '
                                                    'pKey AS keyName '
                                                    'FROM pEventLogTime t1) '
                                                 'WHERE keyName=pKey)'
                                         ),
    sqlCode.addParametersClass         : ('SELECT * '
                                          'FROM tblClass_Parameter '
                                          'ORDER BY Level, '
                                                 'parameterClass, '
                                                 'blockParameter'
                                         ),
    sqlCode.getClassChildren           : ('SELECT childParameterAlias, '
                                                 'childAliasClass '
                                          'FROM tblClass_Child '
                                          'WHERE [Class] = ? '
                                          'ORDER BY childParameterAlias'
                                         ),
    sqlCode.addParametersSFC           : ('SELECT * '
                                          'FROM tblClass_State '
                                          'WHERE [Class] = ? '
                                                 'AND upper(SFC) != ? '
                                          'ORDER BY State'
                                         ),
#    sqlCode.getChildParameters          : ('SELECT * '
#                                          'FROM tblClass_ParameterChild '
#                                          'WHERE parentClass = ? '
#                                          'ORDER BY childAlias, '
#                                                 'childParameter'
#                                         ), # gClass
    sqlCode.getChildParameters          : ('SELECT * '
                                          'FROM tblClass_Parameter '
                                          'WHERE parameterClass = ? '
                                          'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.getDeferredParameters      : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isMC = 0 AND '
                                                 'parameterType LIKE "VAR_%" '
                                          'ORDER BY childParameter'
                                         ), # gClass
    sqlCode.tblCreateGlobalParameter   : ('CREATE TABLE IF NOT EXISTS '
                                          'pGlobal ('
                                                 'Level text NOT NULL, '
                                                 'parameterClass text NOT NULL, '
                                                 'parameterSource text, '
                                                 'parameterState text, '
                                                 'parameterType text NOT NULL, '
                                                 'parameterOrder int NOT NULL, '
                                                 'childParameter text NOT NULL, '
                                                 'blockParameter text NOT NULL, '
                                                 'childParameterAlias text, '
                                                 'childParameterClass text, '
                                                 'childParameterAttribute text, '
                                                 'grandChildParameterAlias text, '
                                                 'grandChildParameterClass text, '
                                                 'grandChildParameterAttribute text, '
                                                 'parameterDataType text NOT NULL, '
                                                 'parameterValue text, '
                                                 'parameterDescription text, '
                                                 'operation text NOT NULL, '
                                                 'isSFC boolean, '
                                                 'isChild boolean, '
                                                 'isGrandchild boolean, '
                                                 'isLink boolean, '
                                                 'isSelection boolean, '
                                                 'isMC boolean, '
                                                 'childIndex int, '
                                                 'isRecipe boolean, '
                                                 'recipeClass text, '
                                                 'idxEvent int, '
                                                 'isEventConfirm boolean, '
                                                 'isEventPrompt boolean, '
                                                 'isEventLogMsg boolean, '
                                                 'isEventLogReal boolean, '
                                                 'isEventLogTime boolean, '
                                                 'isEventDataReal boolean, '
                                                 'isEventDataTime boolean, '
                                                 'isSync boolean)'
                                         ),
    sqlCode.tblCreateEventPrompt       : ('CREATE TABLE IF NOT EXISTS '
                                          'pEventPrompt ('
                                                 'idxEvent int NOT NULL, '
                                                 'pKey text NOT NULL, '
                                                 'Instance text NOT NULL, '
                                                 'ID int NOT NULL, '
                                                 'IDX int NOT NULL, '
                                                 'Class text NOT NULL, '
                                                 'Description text NOT NULL, '
                                                 'instanceChildAlias text NOT NULL, '
                                                 'instanceChildSFCAlias text NOT NULL, '
                                                 'parameterSource text NOT NULL, '
                                                 'parameterState text NOT NULL, '
                                                 'childParameter text NOT NULL, '
                                                 'blockParameter text NOT NULL, '
                                                 'parameterDataType text NOT NULL, '
                                                 'parameterDescription text NOT NULL)'
                                         ),
    sqlCode.tblCreateEventLogMsg       : ('CREATE TABLE IF NOT EXISTS '
                                          'pEventLogMsg ('
                                                 'idxEvent int NOT NULL, '
                                                 'pKey text NOT NULL, '
                                                 'Instance text NOT NULL, '
                                                 'ID int NOT NULL, '
                                                 'IDX int NOT NULL, '
                                                 'Class text NOT NULL, '
                                                 'Description text NOT NULL, '
                                                 'instanceChildAlias text NOT NULL, '
                                                 'instanceChildSFCAlias text NOT NULL, '
                                                 'parameterSource text NOT NULL, '
                                                 'parameterState text NOT NULL, '
                                                 'childParameter text NOT NULL, '
                                                 'blockParameter text NOT NULL, '
                                                 'parameterDataType text NOT NULL, '
                                                 'parameterDescription text NOT NULL)'
                                         ),
    sqlCode.tblCreateEventLogReal      : ('CREATE TABLE IF NOT EXISTS '
                                          'pEventLogReal ('
                                                 'idxEvent int NOT NULL, '
                                                 'pKey text NOT NULL, '
                                                 'Instance text NOT NULL, '
                                                 'ID int NOT NULL, '
                                                 'IDX int NOT NULL, '
                                                 'Class text NOT NULL, '
                                                 'Description text NOT NULL, '
                                                 'instanceChildAlias text NOT NULL, '
                                                 'instanceChildSFCAlias text NOT NULL, '
                                                 'parameterSource text NOT NULL, '
                                                 'parameterState text NOT NULL, '
                                                 'childParameter text NOT NULL, '
                                                 'blockParameter text NOT NULL, '
                                                 'parameterDataType text NOT NULL, '
                                                 'parameterDescription text NOT NULL)'
                                         ),
    sqlCode.tblCreateEventLogTime      : ('CREATE TABLE IF NOT EXISTS '
                                          'pEventLogTime ('
                                                 'idxEvent int NOT NULL, '
                                                 'pKey text NOT NULL, '
                                                 'Instance text NOT NULL, '
                                                 'ID int NOT NULL, '
                                                 'IDX int NOT NULL, '
                                                 'Class text NOT NULL, '
                                                 'Description text NOT NULL, '
                                                 'instanceChildAlias text NOT NULL, '
                                                 'instanceChildSFCAlias text NOT NULL, '
                                                 'parameterSource text NOT NULL, '
                                                 'parameterState text NOT NULL, '
                                                 'childParameter text NOT NULL, '
                                                 'blockParameter text NOT NULL, '
                                                 'parameterDataType text NOT NULL, '
                                                 'parameterDescription text NOT NULL)'
                                         ),
#CREATE TABLE `idxInstance` (
#	`idxItem`	INTEGER,
#	`ID`	INTEGER,
#	`Level`	TEXT,
#	`Instance`	TEXT
#);
    sqlCode.pEventExists               : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 '(isEventPrompt = 1 OR '
                                                 'isEventLogMsg = 1 OR '
                                                 'isEventLogReal = 1) '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventConfirm              : ('SELECT *, '
                                                 'Replace(childParameter,"_confirm",".confirm") AS dbEventParameter '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventConfirm = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
#    sqlCode.pEventPrompt               : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                 'isSFC = 1 AND '
#                                                 'isEventPrompt = 1 '
#                                          'ORDER BY cast(idxEvent as Int)'
#                                         ), # gClass
    sqlCode.pEventPrompt               : ('SELECT * '
                                          'FROM pEventPrompt '
                                          'WHERE Class = ? AND '
                                                 'Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) '
                                          'ORDER BY idxEvent'
                                         ), # gClass
#    sqlCode.pEventLogMsg               : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                 'isSFC = 1 AND '
#                                                 'isEventLogMsg = 1 '
#                                          'ORDER BY cast(idxEvent as Int)'
#                                         ), # gClass
    sqlCode.pEventLogReal              : ('SELECT * '
                                          'FROM pEventLogReal '
                                          'WHERE Class = ? AND '
                                                 'Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) '
                                          'ORDER BY idxEvent'
                                         ), # gClass
    sqlCode.pEventLogTime              : ('SELECT * '
                                          'FROM pEventLogTime '
                                          'WHERE Class = ? AND '
                                                 'Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) '
                                          'ORDER BY idxEvent'
                                         ), # gClass
    sqlCode.pEventDataReal             : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventDataReal = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventDataTime             : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventDataTime = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pSyncRead                  : ('SELECT *, '
                                                 'substr(blockParameter, 1, length(blockParameter) - length(?) - 1) AS childSyncParameter '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'operation = "read" AND '
                                                 'isSync = 1 AND '
                                                 'substr(blockParameter, length(blockParameter) - length(?) + 1, length(?)) = ? '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pSyncWrite                 : ('SELECT *, '
                                                 'substr(blockParameter, 1, length(blockParameter) - length(?) - 1) AS childSyncParameter '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'operation = "write" AND '
                                                 'isSync = 1 AND '
                                                 'substr(blockParameter, length(blockParameter) - length(?) + 1, length(?)) = ? '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
#    sqlCode.pEventPromptInstance       : ('SELECT I.Instance, '
#                                                 'printf("%d",I.ID) AS ID, '
#                                                 'printf("%d",I.IDX) AS IDX, '
#                                                 'I.Class, '
#                                                 'I.Description, '
#                                                 'I.instanceChildAlias, '
#                                                 'I.instanceChildSFCAlias, '
#                                                 'P.parameterSource, '
#                                                 'P.parameterState, '
#                                                 'P.childParameter, '
#                                                 'P.blockParameter, '
#                                                 'P.parameterDataType, '
#                                                 'p.parameterDescription '
#                                          'FROM tblInstance AS I '
#                                                 'INNER JOIN pGlobal AS P '
#                                                 'ON I.Class = P.parameterClass '
#                                          'WHERE P.isSFC = 1 AND '
#                                                 'P.isEventPrompt = 1 AND '
#                                                 'substr(I.Level, 1, 1) != "V" '
#                                          'ORDER BY I.Instance, '
#                                                 'P.parameterState, '
#                                                 'P.childParameter'
#                                         ),
#    sqlCode.pEventPromptInstance       : ('SELECT (SELECT COUNT(pKey) '
#                                                  'FROM pEventPrompt t2 '
#                                                  'WHERE t2.pKey < t1.pKey) '
#                                                  '+ '
#                                                 '(SELECT COUNT(pKey) '
#                                                  'FROM pEventPrompt t3 '
#                                                  'WHERE t3.pKey = T1.pKey) - 1 '
#                                                 'AS idxEvent, '
#                                                 '* '
#                                          'FROM pEventPrompt t1 '
#                                          'ORDER BY pKey'
#                                         ),
#    sqlCode.pEventLogMsgInstance       : ('SELECT I.Instance, '
#                                                 'printf("%d",I.ID) AS ID, '
#                                                 'printf("%d",I.IDX) AS IDX, '
#                                                 'I.Class, '
#                                                 'I.Description, '
#                                                 'I.instanceChildAlias, '
#                                                 'I.instanceChildSFCAlias, '
#                                                 'P.parameterSource, '
#                                                 'P.parameterState, '
#                                                 'P.childParameter, '
#                                                 'P.blockParameter, '
#                                                 'P.parameterDataType, '
#                                                 'p.parameterDescription '
#                                          'FROM tblInstance AS I '
#                                                 'INNER JOIN pGlobal AS P '
#                                                 'ON I.Class = P.parameterClass '
#                                          'WHERE P.isSFC = 1 AND '
#                                                 'P.isEventLogMsg = 1 AND '
#                                                 'substr(I.Level, 1, 1) != "V" '
#                                          'ORDER BY I.Instance, '
#                                                 'P.parameterState, '
#                                                 'P.childParameter'
#                                         ), # gClass
    sqlCode.pEventConfirmExists        : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventConfirm = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventPromptExists         : ('SELECT pKey '
                                          'FROM pEventPrompt '
                                          'WHERE Class = ? '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogRealExists        : ('SELECT pKey '
                                          'FROM pEventLogReal '
                                          'WHERE Class = ? '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogTimeExists        : ('SELECT pKey '
                                          'FROM pEventLogTime '
                                          'WHERE Class = ? '
                                          'LIMIT 1'
                                         ), # gClass
#    sqlCode.pEventLogMsgExists         : ('SELECT isSFC '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                 'isSFC = 1 AND '
#                                                 'isEventLogMsg = 1 '
#                                          'LIMIT 1'
#                                         ), # gClass
    sqlCode.pEventDataRealExists       : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventDataReal = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventDataTimeExists       : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventDataTime = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventConfirmNoExists      : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventConfirm = 1 AND '
                                                 'childParameter = ? || "_confirm_no"'
                                         ), # gClass
    sqlCode.pEventConfirmAll           : ('SELECT *, '
                                                 'Replace(childParameter,"_confirm",".confirm") AS dbEventParameter '
                                          'FROM pGlobal '
                                          'WHERE isEventConfirm = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventPromptAll            : ('SELECT * '
                                          'FROM pEventPrompt '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
#    sqlCode.pEventLogMsgAll            : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE isEventLogMsg = 1 '
#                                          'ORDER BY cast(idxEvent as Int)'
#                                         ), # gClass
#    sqlCode.pEventLogMsgAll            : ('SELECT * '
#                                          'FROM pEventLogMsg '
#                                          'ORDER BY cast(idxEvent as Int)'
#                                         ), # gClass
    sqlCode.pEventLogRealAll           : ('SELECT * '
                                          'FROM pEventLogReal '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventLogTimeAll           : ('SELECT * '
                                          'FROM pEventLogTime '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventPromptNum            : ('SELECT COUNT(pKey) AS idxEventMax '
                                          'FROM pEventPrompt'
                                         ),
#    sqlCode.pEventLogMsgInstanceNum    : ('SELECT COUNT(I.Instance) AS idxEventMax '
#                                          'FROM tblInstance AS I '
#                                                 'INNER JOIN pGlobal AS P '
#                                                 'ON I.Class = P.parameterClass '
#                                          'WHERE P.isSFC = 1 AND '
#                                                 'P.isEventLogMsg = 1 AND '
#                                                 'substr(I.Level, 1, 1) != "V"'
#                                         ),
#    sqlCode.pEventPromptNum            : ('SELECT printf("%d", MAX(idxEvent)) AS idxEventMax '
#                                          'FROM pGlobal '
#                                          'WHERE isEventPrompt = 1'
#                                         ),
#    sqlCode.pEventLogMsgNum            : ('SELECT COUNT(pKey) AS idxEventMax '
#                                          'FROM pEventLogMsg'
#                                         ),
    sqlCode.pEventLogRealNum           : ('SELECT COUNT(pKey) AS idxEventMax '
                                          'FROM pEventLogReal'
                                         ),
    sqlCode.pEventLogTimeNum           : ('SELECT COUNT(pKey) AS idxEventMax '
                                          'FROM pEventLogTime'
                                         ),
    sqlCode.pEventDataLogMatch         : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterSource = ? AND '
                                                 'childParameter = substr(?, 5) '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventDataValueMatch       : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterSource = ? AND '
                                                 'childParameter = "_log" || ? '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pSFCChild                  : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                'parameterSource = ? AND '
                                                'isSFC = 1 AND '
                                                'isLink = 0 AND '
                                                'isChild = 1 AND '
                                                'isMC = 0 AND '
                                                'parameterType != "VAR" '
                                          'ORDER BY parameterOrder, '
                                                 'parameterSource, '
                                                 'childParameter'
                                         ), # gClass, gSFC
    sqlCode.pSFCChildExists            : ('SELECT Level '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                'parameterSource = ? AND '
                                                'isSFC = 1 AND '
                                                'isLink = 0 AND '
                                                'isChild = 1 AND '
                                                'isMC = 0 AND '
                                                'parameterType != "VAR" '
                                          'LIMIT 1'
                                         ), # gClass, gSFC
#    sqlCode.pSFCChildRead              : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterSource = ? AND '
#                                                'isSFC = 1 AND '
#                                                'isLink = 0 AND '
#                                                'isChild = 1 AND '
#                                                'isMC = 0 AND '
#                                                'isWrite = 0 AND '
#                                                'parameterType != "VAR" '
#                                          'ORDER BY parameterOrder, '
#                                                 'parameterSource, '
#                                                 'childParameter'
#                                         ), # gClass, gSFC
#    sqlCode.pSFCChildReadExists        : ('SELECT Level '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterSource = ? AND '
#                                                'isSFC = 1 AND '
#                                                'isLink = 0 AND '
#                                                'isChild = 1 AND '
#                                                'isMC = 0 AND '
#                                                'isWrite = 0 AND '
#                                                'parameterType != "VAR" '
#                                          'LIMIT 1'
#                                         ), # gClass, gSFC
#    sqlCode.pSFCChildWrite             : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterSource = ? AND '
#                                                'isSFC = 1 AND '
#                                                'isLink = 0 AND '
#                                                'isChild = 1 AND '
#                                                'isMC = 0 AND '
#                                                'isWrite = 1 AND '
#                                                'parameterType != "VAR" '
#                                          'ORDER BY parameterOrder, '
#                                                 'parameterSource, '
#                                                 'childParameter'
#                                         ), # gClass, gSFC
#    sqlCode.pSFCChildWriteExists       : ('SELECT Level '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterSource = ? AND '
#                                                'isSFC = 1 AND '
#                                                'isLink = 0 AND '
#                                                'isChild = 1 AND '
#                                                'isMC = 0 AND '
#                                                'isWrite = 1 AND '
#                                                'parameterType != "VAR" '
#                                          'LIMIT 1'
#                                         ), # gClass, gSFC
#    sqlCode.pSFCGrandChildWrite        : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterSource = ? AND '
#                                                'isSFC = 1 AND '
#                                                'isLink = 0 AND '
#                                                'isChild = 1 AND '
#                                                'isGrandchild = 1 AND '
#                                                'isWrite = 1 AND '
#                                                'parameterType != "VAR" '
#                                          'ORDER BY parameterOrder, '
#                                                 'parameterSource, '
#                                                 'childParameter'
#                                         ), # gClass, gSFC
#    sqlCode.pSFCGrandChildWriteExists  : ('SELECT Level '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterSource = ? AND '
#                                                'isSFC = 1 AND '
#                                                'isLink = 0 AND '
#                                                'isChild = 1 AND '
#                                                'isGrandchild = 1 AND '
#                                                'isWrite = 1 AND '
#                                                'parameterType != "VAR" '
#                                          'LIMIT 1'
#                                         ), # gClass, gSFC
    sqlCode.pSFCChildMC                : ('SELECT DISTINCT S.Class, '
                                                 'S.State, '
                                                 'S.childParameterAlias, '
                                                 'S.childClass, '
                                                 'printf("%d", S.IDX) AS childIDX, '
                                                 'printf("%d", S.childIndex) AS childIndex, '
                                                 'P.parameterSource, '
                                                 'P.parameterType, '
                                                 'P.parameterDataType, '
                                                 'P.childParameter, '
                                                 'P.childParameterClass, '
                                                 'P.blockParameter, '
                                                 'P.childParameterAttribute, '
                                                 'P.parameterDescription, '
                                                 'P.operation '
                                          'FROM tblClass_ChildStateValues AS S  '
                                                 'LEFT JOIN pGlobal AS P ON  '
                                                        'S.childParameterAlias = P.childParameterAlias AND '
                                                        'S.SFC = P.parameterSource '
                                          'WHERE S.Class = ? AND '
                                                 'P.parameterSource = ? AND '
                                                 '(S.childAcquire = "TRUE" OR '
                                                 'S.childAcquire = "OWNER") AND '
                                                 'P.isSFC = 1 AND '
                                                 'P.isMC = 1 AND '
                                                 'P.isChild = 1 '
                                          'GROUP BY P.childParameter '
                                          'ORDER BY S.State, '
                                                 'P.parameterOrder, '
                                                 'P.parameterSource, '
                                                 'P.childParameter'
                                         ), # gClass
#                                                        'S.childAlias = substr(P.blockParameter,1,length(S.childAlias)) AND '
    sqlCode.pSFCChildMCExists          : ('SELECT S.Class '
                                          'FROM tblClass_ChildStateValues AS S  '
                                                 'LEFT JOIN pGlobal AS P ON  '
                                                        'S.childParameterAlias = P.childParameterAlias AND '
                                                        'S.SFC = P.parameterSource '
                                          'WHERE S.Class = ? AND '
                                                 'P.parameterSource = ? AND '
                                                 '(S.childAcquire = "TRUE" OR '
                                                 'S.childAcquire = "OWNER") AND '
                                                 'P.isSFC = 1 AND '
                                                 'P.isMC = 1 AND '
                                                 'P.isChild = 1 '
                                          'LIMIT 1'
                                         ), # gClass
#                                                        'S.childAlias = substr(P.blockParameter,1,length(S.childAlias)) AND '
#    sqlCode.pSFCChildMCWrite           : ('SELECT DISTINCT S.Class, '
#                                                 'S.State, '
#                                                 'S.childParameterAlias, '
#                                                 'S.childClass, '
#                                                 'printf("%d", S.IDX) AS childIDX, '
#                                                 'printf("%d", S.childIndex) AS childIndex, '
#                                                 'P.parameterSource, '
#                                                 'P.parameterType, '
#                                                 'P.parameterDataType, '
#                                                 'P.childParameter, '
#                                                 'P.childParameterClass, '
#                                                 'P.blockParameter, '
#                                                 'P.childParameterAttribute, '
#                                                 'P.parameterDescription '
#                                          'FROM tblClass_ChildStateValues AS S  '
#                                                 'LEFT JOIN pGlobal AS P ON  '
#                                                        'S.childParameterAlias = P.childParameterAlias AND '
#                                                        'S.SFC = P.parameterSource '
#                                          'WHERE S.Class = ? AND '
#                                                 'P.parameterSource = ? AND '
#                                                 '(P.parameterType = "VAR_OUTPUT" OR '
#                                                 'P.parameterType = "VAR_IN_OUT") AND '
#                                                 '(S.childAcquire = "TRUE" OR '
#                                                 'S.childAcquire = "OWNER") AND '
#                                                 'P.isSFC = 1 AND '
#                                                 'P.isMC = 1 AND '
#                                                 'P.isWrite = 1 AND '
#                                                 'P.isChild = 1 '
#                                          'GROUP BY P.childParameter '
#                                          'ORDER BY S.State, '
#                                                 'P.parameterOrder, '
#                                                 'P.parameterSource, '
#                                                 'P.childParameter'
#                                         ), # gClass
#    sqlCode.pSFCChildMCWriteExists     : ('SELECT S.Class '
#                                          'FROM tblClass_ChildStateValues AS S  '
#                                                 'LEFT JOIN pGlobal AS P ON  '
#                                                        'S.childParameterAlias = P.childParameterAlias AND '
#                                                        'S.SFC = P.parameterSource '
#                                          'WHERE S.Class = ? AND '
#                                                 'P.parameterSource = ? AND '
#                                                 '(P.parameterType = "VAR_OUTPUT" OR '
#                                                 'P.parameterType = "VAR_IN_OUT") AND '
#                                                 '(S.childAcquire = "TRUE" OR '
#                                                 'S.childAcquire = "OWNER") AND '
#                                                 'P.isSFC = 1 AND '
#                                                 'P.isMC = 1 AND '
#                                                 'P.isWrite = 1 AND '
#                                                 'P.isChild = 1 '
#                                          'LIMIT 1'
#                                         ), # gClass
    sqlCode.pSFCSelectMC               : ('SELECT DISTINCT P.childParameterClass, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.childParameterAlias, '
                                                 'P.childParameterAttribute, '
                                                 'P.operation '
                                          'FROM tblClass_ChildSelection AS S '
                                                 'LEFT JOIN pGlobal AS P ON '
                                                 'S.linkParameterAlias = P.childParameterAlias AND '
                                                 'S.Class = P.parameterClass '
                                          'WHERE S.Class = ? AND '
                                                 'S.selectionState = ? AND '
                                                 'P.isMC = 1 '
                                          'ORDER BY P.childParameterAlias'
                                         ), # gClass
#    sqlCode.pSFCSelectMCWrite          : ('SELECT DISTINCT P.childParameterClass, '
#                                                 'P.childParameter, '
#                                                 'P.blockParameter, '
#                                                 'P.childParameterAlias, '
#                                                 'P.childParameterAttribute '
#                                          'FROM tblClass_ChildSelection AS S '
#                                                 'LEFT JOIN pGlobal AS P ON '
#                                                 'S.linkParameterAlias = P.childParameterAlias AND '
#                                                 'S.Class = P.parameterClass '
#                                          'WHERE S.Class = ? AND '
#                                                 'S.selectionState = ? AND '
#                                                 'P.isMC = 1 AND '
#                                                 'P.isWrite = 1 '
#                                          'ORDER BY P.childParameterAlias'
#                                         ), # gClass
#    sqlCode.pChildInput                : ('SELECT DISTINCT blockParameter, '
#                                                 'childParameterAlias, '
#                                                 'childParameterClass, '
#                                                 'childParameterAttribute, '
#                                                 'parameterDataType '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                 '(parameterType = "VAR_INPUT" OR '
#                                                  'parameterType = "VAR_IN_OUT") AND '
#                                                 'isChild = 1 AND '
#                                                 'isLink = 0 AND '
#                                                 'isMC = 0 AND '
#                                                 'isWrite = 0 AND '
#                                                 'childParameterAlias = ? '
#                                          'ORDER BY blockParameter'
#                                         ), # gClass
#    sqlCode.pChildOutput               : ('SELECT DISTINCT blockParameter, '
#                                                 'childParameterAlias, '
#                                                 'childParameterClass, '
#                                                 'childParameterAttribute, '
#                                                 'parameterDataType '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                 '(parameterType = "VAR_INPUT" OR '
#                                                  'parameterType = "VAR_IN_OUT") AND '
#                                                 'isChild = 1 AND '
#                                                 'isLink = 0 AND '
#                                                 'isMC = 0 AND '
#                                                 'isWrite = 1 AND '
#                                                 'childParameterAlias = ? '
#                                          'ORDER BY blockParameter'
#                                         ), # gClass
#    sqlCode.pChildDefine               : ('SELECT DISTINCT blockParameter, '
#                                                 'parameterDataType  '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                 '(parameterType = "VAR_INPUT" OR '
#                                                  'parameterType = "VAR_IN_OUT") AND '
#                                                 'isChild = 1 AND '
#                                                 'isLink = 0 AND '
#                                                 'isMC = 0 AND '
#                                                 'isWrite = 1 '
#                                          'ORDER BY blockParameter'
#                                         ), # gClass
#    sqlCode.pChildIN                   : ('SELECT DISTINCT S.Class, '
#                                                 'S.State, '
#                                                 'S.childClass, '
#                                                 'printf("%d", S.childIndex) AS childIndex, '
#                                                 'P.parameterType, '
#                                                 'P.parameterDataType, '
#                                                 'P.childParameter, '
#                                                 'P.blockParameter, '
#                                                 'P.childParameterAlias, '
#                                                 'P.childParameterAttribute, '
#                                                 'P.parameterDescription '
#                                          'FROM pGlobal AS P '
#                                          'INNER JOIN tblClass_ChildStateValues AS S ON '
#                                                 'S.Class = P.parameterClass AND '
#                                                 'S.childClass = P.parameterSource '
#                                          'WHERE P.parameterClass = ? AND '
#                                                 'P.parameterType = "VAR_INPUT" AND '
#                                                 'P.isChild = 0 '
#                                          'GROUP BY P.childParameter '
#                                          'ORDER BY P.parameterOrder, '
#                                                 'P.parameterSource, '
#                                                 'P.childParameter'
#                                         ), # gClass
#    sqlCode.pChildIN_OUT               : ('SELECT DISTINCT S.Class, '
#                                                 'S.State, '
#                                                 'S.childClass, '
#                                                 'printf("%d", S.childIndex) AS childIndex, '
#                                                 'P.parameterType, '
#                                                 'P.parameterDataType, '
#                                                 'P.childParameter, '
#                                                 'P.blockParameter, '
#                                                 'P.childParameterAlias, '
#                                                 'P.childParameterAttribute, '
#                                                 'P.parameterDescription '
#                                          'FROM pGlobal AS P '
#                                          'INNER JOIN tblClass_ChildStateValues AS S ON '
#                                                 'S.Class = P.parameterClass AND '
#                                                 'S.childClass = P.parameterSource '
#                                          'WHERE P.parameterClass = ? AND '
#                                                 'P.parameterType = "VAR_IN_OUT" AND '
#                                                 'P.isChild = 0 '
#                                          'GROUP BY P.childParameter '
#                                          'ORDER BY P.parameterOrder, '
#                                                 'P.parameterSource, '
#                                                 'P.childParameter'
#                                         ), # gClass
#    sqlCode.pChildOUT                  : ('SELECT DISTINCT S.Class, '
#                                                 'S.State, '
#                                                 'S.childClass, '
#                                                 'printf("%d", S.childIndex) AS childIndex, '
#                                                 'P.parameterType, '
#                                                 'P.parameterDataType, '
#                                                 'P.childParameter, '
#                                                 'P.blockParameter, '
#                                                 'P.childParameterAlias, '
#                                                 'P.childParameterAttribute, '
#                                                 'P.parameterDescription '
#                                          'FROM pGlobal AS P '
#                                          'INNER JOIN tblClass_ChildStateValues AS S ON '
#                                                 'S.Class = P.parameterClass AND '
#                                                 'S.childClass = P.parameterSource '
#                                          'WHERE P.parameterClass = ? AND '
#                                                 'P.parameterType = "VAR_OUTPUT" AND '
#                                                 'P.isSFC = 0 AND '
#                                                 'P.isChild = 0 '
#                                          'GROUP BY P.childParameter '
#                                          'ORDER BY P.parameterOrder, '
#                                                 'P.parameterSource, '
#                                                 'P.childParameter'
#                                         ), # gClass
#    sqlCode.pClass                     : ('SELECT DISTINCT childParameter, '
#                                                 'childParameterAttribute, '
#                                                 'parameterDataType, '
#                                                 'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'isSFC = 0 AND isMC = 0 '
#                                          'ORDER BY parameterOrder, '
#                                                   'childParameter'
#                                         ), # gClass
#    sqlCode.pClassIN                   : ('SELECT DISTINCT childParameter, '
#                                                 'childParameterAttribute, '
#                                                 'parameterDataType, '
#                                                 'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterType = "VAR_INPUT" AND '
#                                                'isSFC = 0 AND isMC = 0 '
#                                          'ORDER BY childParameter'
#                                         ), # gClass
#    sqlCode.pClassIN_OUT               : ('SELECT DISTINCT childParameter, '
#                                                 'childParameterAttribute, '
#                                                 'parameterDataType, '
#                                                 'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterType = "VAR_IN_OUT" AND '
#                                                'isSFC = 0 AND isMC = 0 '
#                                          'ORDER BY childParameter'
#                                         ), # gClass
#    sqlCode.pClassOUT                  : ('SELECT DISTINCT childParameter, '
#                                                 'childParameterAttribute, '
#                                                 'parameterDataType, '
#                                                 'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterType = "VAR_OUTPUT" AND '
#                                                'isSFC = 0 AND isMC = 0 '
#                                          'ORDER BY childParameter'
#                                         ), # gClass
#    sqlCode.pPairInput                 : ('SELECT * '
#                                          'FROM tblClass_ParameterChild '
#                                          'WHERE parentPairClass = ? AND '
#                                                 'childPairAlias = ? AND '
#                                                 'pairIsWrite = 0 '
#                                          'ORDER BY childPairParameter'
#                                         ), # gClass, gAlias
#    sqlCode.pPairOutput                : ('SELECT * '
#                                          'FROM tblClass_ParameterChild '
#                                          'WHERE parentPairClass = ? AND '
#                                                 'childPairAlias = ? AND '
#                                                 'pairIsWrite = 1 '
#                                      'ORDER BY childPairParameter'
#                                         ), # gClass, gAlias
    sqlCode.pChildRead                 : ('SELECT DISTINCT operation, '
                                                 'childParameterAlias, '
                                                 'childParameterAttribute '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'childParameterAlias = ? AND '
                                                 'isMC = 0 AND '
                                                 'operation = "read" AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'upper(parameterDataType) != "BOOL" AND '
                                                 'substr(blockParameter, 1, 5) != "SYNC_" AND '
                                                 'length(childParameterAlias) > 0 '
                                          'ORDER BY childParameterAlias, '
                                                 'childParameter'
                                         ), # gClass, gAlias
    sqlCode.pChildReadBool             : ('SELECT DISTINCT operation, '
                                                 'childParameterAlias, '
                                                 'childParameterAttribute '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'childParameterAlias = ? AND '
                                                 'isMC = 0 AND '
                                                 'operation = "read" AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'upper(parameterDataType) = "BOOL" AND '
                                                 'substr(blockParameter, 1, 5) != "SYNC_" AND '
                                                 'length(childParameterAlias) > 0 '
                                          'ORDER BY childParameterAlias, '
                                                 'childParameter'
                                         ), # gClass, gAlias
    sqlCode.pChildWrite                : ('SELECT DISTINCT operation, '
                                                 'childParameterAlias, '
                                                 'childParameterAttribute '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'childParameterAlias = ? AND '
                                                 'isMC = 0 AND '
                                                 'operation = "write" AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'upper(parameterDataType) != "BOOL" AND '
                                                 'substr(blockParameter, 1, 5) != "SYNC_" AND '
                                                 'length(childParameterAlias) > 0 '
                                          'ORDER BY childParameterAlias, '
                                                 'childParameter'
                                         ), # gClass, gAlias
    sqlCode.pChildWriteBool            : ('SELECT DISTINCT operation, '
                                                 'childParameterAlias, '
                                                 'childParameterAttribute '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'childParameterAlias = ? AND '
                                                 'isMC = 0 AND '
                                                 'operation = "write" AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'upper(parameterDataType) = "BOOL" AND '
                                                 'substr(blockParameter, 1, 5) != "SYNC_" AND '
                                                 'length(childParameterAlias) > 0 '
                                          'ORDER BY childParameterAlias, '
                                                 'childParameter'
                                         ), # gClass, gAlias
    sqlCode.pParentRead                 : ('SELECT DISTINCT operation, '
                                                 'childParameterAlias, '
                                                 'childParameterAttribute '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'childParameterAlias = ? AND '
                                                 'isMC = 0 AND '
                                                 'operation = "read" AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'upper(parameterDataType) != "BOOL" AND '
                                                 'childParameterAttribute IN '
                                                     '(SELECT blockParameter '
                                                         'FROM pGlobal '
                                                         'WHERE parameterClass = ?) '
                                          'ORDER BY childParameterAlias, '
                                                 'childParameter'
                                         ), # gClass, gAlias
    sqlCode.pParentReadBool             : ('SELECT DISTINCT operation, '
                                                 'childParameterAlias, '
                                                 'childParameterAttribute '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'childParameterAlias = ? AND '
                                                 'isMC = 0 AND '
                                                 'operation = "read" AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'upper(parameterDataType) = "BOOL" AND '
                                                 'childParameterAttribute IN '
                                                     '(SELECT blockParameter '
                                                         'FROM pGlobal '
                                                         'WHERE parameterClass = ?) '
                                          'ORDER BY childParameterAlias, '
                                                 'childParameter'
                                         ), # gClass, gAlias
    sqlCode.pParentWrite                : ('SELECT DISTINCT operation, '
                                                 'childParameterAlias, '
                                                 'childParameterAttribute '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'childParameterAlias = ? AND '
                                                 'isMC = 0 AND '
                                                 'operation = "write" AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'upper(parameterDataType) != "BOOL" AND '
                                                 'childParameterAttribute IN '
                                                     '(SELECT blockParameter '
                                                         'FROM pGlobal '
                                                         'WHERE parameterClass = ?) '
                                          'ORDER BY childParameterAlias, '
                                                 'childParameter'
                                         ), # gClass, gAlias
    sqlCode.pParentWriteBool            : ('SELECT DISTINCT operation, '
                                                 'childParameterAlias, '
                                                 'childParameterAttribute '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'childParameterAlias = ? AND '
                                                 'isMC = 0 AND '
                                                 'operation = "write" AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'upper(parameterDataType) = "BOOL" AND '
                                                 'childParameterAttribute IN '
                                                     '(SELECT blockParameter '
                                                         'FROM pGlobal '
                                                         'WHERE parameterClass = ?) '
                                          'ORDER BY childParameterAlias, '
                                                 'childParameter'
                                         ), # gClass, gAlias
#                                                 'blockParameter NOT LIKE childParameterAlias || "%" AND '
#    sqlCode.pPairInputDefine           : ('SELECT * '
#                                          'FROM tblClass_ParameterChild '
#                                          'WHERE parentPairClass = ? AND '
#                                                 'pairIsWrite = 0 '
#                                          'ORDER BY childPairParameter'
#                                         ), # gClass
#    sqlCode.pPairOutputDefine          : ('SELECT * '
#                                          'FROM tblClass_ParameterChild '
#                                          'WHERE parentPairClass = ? AND '
#                                                 'pairIsWrite = 1 '
#                                          'ORDER BY childPairParameter'
#                                         ), # gClass
    sqlCode.pChildReadDefine           : ('SELECT DISTINCT blockParameter, '
                                                 'parameterDataType '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isMC = 0 AND '
                                                 'operation = "read" AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'length(childParameterAlias) > 0 '
                                          'ORDER BY childParameterAlias, '
                                                 'childParameter'
                                         ), # gClass
#                                                 'blockParameter NOT LIKE childParameterAlias || "%" AND '
    sqlCode.pChildWriteDefine          : ('SELECT DISTINCT blockParameter, '
                                                 'parameterDataType '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isMC = 0 AND '
                                                 'operation = "write" AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'length(childParameterAlias) > 0 '
                                          'ORDER BY childParameterAlias, '
                                                 'childParameter'
                                         ), # gClass
    sqlCode.getSFCBlockParameters      : ('SELECT DISTINCT Level, '
                                                 'parameterClass, '
                                                 'childParameter, '
                                                 'blockParameter, '
                                                 'parameterOrder, '
                                                 'parameterType, '
                                                 'parameterDataType, '
                                                 'parameterDescription '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'isSFC = 1 AND '
                                                 'isChild = 0 AND '
                                                 'isLink = 0 '
                                          'ORDER BY parameterOrder, '
                                                 'childParameter'
                                         ), # gClass
#    sqlCode.pBLOCK_READ                : ('SELECT DISTINCT Level, '
#                                                 'parameterClass, '
#                                                 'blockParameter, '
#                                                 'upper(parameterDataType) AS PARAMETERDATATYPE '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                 'parameterType LIKE "VAR_%" AND '
#                                                 'isChild = 0 AND '
#                                                 'isLink = 0 AND '
#                                                 'isMC = 1 AND '
#                                                 'isWrite = 0 AND '
#                                                 'isRecipe = 0 '
#                                          'ORDER BY childParameter'
#                                         ), # gClass
#    sqlCode.pBLOCK_WRITE               : ('SELECT DISTINCT Level, '
#                                                 'parameterClass, '
#                                                 'blockParameter, '
#                                                 'upper(parameterDataType) AS PARAMETERDATATYPE '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                 'parameterType LIKE "VAR_%" AND '
#                                                 'isChild = 0 AND '
#                                                 'isLink = 0 AND '
#                                                 'isMC = 1 AND '
#                                                 'isWrite = 1 AND '
#                                                 'isRecipe = 0 '
#                                          'ORDER BY childParameter'
#                                         ), # gClass
    sqlCode.pBLOCK_RECIPE              : ('SELECT DISTINCT Level, '
                                                 'parameterClass, '
                                                 'blockParameter, '
                                                 'upper(parameterDataType) AS PARAMETERDATATYPE, '
                                                 'parameterDescription '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'isChild = 0 AND '
                                                 'isLink = 0 AND '
                                                 'isRecipe = 1 '
                                          'ORDER BY childParameter'
                                         ), # gClass
    sqlCode.pBLOCK_RECIPE_EXISTS       : ('SELECT DISTINCT Level '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'isChild = 0 AND '
                                                 'isLink = 0 AND '
                                                 'isRecipe = 1 '
                                          'LIMIT 1'
                                         ), # gClass
#    sqlCode.pCHILD_NotMC               : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                 'parameterType LIKE "VAR_%" AND '
#                                                 'isSFC = 1 AND '
#                                                 'isChild = 1 AND '
#                                                 'isMC = 0 AND '
#                                                 'isLink = 0 '
#                                          'ORDER BY parameterOrder, '
#                                                 'childParameter'
#                                         ), # gClass
#    sqlCode.pSFC                       : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                'isSFC = 1 AND '
#                                                'isChild = 0 AND '
#                                                'isLink = 0 AND '
#                                                'isSelection = 0 AND '
#                                                'parameterType != "VAR" '
#                                          'ORDER BY parameterOrder, '
#                                                 'parameterSource, '
#                                                 'childParameter'
#                                         ), # gClass
    sqlCode.pSFCParametersRecipe       : ("SELECT * FROM pGlobal WHERE parameterSource = ? AND isSFC = 1 AND isChild = 0 AND isLink = 0 AND isSelection = 0 AND parameterType != 'VAR' AND childParameter LIKE '_r\_%' " + "ESCAPE '\\' ORDER BY parameterOrder, parameterSource, childParameter"), # gClass
    sqlCode.pSFCParametersRecipeExist  : ("SELECT Level FROM pGlobal WHERE parameterSource = ? AND isSFC = 1 AND isChild = 0 AND isLink = 0 AND isSelection = 0 AND parameterType != 'VAR' AND childParameter LIKE '_r\_%' " + "ESCAPE '\\' LIMIT 1"), # gClass
#    sqlCode.pSFCParametersRecipeExist  : ('SELECT Level '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                'isSFC = 1 AND '
#                                                'isChild = 0 AND '
#                                                'isLink = 0 AND '
#                                                'isSelection = 0 AND '
#                                                'parameterType != "VAR" AND '
#                                                'childParameter LIKE "_r\_%" '
#                                                "ESCAPE '\' "
#                                          'LIMIT 1'
#                                         ), # gClass
    sqlCode.pSFCParametersBlock        : ("SELECT * FROM pGlobal WHERE parameterSource = ? AND isSFC = 1 AND isChild = 0 AND isLink = 0 AND isSelection = 0 AND parameterType != 'VAR' AND childParameter NOT LIKE '_r\_%' " + "ESCAPE '\\' ORDER BY parameterOrder, parameterSource, childParameter"), # gClass
#    sqlCode.pSFCParametersBlockWrite   : ("SELECT * FROM pGlobal WHERE parameterSource = ? AND isSFC = 1 AND isChild = 0 AND isLink = 0 AND isSelection = 0 AND isWrite = 1 AND parameterType != 'VAR' AND childParameter NOT LIKE '_r\_%' " + "ESCAPE '\\' ORDER BY parameterOrder, parameterSource, childParameter"), # gClass
#    sqlCode.pSFCParametersOthers       : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                'isSFC = 1 AND '
#                                                'isChild = 0 AND '
#                                                'isLink = 0 AND '
#                                                'isSelection = 0 AND '
#                                                'parameterType != "VAR" AND '
#                                                'childParameter NOT LIKE "_r\_%" '
#                                                "ESCAPE '\' "
#                                          'ORDER BY parameterOrder, '
#                                                 'parameterSource, '
#                                                 'childParameter'
#                                         ), # gClass
    sqlCode.pSFCLink                   : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterSource = ? AND '
                                                'isChild = 0 AND '
                                                'isSFC = 1 AND '
                                                'isLink = 1 AND '
                                                'isSelection = 0 AND '
                                                'parameterType != "VAR" '
                                          'ORDER BY parameterOrder, '
                                                 'parameterSource, '
                                                 'childParameter'
                                         ), # gClass
#    sqlCode.pSFCLinkOutput             : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                'isChild = 0 AND '
#                                                'isSFC = 1 AND '
#                                                'isLink = 1 AND '
#                                                'isSelection = 0 AND '
#                                                'isWrite = 1 AND '
#                                                'parameterType != "VAR" '
#                                          'ORDER BY parameterOrder, '
#                                                 'parameterSource, '
#                                                 'childParameter'
#                                         ), # gClass
    sqlCode.pClassBlockRead            : ('SELECT DISTINCT blockParameter, '
                                                 'parameterDataType  '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                'isChild = 0 AND '
                                                'isLink = 0 AND '
                                                'isMC = 0 AND '
                                                'operation = "read" AND '
                                                'length(childParameterAlias) = 0 AND '
                                                'parameterType != "VAR" '
                                          'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pClassBlockWrite           : ('SELECT DISTINCT blockParameter, '
                                                 'parameterDataType  '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                'isChild = 0 AND '
                                                'isLink = 0 AND '
                                                'isMC = 0 AND '
                                                'operation = "write" AND '
                                                'length(childParameterAlias) = 0 AND '
                                                'parameterType != "VAR" '
                                          'ORDER BY blockParameter'
                                         ), # gClass
#    sqlCode.pSFCCallingIN_OUT          : ('SELECT DISTINCT '
#                                                'blockParameter, '
#                                                'parameterDataType, '
#                                                'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                'parameterType = "VAR_OUTPUT" AND '
#                                                'isChild = 0'
#                                         ), # gClass
#    sqlCode.pSFCCallingOUT             : ('SELECT DISTINCT '
#                                                'blockParameter, '
#                                                'parameterDataType, '
#                                                'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                'parameterType = "VAR_IN_OUT" AND '
#                                                'isChild = 0'
#                                         ), # gClass
    sqlCode.pBlock                     : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isChild = 0 AND '
                                                 'isSFC = 0 '
                                          'ORDER BY parameterOrder, '
                                                 'parameterSource, '
                                                 'childParameter'
                                         ), # gClass
    sqlCode.pBlockIN                   : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'parameterType = "VAR_INPUT" AND '
                                                 'isChild = 0 AND '
                                                 'isSFC = 0 '
                                          'ORDER BY parameterOrder, '
                                                 'parameterSource, '
                                                 'childParameter'
                                         ), # gClass
    sqlCode.pBlockIN_OUT               : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'parameterType = "VAR_IN_OUT" AND '
                                                 'isChild = 0 AND '
                                                 'isSFC = 0 '
                                          'ORDER BY parameterOrder, '
                                                 'parameterSource, '
                                                 'childParameter'
                                         ), # gClass
    sqlCode.pBlockOUT                  : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'parameterType = "VAR_OUTPUT" AND '
                                                 'isChild = 0 AND '
                                                 'isSFC = 0 '
                                          'ORDER BY parameterOrder, '
                                                 'parameterSource, '
                                                 'childParameter'
                                         ), # gClass
    sqlCode.numChildren                : ('SELECT COUNT(childParameterAlias) AS NUM '
                                          'FROM tblClass_Child '
                                          'WHERE [Class] = ?'
                                         ), # gClass
    sqlCode.numReadBool                : ('SELECT COUNT(blockParameter) AS NUM '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                              'parameterDataType = "BOOL" AND '
                                              'parameterType LIKE "VAR_%" AND '
                                              'isMC = 0 AND '
                                              'operation = "read" AND '
                                              'isChild = 0 AND '
                                              'isLink = 0 AND '
                                              'isSelection = 0'
                                         ), # gClass
    sqlCode.numReadInt                 : ('SELECT COUNT(blockParameter) AS NUM '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                              'parameterDataType = "INT" AND '
                                              'parameterType LIKE "VAR_%" AND '
                                              'isMC = 0 AND '
                                              'operation = "read" AND '
                                              'isChild = 0 AND '
                                              'isLink = 0 AND '
                                              'isSelection = 0'
                                         ), # gClass
    sqlCode.numReadReal                : ('SELECT COUNT(blockParameter) AS NUM '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                              'parameterDataType = "REAL" AND '
                                              'parameterType LIKE "VAR_%" AND '
                                              'isMC = 0 AND '
                                              'operation = "read" AND '
                                              'isChild = 0 AND '
                                              'isLink = 0 AND '
                                              'isSelection = 0'
                                         ), # gClass
    sqlCode.numReadTime                : ('SELECT COUNT(blockParameter) AS NUM '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                              'parameterDataType = "TIME" AND '
                                              'parameterType LIKE "VAR_%" AND '
                                              'isMC = 0 AND '
                                              'operation = "read" AND '
                                              'isMC = 0 AND '
                                              'isChild = 0 AND '
                                              'isLink = 0 AND '
                                              'isSelection = 0'
                                         ), # gClass
    sqlCode.numWriteBool                : ('SELECT COUNT(blockParameter) AS NUM '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                              'parameterDataType = "BOOL" AND '
                                              'parameterType LIKE "VAR_%" AND '
                                              'isMC = 0 AND '
                                              'operation = "write" AND '
                                              'isChild = 0 AND '
                                              'isLink = 0 AND '
                                              'isSelection = 0'
                                         ), # gClass
    sqlCode.numWriteInt                 : ('SELECT COUNT(blockParameter) AS NUM '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                              'parameterDataType = "INT" AND '
                                              'parameterType LIKE "VAR_%" AND '
                                              'isMC = 0 AND '
                                              'operation = "write" AND '
                                              'isChild = 0 AND '
                                              'isLink = 0 AND '
                                              'isSelection = 0'
                                         ), # gClass
    sqlCode.numWriteReal                : ('SELECT COUNT(blockParameter) AS NUM '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                              'parameterDataType = "REAL" AND '
                                              'parameterType LIKE "VAR_%" AND '
                                              'isMC = 0 AND '
                                              'operation = "write" AND '
                                              'isChild = 0 AND '
                                              'isLink = 0 AND '
                                              'isSelection = 0'
                                         ), # gClass
    sqlCode.numWriteTime                : ('SELECT COUNT(blockParameter) AS NUM '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                              'parameterDataType = "TIME" AND '
                                              'parameterType LIKE "VAR_%" AND '
                                              'isMC = 0 AND '
                                              'operation = "write" AND '
                                              'isChild = 0 AND '
                                              'isLink = 0 AND '
                                              'isSelection = 0'
                                         ), # gClass
    sqlCode.pReadBool                  : ('SELECT DISTINCT parameterClass, '
                                                'blockParameter, '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t2 '
                                                'WHERE t2.blockParameter < t1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "BOOL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                '+  '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t3 '
                                                'WHERE t3.blockParameter = T1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "BOOL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                'AS PIDX '
                                                'FROM pGlobal t1 '
                                                'WHERE parameterClass = ? AND '
                                                    'parameterDataType = "BOOL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0 '
                                                'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pReadInt                   : ('SELECT DISTINCT parameterClass, '
                                                'blockParameter, '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t2 '
                                                'WHERE t2.blockParameter < t1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "INT" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                '+  '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t3 '
                                                'WHERE t3.blockParameter = T1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "INT" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                'AS PIDX '
                                                'FROM pGlobal t1 '
                                                'WHERE parameterClass = ? AND '
                                                    'parameterDataType = "INT" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0 '
                                                'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pReadReal                  : ('SELECT DISTINCT parameterClass, '
                                                'blockParameter, '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t2 '
                                                'WHERE t2.blockParameter < t1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "REAL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                '+  '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t3 '
                                                'WHERE t3.blockParameter = T1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "REAL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                'AS PIDX '
                                                'FROM pGlobal t1 '
                                                'WHERE parameterClass = ? AND '
                                                    'parameterDataType = "REAL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0 '
                                                'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pReadTime                  : ('SELECT DISTINCT parameterClass, '
                                                'blockParameter, '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t2 '
                                                'WHERE t2.blockParameter < t1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "TIME" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                '+  '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t3 '
                                                'WHERE t3.blockParameter = T1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "TIME" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                'AS PIDX '
                                                'FROM pGlobal t1 '
                                                'WHERE parameterClass = ? AND '
                                                    'parameterDataType = "TIME" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "read" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0 '
                                                'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pWriteBool                 : ('SELECT DISTINCT parameterClass, '
                                                'blockParameter, '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t2 '
                                                'WHERE t2.blockParameter < t1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "BOOL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                '+  '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t3 '
                                                'WHERE t3.blockParameter = T1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "BOOL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                'AS PIDX '
                                                'FROM pGlobal t1 '
                                                'WHERE parameterClass = ? AND '
                                                    'parameterDataType = "BOOL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0 '
                                                'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pWriteInt                  : ('SELECT DISTINCT parameterClass, '
                                                'blockParameter, '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t2 '
                                                'WHERE t2.blockParameter < t1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "INT" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                '+  '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t3 '
                                                'WHERE t3.blockParameter = T1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "INT" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                'AS PIDX '
                                                'FROM pGlobal t1 '
                                                'WHERE parameterClass = ? AND '
                                                    'parameterDataType = "INT" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0 '
                                                'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pWriteReal                 : ('SELECT DISTINCT parameterClass, '
                                                'blockParameter, '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t2 '
                                                'WHERE t2.blockParameter < t1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "REAL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                '+  '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t3 '
                                                'WHERE t3.blockParameter = T1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "REAL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                'AS PIDX '
                                                'FROM pGlobal t1 '
                                                'WHERE parameterClass = ? AND '
                                                    'parameterDataType = "REAL" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0 '
                                                'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pWriteTime                 : ('SELECT DISTINCT parameterClass, '
                                                'blockParameter, '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t2 '
                                                'WHERE t2.blockParameter < t1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "TIME" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                '+  '
                                                '(SELECT COUNT (DISTINCT blockParameter) '
                                                'FROM pGlobal t3 '
                                                'WHERE t3.blockParameter = T1.blockParameter AND '
                                                    'parameterClass = ? AND '
                                                    'parameterDataType = "TIME" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0) '
                                                'AS PIDX '
                                                'FROM pGlobal t1 '
                                                'WHERE parameterClass = ? AND '
                                                    'parameterDataType = "TIME" AND '
                                                    'parameterType LIKE "VAR_%" AND '
                                                    'isMC = 0 AND '
                                                    'operation = "write" AND '
                                                    'isChild = 0 AND '
                                                    'isLink = 0 AND '
                                                    'isSelection = 0 '
                                                'ORDER BY blockParameter'
                                         ), # gClass
    sqlCode.pEventLogMsgClass          : ('SELECT idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1) AS cOffset, '
                                                 '((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1)) / 16) AS cWord, '
                                                 'idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1) - 16 * (((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1)) / 16)) AS cBit, '
                                                 'parameterSource, parameterState, childParameter, blockParameter, parameterDescription, cast(val AS int) AS magicNum '
                                          'FROM pEventLogMsg LEFT JOIN bitInt on cast(bit AS int) = idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1) - 16 * (((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1)) / 16)) '
                                          'WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) '
                                          'ORDER BY idxEvent'
                                         ), # gClass
    sqlCode.pEventLogMsgInstance       : ('SELECT idxEvent - (SELECT idxEvent FROM pEventLogMsg ORDER BY idxEvent LIMIT 1) AS gOffset, '
                                                 '((idxEvent - (SELECT idxEvent FROM pEventLogMsg ORDER BY idxEvent LIMIT 1)) / 16) AS gWord, '
                                                 'idxEvent - (SELECT idxEvent FROM pEventLogMsg ORDER BY idxEvent LIMIT 1) - 16 * (((idxEvent - (SELECT idxEvent FROM pEventLogMsg ORDER BY idxEvent LIMIT 1)) / 16)) AS gBit, '
                                                 'idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = ? ORDER BY idxEvent LIMIT 1) AS cOffset, '
                                                 '((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = ? ORDER BY idxEvent LIMIT 1)) / 16) AS cWord, '
                                                 'idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = ? ORDER BY idxEvent LIMIT 1) - 16 * (((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = ? ORDER BY idxEvent LIMIT 1)) / 16)) AS cBit, '
                                                 'cast(G.val AS int) AS gMagicNum, cast(C.val AS int) AS cMagicNum, * '
                                          'FROM pEventLogMsg '
                                          'LEFT JOIN bitInt AS G on cast(G.bit AS int) = idxEvent - (SELECT idxEvent FROM pEventLogMsg ORDER BY idxEvent LIMIT 1) - 16 * (((idxEvent - (SELECT idxEvent FROM pEventLogMsg ORDER BY idxEvent LIMIT 1)) / 16)) '
                                          'LEFT JOIN bitInt AS C on cast(C.bit AS int) = idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = ? ORDER BY idxEvent LIMIT 1) - 16 * (((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = ? ORDER BY idxEvent LIMIT 1)) / 16)) '
                                          'WHERE Instance = ? '
                                          'ORDER BY idxEvent'
                                         ), # gClass
    sqlCode.pEventLogMsgExists         : ('SELECT pKey '
                                          'FROM pEventLogMsg '
                                          'WHERE Class = ? '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogMsgMaxClass       : ('SELECT MAX((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1)) / 16) AS cWordMax '
                                          'FROM pEventLogMsg '
                                          'WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogMsgMaxInstance    : ('SELECT MAX((idxEvent - (SELECT idxEvent FROM pEventLogMsg ORDER BY idxEvent LIMIT 1)) / 16) AS gWordMax '
                                          'FROM pEventLogMsg '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogMsgWordClass      : ('SELECT DISTINCT ((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1)) / 16) AS cWord '
                                          'FROM pEventLogMsg '
                                          'WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) '
                                          'ORDER BY idxEvent'
                                         ), # gClass
    sqlCode.pEventLogMsgWordInstance   : ('SELECT DISTINCT '
                                                '((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = ? ORDER BY idxEvent LIMIT 1)) / 16) AS cWord, '
                                                'Instance '
                                          'FROM pEventLogMsg '
                                          'WHERE Instance = ? '
                                          'ORDER BY idxEvent'
                                         ), # gInstance
    sqlCode.pEventLogMsgWordBitClass   : ('SELECT DISTINCT ((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1)) / 16) AS cWord, '
                                                 'idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1) - 16 * (((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) ORDER BY idxEvent LIMIT 1)) / 16)) AS cBit '
                                          'FROM pEventLogMsg '
                                          'WHERE Instance = (SELECT Instance FROM tblInstance WHERE CLASS = ? LIMIT 1) '
                                          'ORDER BY idxEvent'
                                         ), # gClass
    sqlCode.pEventLogMsgWordBitInstance: ('SELECT DISTINCT '
                                                 '((idxEvent - (SELECT idxEvent FROM pEventLogMsg WHERE Instance = ? ORDER BY idxEvent LIMIT 1)) / 16) AS cWord '
                                                 'FROM pEventLogMsg '
                                                 'WHERE Instance = ? '
                                                 'ORDER BY idxEvent'
                                         ), # gInstance
#    sqlCode.pEventLogMsg               : ('SELECT * '
#                                          'FROM pEventLogMsg '
#                                          'WHERE Class = ? '
#                                          'ORDER BY idxEvent'
#                                         ), # gClass
    sqlCode.simulateDI1                : ('SELECT Instance AS sInstance, '
                                                 'Class AS sClass, '
                                                 'printf("%d", IDX) AS sIDX '
                                          'FROM tblInstance '
                                          'WHERE Class = "DI1" AND '
                                                 '(Parent = ? OR '
                                                 'GParent = ? OR '
                                                 'GGParent = ? OR '
                                                 'GGGParent = ?) '
                                          'ORDER BY cast(IDX as Int)'
                                         ), # gInstance
    sqlCode.simulateDI2                : ('SELECT Instance AS sInstance, '
                                                 'Class AS sClass, '
                                                 'printf("%d", IDX) AS sIDX '
                                          'FROM tblInstance '
                                          'WHERE Class = "DI2" AND '
                                                 '(Parent = ? OR '
                                                 'GParent = ? OR '
                                                 'GGParent = ? OR '
                                                 'GGGParent = ?) '
                                          'ORDER BY cast(IDX as Int)'
                                         ), # gInstance
    sqlCode.simulatePOS2               : ('SELECT Instance AS sInstance, '
                                                 'Class AS sClass, '
                                                 'printf("%d", IDX) AS sIDX '
                                          'FROM tblInstance '
                                          'WHERE Class = "POS2" AND '
                                                 '(Parent = ? OR '
                                                 'GParent = ? OR '
                                                 'GGParent = ? OR '
                                                 'GGGParent = ?) '
                                          'ORDER BY cast(IDX as Int)'
                                         ), # gInstance
    sqlCode.simulatePOS4               : ('SELECT Instance AS sInstance, '
                                                 'Class AS sClass, '
                                                 'printf("%d", IDX) AS sIDX '
                                          'FROM tblInstance '
                                          'WHERE Class = "POS4" AND '
                                                 '(Parent = ? OR '
                                                 'GParent = ? OR '
                                                 'GGParent = ? OR '
                                                 'GGGParent = ?) '
                                          'ORDER BY cast(IDX as Int)'
                                         ), # gInstance
    sqlCode.simulateZSC1               : ('SELECT Instance AS sInstance, '
                                                 'Class AS sClass, '
                                                 'printf("%d", IDX) AS sIDX '
                                          'FROM tblInstance '
                                          'WHERE Class = "ZSC1" AND '
                                                 '(Parent = ? OR '
                                                 'GParent = ? OR '
                                                 'GGParent = ? OR '
                                                 'GGGParent = ?) '
                                          'ORDER BY cast(IDX as Int)'
                                         ), # gInstance
    sqlCode.simulateZSC2               : ('SELECT Instance AS sInstance, '
                                                 'Class AS sClass, '
                                                 'printf("%d", IDX) AS sIDX '
                                          'FROM tblInstance '
                                          'WHERE Class = "ZSC2" AND '
                                                 '(Parent = ? OR '
                                                 'GParent = ? OR '
                                                 'GGParent = ? OR '
                                                 'GGGParent = ?) '
                                          'ORDER BY cast(IDX as Int)'
                                         ), # gInstance
#    sqlCode.pBLKCallingIN_OUT          : ('SELECT DISTINCT '
#                                                'blockParameter, '
#                                                'parameterDataType, '
#                                                'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterType = "VAR_OUTPUT" AND '
#                                                'isChild = 0'
#                                         ), # gClass
#    sqlCode.pBLKCallingOUT             : ('SELECT DISTINCT '
#                                                'blockParameter, '
#                                                'parameterDataType, '
#                                                'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterClass = ? AND '
#                                                'parameterType = "VAR_IN_OUT" AND '
#                                                'isChild = 0'
#                                         ), # gClass
#                                         SELECT parameterSource, childParameter, blockParameter, parameterType, parameterDataType, parameterDescription
#FROM pGlobal
#WHERE parameterClass = 'EMC2' AND (parameterType = "VAR_INPUT" OR parameterType = "VAR_OUTPUT" OR parameterType = "VAR_IN_OUT") AND isChild = 0 ORDER BY parameterOrder
}
#SELECT parameterSource, childParameter
#FROM pGlobal WHERE isEventDataTime = 1 AND "_log" || childParameter NOT IN (SELECT childParameter FROM pGlobal WHERE isEventLogTime = 1)
