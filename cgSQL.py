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
    createClassesForLevel              = -4
    createClassNone                    = -5
    createInstances                    = -6
    createInstancesGlobal              = -7
    numInstances                       = -8
    GLOBAL_INSTANCE                    = -9
    createLevel                        = -10
    createParameterSFC                 = -11
    createProgramFiles                 = -12
    createProgramFilesCount            = -20
    defaultParameters                  = -21
    documentInfo                       = -22
    checkIfChildParameter              = -23
    checkIfLinkParameter               = -24
    getChildIndex                      = -25
    insertGlobalParameters             = -26
    addParametersClass                 = -27
    addParametersChild                 = -28
    addParametersSelect                = -29
    addParametersSFC                   = -30
    getUserParametersChild             = -31
    processLevel                       = -40
    processLevelCount                  = -41
    tblCreateGlobalParameter           = -42
    versionHistory                     = -43
    VERHIST                            = -44
    ANALOG                             = -45
    ANALOG_EMBED                       = -46
    callList                           = -47
    callListExists                     = -48
    callListExistsGlobal               = -49
    callListExistsCRIL                 = -50
    callListExistsNCRIL                = -60
    CHILD                              = -61
    CHILD_ACQUIRED                     = -62
    CHILD_ACQUIRE_REQ                  = -63
    CHILD_INDEX_MAX                    = -64
    CHILD_INIT_COMMAND_TRUE            = -65
    CHILD_INIT_COMMAND_FALSE           = -66
    CHILD_INSTANCE                     = -67
    CHILD_INSTANCE_BIND                = -68
    CRIL                               = -69
    CRIL_EXISTS                        = -70
    CRIL_INSTANCE                      = -71
    CRIL_NUM                           = -72
    CRIL_TARGET                        = -73
    NCRIL                              = -74
    NCRIL_EXISTS                       = -80
    NCRIL_INSTANCE                     = -81
    NCRIL_NUM                          = -82
    NCRIL_TARGET                       = -83
    HYGIENE                            = -84
    INSTANCE_ALL                       = -85
    INSTANCE_BLK                       = -86
    INSTANCE_SFC                       = -87
    ISOWNED                            = -88
    LINK                               = -89
    LINK_BLK                           = -90
    UNIQUEID                           = -91
    PARAMETER_ACQUIRE                  = -92
    PARAMETER_INDEX_MAX                = -93
    PARENT                             = -100
    PARM_CHILD_VAR_INPUT               = -101
    PARM_CHILD_VAR_OUTPUT              = -102
    PARM_CHILD_VAR_IN_OUT              = -103
    PARM_INSTANCE_VAR_INPUT            = -104
    PARM_INSTANCE_VAR_OUTPUT           = -105
    PARM_INSTANCE_VAR_IN_OUT           = -106
    PARM_INSTANCE_VAR                  = -107
    PARM_CLASS_VAR_INPUT               = -108
    PARM_CLASS_VAR_IN_OUT              = -109
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
    STATE                              = -130
    STATE_TIMER                        = -131
    TAGS                               = -132
    TAGSALT                            = -133
    TIMER                              = -134
    TRANSITION                         = -140
    getSFCBlockParameters              = -151
    pBLOCK_UNIQUE                      = -152
    pBLOCK_RECIPE                      = -153
    pBLOCK_RECIPE_EXISTS               = -154
    pCHILD_NotMC                       = -155
    pBlock                             = -141
    pBlockIN                           = -142
    pBlockIN_OUT                       = -143
    pBlockOUT                          = -144
    pChildIN                           = -145
    pChildIN_OUT                       = -146
    pChildOUT                          = -147
    pClass                             = -148
    pClassIN                           = -149
    pClassIN_OUT                       = -150
    pClassOUT                          = -160
    pSFC                               = -161
    pSFCChild                          = -162
    pSFCChildIN                        = -163
    pSFCChildIN_OUT                    = -164
    pSFCChildOUT                       = -165
    pEventExists                       = -166
    pEventConfirm                      = -167
    pEventPrompt                       = -168
    pEventLogMsg                       = -169
    pEventLogReal                      = -180
    pEventLogTime                      = -181
    pEventDataReal                     = -182
    pEventDataTime                     = -183
    pEventConfirmExists                = -184
    pEventPromptExists                 = -185
    pEventLogMsgExists                 = -186
    pEventLogRealExists                = -187
    pEventLogTimeExists                = -188
    pEventDataRealExists               = -189
    pEventDataTimeExists               = -200
    pEventConfirmNoExists              = -201
    pEventConfirmList                  = -202
    pEventPromptList                   = -203
    pEventLogMsgList                   = -204
    pEventLogRealList                  = -205
    pEventLogTimeList                  = -206
    pEventDataRealList                 = -207
    pEventDataTimeList                 = -208
    pEventConfirmNum                   = -209
    pEventPromptNum                    = -220
    pEventLogMsgNum                    = -221
    pEventLogRealNum                   = -222
    pEventLogTimeNum                   = -223
    pEventDataRealNum                  = -224
    pEventDataTimeNum                  = -225

prm = {
    sqlCode.ANALOG                     : ['gInstance'],
    sqlCode.ANALOG_EMBED               : ['gInstance'],
    sqlCode.callList                   : ['gLevel'],
    sqlCode.callListExists             : ['gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.callListExistsGlobal       : ['gClass'],
    sqlCode.callListExistsCRIL         : [],
    sqlCode.callListExistsNCRIL        : [],
    sqlCode.createClassNone            : [],
#    sqlCode.createInstances            : ['gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent', 'gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent', 'gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.createInstances            : ['gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.createInstancesGlobal      : ['gClass'],
#    sqlCode.numInstances               : ['gClass', 'gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.numInstances               : ['gClass'],
    sqlCode.CHILD                      : ['gClass', 'gClass', 'gClass'],
    sqlCode.CHILD_ACQUIRED             : ['gClass', 'gState'],
    sqlCode.CHILD_ACQUIRE_REQ          : ['gClass', 'gState'],
    sqlCode.CHILD_INDEX_MAX            : ['gClass'],
    sqlCode.CHILD_INIT_COMMAND_TRUE    : ['gClass', 'gState'],
    sqlCode.CHILD_INIT_COMMAND_FALSE   : ['gClass', 'gState'],
    sqlCode.CHILD_INSTANCE             : ['gInstance', 'gParent', 'gParent', 'gParent', 'gClass', 'gClass'],
    sqlCode.CHILD_INSTANCE_BIND        : ['gInstance', 'gParent', 'gParent', 'gParent', 'gClass', 'gState'],
    sqlCode.CRIL                       : [],
    sqlCode.CRIL_EXISTS                : ['gInstance'],
    sqlCode.CRIL_INSTANCE              : ['gInstance'],
    sqlCode.CRIL_NUM                   : [],
    sqlCode.CRIL_TARGET                : ['gInstance'],
    sqlCode.NCRIL                      : [],
    sqlCode.NCRIL_EXISTS               : ['gInstance'],
    sqlCode.NCRIL_INSTANCE             : ['gInstance'],
    sqlCode.NCRIL_NUM                  : [],
    sqlCode.NCRIL_TARGET               : ['gInstance'],
    sqlCode.GLOBAL_INSTANCE            : ['gClass'],
    sqlCode.HYGIENE                    : ['gClass'],
    sqlCode.INSTANCE_ALL               : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.INSTANCE_BLK               : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.INSTANCE_SFC               : [],
    sqlCode.ISOWNED                    : ['gInstance'],
    sqlCode.LINK                       : ['gInstance'],
    sqlCode.LINK_BLK                   : ['gInstance'],
    sqlCode.UNIQUEID                   : [],
    sqlCode.PARAMETER_ACQUIRE          : ['gClass', 'gState'],
    sqlCode.PARAMETER_INDEX_MAX        : ['gClass'],
    sqlCode.PARENT                     : [],
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
    sqlCode.SELVALUE                   : ['gClass', 'gSelectParameter' , 'gSelectSelection'],
    sqlCode.SFC                        : ['gClass'],
    sqlCode.STATE                      : ['gClass'],
    sqlCode.STATE_TIMER                : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.TAGS                       : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.TAGSALT                    : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.TIMER                      : ['gClass'],
    sqlCode.pEventExists               : ['gClass'],
    sqlCode.pEventConfirm              : ['gClass'],
    sqlCode.pEventPrompt               : ['gClass'],
    sqlCode.pEventLogMsg               : ['gClass'],
    sqlCode.pEventLogReal              : ['gClass'],
    sqlCode.pEventLogTime              : ['gClass'],
    sqlCode.pEventDataReal             : ['gClass'],
    sqlCode.pEventDataTime             : ['gClass'],
    sqlCode.pEventConfirmExists        : ['gClass'],
    sqlCode.pEventPromptExists         : ['gClass'],
    sqlCode.pEventLogMsgExists         : ['gClass'],
    sqlCode.pEventLogRealExists        : ['gClass'],
    sqlCode.pEventLogTimeExists        : ['gClass'],
    sqlCode.pEventDataRealExists       : ['gClass'],
    sqlCode.pEventDataTimeExists       : ['gClass'],
    sqlCode.pEventConfirmNoExists      : ['gClass', 'gPrompt'],
    sqlCode.pEventConfirmList          : [],
    sqlCode.pEventPromptList           : [],
    sqlCode.pEventLogMsgList           : [],
    sqlCode.pEventLogRealList          : [],
    sqlCode.pEventLogTimeList          : [],
    sqlCode.pEventDataRealList         : [],
    sqlCode.pEventDataTimeList         : [],
    sqlCode.pEventConfirmNum           : [],
    sqlCode.pEventPromptNum            : [],
    sqlCode.pEventLogMsgNum            : [],
    sqlCode.pEventLogRealNum           : [],
    sqlCode.pEventLogTimeNum           : [],
    sqlCode.pEventDataRealNum          : [],
    sqlCode.pEventDataTimeNum          : [],
    sqlCode.pChildIN                   : ['gClass'],
    sqlCode.pChildIN_OUT               : ['gClass'],
    sqlCode.pChildOUT                  : ['gClass'],
    sqlCode.pClass                     : ['gClass'],
    sqlCode.pClassIN                   : ['gClass'],
    sqlCode.pClassIN_OUT               : ['gClass'],
    sqlCode.pClassOUT                  : ['gClass'],
#    sqlCode.pSFCListIN                 : ['gSFC'],
#    sqlCode.pSFCListIN_OUT             : ['gSFC'],
#    sqlCode.pSFCListOUT                : ['gSFC'],
    sqlCode.pSFC                       : ['gSFC'],
#    sqlCode.pSFCCallingIN_OUT          : ['gSFC'],
#    sqlCode.pSFCCallingOUT             : ['gSFC'],
    sqlCode.pSFCChild                  : ['gClass', 'gSFC'],
    sqlCode.pSFCChildIN                : ['gClass', 'gSFC'],
    sqlCode.pSFCChildIN_OUT            : ['gClass', 'gSFC'],
    sqlCode.pSFCChildOUT               : ['gClass', 'gSFC'],
    sqlCode.getSFCBlockParameters      : ['gClass'],
    sqlCode.pBLOCK_UNIQUE              : ['gClass'],
    sqlCode.pBLOCK_RECIPE              : ['gClass'],
    sqlCode.pBLOCK_RECIPE_EXISTS       : ['gClass'],
    sqlCode.pCHILD_NotMC               : ['gClass'],
    sqlCode.pBlock                     : ['gClass'],
    sqlCode.pBlockIN                   : ['gClass'],
    sqlCode.pBlockIN_OUT               : ['gClass'],
    sqlCode.pBlockOUT                  : ['gClass'],
#    sqlCode.pBLKCallingIN_OUT          : ['gClass'],
#    sqlCode.pBLKCallingOUT             : ['gClass'],
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
    sqlCode.createClassesForLevel      : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY [Class]'
                                         ),
    sqlCode.createClassNone            : ('SELECT 1'
                                         ),
#    sqlCode.createInstances            : ('SELECT '
#                                            '(SELECT COUNT (*) '
#                                            	 'FROM (tblInstance AS I '
#                                                       'INNER JOIN tblClass AS C '
#                                                       'ON I.ClassID = C.ID) t2 '
#                                            	 'WHERE I.[Class] = ? AND '
#                                                       '(I.Instance = ? OR '
#                                                       'I.Parent = ? OR '
#                                                       'I.GParent = ? OR '
#                                                       'I.GGParent = ? OR '
#                                                       'I.GGGParent = ?) AND '
#                                                       'substr(I.Level, 1, 1) != "V" AND '
#                                                       't2.ID < t1.ID) '
#                                        	 '+ '
#                                             '(SELECT COUNT (*) '
#                                            	 'FROM (tblInstance AS I '
#                                                       'INNER JOIN tblClass AS C '
#                                                       'ON I.ClassID = C.ID) t3 '
#                                            	 'WHERE I.[Class] = ? AND '
#                                                       '(I.Instance = ? OR '
#                                                       'I.Parent = ? OR '
#                                                       'I.GParent = ? OR '
#                                                       'I.GGParent = ? OR '
#                                                       'I.GGGParent = ?) AND '
#                                                       'substr(I.Level, 1, 1) != "V" AND '
#                                                       't3.Instance = T1.Instance AND '
#                                                       'T3.ID < T1.ID) '
#                                            'AS IDXITEM, '
#                                                  'printf("%d",I.ID) AS ID, '
#                                                  'I.[Level]AS Level, '
#                                                  'I.Instance AS Instance, '
#                                                  'I.[Class] AS Class, '
#                                                  'I.Description AS Description, '
#                                                  'I.Parent AS Parent, '
#                                                  'I.ParentID AS ParentID, '
#                                                  'I.ParentClass AS ParentClass, '
#                                                  'I.Recipe AS Recipe, '
#                                                  'I.GParent AS GParent, '
#                                                  'I.GGParent AS GGParent, '
#                                                  'I.GGGParent AS GGGParent, '
#                                                 'CASE '
#                                                     'WHEN I.NC=0 THEN """alwaysLow""" '
#                                                     'WHEN I.NC=1 THEN """alwaysHigh""" '
#                                                 'END NC, '
#                                                  'C.Description AS ClassDescription '
#                                            'FROM (tblInstance AS I INNER JOIN '
#                                                  'tblClass AS C ON I.ClassID = C.ID) t1 '
#                                            'WHERE I.[Class] = ? AND '
#                                                  '(I.Instance = ? OR '
#                                                  'I.Parent = ? OR '
#                                                  'I.GParent = ? OR '
#                                                  'I.GGParent = ? OR '
#                                                  'I.GGGParent = ?) AND '
#                                                  'substr(I.Level, 1, 1) != "V" '
#                                            'ORDER BY I.Instance ASC'
#                                         ),
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
    sqlCode.createInstancesGlobal      : ('SELECT printf("%d",I.ID) AS ID, '
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
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I INNER JOIN '
                                                  'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Class] = ? AND '
                                                 'substr(I.Level, 1, 1) != "V" '
                                          'ORDER BY I.Instance'
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
    sqlCode.defaultParameters          : ('SELECT * '
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
                                                 'printf("%d", S.childIndex) AS childIndex '
                                          'FROM tblClass_Child AS C '
                                          'INNER JOIN tblClass_ChildStateValues AS S ON '
                                                 'C.childKey = S.childKey '
                                          'WHERE C.Class = ? AND '
                                                 'S.Class = ? AND '
                                          'S.State = (SELECT [State] FROM tblClass_State WHERE Class = ? LIMIT 1) '
                                          'ORDER BY cast(childIndex as Int)'
                                         ), # gClass
    sqlCode.CHILD_ACQUIRED             : ('SELECT childAlias, '
                                                 'childClass, '
                                                 'printf("%d", childIndex) AS childIndex, '
                                                 'childAlias as childAliasBlock, '
                                                 'childAcquireStatement '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND '
                                                 '[State] = ? AND '
                                                 '(childAcquire = "TRUE" OR '
                                                 'childAcquire = "OWNER") '
                                          'ORDER BY childAlias'
                                         ), # gClass, gState
    sqlCode.CHILD_ACQUIRE_REQ          : ('SELECT childAlias, '
                                                 'childClass, '
                                                 'printf("%d", childIndex) AS childIndex, '
                                                 'childAlias as childAliasBlock, '
                                                 'childAcquireStatement '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND '
                                                 '[State] = ? AND '
                                                 'childAcquire = "TRUE" '
                                          'ORDER BY childAlias'
                                         ), # gClass, gState
    sqlCode.CHILD_INDEX_MAX            : ('SELECT printf("%d", MAX(childIndex)) AS childIndexMax '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE Class = ?'
                                         ), # gClass
    sqlCode.CHILD_INIT_COMMAND_TRUE    : ('SELECT childAlias, '
                                                 'childClass, '
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
                                          'ORDER BY childAlias'
                                         ), # gClass, gState
    sqlCode.CHILD_INIT_COMMAND_FALSE   : ('SELECT childAlias, '
                                                 'childClass, '
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
    sqlCode.CHILD_INSTANCE             : ('SELECT C.childAlias, '
                                                 'I.Class AS childClass, '
                                                 'printf("%d", C.childIndex) AS childIndex, '
                                                 'printf("%d", I.IDX) AS childIDX, '
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
    sqlCode.CHILD_INSTANCE_BIND        : ('SELECT C.childAlias, '
                                                 'I.Class AS childClass, '
                                                 'C.conditionStatement, '
                                                 'printf("%d", C.childIndex) AS childIndex, '
                                                 'printf("%d", C.childBind) AS childBind, '
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
#    sqlCode.CRIL                       : ('SELECT DISTINCT Instance, Description '
#                                          'FROM tblInterlockCRIL '
#                                          'ORDER BY Instance'
#                                         ),
    sqlCode.CRIL                       : ('SELECT DISTINCT Instance, '
                                                 'Description, '
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
    sqlCode.CRIL_NUM                   : ('SELECT COUNT(DISTINCT Instance) - 1 AS MAXITEM '
                                          'FROM tblInterlockCRIL '
                                          'ORDER BY Instance'
                                         ),
    sqlCode.NCRIL                      : ('SELECT DISTINCT Instance, '
                                                 'Description, '
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
    sqlCode.INSTANCE_SFC               : ('SELECT printf("%d",I.ID) AS ID, '
                                                 'printf("%d",I.IDX) AS IDX, '
                                                 'I.[Level], '
                                                 'I.Instance, '
                                                 'I.[Class], '
                                                 'I.Description, '
                                                 'I.Parent, '
                                                 'S.SFC, '
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
    sqlCode.LINK                       : ('SELECT userInstance '
                                                 'userClass, '
                                                 'Link, '
                                                 'linkInstance, '
                                                 'linkClass, '
                                                 'printf("%d",linkIDX) AS linkIDX, '
                                                 'linkAttribute, '
                                                 'actualAttribute, '
                                                 'linkDataType '
                                          'FROM tblInstance_Link '
                                          'WHERE [userInstance] = ?'
                                         ), # gInstance
    sqlCode.LINK_BLK                   : ('SELECT userInstance '
                                                 'userClass, '
                                                 'Link, '
                                                 'P.blockParameter, '
                                                 'linkInstance, '
                                                 'linkClass, '
                                                 'printf("%d",linkIDX) AS linkIDX, '
                                                 'linkAttribute, '
                                                 'actualAttribute, '
                                                 'linkDataType '
                                          'FROM tblInstance_Link AS L INNER JOIN '
                                                'pGlobal AS P ON L.userClass = P.parameterClass '
                                                'AND L.Link = P.childParameterAlias AND '
                                                'L.linkAttribute = P.childParameterAttribute '
                                          'WHERE [userInstance] = ? AND '
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
    sqlCode.PARAMETER_ACQUIRE          : ('SELECT parameterName, '
                                                 'childClass, '
                                                 'printf("%d", parameterIndex) AS parameterIndex, '
                                                 'childAlias as childAliasBlock '
                                          'FROM tblClass_Parameter '
                                          'WHERE parameterClass = ? AND parameterState = ? '
                                          'ORDER BY parameterName'
                                         ), # gClass, gState
    sqlCode.PARAMETER_INDEX_MAX        : ('SELECT printf("%d", MAX(parameterIndex)) AS parameterIndexMax '
                                          'FROM tblClass_Parameter '
                                          'WHERE parameterClass = ?'
                                         ), # gClass
    sqlCode.PARENT                     : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE [Level] = "EM" OR '
                                                 '[Level] = "UN" OR '
                                                 '[Level] = "PC" '
                                          'ORDER BY [Level], [Class]'
                                         ),
#    sqlCode.PARM_CHILD_VAR_INPUT       : ('SELECT P.Parameter, '
#                                                 'P.ParameterClass, '
#                                                 'P.ParameterDataType, '
#                                                 'P.ParameterType, '
#                                                 'P.childParameterAlias, '
#                                                 'P.ParameterDescription, '
#                                                 'C.childAlias, '
#                                                 'C.childAliasBlock, '
#                                                 'C.childAliasClass, '
#                                                 'C.childAliasDescription, '
#                                                 'S.State, '
#                                                 'S.StateDescription '
#                                          'FROM tblClass_Parameter AS P '
#                                                 'INNER JOIN tblClass_Child AS C ON '
#                                                 'P.childParameterAlias = c.childAlias '
#                                          'INNER JOIN tblClass_State AS S ON '
#                                                 'P.State = S.State '
#                                          'WHERE C.Class = ? AND ParameterType = "VAR_INPUT" '
#                                          'ORDER BY P.Parameter'
#                                         ), # gClass
#    sqlCode.PARM_CLASS_VAR_INPUT       : ('SELECT P.Parameter, '
#                                                 'P.ParameterClass, '
#                                                 'P.ParameterDataType, '
##                                                 'P.ParameterType, '
#                                                 'P.childParameterAlias, '
#                                                 'P.ParameterDescription '
#                                          'FROM tblClass_Parameter AS P '
#                                          'WHERE P.ParameterClass = ? AND '
#                                                 'length(P.childParameterAlias) = 0 '
#                                                 'AND ParameterType = "VAR_INPUT" '
#                                          'ORDER BY P.Parameter '
#                                         ), # gClass
#    sqlCode.PARM_CLASS_VAR_IN_OUT      : ('SELECT P.Parameter, '
#                                                 'P.ParameterClass, '
#                                                 'P.ParameterDataType, '
#                                                 'P.ParameterType, '
#                                                 'P.childParameterAlias, '
#                                                 'P.ParameterDescription '
#                                          'FROM tblClass_Parameter AS P '
#                                          'WHERE P.ParameterClass = ? AND '
#                                                 'length(P.childParameterAlias) = 0 '
#                                                 'AND ParameterType = "VAR_IN_OUT" '
#                                          'ORDER BY P.Parameter '
#                                         ), # gClass
#    sqlCode.PARM_CLASS_VAR_OUTPUT      : ('SELECT P.Parameter, '
#                                                 'P.ParameterClass, '
#                                                 'P.ParameterDataType, '
#                                                 'P.ParameterType, '
#                                                 'P.childParameterAlias, '
#                                                 'P.ParameterDescription '
#                                          'FROM tblClass_Parameter AS P '
#                                          'WHERE P.ParameterClass = ? AND '
#                                                 'length(P.childParameterAlias) = 0 '
#                                                 'AND ParameterType = "VAR_OUTPUT" '
#                                          'ORDER BY P.Parameter '
#                                         ), # gClass
#    sqlCode.PARM_INSTANCE_VAR_INPUT    : ('SELECT printf("%d",T.ID) AS ID, '
#                                                 'T.Instance, '
#                                                 'T.[Class], '
#                                                 'T.Description, '
#                                                 'P.Parameter, '
#                                                 'P.ParameterDataType, '
##                                                 'P.ParameterType, '
#                                                 'P.ParameterDescription, '
#                                                 'P.UoM, '
#                                                 'P.ParameterMin, '
#                                                 'P.ParameterMax, '
#                                                 'P.ParameterValue '
#                                          'FROM tblInstance AS T INNER JOIN '
#                                                 'tblClass_Parameter AS P ON T.ClassID = P.ClassID '
#                                          'WHERE T.Instance = ? AND P.ParameterType = "VAR_INPUT" '
#                                          'ORDER BY T.Parent, T.Instance, P.Parameter'
#                                         ), # gInstance
#    sqlCode.PARM_INSTANCE_VAR_IN_OUT   : ('SELECT printf("%d",T.ID) AS ID, '
#                                                 'T.Instance, '
#                                                 'T.[Class], '
#                                                 'T.Description, '
#                                                 'P.Parameter, '
#                                                 'P.ParameterDataType, '
#                                                 'P.ParameterType, '
#                                                 'P.ParameterDescription, '
#                                                 'P.UoM, '
#                                                 'P.ParameterMin, '
#                                                 'P.ParameterMax, '
#                                                 'P.ParameterValue '
#                                          'FROM tblInstance AS T INNER JOIN '
#                                                 'tblClass_Parameter AS P ON T.ClassID = P.ClassID '
#                                          'WHERE T.Instance = ? AND P.ParameterType = "VAR_IN_OUT" '
#                                          'ORDER BY T.Parent, T.Instance, P.Parameter'
#                                         ), # gInstance
#    sqlCode.PARM_INSTANCE_VAR_OUTPUT   : ('SELECT printf("%d",T.ID) AS ID, '
#                                                 'T.Instance, '
#                                                 'T.[Class], '
#                                                 'T.Description, '
#                                                 'P.Parameter, '
#                                                 'P.ParameterDataType, '
#                                                 'P.ParameterType, '
#                                                 'P.ParameterDescription, '
#                                                 'P.UoM, '
#                                                 'P.ParameterMin, '
#                                                 'P.ParameterMax, '
#                                                 'P.ParameterValue '
#                                          'FROM tblInstance AS T INNER JOIN '
#                                                 'tblClass_Parameter AS P ON T.ClassID = P.ClassID '
#                                          'WHERE T.Instance = ? AND P.ParameterType = "VAR_OUTPUT" '
#                                          'ORDER BY T.Parent, T.Instance, P.Parameter'
#                                         ), # gInstance
#    sqlCode.PARM_INSTANCE_VAR          : ('SELECT printf("%d",T.ID) AS ID, '
#                                                 'T.Instance, '
#                                                 'T.[Class], '
#                                                 'T.Description, '
#                                                 'P.Parameter, '
#                                                 'P.ParameterDataType, '
#                                                 'P.ParameterType, '
#                                                 'P.ParameterDescription, '
#                                                 'P.UoM, '
#                                                 'P.ParameterMin, '
#                                                 'P.ParameterMax, '
#                                                 'P.ParameterValue '
#                                          'FROM tblInstance AS T INNER JOIN '
#                                                 'tblClass_Parameter AS P ON T.ClassID = P.ClassID '
#                                          'WHERE T.Instance = ? AND P.ParameterType = "VAR" '
#                                          'ORDER BY T.Parent, T.Instance, P.Parameter'
#                                         ), # gInstance
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
                                                   'S.Selection, V.selectionValue'
                                         ), # gClass, gSelectParameter , gSelectSelection
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
                                                 'IO.dataType, '
                                                 'IO.eInstruction, '
                                                 'IO.eVerify, '
                                                 'IO.eResult, '
                                                 'IO.dInstruction, '
                                                 'IO.dVerify, '
                                                 'IO.dResult '
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
                                                     'WHEN IO.dataType="Bool" THEN "%M@@COUNTER|200@@.0" '
                                                     'WHEN IO.dataType="Int" THEN "%MW@@COUNTER@@" '
                                                     'WHEN IO.dataType="Real" THEN "%MD@@COUNTER@@" '
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
                                                 'IO.dataType, '
                                                 'IO.eInstruction, '
                                                 'IO.eVerify, '
                                                 'IO.eResult, '
                                                 'IO.dInstruction, '
                                                 'IO.dVerify, '
                                                 'IO.dResult '
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

    sqlCode.checkIfChildParameter      : ('SELECT childAlias, '
                                                 'childAliasClass '
                                          'FROM tblClass_Child '
                                          'WHERE Class = ? '
                                               'AND childAlias || "_" '
                                               'LIKE substr(?, 1, length(childAlias) + 1) || "%"'
                                         ), # gClass, sParameter
    sqlCode.checkIfLinkParameter       : ('SELECT childAlias, '
                                                 'childAliasClass '
                                          'FROM tblClass_Child '
                                          'WHERE Class != ? '
                                               'AND childAlias || "_" '
                                               'LIKE substr(?, 1, length(childAlias) + 1) || "%"'
                                         ), # gClass, sParameter
    sqlCode.getChildIndex              : ('SELECT printf("%d", childIndex) AS childIndex '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE SFC = ? AND childAlias = ?'
                                         ), # gSFC, gChild
    sqlCode.insertGlobalParameters     : ('INSERT INTO pGlobal '
                                          'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                                         ),
    sqlCode.addParametersClass         : ('SELECT * '
                                          'FROM tblClass_Parameter '
                                          'ORDER BY parameterName'
                                         ),
    sqlCode.addParametersChild         : ('SELECT childAlias, '
                                                 'childAliasClass '
                                          'FROM tblClass_Child '
                                          'WHERE [Class] = ? '
                                          'ORDER BY childAlias'
                                         ),
    sqlCode.addParametersSelect       : ('SELECT [Level] '
                                                 '[Class], '
                                                 'Parameter, '
                                                 'Selection, '
                                                 'Description '
                                          'FROM tblClass_Selection '
                                          'ORDER BY [Level], [Class], Parameter, '
                                                   'Selection'
                                         ), # gClass
    sqlCode.addParametersSFC           : ('SELECT * '
                                          'FROM tblClass_State '
                                          'WHERE [Class] = ? '
                                                 'AND upper(SFC) != ? '
                                          'ORDER BY State'
                                         ),
    sqlCode.getUserParametersChild     : ('SELECT * FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 0 '
                                          'ORDER BY childParameter'
                                         ), # gClass
    sqlCode.tblCreateGlobalParameter   : ('CREATE TABLE IF NOT EXISTS '
                                          'pGlobal ('
                                                 'Level text NOT NULL, '
                                                 'parameterClass text NOT NULL, '
                                                 'parameterSource text, '
                                                 'parameterType text NOT NULL, '
                                                 'parameterOrder int NOT NULL, '
                                                 'childParameter text NOT NULL, '
                                                 'blockParameter text NOT NULL, '
                                                 'childParameterAlias text, '
                                                 'childParameterClass text, '
                                                 'childParameterAttribute text, '
                                                 'parameterDataType text NOT NULL, '
                                                 'parameterValue text, '
                                                 'parameterDescription text, '
                                                 'isSFC boolean, '
                                                 'isChild boolean, '
                                                 'isLink boolean, '
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
                                                 'isEventDataTime boolean)'
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
    sqlCode.pEventPrompt               : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventPrompt = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventLogMsg               : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogMsg = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventLogReal              : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogReal = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventLogTime              : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogTime = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
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
    sqlCode.pEventConfirmExists        : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventConfirm = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventPromptExists         : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventPrompt = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogMsgExists         : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogMsg = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogRealExists        : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogReal = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogTimeExists        : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogTime = 1 '
                                          'LIMIT 1'
                                         ), # gClass
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
    sqlCode.pEventConfirmList          : ('SELECT *, '
                                                 'Replace(childParameter,"_confirm",".confirm") AS dbEventParameter '
                                          'FROM pGlobal '
                                          'WHERE isEventConfirm = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventPromptList           : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE isEventPrompt = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventLogMsgList           : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE isEventLogMsg = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventLogRealList          : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE isEventLogReal = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventLogTimeList          : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE isEventLogTime = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventDataRealList         : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE isEventDataReal = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventDataTimeList         : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE isEventDataTime = 1 '
                                          'ORDER BY cast(idxEvent as Int)'
                                         ), # gClass
    sqlCode.pEventPromptNum            : ('SELECT printf("%d", MAX(idxEvent)) AS idxEventMax '
                                          'FROM pGlobal '
                                          'WHERE isEventPrompt = 1'
                                         ),
    sqlCode.pEventLogMsgNum            : ('SELECT printf("%d", MAX(idxEvent)) AS idxEventMax '
                                          'FROM pGlobal '
                                          'WHERE isEventLogMsg = 1'
                                         ),
    sqlCode.pEventLogRealNum           : ('SELECT printf("%d", MAX(idxEvent)) AS idxEventMax '
                                          'FROM pGlobal '
                                          'WHERE isEventLogReal = 1'
                                         ),
    sqlCode.pEventLogTimeNum           : ('SELECT printf("%d", MAX(idxEvent)) AS idxEventMax '
                                          'FROM pGlobal '
                                          'WHERE isEventLogTime = 1'
                                         ),
    sqlCode.pEventDataRealNum          : ('SELECT printf("%d", MAX(idxEvent)) AS idxEventMax '
                                          'FROM pGlobal '
                                          'WHERE isEventDataReal = 1'
                                         ),
    sqlCode.pEventDataTimeNum          : ('SELECT printf("%d", MAX(idxEvent)) AS idxEventMax '
                                          'FROM pGlobal '
                                          'WHERE isEventDataTime = 1'
                                         ),
    sqlCode.pSFCChild                  : ('SELECT S.Class, '
                                                 'S.State, '
                                                 'S.childAlias, '
                                                 'S.childClass, '
                                                 'printf("%d", S.childIndex) AS childIndex, '
                                                 'P.parameterSource, '
                                                 'P.parameterType, '
                                                 'P.parameterDataType, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.childParameterAlias, '
                                                 'P.childParameterAttribute, '
                                                 'P.parameterDescription '
                                          'FROM tblClass_ChildStateValues AS S  '
                                                 'LEFT JOIN pGlobal AS P ON  '
                                                        'S.childAlias = P.childParameterAlias AND '
                                                        'S.SFC = P.parameterSource '
                                          'WHERE S.Class = ? AND '
                                                 'P.parameterSource = ? AND '
                                                 '(S.childAcquire = "TRUE" OR '
                                                 'S.childAcquire = "OWNER") AND '
                                                 'P.isSFC = 1 AND '
                                                 'P.isMC = 1 AND '
                                                 'P.isChild = 1 '
                                          'ORDER BY S.State, '
                                                 'P.parameterOrder, '
                                                 'P.parameterSource, '
                                                 'P.childParameter'
                                         ), # gClass, gSFC
    sqlCode.pSFCChildIN                : ('SELECT DISTINCT S.Class, '
                                                 'S.State, '
                                                 'S.childAlias, '
                                                 'S.childClass, '
                                                 'printf("%d", S.childIndex) AS childIndex, '
                                                 'P.parameterSource, '
                                                 'P.parameterType, '
                                                 'P.parameterDataType, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.childParameterAlias, '
                                                 'P.childParameterAttribute, '
                                                 'P.parameterDescription '
                                          'FROM tblClass_ChildStateValues AS S  '
                                                 'LEFT JOIN pGlobal AS P ON  '
                                                        'S.childAlias = P.childParameterAlias AND '
                                                        'S.SFC = P.parameterSource '
                                          'WHERE S.Class = ? AND '
                                                 'P.parameterSource = ? AND '
                                                 'P.parameterType = "VAR_INPUT" AND '
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
    sqlCode.pSFCChildIN_OUT            : ('SELECT DISTINCT S.Class, '
                                                 'S.State, '
                                                 'S.childAlias, '
                                                 'S.childClass, '
                                                 'printf("%d", S.childIndex) AS childIndex, '
                                                 'P.parameterSource, '
                                                 'P.parameterType, '
                                                 'P.parameterDataType, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.childParameterAlias, '
                                                 'P.childParameterAttribute, '
                                                 'P.parameterDescription '
                                          'FROM tblClass_ChildStateValues AS S  '
                                                 'LEFT JOIN pGlobal AS P ON  '
                                                        'S.childAlias = P.childParameterAlias AND '
                                                        'S.SFC = P.parameterSource '
                                          'WHERE S.Class = ? AND '
                                                 'P.parameterSource = ? AND '
                                                 'P.parameterType = "VAR_IN_OUT" AND '
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
    sqlCode.pSFCChildOUT               : ('SELECT DISTINCT S.Class, '
                                                 'S.State, '
                                                 'S.childAlias, '
                                                 'S.childClass, '
                                                 'printf("%d", S.childIndex) AS childIndex, '
                                                 'P.parameterSource, '
                                                 'P.parameterType, '
                                                 'P.parameterDataType, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.childParameterAlias, '
                                                 'P.childParameterAttribute, '
                                                 'P.parameterDescription '
                                          'FROM tblClass_ChildStateValues AS S  '
                                                 'LEFT JOIN pGlobal AS P ON  '
                                                        'S.childAlias = P.childParameterAlias AND '
                                                        'S.SFC = P.parameterSource '
                                          'WHERE S.Class = ? AND '
                                                 'P.parameterSource = ? AND '
                                                 'P.parameterType = "VAR_OUTPUT" AND '
                                                 'S.childAcquire = "TRUE" AND '
                                                 'P.isSFC = 1 AND '
                                                 'P.isMC = 1 AND '
                                                 'P.isChild = 1 '
                                          'GROUP BY P.childParameter '
                                          'ORDER BY S.State, '
                                                 'P.parameterOrder, '
                                                 'P.parameterSource, '
                                                 'P.childParameter'
                                         ), # gClass
#    sqlCode.pChildIN                   : ('SELECT * FROM pGlobal '
#                                          'WHERE parameterSource IN '
#                                                    '(SELECT childAliasClass '
#                                                     'FROM tblClass_Child '
#                                                     'WHERE Class = ?) AND '
#                                                 '(parameterType = "VAR_INPUT" OR '
#                                                 'parameterType = "VAR_IN_OUT") '
#                                          'ORDER BY parameterOrder, '
#                                                 'parameterSource, '
#                                                 'childParameter'
#                                         ), # gClass
#    sqlCode.pChildOUT                  : ('SELECT * FROM pGlobal '
#                                          'WHERE parameterSource IN '
#                                                    '(SELECT childAliasClass '
#                                                     'FROM tblClass_Child '
#                                                     'WHERE Class = ?) AND '
#                                                 '(parameterType = "VAR_OUTPUT" OR '
#                                                 'parameterType = "VAR_IN_OUT") '
#                                          'ORDER BY parameterOrder, '
#                                                 'parameterSource, '
#                                                 'childParameter'
#                                         ), # gClass
#    sqlCode.pChildIN                   : ('SELECT S.Class, '
#                                                 'S.State, '
#                                                 'S.childAlias, '
#                                                 'S.childClass, '
#                                                 'printf("%d", S.childIndex) AS childIndex, '
#                                                 'P.parameterSource, '
#                                                 'P.parameterType, '
#                                                 'P.parameterDataType, '
#                                                 'P.childParameter, '
#                                                 'P.blockParameter, '
#                                                 'P.childParameterAlias, '
#                                                 'P.childParameterAttribute, '
#                                                 'P.parameterDescription '
#                                          'FROM tblClass_ChildStateValues AS S  '
#                                                 'LEFT JOIN pGlobal AS P ON  '
#                                                        'S.Class = P.parameterClass AND '
#                                                        'S.childClass = P.parameterSource '
#                                          'WHERE S.Class = ? AND '
#                                                 'P.parameterType = "VAR_INPUT" AND '
#                                                 'S.childAcquire = "TRUE" AND '
#                                                 'P.isSFC = 0 AND '
#                                                 'P.isChild = 0 '
#                                          'ORDER BY S.State, '
#                                                 'P.parameterOrder, '
#                                                 'P.parameterSource, '
#                                                 'P.childParameter'
#                                         ), # gClass
    sqlCode.pChildIN                   : ('SELECT DISTINCT S.Class, '
                                                 'S.State, '
                                                 'S.childAlias, '
                                                 'S.childClass, '
                                                 'printf("%d", S.childIndex) AS childIndex, '
                                                 'P.parameterType, '
                                                 'P.parameterDataType, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.childParameterAlias, '
                                                 'P.childParameterAttribute, '
                                                 'P.parameterDescription '
                                          'FROM pGlobal AS P '
                                          'INNER JOIN tblClass_ChildStateValues AS S ON '
                                                 'S.Class = P.parameterClass AND '
                                                 'S.childClass = P.parameterSource '
                                          'WHERE P.parameterClass = ? AND '
                                                 'P.parameterType = "VAR_INPUT" AND '
                                                 'P.isSFC = 0 AND '
                                                 'P.isChild = 0 '
                                          'GROUP BY P.childParameter '
                                          'ORDER BY P.parameterOrder, '
                                                 'P.parameterSource, '
                                                 'P.childParameter'
                                         ), # gClass
    sqlCode.pChildIN_OUT               : ('SELECT DISTINCT S.Class, '
                                                 'S.State, '
                                                 'S.childAlias, '
                                                 'S.childClass, '
                                                 'printf("%d", S.childIndex) AS childIndex, '
                                                 'P.parameterType, '
                                                 'P.parameterDataType, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.childParameterAlias, '
                                                 'P.childParameterAttribute, '
                                                 'P.parameterDescription '
                                          'FROM pGlobal AS P '
                                          'INNER JOIN tblClass_ChildStateValues AS S ON '
                                                 'S.Class = P.parameterClass AND '
                                                 'S.childClass = P.parameterSource '
                                          'WHERE P.parameterClass = ? AND '
                                                 'P.parameterType = "VAR_IN_OUT" AND '
                                                 'P.isSFC = 0 AND '
                                                 'P.isChild = 0 '
                                          'GROUP BY P.childParameter '
                                          'ORDER BY P.parameterOrder, '
                                                 'P.parameterSource, '
                                                 'P.childParameter'
                                         ), # gClass
    sqlCode.pChildOUT                  : ('SELECT DISTINCT S.Class, '
                                                 'S.State, '
                                                 'S.childAlias, '
                                                 'S.childClass, '
                                                 'printf("%d", S.childIndex) AS childIndex, '
                                                 'P.parameterType, '
                                                 'P.parameterDataType, '
                                                 'P.childParameter, '
                                                 'P.blockParameter, '
                                                 'P.childParameterAlias, '
                                                 'P.childParameterAttribute, '
                                                 'P.parameterDescription '
                                          'FROM pGlobal AS P '
                                          'INNER JOIN tblClass_ChildStateValues AS S ON '
                                                 'S.Class = P.parameterClass AND '
                                                 'S.childClass = P.parameterSource '
                                          'WHERE P.parameterClass = ? AND '
                                                 'P.parameterType = "VAR_OUTPUT" AND '
                                                 'P.isSFC = 0 AND '
                                                 'P.isChild = 0 '
                                          'GROUP BY P.childParameter '
                                          'ORDER BY P.parameterOrder, '
                                                 'P.parameterSource, '
                                                 'P.childParameter'
                                         ), # gClass
    sqlCode.pClass                     : ('SELECT DISTINCT childParameter, '
                                                 'childParameterAttribute, '
                                                 'parameterDataType, '
                                                 'parameterDescription '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                'isSFC = 0 AND isMC = 0 '
                                          'ORDER BY parameterOrder, '
                                                   'childParameter'
                                         ), # gClass
    sqlCode.pClassIN                   : ('SELECT DISTINCT childParameter, '
                                                 'childParameterAttribute, '
                                                 'parameterDataType, '
                                                 'parameterDescription '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                'parameterType = "VAR_INPUT" AND '
                                                'isSFC = 0 AND isMC = 0 '
                                          'ORDER BY childParameter'
                                         ), # gClass
    sqlCode.pClassIN_OUT               : ('SELECT DISTINCT childParameter, '
                                                 'childParameterAttribute, '
                                                 'parameterDataType, '
                                                 'parameterDescription '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                'parameterType = "VAR_IN_OUT" AND '
                                                'isSFC = 0 AND isMC = 0 '
                                          'ORDER BY childParameter'
                                         ), # gClass
    sqlCode.pClassOUT                  : ('SELECT DISTINCT childParameter, '
                                                 'childParameterAttribute, '
                                                 'parameterDataType, '
                                                 'parameterDescription '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                'parameterType = "VAR_OUTPUT" AND '
                                                'isSFC = 0 AND isMC = 0 '
                                          'ORDER BY childParameter'
                                         ), # gClass
#    sqlCode.pChildIN_OUT               : ('SELECT DISTINCT S.Class, '
#                                                 'S.State, '
#    FOR STATE!!!                                 'S.childAlias, '
#                                                 'S.childClass, '
#                                                 'printf("%d", S.childIndex) AS childIndex, '
#                                                 'P.parameterSource, '
#                                                 'P.parameterType, '
#                                                 'P.parameterDataType, '
#                                                 'P.childParameter, '
#                                                 'P.blockParameter, '
#                                                 'P.childParameterAlias, '
#                                                 'P.childParameterAttribute, '
#                                                 'P.parameterDescription '
#                                          'FROM tblClass_ChildStateValues AS S  '
#                                                 'LEFT JOIN pGlobal AS P ON  '
#                                                        'S.Class = P.parameterClass AND '
#                                                        'S.childClass = P.parameterSource '
#                                          'WHERE S.Class = ? AND '
#                                                 'P.parameterType = "VAR_IN_OUT" AND '
#                                                 'S.childAcquire = "TRUE" AND '
#                                                 'P.isSFC = 0 AND '
#                                                 'P.isChild = 0 '
#                                          'ORDER BY S.State, '
#                                                 'P.parameterOrder, '
#                                                 'P.parameterSource, '
#                                                 'P.childParameter'
#                                         ), # gClass
#    sqlCode.pChildOUT                  : ('SELECT DISTINCT S.Class, '
#                                                 'S.State, '
#    FOR STATE!!!                                 'S.childAlias, '
#                                                 'S.childClass, '
#                                                 'printf("%d", S.childIndex) AS childIndex, '
#                                                 'P.parameterSource, '
#                                                 'P.parameterType, '
#                                                 'P.parameterDataType, '
#                                                 'P.childParameter, '
#                                                 'P.blockParameter, '
#                                                 'P.childParameterAlias, '
#                                                 'P.childParameterAttribute, '
#                                                 'P.parameterDescription '
#                                          'FROM tblClass_ChildStateValues AS S  '
#                                                 'LEFT JOIN pGlobal AS P ON  '
#                                                        'S.Class = P.parameterClass AND '
#                                                        'S.childClass = P.parameterSource '
#                                          'WHERE S.Class = ? AND '
#                                                 'P.parameterType = "VAR_OUTPUT" AND '
#                                                 'S.childAcquire = "TRUE" AND '
#                                                 'P.isSFC = 0 AND '
#                                                 'P.isChild = 0 '
#                                          'ORDER BY S.State, '
#                                                 'P.parameterOrder, '
#                                                 'P.parameterSource, '
#                                                 'P.childParameter'
#                                         ), # gClass
#    sqlCode.pSFCListIN                 : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                 'parameterType = "VAR_INPUT" AND '
#                                                 'isSFC = 1'
#                                         ), # gSFC
#    sqlCode.pSFCListIN_OUT             : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                 'parameterType = "VAR_IN_OUT" AND '
#                                                 'isSFC = 1'
#                                         ), # gSFC
#    sqlCode.pSFCListOUT                : ('SELECT * '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                 'parameterType = "VAR_OUTPUT" AND '
#                                                 'isSFC = 1'
#                                         ), # gSFC
#    sqlCode.pSFCChildIN                : ('SELECT childParameter, '
#                                                'blockParameter, '
#                                                'parameterType, '
#                                                'parameterDataType, '
#                                                'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                'parameterType = "VAR_INPUT" AND '
#                                                'isChild = 1'
#                                         ), # gSFC
#    sqlCode.pSFCChildIN_OUT            : ('SELECT childParameter, '
#                                                'blockParameter, '
#                                                'parameterType, '
#                                                'parameterDataType, '
#                                                'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                'parameterType = "VAR_IN_OUT" AND '
#                                                'isChild = 1'
#                                         ), # gSFC
#    sqlCode.pSFCChildOUT               : ('SELECT childParameter, '
#                                                'blockParameter, '
#                                                'parameterType, '
#                                                'parameterDataType, '
#                                                'parameterDescription '
#                                          'FROM pGlobal '
#                                          'WHERE parameterSource = ? AND '
#                                                'parameterType = "VAR_OUTPUT" AND '
#                                                'isChild = 1'
#                                         ), # gSFC
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
    sqlCode.pBLOCK_UNIQUE              : ('SELECT DISTINCT Level, '
                                                 'parameterClass, '
                                                 'blockParameter, '
                                                 'upper(parameterDataType) AS PARAMETERDATATYPE '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'isChild = 0 AND '
                                                 'isLink = 0 AND '
                                                 'isRecipe = 0 '
                                          'ORDER BY childParameter'
                                         ), # gClass
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
    sqlCode.pBLOCK_RECIPE_EXISTS       : ('SELECT DISTINCT Level, '
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
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pCHILD_NotMC               : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'parameterType LIKE "VAR_%" AND '
                                                 'isSFC = 1 AND '
                                                 'isChild = 1 AND '
                                                 'isMC = 0 AND '
                                                 'isLink = 0 '
                                          'ORDER BY parameterOrder, '
                                                 'childParameter'
                                         ), # gClass
    sqlCode.pSFC                       : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterSource = ? AND '
                                                'isChild = 0 AND '
                                                'isSFC = 1 AND '
                                                'parameterType != "VAR" '
                                          'ORDER BY parameterOrder, '
                                                 'parameterSource, '
                                                 'childParameter'
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
