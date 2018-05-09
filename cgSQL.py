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
    createIndexFileCount               = -150
    createIndexFile                    = -151
    createClassAll                     = -1
    createClassNone                    = -2
    createClassOne                     = -3
    createParameterSFC                 = -4
    createProgramFiles                 = -5
    createProgramFilesCount            = -6
    defaultParameters                  = -7
    documentInfo                       = -199
    checkIfChildParameter              = -8
    insertGlobalParameters             = -9
    addUserParametersChild             = -1110
    addUserParametersSFC               = -10
    getUserParametersChild             = -1111
    processLevel                       = -11
    processLevelCount                  = -12
    tblCreateGlobalParameter           = -878
    versionHistory                     = -13
    VERHIST                            = -513
    ANALOG                             = -214
    ANALOG_EMBED                       = -215
    CALL_LEVEL                         = -414
    CALL_LIST                          = -415
    CHILD                              = -14
    CHILD_ACQUIRE                      = -15
    CHILD_INDEX_MAX                    = -714
    CHILD_INIT_COMMAND                 = -16
    CHILD_INSTANCE                     = -171
    CRIL                               = -120
    CRIL_EXISTS                        = -121
    CRIL_INSTANCE                      = -122
    NCRIL                              = -123
    NCRIL_EXISTS                       = -124
    NCRIL_INSTANCE                     = -125
    HYGIENE                            = -19
    INSTANCE_ALL                       = -21
    INSTANCE_BLK                       = -22
    LINK                               = -623
    OWNER                              = -23
    PARENT                             = -24
    PARM_CHILD_VAR_INPUT               = -25
    PARM_CHILD_VAR_OUTPUT              = -26
    PARM_CHILD_VAR_IN_OUT              = -27
    PARM_INSTANCE_VAR_INPUT            = -61
    PARM_INSTANCE_VAR_OUTPUT           = -62
    PARM_INSTANCE_VAR_IN_OUT           = -63
    PARM_INSTANCE_VAR                  = -64
    PARM_CLASS_VAR_INPUT               = -97
    PARM_CLASS_VAR_IN_OUT              = -98
    PARM_CLASS_VAR_OUTPUT              = -99
    REQUIREMENT                        = -69
    SCOPE                              = -70
    SELECT                             = -71
    SELVALUE                           = -72
    SFC                                = -73
    STATE                              = -74
    STATE_TIMER                        = -75
    TAGS                               = -81
    TIMER                              = -82
    TRANSITION                         = -83
    pChildIN                           = -350
    pChildIN_OUT                       = -351
    pChildOUT                          = -352
    pEventConfirm                      = -353
    pEventConfirmExists                = -253
    pEventPrompt                       = -355
    pEventPromptExists                 = -255
    pEventLogMsg                       = -354
    pEventLogMsgExists                 = -254
    pEventLogReal                      = -380
    pEventLogRealExists                = -280
    pEventLogTime                      = -381
    pEventLogTimeExists                = -281
    pEventDataReal                     = -382
    pEventDataTime                     = -383
#    pSFCListIN                         = -356
#    pSFCListIN_OUT                     = -357
#    pSFCListOUT                        = -358
    pSFC                               = -359
#    pSFCCallingIN_OUT                  = -360
#    pSFCCallingOUT                     = -361
    pSFCChild                          = -965
    pSFCChildIN                        = -365
#    pSFCChildIN_OUT                    = -366
    pSFCChildOUT                       = -367
    pBLK                               = -368
#    pBLKCallingIN_OUT                  = -369
#    pBLKCallingOUT                     = -370

prm = {
    sqlCode.ANALOG                     : ['gInstance'],
    sqlCode.ANALOG_EMBED               : ['gInstance'],
    sqlCode.CALL_LIST                  : ['gLevel'],
    sqlCode.CHILD                      : ['gClass'],
    sqlCode.CHILD_ACQUIRE              : ['gClass', 'gState'],
    sqlCode.CHILD_INDEX_MAX            : ['gClass'],
    sqlCode.CHILD_INIT_COMMAND         : ['gClass', 'gState'],
    sqlCode.CHILD_INSTANCE             : ['gInstance'],
    sqlCode.CRIL                       : [],
    sqlCode.CRIL_EXISTS                : ['gInstance'],
    sqlCode.CRIL_INSTANCE              : ['gInstance'],
    sqlCode.NCRIL                      : [],
    sqlCode.NCRIL_EXISTS               : ['gInstance'],
    sqlCode.NCRIL_INSTANCE             : ['gInstance'],
    sqlCode.HYGIENE                    : ['gClass'],
    sqlCode.INSTANCE_ALL               : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.INSTANCE_BLK               : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.LINK                       : ['gInstance'],
    sqlCode.OWNER                      : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.PARENT                     : [],
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
    sqlCode.TIMER                      : ['gClass'],
    sqlCode.pEventConfirm              : ['gClass'],
    sqlCode.pEventConfirmExists        : ['gClass'],
    sqlCode.pEventPrompt               : ['gClass'],
    sqlCode.pEventPromptExists         : ['gClass'],
    sqlCode.pEventLogMsg               : ['gClass'],
    sqlCode.pEventLogMsgExists         : ['gClass'],
    sqlCode.pEventLogReal              : ['gClass'],
    sqlCode.pEventLogRealExists        : ['gClass'],
    sqlCode.pEventLogTime              : ['gClass'],
    sqlCode.pEventLogTimeExists        : ['gClass'],
    sqlCode.pEventDataReal             : ['gClass'],
    sqlCode.pEventDataTime             : ['gClass'],
    sqlCode.pChildIN                   : ['gClass'],
    sqlCode.pChildIN_OUT               : ['gClass'],
    sqlCode.pChildOUT                  : ['gClass'],
#    sqlCode.pSFCListIN                 : ['gSFC'],
#    sqlCode.pSFCListIN_OUT             : ['gSFC'],
#    sqlCode.pSFCListOUT                : ['gSFC'],
    sqlCode.pSFC                       : ['gSFC'],
#    sqlCode.pSFCCallingIN_OUT          : ['gSFC'],
#    sqlCode.pSFCCallingOUT             : ['gSFC'],
    sqlCode.pSFCChild                  : ['gClass', 'gSFC'],
    sqlCode.pSFCChildIN                : ['gClass', 'gSFC'],
#    sqlCode.pSFCChildIN_OUT            : ['gSFC'],
    sqlCode.pSFCChildOUT               : ['gClass', 'gSFC'],
    sqlCode.pBLK                       : ['gClass'],
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
    sqlCode.createClassAll             : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY [Class]'
                                         ),
    sqlCode.createClassNone            : ('SELECT 1'
                                         ),
    sqlCode.createClassOne             : ('SELECT printf("%d",I.ID) AS ID, '
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
                                                 'printf("%d", I.NC) AS NC, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I LEFT JOIN '
                                                  'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Class] = ? AND '
                                                 '(I.Instance = ? OR '
                                                 'I.Parent = ? OR '
                                                 'I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?) '
                                          'ORDER BY I.Instance'
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
                                                'A.Embedded = "FALSE" '
                                          'ORDER BY T.Parent, T.Instance'
                                         ), # gInstance
    sqlCode.ANALOG_EMBED               : ('SELECT printf("%d",T.ID) AS ID, '
                                                 'T.Instance, '
                                                 'T.[Class], '
                                                 'T.Description, '
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
                                                'A.Embedded = "TRUE" '
                                          'ORDER BY T.Parent, T.Instance'
                                         ), # gInstance
    sqlCode.CALL_LEVEL                 : ('SELECT [Level] '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY [Class] '
                                          'LIMIT 1'
                                         ),
    sqlCode.CALL_LIST                  : ('SELECT * '
                                          'FROM tblClass '
                                          'WHERE upper([Level]) = ? '
                                          'ORDER BY [Class]'
                                         ),
    sqlCode.CHILD                      : ('SELECT * '
                                          'FROM tblClass_Child '
                                          'WHERE [Class] = ? '
                                          'ORDER BY childAlias'
                                         ), # gClass
    sqlCode.CHILD_ACQUIRE              : ('SELECT childAlias, '
                                                 'childClass, '
                                                 'printf("%d", childIndex) AS childIndex '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND [State] = ? '
                                                 'AND childAcquire = "TRUE" '
                                          'ORDER BY childAlias'
                                         ), # gClass, gState
    sqlCode.CHILD_INDEX_MAX            : ('SELECT printf("%d", MAX(childIndex)) AS childIndexMax '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE Class = ?'
                                         ), # gClass
    sqlCode.CHILD_INIT_COMMAND         : ('SELECT childAlias, '
                                                 'childClass, '
                                                 'printf("%d", childIndex) AS childIndex, '
                                                 'trueStatement, '
                                                 'trueCommand, '
                                                 'falseStatement, '
                                                 'falseCommand '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND State = ? '
                                          'ORDER BY childAlias'
                                         ), # gClass, gState
    sqlCode.CHILD_INSTANCE             : ('SELECT DISTINCT C.childAlias, '
                                                 'C.childClass, '
                                                 'printf("%d", C.childIndex) AS childIndex, '
                                                 'I.Instance AS childInstance, '
                                                 'I.Description AS childDescription '
                                          'FROM tblClass_ChildStateValues AS C '
                                          'INNER JOIN tblInstance AS I ON '
                                                 'C.Class = I.ParentClass AND '
                                                 'C.childAlias = I.instanceChildAlias '
                                          'WHERE I.Parent = ? '
                                          'ORDER BY childAlias'
                                         ), # gInstance
    sqlCode.CRIL                       : ('SELECT DISTINCT Instance, Description '
                                          'FROM tblInterlockCRIL '
                                          'ORDER BY Instance'
                                         ),
    sqlCode.CRIL_EXISTS                : ('SELECT Instance '
                                          'FROM tblInterlockCRIL '
                                          'WHERE Instance = ? '
                                          'LIMIT 1'
                                         ), # gInstance
    sqlCode.CRIL_INSTANCE              : ('SELECT * '
                                          'FROM tblInterlockCRIL '
                                          'WHERE Instance = ?'
                                         ), # gInstance
    sqlCode.NCRIL                      : ('SELECT DISTINCT Instance, Description '
                                          'FROM tblInterlockNCRIL '
                                          'ORDER BY Instance'
                                         ),
    sqlCode.NCRIL_EXISTS               : ('SELECT Instance '
                                          'FROM tblInterlockNCRIL '
                                          'WHERE Instance = ? '
                                          'LIMIT 1'
                                         ), # gInstance
    sqlCode.NCRIL_INSTANCE             : ('SELECT * '
                                          'FROM tblInterlockNCRIL '
                                          'WHERE Instance = ?'
                                         ), # gInstance
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
                                                 'printf("%d", I.NC) AS NC, '
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
                                                 'printf("%d", I.NC) AS NC, '
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
                                                 'I.GGGParent = ?) '
                                          'ORDER BY I.[Level], I.Instance'
                                         ),
    sqlCode.LINK                       : ('SELECT * '
                                          'FROM tblInstance_Link '
                                          'WHERE [Instance] = ?'
                                         ), # gInstance
    sqlCode.OWNER                      : ('SELECT printf("%d",I.ID) AS ID, '
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
                                                 'printf("%d", I.NC) AS NC, '
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
                                                 'I.GGGParent = ?) '
                                          'ORDER BY I.[Level], I.Instance'
                                         ),
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
    sqlCode.SELVALUE                   : ('SELECT * '
                                          'FROM tblClass_Selection '
                                          'WHERE [Class] = ? AND '
                                                'Parameter = ? AND '
                                                'Selection = ? '
                                          'ORDER BY Parameter, '
                                                'Selection, '
                                                'SelectionValue'
                                          ), # gClass, gSelectParameter , gSelectSelection
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
                                                 'printf("%d", I.NC) AS NC, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I '
                                          'LEFT JOIN tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Level] != "CP" AND '
                                                 '(I.Instance = ? OR '
                                                 'I.Parent = ? OR '
                                                 'I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?) AND '
                                                 'upper(timerTransition) = "YES" '
                                          'ORDER BY I.[Level], Instance'
                                         ),
    sqlCode.TAGS                       : ('SELECT CM.Instance || "-" || IO.Mnemonic AS Symbol, '
                                                 'CM.Instance AS CMTag, '
                                                 'CM.Description AS CMDescription, '
                                                 'CM.[Class] AS CMClass, '
                                                 'CM.Parent, '
                                                 'CM.GParent, '
                                                 'CM.GGParent, '
                                                 'CM.GGGParent, '
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
                                                 'IO.eInstruction , '
                                                 'IO.eVerify, '
                                                 'IO.eResult, '
                                                 'IO.dInstruction, '
                                                 'IO.dVerify, '
                                                 'IO.dResult '
                                          'FROM tblInstance AS CM '
                                          'LEFT JOIN tblClass_IO AS IO ON CM.[Class] = IO.[Class] '
                                          'LEFT JOIN tblIOMaster AS M ON CM.Instance || "-" || IO.Mnemonic = M.Symbol '
                                          'WHERE (CM.Instance = ? OR '
                                                 'CM.Parent = ? OR '
                                                 'CM.GParent = ? OR '
                                                 'CM.GGParent = ? OR '
                                                 'CM.GGGParent = ?) '
                                          'ORDER BY IO.DI DESC , '
                                                 'IO.DO DESC , '
                                                 'IO.AI DESC , '
                                                 'IO.AO DESC , '
                                                 'IO.PDI DESC , '
                                                 'IO.PDO DESC , '
                                                 'IO.PAI DESC , '
                                                 'IO.PAO DESC , '
                                                 'IO.Source DESC , '
                                                 'CM.Instance, '
                                                 'CM.Instance || "-" || IO.Mnemonic'
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
    sqlCode.checkIfChildParameter      : ('SELECT childAlias '
                                          'FROM tblClass_Child '
                                          'WHERE Class = ? '
                                               'AND childAlias LIKE '
                                               'substr(?, 1, length(childAlias)) || "%"'
                                         ), # gClass, sParameter
    sqlCode.insertGlobalParameters     : ('INSERT INTO pGlobal '
                                          'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                                         ),
    sqlCode.addUserParametersChild     : ('SELECT childAlias, '
                                                 'childAliasClass '
                                          'FROM tblClass_Child '
                                          'WHERE [Class] = ? '
                                          'ORDER BY childAlias'
                                         ),
    sqlCode.addUserParametersSFC       : ('SELECT * '
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
                                                 'parameterClass text NOT NULL, '
                                                 'parameterSource text, '
                                                 'parameterType text NOT NULL, '
                                                 'parameterOrder int NOT NULL, '
                                                 'childParameter text NOT NULL, '
                                                 'blockParameter text NOT NULL, '
                                                 'childParameterAlias text, '
                                                 'childParameterAttribute text, '
                                                 'parameterDataType text NOT NULL, '
                                                 'parameterValue text, '
                                                 'parameterDescription text, '
                                                 'isSFC boolean, '
                                                 'isChild boolean, '
                                                 'isEventConfirm boolean, '
                                                 'isEventPrompt boolean, '
                                                 'isEventLogMsg boolean, '
                                                 'isEventLogReal boolean, '
                                                 'isEventLogTime boolean, '
                                                 'isEventDataReal boolean, '
                                                 'isEventDataTime boolean)'
                                         ),
    sqlCode.pEventConfirm              : ('SELECT *, '
                                                 'Replace(childParameter,"_confirm",".confirm") AS dbEventParameter '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventConfirm = 1 '
                                          'ORDER BY parameterOrder, parameterSource, childParameter'
                                         ), # gClass
    sqlCode.pEventConfirmExists        : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventConfirm = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventPrompt               : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventPrompt = 1 '
                                          'ORDER BY parameterOrder, parameterSource, childParameter'
                                         ), # gClass
    sqlCode.pEventPromptExists         : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventPrompt = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogMsg               : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogMsg = 1 '
                                          'ORDER BY parameterOrder, parameterSource, childParameter'
                                         ), # gClass
    sqlCode.pEventLogMsgExists         : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogMsg = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogReal              : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogReal = 1 '
                                          'ORDER BY parameterOrder, parameterSource, childParameter'
                                         ), # gClass
    sqlCode.pEventLogRealExists        : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogReal = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventLogTime              : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogTime = 1 '
                                          'ORDER BY parameterOrder, parameterSource, childParameter'
                                         ), # gClass
    sqlCode.pEventLogTimeExists        : ('SELECT isSFC '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventLogTime = 1 '
                                          'LIMIT 1'
                                         ), # gClass
    sqlCode.pEventDataReal             : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventDataReal = 1 '
                                          'ORDER BY parameterOrder, parameterSource, childParameter'
                                         ), # gClass
    sqlCode.pEventDataTime             : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
                                                 'isSFC = 1 AND '
                                                 'isEventDataTime = 1 '
                                          'ORDER BY parameterOrder, parameterSource, childParameter'
                                         ), # gClass
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
                                                        'S.childAlias = substr(P.blockParameter,1,length(S.childAlias)) AND '
                                                        'S.SFC = P.parameterSource '
                                          'WHERE S.Class = ? AND '
                                                 'P.parameterSource = ? AND '
                                                 'S.childAcquire = "TRUE" AND '
                                                 'P.isSFC = 1 AND '
                                                 'P.isChild = 1 '
                                          'ORDER BY S.State, '
                                                 'P.parameterOrder, '
                                                 'P.parameterSource, '
                                                 'P.childParameter'
                                         ), # gClass, gSFC
    sqlCode.pSFCChildIN                : ('SELECT S.Class, '
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
                                                        'S.childAlias = substr(P.blockParameter,1,length(S.childAlias)) AND '
                                                        'S.SFC = P.parameterSource '
                                          'WHERE S.Class = ? AND '
                                                 'P.parameterSource = ? AND '
                                                 'P.parameterType = "VAR_INPUT" AND '
                                                 'S.childAcquire = "TRUE" AND '
                                                 'P.isChild = 1 '
                                          'ORDER BY S.State, '
                                                 'P.parameterOrder, '
                                                 'P.parameterSource, '
                                                 'P.childParameter'
                                         ), # gClass
    sqlCode.pSFCChildOUT               : ('SELECT S.Class, '
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
                                                        'S.childAlias = substr(P.blockParameter,1,length(S.childAlias)) AND '
                                                        'S.SFC = P.parameterSource '
                                          'WHERE S.Class = ? AND '
                                                 'P.parameterSource = ? AND '
                                                 'P.parameterType = "VAR_OUTPUT" AND '
                                                 'S.childAcquire = "TRUE" AND '
                                                 'P.isChild = 1 '
                                          'ORDER BY S.State, '
                                                 'P.parameterOrder, '
                                                 'P.parameterSource, '
                                                 'P.childParameter'
                                         ), # gClass
    sqlCode.pChildIN                   : ('SELECT * FROM pGlobal '
                                          'WHERE parameterClass IN '
                                                    '(SELECT childAliasClass '
                                                     'FROM tblClass_Child '
                                                     'WHERE parameterClass = ?) AND '
                                                 'parameterSource = "" AND '
                                                 'parameterType = "VAR_INPUT" AND '
                                                 'isSFC = 0'
                                         ), # gClass
    sqlCode.pChildIN_OUT               : ('SELECT * FROM pGlobal '
                                          'WHERE parameterClass IN '
                                                    '(SELECT childAliasClass '
                                                     'FROM tblClass_Child '
                                                     'WHERE parameterClass = ?) AND '
                                                 'parameterSource = "" AND '
                                                 'parameterType = "VAR_INPUT" AND '
                                                 'isSFC = 0'
                                         ), # gClass
    sqlCode.pChildOUT                  : ('SELECT * FROM pGlobal '
                                          'WHERE parameterClass IN '
                                                    '(SELECT childAliasClass '
                                                     'FROM tblClass_Child '
                                                     'WHERE parameterClass = ?) AND '
                                                 'parameterSource = "" AND '
                                                 'parameterType = "VAR_INPUT" AND '
                                                 'isSFC = 0'
                                         ), # gClass
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
    sqlCode.pSFC                       : ('SELECT DISTINCT '
                                                'blockParameter, '
                                                'parameterDataType, '
                                                'parameterDescription '
                                          'FROM pGlobal '
                                          'WHERE parameterSource = ? AND '
                                                'isChild = 0 AND '
                                                'isSFC = 1 '
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
    sqlCode.pBLK                       : ('SELECT * '
                                          'FROM pGlobal '
                                          'WHERE parameterClass = ? AND '
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
