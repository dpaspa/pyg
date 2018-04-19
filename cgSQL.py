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
    populateSFCParmsChild              = -8
    populateSFCParmsInsert             = -9
    populateSFCParmsSubstate           = -10
    processLevel                       = -11
    processLevelCount                  = -12
    versionHistory                     = -13
    CHILD                              = -14
    CHILD_ACQUIRE                      = -15
    CHILD_INIT_COMMAND                 = -16
    CR_IL                              = -17
    NCR_IL                             = -18
    HYGIENE                            = -19
    INSTANCE_ALL                       = -21
    INSTANCE_BLK                       = -22
    OWNER                              = -23
    PARENT                             = -24
    PARM_CHILD_VAR_INPUT               = -25
    PARM_CHILD_VAR_OUTPUT              = -26
    PARM_CHILD_VAR_IN_OUT              = -27
    PARM_SFC_VAR_INPUT                 = -34
    PARM_SFC_VAR_IN_OUT                = -35
    PARM_SFC_VAR_OUTPUT                = -41
    PARM_SFC_CHILD_VAR_INPUT           = -42
    PARM_SFC_CHILD_VAR_OUTPUT          = -43
    PARM_SFC_CHILD_VAR_IN_OUT          = -44
    PARM_SFC_DATA_VAR_INPUT            = -45
    PARM_SFC_DATA_VAR_OUTPUT           = -51
    PARM_SFC_DATA_VAR_IN_OUT           = -52
    PARM_SFC_CONFIRM                   = -53
    PARM_SFC_LOG                       = -54
    PARM_SFC_PROMPT                    = -55
    PARM_INSTANCE_VAR_INPUT            = -61
    PARM_INSTANCE_VAR_OUTPUT           = -62
    PARM_INSTANCE_VAR_IN_OUT           = -63
    PARM_VAR                           = -64
    PARM_VAR_INPUT                     = -97
    PARM_VAR_IN_OUT                    = -98
    PARM_VAR_OUTPUT                    = -99
    PARM_VAR_TEMP                      = -65
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

prm = {
    sqlCode.CHILD                      : ['gClass'],
    sqlCode.CHILD_ACQUIRE              : ['gClass', 'gState'],
    sqlCode.CHILD_INIT_COMMAND         : ['gClass', 'gState'],
    sqlCode.CR_IL                      : ['gInstance'],
    sqlCode.NCR_IL                     : ['gInstance'],
    sqlCode.HYGIENE                    : ['gClass'],
    sqlCode.INSTANCE_ALL               : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.INSTANCE_BLK               : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.OWNER                      : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.PARENT                     : [],
    sqlCode.PARM_VAR_INPUT             : ['gClass'],
    sqlCode.PARM_VAR_IN_OUT            : ['gClass'],
    sqlCode.PARM_VAR_OUTPUT            : ['gClass'],
    sqlCode.PARM_CHILD_VAR_INPUT       : ['gClass'],
    sqlCode.PARM_CHILD_VAR_OUTPUT      : ['gClass', 'gState'],
    sqlCode.PARM_CHILD_VAR_IN_OUT      : ['gClass', 'gState'],
    sqlCode.PARM_SFC_VAR_INPUT         : ['gSFC'],
    sqlCode.PARM_SFC_VAR_IN_OUT        : ['gSFC'],
    sqlCode.PARM_SFC_VAR_OUTPUT        : ['gSFC'],
    sqlCode.PARM_SFC_CHILD_VAR_INPUT   : ['gSFC'],
    sqlCode.PARM_SFC_CHILD_VAR_IN_OUT  : ['gSFC'],
    sqlCode.PARM_SFC_CHILD_VAR_OUTPUT  : ['gSFC'],
    sqlCode.PARM_SFC_DATA_VAR_INPUT    : ['gClass'],
    sqlCode.PARM_SFC_DATA_VAR_IN_OUT   : ['gClass'],
    sqlCode.PARM_SFC_DATA_VAR_OUTPUT   : ['gClass'],
    sqlCode.PARM_SFC_CONFIRM           : ['gClass'],
    sqlCode.PARM_SFC_LOG               : ['gClass'],
    sqlCode.PARM_SFC_PROMPT            : ['gClass'],
    sqlCode.PARM_INSTANCE_VAR_INPUT    : ['gInstance'],
    sqlCode.PARM_INSTANCE_VAR_IN_OUT   : ['gInstance'],
    sqlCode.PARM_INSTANCE_VAR_OUTPUT   : ['gInstance'],
    sqlCode.PARM_VAR                   : ['gInstance'],
    sqlCode.SELECT                     : ['gClass'],
    sqlCode.SELVALUE                   : ['gClass', 'gSelectParameter' , 'gSelectSelection'],
    sqlCode.SFC                        : ['gClass'],
    sqlCode.STATE                      : ['gClass'],
    sqlCode.STATE_TIMER                : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.TAGS                       : ['gParent', 'gParent', 'gParent', 'gParent', 'gParent'],
    sqlCode.TIMER                      : ['gClass'],
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
                                                 'I.Module, '
                                                 'I.NumInstance, '
                                                 'I.lnk1Tag, '
                                                 'I.lnk1Class, '
                                                 'I.lnk2Tag, '
                                                 'I.lnk2Class, '
                                                 'I.childAlias, '
                                                 'I.childAliasClass, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I LEFT JOIN '
                                                  'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Level] != ? '
                                                 'AND I.[Class] = ? AND '
                                                 '(I.Instance = ? OR '
                                                 'I.Parent = ? OR '
                                                 'I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?) '
                                          'ORDER BY I.Instance'
                                         ),
    sqlCode.createParameterSFC         : ('CREATE TABLE IF NOT EXISTS '
                                          'tblParameter_SFC ('
                                                 '[Class] text NOT NULL, '
                                                 'SFC text NOT NULL, '
                                                 'ParameterType text NOT NULL, '
                                                 'sfcParameter text NOT NULL, '
                                                 'blockParameter text NOT NULL, '
                                                 'ParameterDataType text NOT NULL, '
                                                 'ParameterValue text, '
                                                 'ParameterDescription text, '
                                                 'isChild integer)'
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
    sqlCode.defaultParameters          : ('SELECT * '
                                          'FROM tblParameter_Default'
                                         ),
    sqlCode.populateSFCParmsChild      : ('SELECT childSFCAlias '
                                          'FROM tblClass_Child '
                                          'WHERE Class = ? '
                                               'AND childSFCAlias LIKE '
                                               'substr(?, 1, length(childSFCAlias)) || "%"'
                                         ), # gClass, sParameter

    sqlCode.populateSFCParmsInsert     : ('INSERT INTO tblParameter_SFC '
                                          'VALUES (?,?,?,?,?,?,?,?,?)'
                                         ),
    sqlCode.populateSFCParmsSubstate   : ('SELECT * '
                                          'FROM tblClass_State '
                                          'WHERE [Class] = ? '
                                                 'AND upper(SFC) != ? '
                                          'ORDER BY State'
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
    sqlCode.CHILD                      : ('SELECT * '
                                          'FROM tblClass_Child '
                                          'WHERE [Class] = ? '
                                          'ORDER BY childAlias'
                                         ), # gClass
    sqlCode.CHILD_ACQUIRE              : ('SELECT * '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND [State] = ? '
                                                 'AND childAcquire = "TRUE" '
                                          'ORDER BY childAlias'
                                         ), # gClass, gState
    sqlCode.CHILD_INIT_COMMAND         : ('SELECT * '
                                          'FROM tblClass_ChildStateValues '
                                          'WHERE [Class] = ? AND State = ? '
                                          'ORDER BY childAlias'
                                         ), # gClass, gState
    sqlCode.CR_IL                      : ('SELECT * '
                                          'FROM tblInterlockCR '
                                          'WHERE Target = ?'
                                         ), # gInstance
    sqlCode.NCR_IL                     : ('SELECT * '
                                          'FROM tblInterlockNCR '
                                          'WHERE Target = ?'
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
                                                 'I.Module, '
                                                 'I.NumInstance, '
                                                 'I.lnk1Tag, '
                                                 'I.lnk1Class, '
                                                 'I.lnk2Tag, '
                                                 'I.lnk2Class, '
                                                 'I.childAlias, '
                                                 'I.childAliasClass, '
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
                                                 'I.Module, '
                                                 'I.NumInstance, '
                                                 'I.lnk1Tag, '
                                                 'I.lnk1Class, '
                                                 'I.lnk2Tag, '
                                                 'I.lnk2Class, '
                                                 'I.childAlias, '
                                                 'I.childAliasClass, '
                                                 'C.Description AS ClassDescription '
                                          'FROM tblInstance AS I LEFT JOIN '
                                                 'tblClass AS C ON I.ClassID = C.ID '
                                          'WHERE I.[Level] != "CM" AND '
                                                 'I.[Level] != "PC" AND '
                                                 '(I.Instance = ? OR '
                                                 'I.Parent = ? OR '
                                                 'I.GParent = ? OR '
                                                 'I.GGParent = ? OR '
                                                 'I.GGGParent = ?) '
                                          'ORDER BY I.[Level], I.Instance'
                                         ),
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
                                                 'I.Module, '
                                                 'I.NumInstance, '
                                                 'I.lnk1Tag, '
                                                 'I.lnk1Class, '
                                                 'I.lnk2Tag, '
                                                 'I.lnk2Class, '
                                                 'I.childAlias, '
                                                 'I.childAliasClass, '
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
    sqlCode.PARM_CHILD_VAR_INPUT       : ('SELECT P.Parameter, '
                                                 'P.ParameterClass, '
                                                 'P.ParameterDataType, '
                                                 'P.ParameterType, '
                                                 'P.childParameterAlias, '
                                                 'P.ParameterDescription, '
                                                 'C.childAlias, '
                                                 'C.childAliasClass, '
                                                 'C.childAliasDescription, '
                                                 'S.State, '
                                                 'S.StateDescription '
                                          'FROM tblClass_Parameter AS P '
                                                 'INNER JOIN tblClass_Child AS C ON '
                                                 'P.childParameterAlias = c.childAlias '
                                          'INNER JOIN tblClass_State AS S ON '
                                                 'P.State = S.State '
                                          'WHERE C.Class = ? AND ParameterType = "VAR_INPUT" '
                                          'ORDER BY P.Parameter'
                                         ), # gClass
    sqlCode.PARM_VAR_INPUT             : ('SELECT P.Parameter, '
                                                 'P.ParameterClass, '
                                                 'P.ParameterDataType, '
                                                 'P.ParameterType, '
                                                 'P.childParameterAlias, '
                                                 'P.ParameterDescription '
                                          'FROM tblClass_Parameter AS P '
                                          'WHERE P.ParameterClass = ? AND '
                                                 'length(P.childParameterAlias) = 0 '
                                                 'AND ParameterType = "VAR_INPUT" '
                                          'ORDER BY P.Parameter '
                                         ), # gClass
    sqlCode.PARM_VAR_IN_OUT            : ('SELECT P.Parameter, '
                                                 'P.ParameterClass, '
                                                 'P.ParameterDataType, '
                                                 'P.ParameterType, '
                                                 'P.childParameterAlias, '
                                                 'P.ParameterDescription '
                                          'FROM tblClass_Parameter AS P '
                                          'WHERE P.ParameterClass = ? AND '
                                                 'length(P.childParameterAlias) = 0 '
                                                 'AND ParameterType = "VAR_IN_OUT" '
                                          'ORDER BY P.Parameter '
                                         ), # gClass
    sqlCode.PARM_VAR_OUTPUT            : ('SELECT P.Parameter, '
                                                 'P.ParameterClass, '
                                                 'P.ParameterDataType, '
                                                 'P.ParameterType, '
                                                 'P.childParameterAlias, '
                                                 'P.ParameterDescription '
                                          'FROM tblClass_Parameter AS P '
                                          'WHERE P.ParameterClass = ? AND '
                                                 'length(P.childParameterAlias) = 0 '
                                                 'AND ParameterType = "VAR_OUTPUT" '
                                          'ORDER BY P.Parameter '
                                         ), # gClass
    sqlCode.PARM_SFC_VAR_INPUT         : ('SELECT * '
                                          'FROM tblParameter_SFC '
                                          'WHERE SFC = ? AND '
                                                 'ParameterType = "VAR_INPUT"'
                                         ), # gSFC
    sqlCode.PARM_SFC_VAR_IN_OUT        : ('SELECT * '
                                          'FROM tblParameter_SFC '
                                          'WHERE SFC = ? AND '
                                                 'ParameterType = "VAR_IN_OUT"'
                                         ), # gSFC
    sqlCode.PARM_SFC_VAR_OUTPUT        : ('SELECT * '
                                          'FROM tblParameter_SFC '
                                          'WHERE SFC = ? AND '
                                                 'ParameterType = "VAR_OUTPUT"'
                                         ), # gSFC
    sqlCode.PARM_SFC_CHILD_VAR_INPUT   : ('SELECT sfcParameter, '
                                                 'blockParameter, '
                                                 'ParameterType, '
                                                 'ParameterDataType, '
                                                 'ParameterDescription '
                                          'FROM tblParameter_SFC '
                                          'WHERE SFC = ? AND '
                                                 'ParameterType = "VAR_INPUT" AND '
                                                 'isChild = "TRUE"'
                                         ), # gSFC
    sqlCode.PARM_SFC_CHILD_VAR_IN_OUT  : ('SELECT sfcParameter, '
                                                 'blockParameter, '
                                                 'ParameterType, '
                                                 'ParameterDataType, '
                                                 'ParameterDescription '
                                          'FROM tblParameter_SFC '
                                          'WHERE SFC = ? AND '
                                                 'ParameterType = "VAR_IN_OUT" AND '
                                                 'isChild = "TRUE"'
                                         ), # gSFC
    sqlCode.PARM_SFC_CHILD_VAR_OUTPUT  : ('SELECT sfcParameter, '
                                                 'blockParameter, '
                                                 'ParameterType, '
                                                 'ParameterDataType, '
                                                 'ParameterDescription '
                                          'FROM tblParameter_SFC '
                                          'WHERE SFC = ? AND '
                                                 'ParameterType = "VAR_OUTPUT" AND '
                                                 'isChild = "TRUE"'
                                         ), # gSFC
    sqlCode.PARM_SFC_DATA_VAR_INPUT    : ('SELECT DISTINCT '
                                                 'blockParameter, '
                                                 'ParameterDataType, '
                                                 'ParameterDescription '
                                          'FROM tblParameter_SFC '
                                          'WHERE [Class] = ? AND '
                                                 'ParameterType = "VAR_INPUT" AND '
                                                 'isChild = "FALSE"'
                                         ), # gClass
    sqlCode.PARM_SFC_DATA_VAR_IN_OUT   : ('SELECT DISTINCT '
                                                 'blockParameter, '
                                                 'ParameterDataType, '
                                                 'ParameterDescription '
                                          'FROM tblParameter_SFC '
                                          'WHERE [Class] = ? AND '
                                                 'ParameterType = "VAR_IN_OUT" AND '
                                                 'isChild = "FALSE"'
                                         ), # gClass
    sqlCode.PARM_SFC_DATA_VAR_OUTPUT   : ('SELECT DISTINCT '
                                                 'blockParameter, '
                                                 'ParameterDataType, '
                                                 'ParameterDescription '
                                          'FROM tblParameter_SFC '
                                          'WHERE [Class] = ? AND '
                                                 'ParameterType = "VAR_OUTPUT" AND '
                                                 'isChild = "FALSE"'
                                         ), # gClass
    sqlCode.PARM_SFC_CONFIRM           : ('SELECT [Class], '
                                                 'SFC, '
                                                 'ParameterType, '
                                                 'sfcParameter, '
                                                 'blockParameter, '
                                                 'ParameterDataType, '
                                                 'ParameterValue, '
                                                 'ParameterDescription, '
                                                 'Replace(sfcParameter,"_confirm",".confirm") AS dbEventParameter '
                                          'FROM tblParameter_SFC '
                                          'WHERE [Class] = ? AND '
                                                 'blockParameter LIKE "%CONFIRM%"'
                                'ORDER BY SFC, sfcParameter'
                                         ), # gClass
    sqlCode.PARM_SFC_LOG               : ('SELECT * '
                                          'FROM tblParameter_SFC '
                                          'WHERE [Class] = ? AND '
                                                 'substr(blockParameter, 1, 4) = "LOG_" '
                                          'ORDER BY SFC, sfcParameter'
                                         ), # gClass
    sqlCode.PARM_SFC_PROMPT            : ('SELECT * '
                                          'FROM tblParameter_SFC '
                                          'WHERE [Class] = ? AND '
                                                 'substr(blockParameter, 1, 7) = "PROMPT_" AND '
                                                 'blockParameter NOT LIKE "%CONFIRM%" '
                                          'ORDER BY SFC, sfcParameter'
                                         ), # gClass
    sqlCode.PARM_INSTANCE_VAR_INPUT    : ('SELECT printf("%d",T.ID) AS ID, '
                                                 'T.Instance, '
                                                 'T.[Class], '
                                                 'T.Description, '
                                                 'P.Parameter, '
                                                 'P.ParameterDataType, '
                                                 'P.ParameterType, '
                                                 'P.ParameterDescription, '
                                                 'P.UoM, '
                                                 'P.ParameterMin, '
                                                 'P.ParameterMax, '
                                                 'P.ParameterValue '
                                          'FROM tblInstance AS T INNER JOIN '
                                                 'tblClass_Parameter AS P ON T.ClassID = P.ClassID '
                                          'WHERE T.Instance = ? AND P.ParameterType = "VAR_INPUT" '
                                          'ORDER BY T.Parent, T.Instance, P.Parameter'
                                         ), # gInstance
    sqlCode.PARM_INSTANCE_VAR_IN_OUT   : ('SELECT printf("%d",T.ID) AS ID, '
                                                 'T.Instance, '
                                                 'T.[Class], '
                                                 'T.Description, '
                                                 'P.Parameter, '
                                                 'P.ParameterDataType, '
                                                 'P.ParameterType, '
                                                 'P.ParameterDescription, '
                                                 'P.UoM, '
                                                 'P.ParameterMin, '
                                                 'P.ParameterMax, '
                                                 'P.ParameterValue '
                                          'FROM tblInstance AS T INNER JOIN '
                                                 'tblClass_Parameter AS P ON T.ClassID = P.ClassID '
                                          'WHERE T.Instance = ? AND P.ParameterType = "VAR_IN_OUT" '
                                          'ORDER BY T.Parent, T.Instance, P.Parameter'
                                         ), # gInstance
    sqlCode.PARM_INSTANCE_VAR_OUTPUT   : ('SELECT printf("%d",T.ID) AS ID, '
                                                 'T.Instance, '
                                                 'T.[Class], '
                                                 'T.Description, '
                                                 'P.Parameter, '
                                                 'P.ParameterDataType, '
                                                 'P.ParameterType, '
                                                 'P.ParameterDescription, '
                                                 'P.UoM, '
                                                 'P.ParameterMin, '
                                                 'P.ParameterMax, '
                                                 'P.ParameterValue '
                                          'FROM tblInstance AS T INNER JOIN '
                                                 'tblClass_Parameter AS P ON T.ClassID = P.ClassID '
                                          'WHERE T.Instance = ? AND P.ParameterType = "VAR_OUTPUT" '
                                          'ORDER BY T.Parent, T.Instance, P.Parameter'
                                         ), # gInstance
    sqlCode.PARM_VAR                   : ('SELECT printf("%d",T.ID) AS ID, '
                                                 'T.Instance, '
                                                 'T.[Class], '
                                                 'T.Description, '
                                                 'P.Parameter, '
                                                 'P.ParameterDataType, '
                                                 'P.ParameterType, '
                                                 'P.ParameterDescription, '
                                                 'P.UoM, '
                                                 'P.ParameterMin, '
                                                 'P.ParameterMax, '
                                                 'P.ParameterValue '
                                          'FROM tblInstance AS T INNER JOIN '
                                                 'tblClass_Parameter AS P ON T.ClassID = P.ClassID '
                                          'WHERE T.Instance = ? AND P.ParameterType = "VAR" '
                                          'ORDER BY T.Parent, T.Instance, P.Parameter'
                                         ), # gInstance
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
                                                 'I.Module, '
                                                 'I.NumInstance, '
                                                 'I.lnk1Tag, '
                                                 'I.lnk1Class, '
                                                 'I.lnk2Tag, '
                                                 'I.lnk2Class, '
                                                 'I.childAlias, '
                                                 'I.childAliasClass, '
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
                                                 'CASE WHEN IO.DI=1 THEN "DI" WHEN IO.DO=1 THEN "DO" WHEN IO.AI=1 THEN "AI" WHEN IO.AO=1 THEN "AO" WHEN IO.PDI=1 THEN "PDI" WHEN IO.PDO=1 THEN "PDO" WHEN IO.PAI=1 THEN "PAI" WHEN IO.PAO=1 THEN "PAO" END IOClass, '
                                                 'CASE WHEN IO.DI=1 THEN "%I" WHEN IO.DO=1 THEN "%Q" WHEN IO.AI=1 THEN "%IW" WHEN IO.AO=1 THEN "%QW" WHEN IO.PDI=1 THEN "PDI" WHEN IO.PDO=1 THEN "PDO" WHEN IO.PAI=1 THEN "PAI" WHEN IO.PAO=1 THEN "PAO" END Prefix, '
                                                 'CASE WHEN IO.DI=1 THEN "Bool" WHEN IO.DO=1 THEN "Bool" WHEN IO.AI=1 THEN "Int" WHEN IO.AO=1 THEN "Int" WHEN IO.PDI=1 THEN "Bool" WHEN IO.PDO=1 THEN "Bool" WHEN IO.PAI=1 THEN "Int" WHEN IO.PAO=1 THEN "Int" END DataType, '
                                                 'IO.eInstruction , '
                                                 'IO.eVerify, '
                                                 'IO.eResult, '
                                                 'IO.dInstruction, '
                                                 'IO.dVerify, '
                                                 'IO.dResult '
                                          'FROM tblInstance AS CM '
                                          'INNER JOIN tblClass_IO AS IO ON CM.[Class] = IO.[Class] '
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
}
