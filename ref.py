#------------------------------------------------------------------------------#
#                      Copyright © 2016 ipoogi.com                             #
#                                                                              #
# Description:                                                                 #
# Checks to see if a reference document format and converts to XML data.       #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Rev By                Date        CC   Note                                  #
# 3   David Paspa       18-Oct-2016 NA   Convert to vb.net.                    #
# 2   David Paspa       06-Dec-2015 NA   Made into separate Word effector.     *
# 1   David Paspa       11-Sep-2011 NA   Initial design.                       #
#------------------------------------------------------------------------------#
'Option Strict On
Imports System.Reflection
Imports Word = Microsoft.Office.Interop.Word
Public Class secondaryFunction
    #--------------------------------------------------------------------------#
    # Declare structure for secondary function variables:                      #
    #--------------------------------------------------------------------------#
    Structure functionStructure
        Public checkOnStart As Boolean
        Public ignoreBlanks As Boolean
        Public keyCount As Integer
    End Structure
    Public mf As functionStructure

    #--------------------------------------------------------------------------#
    # Declare module level application object variables for the effectors:     *
    #--------------------------------------------------------------------------#
    Private wdApp As Word.Application = Nothing
    Private wdDoc As Word.Document = Nothing
    Private oType As String

    #--------------------------------------------------------------------------#
    # Get the procedure name:                                                  #
    #--------------------------------------------------------------------------#
    Private _errorModule As String = Me.GetType().FullName

    #--------------------------------------------------------------------------#
    # Local error handler which passes error information to the host. Uses */
    # the global error variable iErr from secondaryMessenger. If a fatal       #
    # error then never return. If a warning or just a message then the         #
    # error is reset by the host and the program returns:                      #
    #--------------------------------------------------------------------------#
    Private Sub eH(ByVal errorLevel As Integer, ByVal errorProcedure As String, ByVal errorNumber As Long, ByVal errorSystemMessage As String, ParamArray errorParameters() As String)
        #----------------------------------------------------------------------#
        # Stop processing if a fatal error:                                    #
        #----------------------------------------------------------------------#
        If (oHost Is Nothing) Then
            Debug.Print("Host is not defined so cannot report error " & errorNumber & " in procedure " & errorProcedure & "." & vbCrLf & errorSystemMessage & vbCrLf & getErrorConstant(iErr))
        Else
            oHost.errHandler(iErr, errorNumber, errorLevel, _errorModule, errorProcedure, AddressOf getErrorMessage, AddressOf getErrorConstant, errorSystemMessage, errorParameters)
        End If

        #----------------------------------------------------------------------#
        # Show the office application if any error:                            #
        #----------------------------------------------------------------------#
        Debug.Print("Error " & CType(errorNumber, String) & " in procedure " & errorProcedure)
        showOfficeApp()
    End Sub

    #--------------------------------------------------------------------------#
    # Get the error constant string:                                           #
    #--------------------------------------------------------------------------#
    Private Function getErrorConstant(ByVal errNumber As Long) As String
        #----------------------------------------------------------------------#
        # Declare local varaiables and parse the Enum:                         #
        #----------------------------------------------------------------------#
        Dim names() As String = [Enum].GetNames(GetType(_errorValue))
        getErrorConstant = ""

        #----------------------------------------------------------------------#
        # Return the matching constant name:                                   #
        #----------------------------------------------------------------------#
        For Each name In names
            If (errNumber = CType([Enum].Parse(GetType(_errorValue), name), Long)) Then
                getErrorConstant = name
                Exit For
            End If
        Next
    End Function

    #--------------------------------------------------------------------------#
    # Enumerate the error constants:                                           #
    #--------------------------------------------------------------------------#
    Private Enum _errorValue
        #----------------------------------------------------------------------#
        # Error constants start at vbObjectError + 512:                        #
        #----------------------------------------------------------------------#
        applicationHandle = vbObjectError + 512
        cannotCreateXML = vbObjectError + 513
        docParmInvalid = vbObjectError + 514
        docParmInvalidTable = vbObjectError + 515
        docParmInvalidType = vbObjectError + 516
        docParmNotFound = vbObjectError + 517
        docParmRequired = vbObjectError + 518
        docParmDataTypeInvalid = vbObjectError + 519
        docRefInvalidTable = vbObjectError + 520
        duplicateTag = vbObjectError + 521
        invalidExternalRefDoc = vbObjectError + 522
        invalidHost = vbObjectError + 523
        invalidObject = vbObjectError + 524
        invalidParameter = vbObjectError + 525
        InvalidPrefix = vbObjectError + 526
        InvalidStructure = vbObjectError + 527
        invalidTag = vbObjectError + 528
        noMergedCells = vbObjectError + 529
        noRefTablesFound = vbObjectError + 530
        noTagSpecified = vbObjectError + 531
        notTable = vbObjectError + 532
        parameterMissing = vbObjectError + 533
        refsLocked = vbObjectError + 534
        singleValueOnly = vbObjectError + 535
        tableAccess = vbObjectError + 536
        XMLFileError = vbObjectError + 537

        sessionCmdUnknown = vbObjectError + 550
        sessionException = vbObjectError + 551
    End Enum

    #--------------------------------------------------------------------------#
    # Define the message for each of the above error constants:                #
    #--------------------------------------------------------------------------#
    Private Function getErrorMessage(ByVal errNumber As Long) As String
        #----------------------------------------------------------------------#
        # Get the error message for the current error:                         #
        #----------------------------------------------------------------------#
        Select Case errNumber
            Case _errorValue.applicationHandle : getErrorMessage = "Cannot access MS Word application or document."
            Case _errorValue.cannotCreateXML : getErrorMessage = "Cannot create XML object."
            Case _errorValue.docParmInvalid : getErrorMessage = "Document parameter @1 value @2 is invalid in document @4. Value should match datatype of @3."
            Case _errorValue.docParmInvalidTable : getErrorMessage = "Document parameter table with parameter @1 has invalid number of columns @2."
            Case _errorValue.docParmInvalidType : getErrorMessage = "Document parameter @1 type @2 is invalid."
            Case _errorValue.docParmNotFound : getErrorMessage = "Could not find parameter @1."
            Case _errorValue.docParmRequired : getErrorMessage = "Document parameter @1 is required but no value specified in document @3. Value should match datatype of @2."
            Case _errorValue.docParmDataTypeInvalid : getErrorMessage = "Document parameter @1 value @2 in document @3 has no datatype specified in parameter table."
            Case _errorValue.docRefInvalidTable : getErrorMessage = "Reference document table has invalid number of columns @2."
            Case _errorValue.duplicateTag : getErrorMessage = "Tag @1 in field @2 with type @3 is duplicated in document @4. The index part @5 without the prefix @6 must be unique."
            Case _errorValue.invalidExternalRefDoc : getErrorMessage = "Reference document number @1 has an invalid type of @2. Expected R for reference or T for test."
            Case _errorValue.invalidHost : getErrorMessage = "Host object reference is not set."
            Case _errorValue.invalidObject : getErrorMessage = "Receptor object is invalid."
            Case _errorValue.invalidParameter : getErrorMessage = "Parameter dictionary object reference is not set."
            Case _errorValue.InvalidPrefix : getErrorMessage = "Prefix @1 format invalid for parameter @2. Must be of the form 'Un'."
            Case _errorValue.InvalidStructure : getErrorMessage = "Structure parameter @1 could not be accessed."
            Case _errorValue.invalidTag : getErrorMessage = "Tag reference number @1 contains invalid characters. Remove any non-alphanumeric characters."
            Case _errorValue.noMergedCells : getErrorMessage = "Merged tables cells are not permitted."
            Case _errorValue.noRefTablesFound : getErrorMessage = "No reference tables found in this document. Perhaps the table titles do match EXAAAACTLY with the parameter field name values."
            Case _errorValue.noTagSpecified : getErrorMessage = "No tag specified to get table row data. Select a row of a reference number table."
            Case _errorValue.notTable : getErrorMessage = "This operation can only be performed inside a table."
            Case _errorValue.parameterMissing : getErrorMessage = "Expected messenger parameter @1 is missing from the dictionary."
            Case _errorValue.refsLocked : getErrorMessage = "Cannot renumber references because the document is locked. Unlock it manually and try again."
            Case _errorValue.singleValueOnly : getErrorMessage = "Document parameter @1 value @2 is invalid for reference @3 in document @4. Must be a single value only."
            Case _errorValue.tableAccess : getErrorMessage = "Cannot access tables in MS Word document."
            Case _errorValue.XMLFileError : getErrorMessage = "Cannot read or write to file @1 because @2."

            Case _errorValue.sessionCmdUnknown : getErrorMessage = "Unknown session command @1."
            Case _errorValue.sessionException : getErrorMessage = "Exception occurred whilst processing session command @1."
            Case Else
                getErrorMessage = "No message defined."
        End Select
    End Function

    #--------------------------------------------------------------------------#
    # Document information table column numbers in MS Word:                    #
    #--------------------------------------------------------------------------#
    Public Const NUM_COLS_INFO = 3
    Public Enum di
        information = 1
        value = 2
        description = 3
    End Enum

    #--------------------------------------------------------------------------#
    # Table cell parameter data type:                                          #
    #--------------------------------------------------------------------------#
    Public Structure dType
        Public info As String
        Public value As String
        Public description As String
    End Structure

    #--------------------------------------------------------------------------#
    # Parameter table column numbers in MS Word:                               #
    #--------------------------------------------------------------------------#
    Public Const NUM_COLS_PARM = 6
    Public Enum pi
        name = 1
        description = 2
        need = 3
        view = 4
        entry = 5
        key = 6
    End Enum

    #--------------------------------------------------------------------------#
    # Table cell parameter data type:                                          #
    #--------------------------------------------------------------------------#
    Public Structure pType
        Public id As Integer
        Public name As String
        Public description As String
        Public need As Boolean
        Public view As Boolean
        Public dataType As String
        Public keyType As String
        Public keyPrefix As String
        Public keySeries As Integer
        Public keyContainer As String
        Public value As String
        Public order As Integer
        Public tableId As Integer
        Public rowId As Integer
        Public columnId As Integer
    End Structure

    #--------------------------------------------------------------------------#
    # Declare module level variables:                                          #
    #--------------------------------------------------------------------------#
    Public xmlDoc As MSXML2.DOMDocument60
    Public objDocument As MSXML2.IXMLDOMElement
    Public objParameters As MSXML2.IXMLDOMElement
    Public objRoot As MSXML2.IXMLDOMElement
    Public objTables As MSXML2.IXMLDOMElement
    Public docPrefix As String = ""
    Dim dictDocumentDefs As New Dictionary(Of String, dType)
    Dim dictParameterDefs As New Dictionary(Of String, pType)
    Dim dictParameterTables As New Dictionary(Of String, Integer)
    Dim dictTags As New Dictionary(Of Integer, pType)
    Dim dictUnique As New Dictionary(Of String, pType)

    #--------------------------------------------------------------------------#
    # Set the module structure variable values:                                #
    #--------------------------------------------------------------------------#
    Public Function StructSetValue(ByRef iStruct As Object, ByVal iFldName As String, ByVal iValue As Object) As Object
        #----------------------------------------------------------------------#
        # Define the procedure name and declare local variables:               #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name

        #----------------------------------------------------------------------#
        # Define the structure type:                                           #
        #----------------------------------------------------------------------#
        Dim tStruct As ValueType = iStruct
        Dim field As FieldInfo = tStruct.[GetType]().GetField(iFldName)
        Try
            field.SetValue(tStruct, iValue)
            Return tStruct

        Catch ex As NotSupportedException
            eH(_el.Fatal, _errorProcedure, _errorValue.InvalidStructure, ex.Message, field.Name)
            Return Nothing
        End Try
    End Function

    #--------------------------------------------------------------------------#
    # Set the module structure variable values:                                #
    #--------------------------------------------------------------------------#
    Public Function StrToStruct(ByRef iStruct As Object) As Object
        Dim tStruct As ValueType = iStruct
        Dim fields As FieldInfo() = tStruct.[GetType]().GetFields(BindingFlags.Instance Or BindingFlags.[Public])
        For Each field As FieldInfo In fields
            tStruct = StructSetValue(tStruct, field.Name, dictParameters.Item(field.Name))
            If (iErr <> 0) Then
                Exit For
            End If
        Next field
        Return tStruct
    End Function

    #--------------------------------------------------------------------------#
    # Function: check                                                          #
    #                                                                          #
    # Description:                                                             #
    # Checks the receptor document for compatibility with this secondary       #
    # messenger function. If compatible then there will be no errors. If       #
    # not compatible then return the incompatibility information as one or */
    # more errors.                                                             #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Public Function check() As Long
        #----------------------------------------------------------------------#
        # Define the procedure name and declare local variables:               #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name

        #----------------------------------------------------------------------#
        # Perform application and file specific check to see if the            #
        # is valid for this function to run:                                   #
        #----------------------------------------------------------------------#
        check = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: main                                                           #
    #                                                                          #
    # Description:                                                             #
    # This is the main functionality of the secondary messenger.               #
    # Gets reference document data and converts to XML.                        #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Public Function main() As Long
        #----------------------------------------------------------------------#
        # Define the procedure name and declare local variables:               #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim s As String = ""

        #----------------------------------------------------------------------#
        # Messenger function parameters are added to the messenger data        #
        # structure at the top of this page.                                   #
        #                                                                      #
        # For defined parameters, dictionary data has already been             #
        # verified by now so no need to verify the data again. However, it */
        # is quite possible that expected parameters have not been             #
        # specified at all:                                                    #
        #----------------------------------------------------------------------#
        mf = StrToStruct(mf)
        'Try
        '    s = "ignoreBlanks"
        '    mf.ignoreBlanks = CType(dictParameters.Item(s), Boolean)

        'Catch e As Exception
        '    eH(_el.Fatal, _errorProcedure, _errorValue.parameterMissing, e.Message, s)
        '    Debug.Print("Expected parameter " & s & " is missing from the dictionary.")
        'End Try

        'Try
        '    s = "checkOnStart"
        '    mf.checkOnStart = CType(dictParameters.Item(s), Boolean)

        'Catch e As Exception
        '    eH(_el.Fatal, _errorProcedure, _errorValue.parameterMissing, e.Message, s)
        '    Debug.Print("Expected parameter " & s & " is missing from the dictionary.")
        'End Try

        #----------------------------------------------------------------------#
        # Set the application type:                                            #
        #----------------------------------------------------------------------#
        If (iErr <> 0) Then
        ElseIf (oHost.oAppType(oAppPlugin, m.fileReceptor, oType) <> 0) Then

            #------------------------------------------------------------------#
            # Start the application:                                           #
            #------------------------------------------------------------------#
        ElseIf (oHost.oApp(oAppPlugin, wdApp) <> 0) Then

            #------------------------------------------------------------------#
            # Open the receptor document:                                      #
            #------------------------------------------------------------------#
        ElseIf (oHost.oDoc(oAppPlugin, m.fileReceptor, m.template, False, wdDoc) <> 0) Then
        Else
            #------------------------------------------------------------------#
            # Save the window title and activate the document if visible:      #
            #------------------------------------------------------------------#
            If (m.visible) Then
                m.activeWindow = wdDoc.Application.Caption
                '                m.activeWindow = wdApp.ActiveWindow.Caption
                m.hWnd = FindWindow("OpusApp", m.activeWindow)
                If (m.hWnd > 0) Then
                    SetForegroundWindow(m.hWnd)
                Else
                    m.hWnd = FindWindow("OpusApp", m.activeWindow & " - Word")
                    If (m.hWnd > 0) Then
                        SetForegroundWindow(m.hWnd)
                    End If
                End If
            End If

            #------------------------------------------------------------------#
            # See if the document is not to be checked on startup:             #
            #------------------------------------------------------------------#
            If (Not mf.checkOnStart) Then

                #--------------------------------------------------------------#
                # Try to get the reference document numbers:                   #
                #--------------------------------------------------------------#
            ElseIf (processDocumentData(False) <> 0) Then
            End If
        End If

        #----------------------------------------------------------------------#
        # Close the MS Word document if it was opened. Error display of        #
        # the application is performed by the error handler:                   #
        #----------------------------------------------------------------------#
        Try
            If (iErr <> 0) Then
            ElseIf (m.session) Then
            Else
                showOfficeApp()
            End If

        Catch e As Exception
            eH(_el.Fatal, _errorProcedure, _errorValue.applicationHandle, e.Message)
            Debug.Print(e.Message)
        End Try
        main = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: session                                                        #
    #                                                                          #
    # Description:                                                             #
    # Session manager.                                                         #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # cmd                   The session command to execute.                    #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Public Function session(ByVal cmd As String) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name

        #----------------------------------------------------------------------#
        # Clear any previous erros which must have been reported already:      #
        #----------------------------------------------------------------------#
        iErr = 0

        #----------------------------------------------------------------------#
        # Set all session commands to normal:                                  #
        #----------------------------------------------------------------------#
        dictParameters.Item("messenger.toolset.check") = _tool.normal
        dictParameters.Item("messenger.toolset.index") = _tool.normal
        dictParameters.Item("messenger.toolset.insert") = _tool.normal
        dictParameters.Item("messenger.toolset.lock") = _tool.normal
        dictParameters.Item("messenger.toolset.renumber") = _tool.normal
        dictParameters.Item("messenger.toolset.test") = _tool.normal
        dictParameters.Item("messenger.toolset.unlock") = _tool.normal
        dictParameters.Item("messenger.toolset.xml") = _tool.normal
        dictParameters.Item("messenger.toolset.quit") = _tool.normal

        #----------------------------------------------------------------------#
        # Process according to session command:                                #
        #----------------------------------------------------------------------#
        m.sessionCommand = cmd
        Select Case cmd
            #------------------------------------------------------------------#
            # Check document data integrity:                                   #
            #------------------------------------------------------------------#
            Case "check"
                iErr = processDocumentData(True)

            #------------------------------------------------------------------#
            # Tag number index at the end of the document:                     #
            #------------------------------------------------------------------#
            Case "index"
                iErr = indexRefs()

            #------------------------------------------------------------------#
            # Insert next reference tag number:                                #
            #------------------------------------------------------------------#
            Case "insert"
                iErr = insertRef()

            #------------------------------------------------------------------#
            # Lock tags by setting the lock document variable:                 #
            #------------------------------------------------------------------#
            Case "lock"
                setLock(True)

            #------------------------------------------------------------------#
            # Renumber requirement reference numbers sequentially:             #
            #------------------------------------------------------------------#
            Case "renumber"
                iErr = renumberRefs()

            #------------------------------------------------------------------#
            # Generate test script from document data:                         #
            #------------------------------------------------------------------#
            Case "test"
                iErr = processDocumentData(False)

            #------------------------------------------------------------------#
            # Run the test:                                                    #
            #------------------------------------------------------------------#
            Case "runTest"
                m.session = False

            #------------------------------------------------------------------#
            # Unlock tags by clearing the lock document variable:              #
            #------------------------------------------------------------------#
            Case "unlock"
                setLock(False)

            #------------------------------------------------------------------#
            # Get the document data as xml and send to focal point client:     #
            #------------------------------------------------------------------#
            Case "xml"
                iErr = processDocumentData(False)

            #------------------------------------------------------------------#
            # Quit the interactive editing session:                            #
            #------------------------------------------------------------------#
            Case "quit"
                m.session = False

                #--------------------------------------------------------------#
                # Other commands are not known:                                #
                #--------------------------------------------------------------#
            Case Else
                eH(_el.Fatal, _errorProcedure, _errorValue.sessionCmdUnknown, "", cmd)
        End Select

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        If (iErr <> 0) Then
            dictParameters.Item("messenger.toolset." & cmd) = _tool.fail
        Else
            dictParameters.Item("messenger.toolset." & cmd) = _tool.success
        End If
        session = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Subroutine: showOfficeApp                                                #
    #                                                                          #
    # Description:                                                             #
    # Show the office application at the end if any error. If no error         #
    # then save the document and close it if required.                         #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Sub showOfficeApp()
        #----------------------------------------------------------------------#
        # Show the office application:                                         #
        #----------------------------------------------------------------------#
        Try
            If (iErr <> 0) Then
                wdApp.Visible = True
            Else
                If (m.close And wdDoc IsNot Nothing) Then
                    If (m.save) Then
                        wdDoc.Close(True)
                    Else
                        wdDoc.Close(False)
                    End If
                End If

                If (wdApp IsNot Nothing) Then
                    If (wdApp.Documents.Count > 0) Then
                        wdApp.Visible = True
                    Else
                        wdApp.Quit()
                    End If
                End If
            End If

        Catch e As Exception
        End Try
    End Sub

    #--------------------------------------------------------------------------#
    # Little ditty to clean up cell text for conversion to XML:                #
    #--------------------------------------------------------------------------#
    Private Function CleanText(ByVal s As String) As String
        CleanText = Replace(s, vbCrLf, ",")
        CleanText = Replace(CleanText, vbCr, ",")
        CleanText = Replace(CleanText, vbLf, ",")
        CleanText = Replace(CleanText, vbTab, ",")
        CleanText = Replace(CleanText, "&", "+")
        CleanText = Replace(CleanText, Chr(7), "")
        CleanText = Replace(CleanText, Chr(11), "")
        CleanText = Replace(CleanText, "@", "__at__")
        CleanText = Replace(CleanText, Chr(1), "")
        CleanText = Replace(CleanText, "^", "(caret)")
        CleanText = Replace(CleanText, "=", "")
        CleanText = Replace(CleanText, "/", "")
        CleanText = Trim(CleanText)
    End Function

    #--------------------------------------------------------------------------#
    # Function: processDocumentData                                            #
    #                                                                          #
    # Description:                                                             #
    # Reads the document, verifies the data and gets it in XML format then */
    # sends it to the focal point client for conversion to JSON.               #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # getRefsOnly           True if should only get the list of unique         #
    #                       reference numbers so much faster as don't          #
    #                       check all document data or return XML.             #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Public Function processDocumentData(ByVal getRefsOnly As Boolean) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim i As Integer = 0
        Dim s As String = ""
        Dim tTable As Word.Table

        #----------------------------------------------------------------------#
        # Clear the dictionaries:                                              #
        #----------------------------------------------------------------------#
        dictParameterDefs.Clear()
        dictParameterTables.Clear()
        dictTags.Clear()
        dictUnique.Clear()

        #----------------------------------------------------------------------#
        # Initialise the XML file object handler and add a root node:          #
        #----------------------------------------------------------------------#
        mf.keyCount = 0
        If (getRefsOnly) Then
        Else
            Try
                dictParameters.Remove("messenger.output.XML")
                xmlDoc = New MSXML2.DOMDocument60
                objRoot = xmlDoc.createElement("root")
                objDocument = xmlDoc.createElement("document")
                objParameters = xmlDoc.createElement("parameters")
                objTables = xmlDoc.createElement("tables")

            Catch e As Exception
                eH(_el.Fatal, _errorProcedure, _errorValue.cannotCreateXML, e.Message)
                Debug.Print(e.Message)
            End Try
        End If

        #----------------------------------------------------------------------#
        # Loop through all the tables in the document's table collection:      #
        #----------------------------------------------------------------------#
        Try
            Debug.Print("Number of tables to process is " & wdDoc.Tables.Count)
            For Each tTable In wdDoc.Tables
                #--------------------------------------------------------------#
                # Check if the document prefix is already found:               #
                #--------------------------------------------------------------#
                i = i + 1
                tTable.ID = i
                If (getRefsOnly) Then
                ElseIf (docPrefix.Length > 0) Then
                    Debug.Print("Document prefix already found and is '" & docPrefix & "'")

                    #----------------------------------------------------------#
                    # Try to get the document information from this table: */
                    #----------------------------------------------------------#
                ElseIf (getDocumentInfo(tTable, getRefsOnly) <> 0) Then
                    Exit For
                End If
                Debug.Print("Document prefix is " & docPrefix)

                #--------------------------------------------------------------#
                # Try to find a table parameter definition:                    #
                #--------------------------------------------------------------#
                If (iErr <> 0) Then
                ElseIf (findTableParameters(tTable) <> 0) Then
                    Exit For
                End If

                #--------------------------------------------------------------#
                # Exit the loop if any error:                                  #
                #--------------------------------------------------------------#
                If (iErr <> 0) Then
                    Debug.Print("Exiting table traverse loop due to error " & iErr)
                    Exit For
                End If
            Next

            #------------------------------------------------------------------#
            # Check if any parameter tables found. Can't be a refDoc           #
            # without them:                                                    #
            #------------------------------------------------------------------#
            Debug.Print("Number of parameter tables is " & dictParameterTables.Count)
            If (dictParameterTables.Count > 0) Then
                #--------------------------------------------------------------#
                # Now have all table parameter data. Loop through all the      #
                # tables again, this time processing the data tables into      #
                # XML:                                                         #
                #--------------------------------------------------------------#
                For Each tTable In wdDoc.Tables
                    #----------------------------------------------------------#
                    # Add the document reference tables into the XML           #
                    # object:                                                  #
                    #----------------------------------------------------------#
                    If (getTableData(tTable, getRefsOnly) <> 0) Then
                        Exit For
                    End If
                Next

                #--------------------------------------------------------------#
                # Add the XML root node if any reference tables found:         #
                #--------------------------------------------------------------#
                If (iErr <> 0) Then
                ElseIf (getRefsOnly) Then
                Else
                    #----------------------------------------------------------#
                    # Replace any quotes with single quotes for JSON:          #
                    #----------------------------------------------------------#
                    objRoot.appendChild(objDocument)
                    objRoot.appendChild(objParameters)
                    objRoot.appendChild(objTables)
                    xmlDoc.appendChild(objRoot)
#?                    s = Replace(xmlDoc.xml, """", "'")
                    Debug.Print("Created XML: " & s)
                    dictParameters.Add("messenger.output.XML", s)
                End If
                If (iErr <> 0) Then
                Else
                    dictParameters.Item("messenger.toolset.insert") = _tool.normal
                End If
            End If

        Catch e As Exception
            eH(_el.Fatal, _errorProcedure, _errorValue.applicationHandle, e.Message)
            Debug.Print(e.Message)
        End Try

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        objRoot = Nothing
        processDocumentData = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: getDocumentInfo                                                #
    #                                                                          #
    # Description:                                                             #
    # Checks the table to see if the document information table and saves      #
    # the document info if it is.                                              #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # tTable                The table to check.                                #
    # getRefsOnly           True if should only get the reference numbers. */
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Function getDocumentInfo(ByRef tTable As Word.Table, ByVal getRefsOnly As Boolean) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim s As String = ""
        Dim sr As String = ""
        Dim d As dType = Nothing
        Dim objInfo As MSXML2.IXMLDOMNode = Nothing
        Dim objAttr As MSXML2.IXMLDOMAttribute = Nothing

        #----------------------------------------------------------------------#
        # Catch application specific exceptions:                               #
        #----------------------------------------------------------------------#
        Try
            #------------------------------------------------------------------#
            # Check if the table could be the document prefix table:           #
            #------------------------------------------------------------------#
            Debug.Print("Check if info table with " & tTable.Columns.Count & " columns and " & tTable.Rows.Count & " rows.")
            If (tTable.Columns.Count = NUM_COLS_INFO) Then
                #--------------------------------------------------------------#
                # Get the text from the first cell. Catch any merged cell      #
                # errors:                                                      #
                #--------------------------------------------------------------#
                Debug.Print("Could be prefix table...")
                sr = tTable.Cell(1, di.information).Range.Text
                s = Left(sr, Len(sr) - 2)
                sr = tTable.Cell(1, di.value).Range.Text
                s = s & Left(sr, Len(sr) - 2)
                sr = tTable.Cell(1, di.description).Range.Text
                s = s & Left(sr, Len(sr) - 2)

                #--------------------------------------------------------------#
                # Check if this is the document prefix table:                  #
                #--------------------------------------------------------------#
                If (UCase(s) = "INFORMATIONVALUEDESCRIPTION") Then
                    #----------------------------------------------------------#
                    # Enter a loop to process all the rows and add the         #
                    # document information to the global dictionary:           #
                    #----------------------------------------------------------#
                    For i = 2 To tTable.Rows.Count
                        sr = tTable.Cell(i, di.information).Range.Text
                        d.info = Left(sr, Len(sr) - 2)
                        sr = tTable.Cell(i, di.value).Range.Text
                        d.value = Left(sr, Len(sr) - 2)
                        sr = tTable.Cell(i, di.description).Range.Text
                        d.description = Left(sr, Len(sr) - 2)
                        dictDocumentDefs.Add(UCase(d.info), d)
                        If (iErr <> 0) Then
                            Exit For
                        ElseIf (getRefsOnly) Then
                        Else
                            objInfo = xmlDoc.createElement("information")
                            objInfo.text = d.value
                            objAttr = xmlDoc.createAttribute("name")
                            objInfo.attributes.setNamedItem(objAttr).text = d.info
                            objAttr = xmlDoc.createAttribute("description")
                            objInfo.attributes.setNamedItem(objAttr).text = d.description
                            objDocument.appendChild(objInfo)
                        End If

                        #------------------------------------------------------#
                        # Save the document prefix to flag the document        #
                        # information has been acquired:                       #
                        #------------------------------------------------------#
                        If (UCase(d.info) = "PREFIX") Then
                            docPrefix = d.info
                        End If
                    Next i

                    #----------------------------------------------------------#
                    # Add the file details:                                    #
                    #----------------------------------------------------------#
                    objInfo = xmlDoc.createElement("information")
                    objInfo.text = wdDoc.FullName
                    objAttr = xmlDoc.createAttribute("name")
                    objInfo.attributes.setNamedItem(objAttr).text = "Filename"
                    objAttr = xmlDoc.createAttribute("description")
                    objInfo.attributes.setNamedItem(objAttr).text = "File containing the table information"
                    objDocument.appendChild(objInfo)
                End If
            End If

            #------------------------------------------------------------------#
            # Most likely a merged cell exception. Ignore this table if so:*/
            #------------------------------------------------------------------#
        Catch e As Exception
            Debug.Print(e.Message)
            If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
            Else
                eH(_el.Fatal, _errorProcedure, _errorValue.cannotCreateXML, e.Message)
            End If
        End Try

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        getDocumentInfo = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: findTableParameters                                            #
    #                                                                          #
    # Description:                                                             #
    # Checks the table to see if it has the parameter definition for           #
    # another data table.                                                      #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # tTable                The table to check.                                #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Function findTableParameters(ByRef tTable As Word.Table) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim cntTCols As Integer
        Dim cntTRows As Integer
        Dim s As String = ""
        Dim sr As String = ""

        #----------------------------------------------------------------------#
        # Catch application specific exceptions:                               #
        #----------------------------------------------------------------------#
        Try
            #------------------------------------------------------------------#
            # Check if could be a parameter table:                             #
            #------------------------------------------------------------------#
            cntTRows = tTable.Rows.Count
            cntTCols = tTable.Columns.Count
            Debug.Print("Check if parameter table with " & cntTCols & " columns and " & cntTRows & " rows.")
            If (cntTCols = NUM_COLS_PARM And cntTRows >= 2) Then
                #--------------------------------------------------------------#
                # Get the text from the name column. Catch any merged cell */
                # errors:                                                      #
                #--------------------------------------------------------------#
                Debug.Print("Could be parameter table...")
                sr = tTable.Cell(1, pi.name).Range.Text
                s = Left(sr, Len(sr) - 2)
                sr = tTable.Cell(1, pi.description).Range.Text
                s = s & Left(sr, Len(sr) - 2)
                sr = tTable.Cell(1, pi.need).Range.Text
                s = s & Left(sr, Len(sr) - 2)
                sr = tTable.Cell(1, pi.view).Range.Text
                s = s & Left(sr, Len(sr) - 2)
                sr = tTable.Cell(1, pi.entry).Range.Text
                s = s & Left(sr, Len(sr) - 2)
                sr = tTable.Cell(1, pi.key).Range.Text
                s = s & Left(sr, Len(sr) - 2)

                #--------------------------------------------------------------#
                # Check if this is a parameter table:                          #
                #--------------------------------------------------------------#
                If (UCase(s) = "NAMEDESCRIPTIONNEEDVIEWENTRYKEY") Then
                    #----------------------------------------------------------#
                    # Enter a loop to process all the rows in the table:       #
                    #----------------------------------------------------------#
                    Debug.Print("Found parameter table.")
                    s = ""
                    For i = 2 To cntTRows
                        #------------------------------------------------------#
                        # Get the text from the name column. Ignore any        #
                        # merged cell errors:                                  #
                        #------------------------------------------------------#
                        sr = tTable.Cell(i, pi.name).Range.Text
                        s = s & Left(sr, Len(sr) - 2)
                    Next i
                    Debug.Print("Adding table " & tTable.ID & " heading " & s & " to tables dictionary.")
                    dictParameterTables.Add(s, tTable.ID)
                End If
            End If

            #------------------------------------------------------------------#
            # Most likely a merged cell exception. Ignore this table if so:*/
            #------------------------------------------------------------------#
        Catch e As Exception
            Debug.Print(e.Message)
            If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
            Else
                eH(_el.Fatal, _errorProcedure, _errorValue.cannotCreateXML, e.Message)
            End If
        End Try

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        findTableParameters = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: getTableData                                                   #
    #                                                                          #
    # Description:                                                             #
    # Checks the table to see if it is a data table and extracts the data. */
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # tTable                The table to check.                                #
    # getRefsOnly           True if should only get the reference numbers. */
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Function getTableData(ByRef dTable As Word.Table, ByVal getRefsOnly As Boolean) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim bFound As Boolean = False
        Dim isHeading As Boolean = False
        Dim i As Integer
        Dim cntTRows As Integer
        Dim iColPrimaryKey As Integer
        Dim iTableId As Integer
        Dim s As String = ""
        Dim sr As String = ""
        Dim sHeader As String = ""
        Dim pTable As Word.Table = Nothing
        Dim dRow As Word.Row
        Dim pair As KeyValuePair(Of String, Integer)
        Dim objTable As MSXML2.IXMLDOMNode = Nothing

        #----------------------------------------------------------------------#
        # Check if already processed this table if a parameter table:          #
        #----------------------------------------------------------------------#
        cntTRows = dTable.Rows.Count
        For Each pair In dictParameterTables
            If (dTable.ID = pair.Value) Then
                Debug.Print("Found parameter table ID " & pair.Value & ". Ignore it.")
                bFound = True
                Exit For
            End If
        Next

        #----------------------------------------------------------------------#
        # Check if a data table and has some data:                             #
        #----------------------------------------------------------------------#
        If (Not bFound And cntTRows >= 2) Then
            Try
                #--------------------------------------------------------------#
                # Get the heading text from the first row. Ignore any          #
                # merged cell errors:                                          #
                #--------------------------------------------------------------#
                dRow = dTable.Rows(1)
                Debug.Print("Processing table with " & dRow.Cells.Count & " cells in header and " & cntTRows & " rows.")
                For i = 1 To dRow.Cells.Count
                    'rTag = dRow.Cells(i).Range
                    'rTag.End = rTag.End - 1
                    'sHeader = sHeader & rTag.Text
                    sr = dRow.Cells(i).Range.Text
                    sHeader = sHeader & Left(sr, Len(sr) - 2)
                Next i
                Debug.Print("Processing table with heading row " & sHeader)

                #--------------------------------------------------------------#
                # Most likely number of table columns does not match first */
                # row number of cells. Ignore remaining columns:               #
                #--------------------------------------------------------------#
            Catch e As Exception
                Debug.Print(e.Message)
                If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
                Else
                    eH(_el.Fatal, _errorProcedure, _errorValue.cannotCreateXML, e.Message)
                End If
            End Try

            #------------------------------------------------------------------#
            # Try to get the matching parameters table ID:                     #
            #------------------------------------------------------------------#
            If (dictParameterTables.TryGetValue(sHeader, iTableId)) Then
                #--------------------------------------------------------------#
                # Found the matching data table parameters definition          #
                # table ID. Find the table in the document:                    #
                #--------------------------------------------------------------#
                bFound = False
                For Each pTable In wdDoc.Tables
                    #----------------------------------------------------------#
                    # Check if this is the matching parameters table:          #
                    #----------------------------------------------------------#
                    If (pTable.ID = iTableId) Then
                        bFound = True
                        Debug.Print("Found corresponding parameters table ID " & iTableId)
                        Exit For
                    End If
                Next

                #--------------------------------------------------------------#
                # Check if the matching parameter table was not found.         #
                # This is not a data table so nothing more to do:              #
                #--------------------------------------------------------------#
                If (Not bFound) Then
                    Debug.Print("No corresponding parameters table ID so not a data table. Ignore it.")

                    #----------------------------------------------------------#
                    # Read the data table parameter definition:                #
                    #----------------------------------------------------------#
                ElseIf (readParameters(pTable, getRefsOnly, iColPrimaryKey) <> 0) Then
                Else
                    #----------------------------------------------------------#
                    # Enter a loop to process all of the rows in the data      #
                    # table:                                                   #
                    #----------------------------------------------------------#
                    If (Not getRefsOnly) Then
                        objTable = xmlDoc.createElement("table")
                    End If
                    For i = 1 To cntTRows
                        #------------------------------------------------------#
                        # Don't verify the data in the header row:             #
                        #------------------------------------------------------#
                        If (i = 1) Then
                            isHeading = True
                        Else
                            isHeading = False
                        End If
                        Debug.Print("Processing row " & i & " of " & cntTRows)

                        #------------------------------------------------------#
                        # If only getting reference numbers then process       #
                        # the reference number column, ignoring the header:*/
                        #------------------------------------------------------#
                        If (getRefsOnly) Then
                            #--------------------------------------------------#
                            # Set the progress message based on command:       #
                            #--------------------------------------------------#
                            If (m.sessionCommand = "check") Then
                                s = "Verifying reference number data integrity in row " & i & " of " & cntTRows

                            ElseIf (m.sessionCommand = "index") Then
                                s = "Checking index reference number data integrity in row " & i & " of " & cntTRows

                            ElseIf (m.sessionCommand = "renumber") Then
                                s = "Renumbering reference number in row " & i & " of " & cntTRows
                            Else
                                s = "Verifying reference number data integrity in row " & i & " of " & cntTRows
                            End If

                            #--------------------------------------------------#
                            # Ignoring the header row, check reference         #
                            # numbers:                                         #
                            #--------------------------------------------------#
                            If (i = 1) Then
                            ElseIf (readRefRow(sHeader, dTable.Rows(i), iColPrimaryKey) <> 0) Then
                                Exit For
                                #----------------------------------------------#
                                # Update the status for the user every 10      #
                                # rows because hopefully very fast:            #
                                #----------------------------------------------#
                            ElseIf (i Mod 10 <> 0) Then
                            ElseIf (oHost.updateStatus(m._id, s, i / cntTRows, True) <> 0) Then
                                Exit For
                            End If

                            #--------------------------------------------------#
                            # Process the data row to get the XML:             #
                            #--------------------------------------------------#
                        ElseIf (readDataRow(sHeader, isHeading, dTable.Rows(1), dTable.Rows(i), objTable) <> 0) Then
                            Exit For
                        Else
                            #--------------------------------------------------#
                            # Set the progress message based on command:       #
                            #--------------------------------------------------#
                            If (m.sessionCommand = "test") Then
                                s = "Checking reference number in row " & i & " of " & cntTRows & " for testing"

                            ElseIf (m.sessionCommand = "xml") Then
                                s = "Verifying table data integrity in row " & i & " of " & cntTRows
                            Else
                                s = "Verifying table data integrity in row " & i & " of " & cntTRows
                            End If

                            #--------------------------------------------------#
                            # Update the status for the user every row:        #
                            #--------------------------------------------------#
                            If (oHost.updateStatus(m._id, s, i / cntTRows, True) <> 0) Then
                                Exit For
                            End If
                        End If

                        #------------------------------------------------------#
                        # Display status for all rows checked:                 #
                        #------------------------------------------------------#
                        If (iErr <> 0) Then
                        ElseIf (i < cntTRows) Then
                        Else
                            #--------------------------------------------------#
                            # Set the progress complete message:               #
                            #--------------------------------------------------#
                            If (oHost.updateStatus(m._id, "Table data integrity check complete", 1, True) <> 0) Then
                                Exit For
                            End If
                        End If
                    Next i
                    If (iErr <> 0) Then
                    ElseIf (Not getRefsOnly) Then
                        objTables.appendChild(objTable)
                    End If
                End If
            End If
        End If

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        getTableData = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: readParameters                                                 #
    #                                                                          #
    # Description:                                                             #
    # Scans through the table and reads in the parameter data and saves it */
    # in the global collection.                                                #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # pTable                The table to check.                                #
    # getRefsOnly           True if only getting primary key.                  #
    # iColPrimaryKey        The primary key column (cell) number.              #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Function readParameters(ByRef pTable As Word.Table,
                                    ByVal getRefsOnly As Boolean, ByRef iColPrimaryKey As Integer) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim i As Integer
        Dim cntPRows As Integer
        Dim s As String = ""
        Dim sr As String = ""
        Dim sHeader As String = ""
        Dim p As pType = Nothing
        Dim rTag As Word.Range
        Dim objParm As MSXML2.IXMLDOMNode = Nothing
        Dim objAttr As MSXML2.IXMLDOMAttribute = Nothing

        #----------------------------------------------------------------------#
        # Catch application specific exceptions:                               #
        #----------------------------------------------------------------------#
        dictParameterDefs.Clear()
        Try
            #------------------------------------------------------------------#
            # First enter a loop to build the table heading row from the       #
            # parameter names:                                                 #
            #------------------------------------------------------------------#
            cntPRows = pTable.Rows.Count
            For i = 2 To cntPRows
                #--------------------------------------------------------------#
                # Get the text from the name column. Catch any merged cell */
                # errors:                                                      #
                #--------------------------------------------------------------#
                sr = pTable.Cell(i, pi.name).Range.Text
                sHeader = sHeader & Left(sr, Len(sr) - 2)
            Next i

            #------------------------------------------------------------------#
            # Enter another loop to process all of the parameter rows in       #
            # the table:                                                       #
            #------------------------------------------------------------------#
            For i = 2 To cntPRows
                #--------------------------------------------------------------#
                # Get the text from the parameter table row:                   #
                #--------------------------------------------------------------#
                sr = pTable.Cell(i, pi.name).Range.Text
                p.name = Left(sr, Len(sr) - 2)

                #--------------------------------------------------------------#
                # Get the text from the description column. Catch any          #
                # merged cell errors:                                          #
                #--------------------------------------------------------------#
                sr = pTable.Cell(i, pi.description).Range.Text
                p.description = Left(sr, Len(sr) - 2)

                #--------------------------------------------------------------#
                # Get the required flag and return true or false:              #
                #--------------------------------------------------------------#
                sr = pTable.Cell(i, pi.need).Range.Text
                s = Left(sr, Len(sr) - 2)
                If (UCase(s) = "Y" Or UCase(s) = "YES") Then
                    p.need = True
                Else
                    p.need = False
                End If

                #--------------------------------------------------------------#
                # Get the display flag and return true or false:               #
                #--------------------------------------------------------------#
                sr = pTable.Cell(i, pi.view).Range.Text
                s = Left(sr, Len(sr) - 2)
                If (UCase(s) = "Y" Or UCase(s) = "YES") Then
                    p.view = True
                Else
                    p.view = False
                End If

                #--------------------------------------------------------------#
                # Get the parameter data type:                                 #
                #--------------------------------------------------------------#
                sr = pTable.Cell(i, pi.entry).Range.Text
                p.dataType = Left(sr, Len(sr) - 2)

                #--------------------------------------------------------------#
                # Get the parameter primary or foreign key type:               #
                #--------------------------------------------------------------#
                sr = pTable.Cell(i, pi.key).Range.Text
                s = Left(sr, Len(sr) - 2)

                #--------------------------------------------------------------#
                # Return a data key type if the cell is blank:                 #
                #--------------------------------------------------------------#
                If (Len(s) = 0) Then
                    p.keyType = "D"
                Else
                    #----------------------------------------------------------#
                    # Get the parameter key type:                              #
                    #----------------------------------------------------------#
                    p.keyType = s
                End If

                #--------------------------------------------------------------#
                # Save the primary key column number if the primary key:       #
                #--------------------------------------------------------------#
                If (p.keyType.ToUpper = "P") Then
                    iColPrimaryKey = i - 1
                End If

                #--------------------------------------------------------------#
                # Add the parameter to the parameter dictionary with the       #
                # key matching the column heading number (the parameter        #
                # table row order must match the column heading order of       #
                # the Data table):                                             #
                #--------------------------------------------------------------#
                Debug.Print("Read parameter definition for row " & i)
                dictParameterDefs.Add(sHeader & i - 1, p)

                #--------------------------------------------------------------#
                # Don't need to create XML if only getting reference           #
                # numbers:                                                     #
                #--------------------------------------------------------------#
                If (iErr <> 0) Then
                    Exit For
                ElseIf (getRefsOnly) Then
                Else
                    objParm = xmlDoc.createElement("parameter")
                    objParm.text = p.name
                    objAttr = xmlDoc.createAttribute("description")
                    objParm.attributes.setNamedItem(objAttr).text = p.description
                    objAttr = xmlDoc.createAttribute("need")
                    objParm.attributes.setNamedItem(objAttr).text = p.need
                    objAttr = xmlDoc.createAttribute("view")
                    objParm.attributes.setNamedItem(objAttr).text = p.view
                    objAttr = xmlDoc.createAttribute("dataType")
                    objParm.attributes.setNamedItem(objAttr).text = p.dataType
                    objAttr = xmlDoc.createAttribute("key")
                    objParm.attributes.setNamedItem(objAttr).text = p.keyType
                    objParameters.appendChild(objParm)
                End If
            Next i

            #------------------------------------------------------------------#
            # Most likely a merged cell exception. Ignore this table if so:*/
            #------------------------------------------------------------------#
        Catch e As Exception
            Debug.Print(e.Message)
            If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
            Else
                eH(_el.Fatal, _errorProcedure, _errorValue.cannotCreateXML, e.Message)
            End If
        End Try

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        rTag = Nothing
        pTable = Nothing
        readParameters = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: readDataRow                                                    #
    #                                                                          #
    # Description:                                                             #
    # Process the data in the current table row.                               #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # sHeader               The table heading concatenated string.             #
    # isHeading             If true then don't verify data values.             #
    # dHeaderRow            The data table row 1.                              #
    # dRow                  The data table row to process.                     #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Function readDataRow(ByVal sHeader As String, ByVal isHeading As Boolean,
                                 ByRef dHeaderRow As Word.Row, ByRef dRow As Word.Row,
                                 ByRef objTable As MSXML2.IXMLDOMNode) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim ignoreRow As Boolean = False
        Dim cntHCells As Integer
        Dim cntRCells As Integer
        Dim i As Integer
        Dim iRow As Integer
        Dim j As Integer
        Dim iHeaderCell As Integer
        Dim splitWidth As Single
        Dim bm As String = ""
        Dim s As String = ""
        Dim sr As String = ""
        Dim splitText As String = ""
        Dim rTag As Word.Range
        Dim objCell As MSXML2.IXMLDOMNode = Nothing
        Dim objRow As MSXML2.IXMLDOMNode = Nothing
        Dim objAttr As MSXML2.IXMLDOMAttribute = Nothing
        Dim p As pType = Nothing

        #----------------------------------------------------------------------#
        # Catch application specific exceptions:                               #
        #----------------------------------------------------------------------#
        Try
            #------------------------------------------------------------------#
            # Enter a loop to process all of the cells in the row:             #
            #------------------------------------------------------------------#
            iRow = dRow.Index
            cntHCells = dHeaderRow.Cells.Count
            cntRCells = dRow.Cells.Count
            objRow = xmlDoc.createElement("row")
            iHeaderCell = 1
            Debug.Print("Need to process " & dRow.Cells.Count & " cells.")
            For i = 1 To cntRCells
                #--------------------------------------------------------------#
                # Get the text from the cell. Ignore any merged cell           #
                # errors:                                                      #
                #--------------------------------------------------------------#
                j = 0
                'rTag = dRow.Cells(i).Range
                'rTag.End = rTag.End - 1
                's = rTag.Text
                sr = dRow.Cells(i).Range.Text
                s = Left(sr, Len(sr) - 2)

                #--------------------------------------------------------------#
                # Get the matching parameter definition. First cell must       #
                # be first:                                                    #
                #--------------------------------------------------------------#
                If (i = 1) Then
                    iHeaderCell = 1
                    Debug.Print("First cell on row " & CType(iRow, String))

                    #----------------------------------------------------------#
                    # Last cell must be last:                                  #
                    #----------------------------------------------------------#
                ElseIf (i = cntRCells) Then
                    iHeaderCell = cntHCells
                    Debug.Print("Last cell on row " & CType(iRow, String))

                    #----------------------------------------------------------#
                    # Rows with the same number of cells must match:           #
                    #----------------------------------------------------------#
                ElseIf (cntRCells = cntHCells) Then
                    iHeaderCell = i
                    Debug.Print("Matching row " & CType(iRow, String))

                    #----------------------------------------------------------#
                    # Rows with the same width cells probably match:           #
                    #----------------------------------------------------------#
                ElseIf (dRow.Cells(i).Width = dHeaderRow.Cells(iHeaderCell).Width) Then
                    iHeaderCell = i
                    Debug.Print("Cell " & i & " width matches on row " & CType(iRow, String))

                    #----------------------------------------------------------#
                    # Merged cells are not allowed:                            #
                    #----------------------------------------------------------#
                ElseIf (cntRCells < cntHCells) Then
                    Debug.Print("Merged cells on row " & CType(iRow, String))
                    eH(_el.Fatal, _errorProcedure, _errorValue.noMergedCells, "")
                    Exit For
                Else
                    #----------------------------------------------------------#
                    # This row containts split cells. Enter a loop to          #
                    # check how many cells are split:                          #
                    #----------------------------------------------------------#
                    Debug.Print(cntRCells & " split cells on row " & CType(iRow, String) & " and now looking at cell " & CType(i, String))
                    splitText = s
                    splitWidth = dRow.Cells(i).Width
                    For j = i + 1 To cntRCells
                        #------------------------------------------------------#
                        # Get the text from the next cell:                     #
                        #------------------------------------------------------#
                        'rTag = dRow.Cells(j).Range
                        'rTag.End = rTag.End - 1
                        's = rTag.Text
                        sr = dRow.Cells(j).Range.Text
                        s = Left(sr, Len(sr) - 2)
                        splitText = splitText + ", " + s

                        #------------------------------------------------------#
                        # Check if that is the extent of split:                #
                        #------------------------------------------------------#
                        splitWidth = splitWidth + dRow.Cells(j).Width
                        If (splitWidth >= dHeaderRow.Cells(iHeaderCell).Width) Then
                            #--------------------------------------------------#
                            # Found the extent of the split. Combine the       #
                            # cell values:                                     #
                            #--------------------------------------------------#
                            s = splitText

                            #--------------------------------------------------#
                            # Increment the outer loop counter (not good       #
                            # practice):                                       #
                            #--------------------------------------------------#
                            i = j
                            Exit For
                        End If
                    Next j
                End If
                p = dictParameterDefs.Item(sHeader & CType(iHeaderCell, String))
                Debug.Print("Retrieved parameter definition for " & sHeader & CType(iHeaderCell, String))
                p.value = s

                #--------------------------------------------------------------#
                # Ignore any table headings in the first row:                  #
                #--------------------------------------------------------------#
                If (iErr <> 0) Then
                    Exit For
                ElseIf (isHeading) Then

                    #----------------------------------------------------------#
                    # Verify the cell data:                                    #
                    #----------------------------------------------------------#
                ElseIf (verifyCellValue(p) <> 0) Then
                    dRow.Cells(i).Range.Shading.BackgroundPatternColor = Word.WdColor.wdColorPink
                    Exit For

                    #----------------------------------------------------------#
                    # Verify the data index if a primary or unique key:        #
                    #----------------------------------------------------------#
                ElseIf (verifyCellIndex(p, ignoreRow) <> 0) Then
                    dRow.Cells(i).Range.Shading.BackgroundPatternColor = Word.WdColor.wdColorPink
                    Exit For

                    #----------------------------------------------------------#
                    # Check if this is the primary key and renumbering or      #
                    # need a bookmark for the index:                           #
                    #----------------------------------------------------------#
                ElseIf (UCase(p.keyType) = "P" And
                        (m.sessionCommand = "renumber" Or m.sessionCommand = "index")) Then
                    #----------------------------------------------------------#
                    # Set the tag range:                                       #
                    #----------------------------------------------------------#
                    rTag = dRow.Cells(i).Range
                    rTag.End = rTag.End - 1

                    #----------------------------------------------------------#
                    # Update the tag value if renumbering:                     #
                    #----------------------------------------------------------#
                    If (m.sessionCommand = "renumber") Then
                        rTag.Text = p.value
                    End If

                    #----------------------------------------------------------#
                    # Drop a bookmark to mark the start of the tag index:      #
                    #----------------------------------------------------------#
                    If (m.sessionCommand = "index") Then
                        With wdDoc.Bookmarks
                            bm = "bm" & Replace(p.value, "!", "_")
                            bm = Replace(bm, "|", "_")
                            Debug.Print(bm)
                            .Add(Name:=bm, Range:=rTag)
                            .DefaultSorting = Word.WdBookmarkSortBy.wdSortByName
                            .ShowHidden = True
                        End With
                    End If
                End If

                #--------------------------------------------------------------#
                # Exit the loop if the row should be ignored if the            #
                # primary key is blank and allowed to be:                      #
                #--------------------------------------------------------------#
                If (iErr <> 0) Then
                    Exit For

                    #----------------------------------------------------------#
                    # Abort this row if primary key is blank or if just        #
                    # getting the primary keys for a session:                  #
                    #----------------------------------------------------------#
                ElseIf (ignoreRow) Then
                    Exit For
                Else
                    #----------------------------------------------------------#
                    # Add the cell data to the xml object:                     #
                    #----------------------------------------------------------#
                    objCell = xmlDoc.createElement("cell")
                    objCell.text = p.value
                    objAttr = xmlDoc.createAttribute("need")
                    objCell.attributes.setNamedItem(objAttr).text = p.need
                    objAttr = xmlDoc.createAttribute("view")
                    objCell.attributes.setNamedItem(objAttr).text = p.view
                    objAttr = xmlDoc.createAttribute("entry")
                    objCell.attributes.setNamedItem(objAttr).text = p.dataType
                    objAttr = xmlDoc.createAttribute("key")
                    objCell.attributes.setNamedItem(objAttr).text = p.keyType
                    objRow.appendChild(objCell)
                End If
                If (j <> 0) Then
                    Debug.Print("Read data table cell " & CType(iHeaderCell, String) & " with data row cell range " & CType(iHeaderCell, String) & " to " & j)
                Else
                    Debug.Print("Read data table cell " & CType(iHeaderCell, String))
                End If
                iHeaderCell = iHeaderCell + 1
            Next i

            #------------------------------------------------------------------#
            # Add the XML node for the row if the not ignoring it:             #
            #------------------------------------------------------------------#
            If (iErr <> 0) Then
            ElseIf (Not ignoreRow) Then
                objTable.appendChild(objRow)
            End If

            #------------------------------------------------------------------#
            # Most likely a merged cell exception. Ignore this table if so:*/
            #------------------------------------------------------------------#
        Catch e As Exception
            Debug.Print(e.Message)
            If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
            Else
                eH(_el.Fatal, _errorProcedure, _errorValue.cannotCreateXML, e.Message)
            End If
        End Try

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        rTag = Nothing
        objCell = Nothing
        readDataRow = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: readRefRow                                                     #
    #                                                                          #
    # Description:                                                             #
    # Process the reference number in the current table row.                   #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # sHeader               The table heading concatenated string.             #
    # dRow                  The data table row to process.                     #
    # iColPrimaryKey        The primary key column (cell) number.              #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Function readRefRow(ByVal sHeader As String, ByRef dRow As Word.Row, ByVal iColPrimaryKey As Integer) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim ignoreRow As Boolean = False
        Dim bm As String = ""
        Dim s As String = ""
        Dim sr As String = ""
        Dim rTag As Word.Range
        Dim p As pType = Nothing

        #----------------------------------------------------------------------#
        # Catch application specific exceptions:                               #
        #----------------------------------------------------------------------#
        Try
            #------------------------------------------------------------------#
            # Get the text from the primary key cell:                          #
            #------------------------------------------------------------------#
            sr = dRow.Cells(iColPrimaryKey).Range.Text
            s = Left(sr, Len(sr) - 2)

            p = dictParameterDefs.Item(sHeader & CType(iColPrimaryKey, String))
            Debug.Print("Retrieved parameter definition for " & sHeader & CType(iColPrimaryKey, String))
            p.value = s

            #------------------------------------------------------------------#
            # Verify the cell data:                                            #
            #------------------------------------------------------------------#
            If (verifyCellValue(p) <> 0) Then
                dRow.Cells(iColPrimaryKey).Range.Shading.BackgroundPatternColor = Word.WdColor.wdColorPink

                #--------------------------------------------------------------#
                # Verify the data index if a primary or unique key:            #
                #--------------------------------------------------------------#
            ElseIf (verifyCellIndex(p, ignoreRow) <> 0) Then
                dRow.Cells(iColPrimaryKey).Range.Shading.BackgroundPatternColor = Word.WdColor.wdColorPink

                #--------------------------------------------------------------#
                # Check if this is the primary key and renumbering or          #
                # need a bookmark for the index:                               #
                #--------------------------------------------------------------#
            ElseIf (m.sessionCommand = "renumber" Or m.sessionCommand = "index") Then
                #--------------------------------------------------------------#
                # Set the tag range:                                           #
                #--------------------------------------------------------------#
                rTag = dRow.Cells(iColPrimaryKey).Range
                rTag.End = rTag.End - 1

                #--------------------------------------------------------------#
                # Update the tag value if renumbering as it was updated        #
                # in verifyCellIndex:                                          #
                #--------------------------------------------------------------#
                If (m.sessionCommand = "renumber") Then
                    rTag.Text = p.value
                End If

                #--------------------------------------------------------------#
                # Drop a bookmark to mark the start of the tag index:          #
                #--------------------------------------------------------------#
                If (m.sessionCommand = "index") Then
                    With wdDoc.Bookmarks
                        bm = "bm" & Replace(p.value, "!", "_")
                        bm = Replace(bm, "|", "_")
                        Debug.Print(bm)
                        .Add(Name:=bm, Range:=rTag)
                        .DefaultSorting = Word.WdBookmarkSortBy.wdSortByName
                        .ShowHidden = True
                    End With
                End If
            End If

            #------------------------------------------------------------------#
            # Most likely a merged cell exception. Ignore this table if so:*/
            #------------------------------------------------------------------#
        Catch e As Exception
            Debug.Print(e.Message)
            If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
            Else
                eH(_el.Fatal, _errorProcedure, _errorValue.cannotCreateXML, e.Message)
            End If
        End Try

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        rTag = Nothing
        readRefRow = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: verifyCellIndex                                                #
    #                                                                          #
    # Description:                                                             #
    # Confirms the table cell value is unique if primary key or unique key */
    # data types.                                                              #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # p                     The parameter type structure.                      #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # ignoreRow             True if there is no primary key in which case      #
    #                       the row should be ignored if ignoring blanks.      #
    #--------------------------------------------------------------------------#
    Private Function verifyCellIndex(ByRef p As pType, ByRef ignoreRow As Boolean) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name

        #----------------------------------------------------------------------#
        # Check if a primary key:                                              #
        #----------------------------------------------------------------------#
        Debug.Print("verifyCellIndex")
        If (UCase(p.keyType) = "P") Then
            #------------------------------------------------------------------#
            # Check if blank and not needed:                                   #
            #------------------------------------------------------------------#
            If (Not p.need And p.value.Length = 0) Then
                #--------------------------------------------------------------#
                # Primary key on this row is blank. Ignore it if required: */
                #--------------------------------------------------------------#
                If (mf.ignoreBlanks) Then
                    ignoreRow = True
                Else
                    ignoreRow = False
                End If

                #--------------------------------------------------------------#
                # Value is blank but is needed:                                #
                #--------------------------------------------------------------#
            ElseIf (p.value.Length = 0) Then
                eH(_el.Fatal, _errorProcedure, _errorValue.docParmInvalid, "", p.name, p.value, p.dataType, wdDoc.FullName)
            Else
                #--------------------------------------------------------------#
                # Use sequential number if renumbering:                        #
                #--------------------------------------------------------------#
                If (m.sessionCommand = "renumber") Then
                    mf.keyCount = mf.keyCount + 1
                    p.keySeries = mf.keyCount
                    p.value = p.keyPrefix & p.keySeries
                End If

                #--------------------------------------------------------------#
                # Get the value and add it to the tag dictionary:              #
                #--------------------------------------------------------------#
                Try
                    Debug.Print("Adding tag dictionary value " & p.value)
                    dictTags.Add(p.keySeries, p)

                Catch e As Exception
                    Debug.Print(e.Message)
                    eH(_el.Fatal, _errorProcedure, _errorValue.duplicateTag, e.Message, p.value, p.name, p.keyType, wdDoc.FullName, p.keySeries, p.keyPrefix)
                End Try
            End If

            #------------------------------------------------------------------#
            # Check if a unique key:                                           #
            #------------------------------------------------------------------#
        ElseIf (UCase(p.keyType = "U")) Then
            #------------------------------------------------------------------#
            # Check if blank and not needed:                                   #
            #------------------------------------------------------------------#
            If (Not p.need And p.value.Length = 0) Then

                #--------------------------------------------------------------#
                # Value is blank but is needed:                                #
                #--------------------------------------------------------------#
            ElseIf (p.value.Length = 0) Then
                eH(_el.Fatal, _errorProcedure, _errorValue.docParmInvalid, "", p.name, p.value, p.dataType, wdDoc.FullName)
            Else
                #--------------------------------------------------------------#
                # Get the value and add it to the unique field dictionary: */
                #--------------------------------------------------------------#
                Try
                    Debug.Print("Adding unique field dictionary value " & p.value)
                    dictUnique.Add(p.value, p)

                Catch e As Exception
                    Debug.Print(e.Message)
                    eH(_el.Fatal, _errorProcedure, _errorValue.duplicateTag, e.Message, p.value, p.name, p.keyType, wdDoc.FullName, p.keySeries, p.keyPrefix)
                End Try
            End If
        End If

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        verifyCellIndex = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: verifyCellValue                                                #
    #                                                                          #
    # Description:                                                             #
    # Confirms the table cell value complies with its specified type.          #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # p                     The parameter type structure.                      #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Function verifyCellValue(ByRef p As pType) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name

        #----------------------------------------------------------------------#
        # Make sure the parameter value conforms with its data type:           #
        #----------------------------------------------------------------------#
        Debug.Print("verifyCellValue")
        Select Case UCase(p.dataType)
            #------------------------------------------------------------------#
            # Boolean:                                                         #
            #------------------------------------------------------------------#
            Case "BOOLEAN"
                If (Not p.need And p.value.Length = 0) Then
                ElseIf (p.value.Length = 0) Then
                    eH(_el.Fatal, _errorProcedure, _errorValue.docParmRequired, "", p.name, p.dataType, wdDoc.FullName)

                ElseIf (UCase(p.value) <> "FALSE" And UCase(p.value) <> "TRUE" And
                        UCase(p.value) <> "YES" And UCase(p.value) <> "NO" And
                        UCase(p.value) <> "Y" And UCase(p.value) <> "N") Then
                    eH(_el.Fatal, _errorProcedure, _errorValue.docParmInvalid, "", p.name, p.value, p.dataType, wdDoc.FullName)
                End If

            #------------------------------------------------------------------#
            # Can't check file exists because don't know which path:           #
            #------------------------------------------------------------------#
            Case "FILE", "TEXT"
                If (Not p.need And p.value.Length = 0) Then
                ElseIf (p.value.Length = 0) Then
                    eH(_el.Fatal, _errorProcedure, _errorValue.docParmRequired, "", p.name, p.dataType, wdDoc.FullName)
                Else
                    p.keyPrefix = p.value

                    If (UCase(p.keyType) = "P") Then
                        mf.keyCount = mf.keyCount + 1
                        p.keySeries = mf.keyCount
                    End If
                End If

            #------------------------------------------------------------------#
            # Number:                                                          #
            #------------------------------------------------------------------#
            Case "NUMBER"
                If (Not p.need And p.value.Length = 0) Then
                ElseIf (p.value.Length = 0) Then
                    eH(_el.Fatal, _errorProcedure, _errorValue.docParmRequired, "", p.name, p.dataType, wdDoc.FullName)

                ElseIf (Not IsNumeric(p.value)) Then
                    eH(_el.Fatal, _errorProcedure, _errorValue.docParmInvalid, "", p.name, p.value, p.dataType, wdDoc.FullName)

                ElseIf (UCase(p.keyType) = "P") Then
                    p.keySeries = CType(p.value, Integer)
                End If

                #--------------------------------------------------------------#
                # Specific entry type:                                         #
                #--------------------------------------------------------------#
            Case Else
                #--------------------------------------------------------------#
                # Check if no type specified:                                  #
                #--------------------------------------------------------------#
                If (Not p.need And p.value.Length = 0) Then
                ElseIf (p.value.Length = 0) Then
                    eH(_el.Fatal, _errorProcedure, _errorValue.docParmRequired, "", p.name, p.dataType, wdDoc.FullName)

                ElseIf (p.dataType.Length = 0) Then
                    eH(_el.Fatal, _errorProcedure, _errorValue.docParmDataTypeInvalid, "", p.name, p.value, wdDoc.FullName)

                    #----------------------------------------------------------#
                    # Check if the value matches it's specific entry mask: */
                    #----------------------------------------------------------#
                ElseIf (VerifyMaskValue(p) <> 0) Then
                End If
        End Select

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        verifyCellValue = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: VerifyMaskValue                                                #
    #                                                                          #
    # Description:                                                             #
    # Confirms the parameter value complies with its specific mask.            #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # p                     The parameter type structure.                      #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Function VerifyMaskValue(ByRef p As pType) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim i As Integer
        Dim iNumMatches As Integer
        Dim iNumValues As Integer
        Dim j As Integer
        'Dim k As Integer
        Dim sPat As String
        'Dim sPrefix As String
        'Dim sPrefix1 As String
        Dim sPrefixPat As String
        Dim sPrefixVal As String
        Dim sVal As String
        Dim sValVal As String
        Dim bMatch(1) As Boolean
        Dim sDataPattern() As String
        Dim sDataValue() As String
        'Dim sPrefixPart() As String
        'Dim sRefPart() As String

        #----------------------------------------------------------------------#
        # Get the array of allowable values if more than one:                  #
        #----------------------------------------------------------------------#
        sDataPattern = Split(p.dataType, ",")
        If (InStr(1, p.value, vbCr) > 0) Then
            sDataValue = Split(p.value, vbCr)

        ElseIf (InStr(1, p.value, vbCrLf) > 0) Then
            sDataValue = Split(p.value, vbCrLf)

        ElseIf (InStr(1, p.value, ",") > 0) Then
            sDataValue = Split(p.value, ",")
        Else
            ReDim sDataValue(0)
            sDataValue(0) = p.value
        End If
        iNumValues = UBound(sDataValue) + 1
        iNumMatches = 0

        #----------------------------------------------------------------------#
        # Enter a loop to check for a matching value:                          #
        #----------------------------------------------------------------------#
        For i = 0 To UBound(sDataValue)
            #------------------------------------------------------------------#
            # Enter another loop to check for each pattern:                    #
            #------------------------------------------------------------------#
            For j = 0 To UBound(sDataPattern)
                #--------------------------------------------------------------#
                # Check if a simple list item match:                           #
                #--------------------------------------------------------------#
                sVal = Trim(sDataValue(i))
                sPat = Trim(sDataPattern(j))
                If (UCase(sVal) = UCase(sPat)) Then
                    iNumMatches = iNumMatches + 1
                    p.keyPrefix = sVal
                    If (IsNumeric(sVal)) Then
                        p.keySeries = CType(sVal, Integer)
                    End If

                    #----------------------------------------------------------#
                    # Check if a simple reference tag type Un:                 #
                    #----------------------------------------------------------#
                ElseIf (Mid(sPat, Len(sPat), 1) = "n") Then
                    sPrefixPat = Left(sPat, Len(sPat) - 1)
                    sPrefixVal = Left(sVal, Len(sPrefixPat))
                    sValVal = Right(sVal, Len(sVal) - Len(sPrefixVal))
                    If (UCase(sPrefixVal) = UCase(sPrefixPat) And IsNumeric(sValVal)) Then
                        iNumMatches = iNumMatches + 1
                        p.keyPrefix = sPrefixVal
                        If (IsNumeric(sValVal)) Then
                            p.keySeries = CType(sValVal, Integer)
                        End If
                    End If

                    #----------------------------------------------------------#
                    # Check if an MS Word section number reference tag         #
                    # Type Ur:                                                 #
                    #----------------------------------------------------------#
                ElseIf (Mid(sPat, Len(sPat), 1) = "r") Then
                    sPrefixPat = Left(sPat, Len(sPat) - 1)
                    sPrefixVal = Left(sVal, Len(sPrefixPat))
                    sValVal = Right(sVal, Len(sVal) - Len(sPrefixVal))
                    If (UCase(sPrefixVal) = UCase(sPrefixPat)) Then
                        iNumMatches = iNumMatches + 1
                        p.keyPrefix = sPrefixVal
                        If (IsNumeric(sValVal)) Then
                            p.keySeries = CType(sValVal, Integer)
                        End If
                    End If
                    'Else
                    '    #----------------------------------------------------------#
                    '    # Check if a container reference tag type Dm|Rn. Get       #
                    '    # the parent document container and the reference          #
                    '    # number:                                                  #
                    '    #----------------------------------------------------------#
                    '    sPrefixPart = Split(sPat, "|")
                    '    sRefPart = Split(sVal, "|")

                    '    #----------------------------------------------------------#
                    '    # Check if not valid container references:                 #
                    '    #----------------------------------------------------------#
                    '    If (UBound(sPrefixPart) <> 1 Or UBound(sRefPart) <> 1) Then
                    '    Else
                    '        #------------------------------------------------------#
                    '        # Check if valid container references:                 #
                    '        #------------------------------------------------------#
                    '        For k = 0 To 1
                    '            bMatch(k) = False
                    '            If (Mid(sPrefixPart(k), Len(sPrefixPart(k)), 1) <> "n") Then
                    '            Else
                    '                sPrefix = Left(sPrefixPart(k), Len(sPrefixPart(k)) - 1)
                    '                sPrefix1 = Left(sRefPart(k), Len(sPrefix))
                    '                If (sPrefix <> sPrefix1) Then
                    '                ElseIf (Not IsNumeric(Right(sRefPart(k), Len(sRefPart(k)) - Len(sPrefix1)))) Then
                    '                Else
                    '                    bMatch(k) = True
                    '                End If
                    '            End If
                    '        Next k
                    '        If (bMatch(0) And bMatch(1)) Then
                    '            iNumMatches = iNumMatches + 1
                    '        End If
                    '    End If
                End If
            Next j
        Next i

        #----------------------------------------------------------------------#
        # Throw an error if the parameter value is not one of the allowed      #
        # values:                                                              #
        #----------------------------------------------------------------------#
        If (iNumMatches <> iNumValues) Then
            eH(_el.Fatal, _errorProcedure, _errorValue.docParmInvalid, "", p.name, p.value, p.dataType, wdDoc.FullName)
        End If

        #----------------------------------------------------------------------#
        # Return completion status:                                            #
        #----------------------------------------------------------------------#
        VerifyMaskValue = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: insertRef                                                      #
    #                                                                          #
    # Description:                                                             #
    # Session command to insert a new reference number.                        #
    #                                                                          #
    # All code is encapsulated in a try-catch to detect any automation         #
    # error in case user renders the Word application and document             #
    # inaccessible, for example by closing the document.                       #
    #--------------------------------------------------------------------------#
    Private Function insertRef() As Long
        #----------------------------------------------------------------------#
        # Declare the procedure name and local variables:                      #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim bm As String = ""
        Dim keys As List(Of Integer)
        'Dim rTag As Word.Range

        #----------------------------------------------------------------------#
        # Get the list of keys and sort them reversed:                         #
        #----------------------------------------------------------------------#
        keys = dictTags.Keys.ToList
        keys.Sort()
        keys.Reverse()

        #----------------------------------------------------------------------#
        # Output the next tag number:                                          #
        #----------------------------------------------------------------------#
        Try
            Dim p As New pType
            p = dictTags.Item(keys(0))
            p.keySeries = p.keySeries + 1
            p.value = p.keyPrefix + p.keySeries.ToString
            dictTags.Add(p.keySeries, p)
            wdApp.Selection.Range.InsertAfter(p.value)

            #------------------------------------------------------------------#
            # Get the range of the new tag entry:                              #
            #------------------------------------------------------------------#
            'rTag = wdApp.Selection.Cells(1).Range
            'rTag.End = rTag.End - 1

            #------------------------------------------------------------------#
            # Drop a bookmark for the new tag:                                 #
            #------------------------------------------------------------------#
            'With wdDoc.Bookmarks
            '    bm = "bm" & Replace(p.value, "!", "_")
            '    bm = Replace(bm, "|", "_")
            '    .Add(Name:=bm, Range:=rTag)
            '    .DefaultSorting = Word.WdBookmarkSortBy.wdSortByName
            '    .ShowHidden = True
            'End With

            #------------------------------------------------------------------#
            # Exit if the connection to the Word document is lost:             #
            #------------------------------------------------------------------#
        Catch e As Exception
            Console.WriteLine(e.Message & "\r\n")
            If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
                m.session = False
            Else
                eH(_el.Fatal, _errorProcedure, _errorValue.sessionException, e.Message, "insert")
            End If
        End Try

        insertRef = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: indexRefs                                                      #
    #                                                                          #
    # Description:                                                             #
    # Session command to insert a reference number index at the end of the */
    # document.                                                                #
    #                                                                          #
    # All code is encapsulated in a try-catch to detect any automation         #
    # error in case user renders the Word application and document             #
    # inaccessible, for example by closing the document.                       #
    #--------------------------------------------------------------------------#
    Private Function indexRefs() As Long
        #----------------------------------------------------------------------#
        # Declare the procedure name:                                          #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim bm As String = ""
        Dim s As String = ""
        Dim num As Integer
        Dim keys As List(Of Integer)
        Dim rRange As Word.Range

        #----------------------------------------------------------------------#
        # Get the list of keys and sort them reversed:                         #
        #----------------------------------------------------------------------#
        keys = dictTags.Keys.ToList
        keys.Sort()

        #----------------------------------------------------------------------#
        # Check the tag numbers and drop index bookmarks:                      #
        #----------------------------------------------------------------------#
        If (processDocumentData(True) <> 0) Then

            #------------------------------------------------------------------#
            # Create the tag index style:                                      #
            #------------------------------------------------------------------#
        ElseIf (createIndexStyle() <> 0) Then
        Else
            #------------------------------------------------------------------#
            # Delete any previous tag index if there is one:                   #
            #------------------------------------------------------------------#
            Try
                rRange = wdDoc.Range(Start:=wdDoc.Bookmarks("beginTagIndex").Range.Start,
                                     End:=wdDoc.Bookmarks("endTagIndex").Range.End)
                rRange.Delete()
                wdDoc.Bookmarks("beginTagIndex").Delete()
                wdDoc.Bookmarks("endTagIndex").Delete()

                #--------------------------------------------------------------#
                # Just continue if no existing index:                          #
                #--------------------------------------------------------------#
            Catch e As Exception
                If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
                    #----------------------------------------------------------#
                    # No existing index. Insert a page break at the end of */
                    # the document:                                            #
                    #----------------------------------------------------------#
                    wdApp.Selection.EndKey(Word.WdUnits.wdStory, Word.WdMovementType.wdMove)
                    wdDoc.Application.Selection.InsertBreak(Type:=Word.WdBreakType.wdPageBreak)
                Else
                    eH(_el.Fatal, _errorProcedure, _errorValue.sessionException, e.Message, "insert")
                End If
            End Try

            Try
                #--------------------------------------------------------------#
                # Go to the end of the document:                               #
                #--------------------------------------------------------------#
                wdApp.Selection.EndKey(Word.WdUnits.wdStory, Word.WdMovementType.wdMove)

                #--------------------------------------------------------------#
                # Drop a bookmark to mark the start of the tag index:          #
                #--------------------------------------------------------------#
                With wdDoc.Bookmarks
                    .Add(Name:="beginTagIndex", Range:=wdDoc.Application.Selection.Range)
                    .DefaultSorting = Word.WdBookmarkSortBy.wdSortByName
                    .ShowHidden = True
                End With

                #--------------------------------------------------------------#
                # Add the tag index heading at the end of the document:        #
                #--------------------------------------------------------------#
                wdDoc.Application.Selection.Style = wdDoc.Styles("Heading 1")
                wdDoc.Application.Selection.TypeText(Text:="Tag Index")
                wdDoc.Application.Selection.TypeParagraph()
                wdDoc.Application.Selection.Style = wdDoc.Styles("TagIndex")

                #--------------------------------------------------------------#
                # Add the tag index data:                                      #
                #--------------------------------------------------------------#
                For Each num In keys
                    s = dictTags.Item(num).value
                    bm = "bm" & Replace(s, "!", "_")
                    bm = Replace(bm, "|", "_")
                    wdDoc.Range.InsertAfter(s & vbTab)
                    wdApp.Selection.EndKey(Word.WdUnits.wdStory, Word.WdMovementType.wdMove)
                    wdApp.Selection.InsertCrossReference(ReferenceType:=Word.WdReferenceType.wdRefTypeBookmark, ReferenceKind:=Word.WdReferenceKind.wdPageNumber, ReferenceItem:=bm, InsertAsHyperlink:=True, IncludePosition:=False, SeparateNumbers:=False, SeparatorString:=" ")
                    wdDoc.Range.InsertAfter(vbCrLf)
                Next

                #--------------------------------------------------------------#
                # Drop a bookmark to mark the end of the tag index:            #
                #--------------------------------------------------------------#
                With wdDoc.Bookmarks
                    .Add(Name:="endTagIndex", Range:=wdDoc.Application.Selection.Range)
                    .DefaultSorting = Word.WdBookmarkSortBy.wdSortByName
                    .ShowHidden = True
                End With

                #--------------------------------------------------------------#
                # Exit if the connection to the Word document is lost:         #
                #--------------------------------------------------------------#
            Catch e As Exception
                Console.WriteLine(e.Message & "\r\n")
                If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
                    m.session = False
                Else
                    eH(_el.Fatal, _errorProcedure, _errorValue.sessionException, e.Message, "insert")
                End If
            End Try
        End If

        indexRefs = iErr
    End Function

    Private Function createIndexStyle() As Long
        #----------------------------------------------------------------------#
        # Declare the procedure name:                                          #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim hasStyle As Boolean = "false"
        Dim tiStyle As Word.Style

        #----------------------------------------------------------------------#
        # Check if the TagIndex style already exists:                          #
        #----------------------------------------------------------------------#
        Try
            tiStyle = wdDoc.Styles("TagIndex")
            hasStyle = True

            #------------------------------------------------------------------#
            # Only need to create it if it doesn't exist:                      #
            #------------------------------------------------------------------#
        Catch e As Exception
            If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
                #--------------------------------------------------------------#
                # Style doesn't exist. Need to create it:                      #
                #--------------------------------------------------------------#
                hasStyle = False
            Else
                eH(_el.Fatal, _errorProcedure, _errorValue.sessionException, e.Message, "insert")
            End If
        End Try

        #----------------------------------------------------------------------#
        # Create and format a text style called 'TagIndex':                    #
        #----------------------------------------------------------------------#
        If (Not hasStyle) Then
            Try
                wdDoc.Styles.Add("TagIndex")
                With wdDoc.Styles("TagIndex").Font
                    .Name = "Arial"
                    .Size = 9
                    .Bold = False
                    .Italic = False
                    .Underline = Word.WdUnderline.wdUnderlineNone
                    .UnderlineColor = Word.WdColor.wdColorAutomatic
                    .StrikeThrough = False
                    .DoubleStrikeThrough = False
                    .Outline = False
                    .Emboss = False
                    .Shadow = False
                    .Hidden = False
                    .SmallCaps = False
                    .AllCaps = False
                    .Color = Word.WdColor.wdColorAutomatic
                    .Engrave = False
                    .Superscript = False
                    .Subscript = False
                    .Scaling = 100
                    .Kerning = 0
                    .Animation = Word.WdAnimation.wdAnimationNone
                End With
                '    CommandBars("Apply Styles").Visible = False
                With wdDoc.Styles("TagIndex").ParagraphFormat
                    .LeftIndent = wdApp.CentimetersToPoints(0)
                    .RightIndent = wdApp.CentimetersToPoints(0)
                    .SpaceBefore = 2
                    .SpaceBeforeAuto = False
                    .SpaceAfter = 2
                    .SpaceAfterAuto = False
                    .LineSpacingRule = Word.WdLineSpacing.wdLineSpaceSingle
                    .Alignment = Word.WdParagraphAlignment.wdAlignParagraphJustify
                    .WidowControl = True
                    .KeepWithNext = False
                    .KeepTogether = False
                    .PageBreakBefore = False
                    .NoLineNumber = False
                    .Hyphenation = True
                    .FirstLineIndent = wdApp.CentimetersToPoints(0)
                    .OutlineLevel = Word.WdOutlineLevel.wdOutlineLevelBodyText
                    .CharacterUnitLeftIndent = 0
                    .CharacterUnitRightIndent = 0
                    .CharacterUnitFirstLineIndent = 0
                    .LineUnitBefore = 0
                    .LineUnitAfter = 0
                    .MirrorIndents = False
                    .TextboxTightWrap = Word.WdTextboxTightWrap.wdTightNone
                End With

                wdDoc.Styles("TagIndex").NoSpaceBetweenParagraphsOfSameStyle =
                    False
                wdDoc.Styles("TagIndex").ParagraphFormat.TabStops.ClearAll()
                wdDoc.Styles("TagIndex").ParagraphFormat.TabStops.Add(Position:=wdApp.CentimetersToPoints(19), Alignment:=Word.WdTabAlignment.wdAlignTabRight, Leader:=Word.WdTabLeader.wdTabLeaderDots)
                With wdDoc.Styles("TagIndex").ParagraphFormat
                    With .Shading
                        .Texture = Word.WdTextureIndex.wdTextureNone
                        .ForegroundPatternColor = Word.WdColor.wdColorAutomatic
                        .BackgroundPatternColor = Word.WdColor.wdColorAutomatic
                    End With
                    .Borders(Word.WdBorderType.wdBorderLeft).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    .Borders(Word.WdBorderType.wdBorderRight).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    .Borders(Word.WdBorderType.wdBorderTop).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    .Borders(Word.WdBorderType.wdBorderBottom).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    With .Borders
                        .DistanceFromTop = 1
                        .DistanceFromLeft = 4
                        .DistanceFromBottom = 1
                        .DistanceFromRight = 4
                        .Shadow = False
                    End With
                End With
                wdDoc.Styles("TagIndex").LanguageID = Word.WdLanguageID.wdEnglishUK
                wdDoc.Styles("TagIndex").NoProofing = True
                wdDoc.Styles("TagIndex").Frame.Delete()

                #--------------------------------------------------------------#
                # Exit if the connection to the Word document is lost:         #
                #--------------------------------------------------------------#
            Catch e As Exception
                Console.WriteLine(e.Message & "\r\n")
                If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
                    m.session = False
                Else
                    eH(_el.Fatal, _errorProcedure, _errorValue.sessionException, e.Message, "insert")
                End If
            End Try
        End If
        createIndexStyle = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: renumberRefs                                                   #
    #                                                                          #
    # Description:                                                             #
    # Session command to renumber all reference numbers.                       #
    #                                                                          #
    # All code is encapsulated in a try-catch to detect any automation         #
    # error in case user renders the Word application and document             #
    # inaccessible, for example by closing the document.                       #
    #--------------------------------------------------------------------------#
    Private Function renumberRefs() As Long
        #----------------------------------------------------------------------#
        # Declare the procedure name:                                          #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name

        #----------------------------------------------------------------------#
        # Check if document reference numbers have been locked:                #
        #----------------------------------------------------------------------#
        If (isLocked()) Then
            #------------------------------------------------------------------#
            # Not allowed to renumber without manual unlocking:                #
            #------------------------------------------------------------------#
            eH(_el.Fatal, _errorProcedure, _errorValue.refsLocked, "", "insert")

            #------------------------------------------------------------------#
            # Process the document renumbering as we go:                       #
            #------------------------------------------------------------------#
        ElseIf (processDocumentData(True) <> 0) Then
        End If
        renumberRefs = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Check if the document lock variable is true:                             #
    #--------------------------------------------------------------------------#
    Private Function isLocked() As Boolean
        #----------------------------------------------------------------------#
        # Declare the procedure name and local variables:                      #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim bFound As Boolean = False

        #----------------------------------------------------------------------#
        # Check if the lock variable is already defined:                       #
        #----------------------------------------------------------------------#
        isLocked = False
        Try
            For Each var In wdDoc.Variables
                If (var.name = "refDocLock") Then
                    bFound = True
                    Exit For
                End If
            Next

            #------------------------------------------------------------------#
            # It exists so use the value:                                      #
            #------------------------------------------------------------------#
            If (bFound) Then
                isLocked = wdDoc.Variables("refDocLock").Value
            End If

            #------------------------------------------------------------------#
            # Exit if the connection to the Word document is lost:             #
            #------------------------------------------------------------------#
        Catch e As Exception
            Console.WriteLine(e.Message & "\r\n")
            If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
                m.session = False
            Else
                eH(_el.Fatal, _errorProcedure, _errorValue.sessionException, e.Message, "insert")
            End If
        End Try
    End Function

    #--------------------------------------------------------------------------#
    # Set the document lock variable to true or false:                         #
    #--------------------------------------------------------------------------#
    Private Sub setLock(ByVal action As Boolean)
        #----------------------------------------------------------------------#
        # Declare the procedure name and local variables:                      #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim bFound As Boolean = False

        #----------------------------------------------------------------------#
        # Check if the lock variable is already defined:                       #
        #----------------------------------------------------------------------#
        Try
            For Each var In wdDoc.Variables
                If (var.name = "refDocLock") Then
                    bFound = True
                    Exit For
                End If
            Next

            #------------------------------------------------------------------#
            # It doesn't exist so add it and set the value:                    #
            #------------------------------------------------------------------#
            If (Not bFound) Then
                wdDoc.Variables.Add("refDocLock")
            End If
            wdDoc.Variables("refDocLock").Value = action

            #------------------------------------------------------------------#
            # Exit if the connection to the Word document is lost:             #
            #------------------------------------------------------------------#
        Catch e As Exception
            Console.WriteLine(e.Message & "\r\n")
            If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
                m.session = False
            Else
                eH(_el.Fatal, _errorProcedure, _errorValue.sessionException, e.Message, "insert")
            End If
        End Try
    End Sub

    #--------------------------------------------------------------------------#
    # Subroutine: createTest                                                   #
    #                                                                          #
    # Description:                                                             #
    # Create a test script from the reference document data:                   #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # testType              The type of test - ca, gep or gmp.                 #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Function createTest(ByVal testType As Integer) As Long
        #----------------------------------------------------------------------#
        # Declare local variables:                                             #
        #----------------------------------------------------------------------#
        Dim i As Integer
        Dim iCol As Integer
        Dim iRow As Integer
        Dim s As String
        Dim sColTarget As String
        Dim sKey As String
        Dim xPath As String
        Dim tTable As Word.Table = Nothing
        Dim xNode As MSXML2.IXMLDOMNode = Nothing
        Dim xNodeSpec As MSXML2.IXMLDOMNode = Nothing
        Dim xNodeSpecList As MSXML2.IXMLDOMNodeList = Nothing
        Dim xTagList As MSXML2.IXMLDOMNodeList = Nothing
        Dim docXML As MSXML2.DOMDocument60 = Nothing
        Dim phembot As Object = Nothing

        #----------------------------------------------------------------------#
        # Create the test table:                                               #
        #----------------------------------------------------------------------#
        If (createTestStyle() <> 0) Then
        Else
            #--------------------------------------------------------------#
            # Loop through all of the reference document tags:             #
            #--------------------------------------------------------------#
            For Each xNode In xTagList
                #----------------------------------------------------------#
                # Get the tag:                                             #
                #----------------------------------------------------------#
                sKey = xNode.selectSingleNode("Value").text

                #----------------------------------------------------------#
                # Get the specification text for the tag:                  #
                #----------------------------------------------------------#
                xPath = "/root/data/element[key='" & sKey & "']"
                xNodeSpecList = docXML.selectNodes(xPath)

                #----------------------------------------------------------#
                # Check if no specification fields found:                  #
                #----------------------------------------------------------#
                If (xNodeSpecList Is Nothing) Then
                Else
                    #------------------------------------------------------#
                    # Add a new table row if required:                     #
                    #------------------------------------------------------#
                    If (iRow > 1) Then
                        tTable.Rows.Add()
                    End If

                    #------------------------------------------------------#
                    # Add the reference information first:                 #
                    #------------------------------------------------------#
                    s = ""
                    iRow = iRow + 1
                    tTable.Cell(iRow, 1).Range.Text = "T" & iRow - 1
                    '                    tTable.Cell(iRow, 2).Range.text = sKey

                    #------------------------------------------------------#
                    # Enter a loop to process the column map:              #
                    #------------------------------------------------------#
                    For i = 1 To 12
                        #--------------------------------------------------#
                        # Get each specification:                          #
                        #--------------------------------------------------#
                        For Each xNodeSpec In xNodeSpecList
                            If (xNodeSpec Is Nothing) Then

                                #----------------------------------------------#
                                # Check if the source field matches the        #
                                # current column field:                        #
                                #----------------------------------------------#
                            ElseIf (xNodeSpec.selectSingleNode("Description").text =
                                        phembot.Item("request").Item("S" & CStr(i))) Then
                                #------------------------------------------#
                                # Find the target column, hardcoded:       #
                                #------------------------------------------#
                                sColTarget = phembot.Item("request").Item("T" & CStr(i))
                                Select Case sColTarget
                                    Case "Test Ref"
                                        iCol = 1
                                    Case "Req Ref"
                                        iCol = 2
                                    Case "Test Method"
                                        iCol = 3
                                    Case "Expected Result"
                                        iCol = 4
                                    Case "Actual Result"
                                        iCol = 5
                                    Case "PASS or FAIL"
                                        iCol = 6
                                    Case "Initial and Date"
                                        iCol = 7
                                    Case "Result Ref"
                                        iCol = 8
                                End Select

                                #------------------------------------------#
                                # Update the target column text:           #
                                #------------------------------------------#
                                tTable.Cell(iRow, iCol).Range.Select()
                                s = tTable.Cell(iRow, iCol).Range.Text
                                tTable.Cell(iRow, iCol).Range.Collapse(Word.WdCollapseDirection.wdCollapseEnd)
                                If (Len(s) > 3) Then
                                    tTable.Cell(iRow, iCol).Range.Text = vbCrLf
                                End If
                                tTable.Cell(iRow, iCol).Range.Text = xNodeSpec.selectSingleNode("Value").text
                                Exit For
                            End If
                        Next
                    Next i
                End If
            Next
        End If
        createTest = iErr
    End Function

    #--------------------------------------------------------------------------#
    # Function: createTestStyle                                                #
    #                                                                          #
    # Description:                                                             #
    # Format the test table.                                                   #
    #--------------------------------------------------------------------------#
    # Calling parameters:                                                      #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    # Returned parameters:                                                     #
    #                                                                          #
    # none                                                                     #
    #--------------------------------------------------------------------------#
    Private Function createTestStyle() As Long
        #----------------------------------------------------------------------#
        # Declare the procedure name:                                          #
        #----------------------------------------------------------------------#
        Dim _errorProcedure As String = System.Reflection.MethodBase.GetCurrentMethod().Name
        Dim hasStyle As Boolean = "false"
        Dim ttStyle As Word.Style
        Dim rStart As Word.Range
        Dim testDoc As Word.Document = Nothing
        Dim tTable As Word.Table

        #----------------------------------------------------------------------#
        # Create a new test document and check if the TestTable style          #
        # already exists:                                                      #
        #----------------------------------------------------------------------#
        Try
            testDoc = wdApp.Documents.Add
            ttStyle = testDoc.Styles("TestTable")
            hasStyle = True

            #------------------------------------------------------------------#
            # Only need to create it if it doesn't exist:                      #
            #------------------------------------------------------------------#
        Catch e As Exception
            If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
                #--------------------------------------------------------------#
                # Style doesn't exist. Need to create it:                      #
                #--------------------------------------------------------------#
                hasStyle = False
            Else
                eH(_el.Fatal, _errorProcedure, _errorValue.sessionException, e.Message, "test")
            End If
        End Try

        #----------------------------------------------------------------------#
        # Create and format a text style called 'TestTable':                   #
        #----------------------------------------------------------------------#
        If (Not hasStyle) Then
            Try
                #--------------------------------------------------------------#
                # Create the test table style and set up the new document: */
                #--------------------------------------------------------------#
                testDoc.Styles.Add("TestTable")
                With testDoc.PageSetup
                    .LineNumbering.Active = False
                    .Orientation = wdApp.wdOrientLandscape
                    .TopMargin = wdApp.MillimetersToPoints(10)
                    .BottomMargin = wdApp.MillimetersToPoints(10)
                    .LeftMargin = wdApp.MillimetersToPoints(10)
                    .RightMargin = wdApp.MillimetersToPoints(10)
                    .Gutter = wdApp.MillimetersToPoints(0)
                    .HeaderDistance = wdApp.MillimetersToPoints(10)
                    .FooterDistance = wdApp.MillimetersToPoints(10)
                    .PageWidth = wdApp.MillimetersToPoints(297)
                    .PageHeight = wdApp.MillimetersToPoints(210)
                    .FirstPageTray = wdApp.wdPrinterDefaultBin
                    .OtherPagesTray = wdApp.wdPrinterDefaultBin
                    .SectionStart = wdApp.wdSectionNewPage
                    .OddAndEvenPagesHeaderFooter = False
                    .DifferentFirstPageHeaderFooter = False
                    .VerticalAlignment = wdApp.wdAlignVerticalTop
                    .SuppressEndnotes = False
                    .MirrorMargins = False
                    .TwoPagesOnOne = False
                    .BookFoldPrinting = False
                    .BookFoldRevPrinting = False
                    .BookFoldPrintingSheets = 1
                    .GutterPos = wdApp.wdGutterPosLeft
                End With
                rStart = testDoc.Range

                With testDoc.Styles("TestTable")
                    .AutomaticallyUpdate = False
                    .BaseStyle = "Normal"
                    .NextParagraphStyle = "TestTable"
                End With
                With testDoc.Styles("TestTable").ParagraphFormat
                    With .Shading
                        .Texture = wdApp.wdTextureNone
                        .ForegroundPatternColor = wdApp.wdColorAutomatic
                        .BackgroundPatternColor = wdApp.wdColorAutomatic
                    End With
                    .Borders(Word.WdBorderType.wdBorderLeft).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    .Borders(Word.WdBorderType.wdBorderRight).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    .Borders(Word.WdBorderType.wdBorderTop).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    .Borders(Word.WdBorderType.wdBorderBottom).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    .Borders(Word.WdBorderType.wdBorderHorizontal).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    With .Borders
                        .DistanceFromTop = 1
                        .DistanceFromLeft = 4
                        .DistanceFromBottom = 1
                        .DistanceFromRight = 4
                        .Shadow = False
                    End With
                    .LeftIndent = wdApp.CentimetersToPoints(0)
                    .RightIndent = wdApp.CentimetersToPoints(0)
                    .SpaceBefore = 3
                    .SpaceBeforeAuto = False
                    .SpaceAfter = 3
                    .SpaceAfterAuto = False
                    .LineSpacingRule = Word.WdLineSpacing.wdLineSpaceSingle
                    .Alignment = Word.WdParagraphAlignment.wdAlignParagraphJustify
                    .WidowControl = True
                    .KeepWithNext = False
                    .KeepTogether = False
                    .PageBreakBefore = False
                    .NoLineNumber = False
                    .Hyphenation = True
                    .FirstLineIndent = wdApp.CentimetersToPoints(0)
                    .OutlineLevel = Word.WdOutlineLevel.wdOutlineLevelBodyText
                    .CharacterUnitLeftIndent = 0
                    .CharacterUnitRightIndent = 0
                    .CharacterUnitFirstLineIndent = 0
                    .LineUnitBefore = 0
                    .LineUnitAfter = 0
                    .MirrorIndents = False
                    .TextboxTightWrap = Word.WdTextboxTightWrap.wdTightNone
                End With

                testDoc.Styles("TestTable").NoProofing = False
                testDoc.Styles("TestTable").Frame.Delete()

                With testDoc.Styles("TestTable").Font
                    .Name = "Arial"
                    .Size = 8
                    .Bold = False
                    .Italic = False
                    .Underline = Word.WdUnderline.wdUnderlineNone
                    .UnderlineColor = Word.WdColor.wdColorAutomatic
                    .StrikeThrough = False
                    .DoubleStrikeThrough = False
                    .Outline = False
                    .Emboss = False
                    .Shadow = False
                    .Hidden = False
                    .SmallCaps = False
                    .AllCaps = False
                    .Color = Word.WdColor.wdColorAutomatic
                    .Engrave = False
                    .Superscript = False
                    .Subscript = False
                    .Scaling = 100
                    .Kerning = 0
                    .Animation = Word.WdAnimation.wdAnimationNone
                End With
                testDoc.Styles("TestTable").NoSpaceBetweenParagraphsOfSameStyle = False
                testDoc.Styles("TestTable").ParagraphFormat.TabStops.ClearAll()

                #--------------------------------------------------------------------------#
                # Insert the test table:                                                   #
                #--------------------------------------------------------------------------#
                testDoc.Tables.Add(rStart, 2, 8)

                #--------------------------------------------------------------------------#
                # Select the entire table and format the text style:                       #
                #--------------------------------------------------------------------------#
                tTable = testDoc.Tables(1)
                '    tTable.Range.Style = wdDoc.Styles("TestTable")

                #--------------------------------------------------------------------------#
                # Format the table, especially turning off auto fit and setting the        #
                # preferred width to auto:                                                 #
                #--------------------------------------------------------------------------#
                With tTable
                    .TopPadding = wdApp.MillimetersToPoints(0)
                    .BottomPadding = wdApp.MillimetersToPoints(0)
                    .LeftPadding = wdApp.MillimetersToPoints(1.9)
                    .RightPadding = wdApp.MillimetersToPoints(1.9)
                    .Spacing = 0
                    .AllowPageBreaks = False
                    .AllowAutoFit = False
                    .Rows.LeftIndent = wdApp.MillimetersToPoints(2)
                    .PreferredWidthType = Word.WdPreferredWidthType.wdPreferredWidthAuto
                    .PreferredWidth = 0
                End With

                #--------------------------------------------------------------------------#
                # Set the column widths:                                                   #
                #--------------------------------------------------------------------------#
                tTable.Columns(1).PreferredWidthType = Word.WdPreferredWidthType.wdPreferredWidthPoints
                tTable.Columns(2).PreferredWidthType = Word.WdPreferredWidthType.wdPreferredWidthPoints
                tTable.Columns(3).PreferredWidthType = Word.WdPreferredWidthType.wdPreferredWidthPoints
                tTable.Columns(4).PreferredWidthType = Word.WdPreferredWidthType.wdPreferredWidthPoints
                tTable.Columns(5).PreferredWidthType = Word.WdPreferredWidthType.wdPreferredWidthPoints
                tTable.Columns(6).PreferredWidthType = Word.WdPreferredWidthType.wdPreferredWidthPoints
                tTable.Columns(7).PreferredWidthType = Word.WdPreferredWidthType.wdPreferredWidthPoints
                tTable.Columns(8).PreferredWidthType = Word.WdPreferredWidthType.wdPreferredWidthPoints

                tTable.Columns(1).PreferredWidth = wdApp.CentimetersToPoints(1.2)
                tTable.Columns(2).PreferredWidth = wdApp.CentimetersToPoints(1.2)
                tTable.Columns(3).PreferredWidth = wdApp.CentimetersToPoints(6.5)
                tTable.Columns(4).PreferredWidth = wdApp.CentimetersToPoints(6.5)
                tTable.Columns(5).PreferredWidth = wdApp.CentimetersToPoints(6.5)
                tTable.Columns(6).PreferredWidth = wdApp.CentimetersToPoints(1.5)
                tTable.Columns(7).PreferredWidth = wdApp.CentimetersToPoints(2.8)
                tTable.Columns(8).PreferredWidth = wdApp.CentimetersToPoints(1.5)

                #--------------------------------------------------------------------------#
                # Set the header row and prevent rows breaking across pages:               #
                #--------------------------------------------------------------------------#
                tTable.Rows.AllowBreakAcrossPages = False
                tTable.Rows.HeightRule = Word.WdRowHeightRule.wdRowHeightAuto
                tTable.Rows.Height = wdApp.CentimetersToPoints(0)
                tTable.Rows(1).HeadingFormat = True

                #--------------------------------------------------------------------------#
                # Enter the table headings:                                                #
                #--------------------------------------------------------------------------#
                tTable.Cell(1, 1).Range.Text = "Test Ref"
                tTable.Cell(1, 2).Range.Text = "Req Ref"
                tTable.Cell(1, 3).Range.Text = "Test Method"
                tTable.Cell(1, 4).Range.Text = "Expected Result"
                tTable.Cell(1, 5).Range.Text = "Actual Result"
                tTable.Cell(1, 6).Range.Text = "PASS or FAIL"
                tTable.Cell(1, 7).Range.Text = "Initial and Date"
                tTable.Cell(1, 8).Range.Text = "Result Ref"

                tTable.Cell(1, 1).Range.Font.Bold = True
                tTable.Cell(1, 2).Range.Font.Bold = True
                tTable.Cell(1, 3).Range.Font.Bold = True
                tTable.Cell(1, 4).Range.Font.Bold = True
                tTable.Cell(1, 5).Range.Font.Bold = True
                tTable.Cell(1, 6).Range.Font.Bold = True
                tTable.Cell(1, 7).Range.Font.Bold = True
                tTable.Cell(1, 8).Range.Font.Bold = True

                #--------------------------------------------------------------------------#
                # Format the header row:                                                   #
                #--------------------------------------------------------------------------#
                tTable.Rows(1).Shading.Texture = Word.WdTextureIndex.wdTextureNone
                tTable.Rows(1).Shading.ForegroundPatternColor = Word.WdColor.wdColorAutomatic
                tTable.Rows(1).Shading.BackgroundPatternColor = -603917569

                #--------------------------------------------------------------------------#
                # Format the borders:                                                      #
                #--------------------------------------------------------------------------#
                With tTable
                    With .Borders(Word.WdBorderType.wdBorderLeft)
                        .LineStyle = Word.WdLineStyle.wdLineStyleSingle
                        .LineWidth = Word.WdLineWidth.wdLineWidth025pt
                        '            .Color = -603946753
                        .Color = -603930625
                    End With
                    With .Borders(Word.WdBorderType.wdBorderRight)
                        .LineStyle = Word.WdLineStyle.wdLineStyleSingle
                        .LineWidth = Word.WdLineWidth.wdLineWidth025pt
                        .Color = -603930625
                    End With
                    With .Borders(Word.WdBorderType.wdBorderTop)
                        .LineStyle = Word.WdLineStyle.wdLineStyleSingle
                        .LineWidth = Word.WdLineWidth.wdLineWidth025pt
                        .Color = -603930625
                    End With
                    With .Borders(Word.WdBorderType.wdBorderBottom)
                        .LineStyle = Word.WdLineStyle.wdLineStyleSingle
                        .LineWidth = Word.WdLineWidth.wdLineWidth025pt
                        .Color = -603930625
                    End With
                    With .Borders(Word.WdBorderType.wdBorderHorizontal)
                        .LineStyle = Word.WdLineStyle.wdLineStyleSingle
                        .LineWidth = Word.WdLineWidth.wdLineWidth025pt
                        .Color = -603930625
                    End With
                    With .Borders(Word.WdBorderType.wdBorderVertical)
                        .LineStyle = Word.WdLineStyle.wdLineStyleSingle
                        .LineWidth = Word.WdLineWidth.wdLineWidth025pt
                        .Color = -603930625
                    End With
                    .Borders(Word.WdBorderType.wdBorderDiagonalDown).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    .Borders(Word.WdBorderType.wdBorderDiagonalUp).LineStyle = Word.WdLineStyle.wdLineStyleNone
                    .Borders.Shadow = False
                End With

                #--------------------------------------------------------------#
                # Exit if the connection to the Word document is lost:         #
                #--------------------------------------------------------------#
            Catch e As Exception
                Console.WriteLine(e.Message & "\r\n")
                If (TypeOf e Is System.Runtime.InteropServices.COMException) Then
                    m.session = False
                Else
                    eH(_el.Fatal, _errorProcedure, _errorValue.sessionException, e.Message, "insert")
                End If
            End Try
        End If
        createTestStyle = iErr
    End Function
End Class
