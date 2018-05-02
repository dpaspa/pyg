#------------------------------------------------------------------------------#
#                 Copyright © 2018 complianceSHORTCUTS.com                     #
#------------------------------------------------------------------------------#
#                                                                              #
# This program is free software; you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the        #
# Free Software Foundation; either version 3 of the License (GPLv3), or        #
# at your option) any later version.                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but          #
# WITHOUT ANY WARRANTY; without even the implied warranty of                   #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General     #
# Public License for more details.                                             #
#                                                                              #
# Description:                                                                 #
# Generates open document format documents from a format template combined     #
# with a separate content template.                                            #
#------------------------------------------------------------------------------#
# Revision history:                                                            #
# Rev By                Date        CC   Note                                  #
# 1   David Paspa       06-Apr-2018 NA   Initial design.                       #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# Define the global error variables:                                           #
#------------------------------------------------------------------------------#
Public iErr As Long
Public sErrProc As String
Public sErr() As String

#------------------------------------------------------------------------------#
# Declare module level variables:                                              #
#------------------------------------------------------------------------------#
Private wdDoc As Word.Document

#------------------------------------------------------------------------------#
# Function: DeclareGetMessage                                                  #
#                                                                              #
# Description:                                                                 #
# Defines the global message constants which correspond to the various         #
# program status constants CS_xxx.                                             #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# iStatus               The status number to return the message for.           #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# none                                                                         #
#------------------------------------------------------------------------------#
# First enumerate the global completion status and error constants:            #
#------------------------------------------------------------------------------#
Public Enum CS_ERR
    userCancel = -1
    fileNotExist = -2
    tableFormatBad = -3
End Enum

#------------------------------------------------------------------------------#
# Now determine which error message to display:                                #
#------------------------------------------------------------------------------#
Private Function DeclareGetMessage(ByVal iStatus As Integer) As String
    Select Case iStatus
       #----------------------------------------------------------------------#
       # Traceability error messages:                                         #
       #----------------------------------------------------------------------#
        Case CS_ERR.fileNotExist:           DeclareGetMessage = "File @1 does not exist."
        Case CS_ERR.tableFormatBad:         DeclareGetMessage = "The requirement table has merged cells! Unmerge please."
        Case Default:                       DeclareGetMessage = "No message defined."
    End Select
End Function


Sub UICallBack(ctlRibbon As IRibbonControl)
    iErr = 0
    If (processTables <> 0) Then
    End If
End Sub

#------------------------------------------------------------------------------#
# Function: processTables                                                      #
#                                                                              #
# Description:                                                                 #
# Process all of the file names in the table.                                  #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# none                                                                         #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# none                                                                         #
#------------------------------------------------------------------------------#
Public Function processTables() As Integer
   #--------------------------------------------------------------------------#
   # Declare local variables:                                                 #
   #--------------------------------------------------------------------------#
    Dim bPrint As Boolean
    Dim i As Integer               # Basic counter                            #
    Dim documentAuthor As String
    Dim documentDelete As String
    Dim documentDiscipline As String
    Dim documentNumber As String
    Dim documentTitle As String
    Dim documentType As String
    Dim fileNameContent As String
    Dim fileNameFormat As String
    Dim fileNameFormatPath As String
    Dim inputPath As String
    Dim outputPath As String
    Dim rFile As Word.Range
    Dim tTable As Word.Table
    Dim answer As Variant

   #--------------------------------------------------------------------------#
   # Define the procedure name and trap any programming errors:               #
   #--------------------------------------------------------------------------#
On Error GoTo Err_processTables
    Const ERR_PROC = "processTables"

   #--------------------------------------------------------------------------#
   # Ask the user if printing the cover page:                                 #
   #--------------------------------------------------------------------------#
    bPrint = False
    answer = MsgBox("Print document cover pages?", vbYesNoCancel, "Confirm to Print")

   #--------------------------------------------------------------------------#
   # Check if the user cancelled. Do nothing more:                            #
   #--------------------------------------------------------------------------#
    If (answer = vbCancel) Then
        iErr = CS_ERR.userCancel
    Else
       #----------------------------------------------------------------------#
       # Print if required:                                                   #
       #----------------------------------------------------------------------#
        If (answer = vbYes) Then
            bPrint = True
        Else
            bPrint = False
        End If

       #----------------------------------------------------------------------#
       # Get the format template path from the first row:                     #
       #----------------------------------------------------------------------#
        Set tTable = ActiveDocument.Tables(1)
        Set rFile = tTable.Cell(2, 1).Range
        rFile.End = rFile.End - 1
        fileNameFormatPath = rFile.Text

       #----------------------------------------------------------------------#
       # Get the output path from the third row:                              #
       #----------------------------------------------------------------------#
        Set rFile = tTable.Cell(3, 1).Range
        rFile.End = rFile.End - 1
        outputPath = rFile.Text

       #----------------------------------------------------------------------#
       # Get the content template path from the fourth row:                   #
       #----------------------------------------------------------------------#
        Set rFile = tTable.Cell(4, 1).Range
        rFile.End = rFile.End - 1
        inputPath = rFile.Text
'        inputPath = ActiveDocument.AttachedTemplate.Path

       #----------------------------------------------------------------------#
       # Get the document type from the fifth row:                            #
       #----------------------------------------------------------------------#
        Set rFile = tTable.Cell(5, 1).Range
        rFile.End = rFile.End - 1
        documentType = rFile.Text

       #----------------------------------------------------------------------#
       # Loop through the current table's rows:                               #
       #----------------------------------------------------------------------#
        For i = 6 To tTable.Rows.Count
           #------------------------------------------------------------------#
           # Get the filename from the table cell:                            #
           #------------------------------------------------------------------#
            Set rFile = tTable.Cell(i, 1).Range
            rFile.End = rFile.End - 1

           #------------------------------------------------------------------#
           # Check if the row is not highlighted. Ignore it if so:            #
           #------------------------------------------------------------------#
            If (rFile.Shading.BackgroundPatternColor = wdColorAutomatic) Then
            Else
               #--------------------------------------------------------------#
               # Get the document filename and path:                          #
               #--------------------------------------------------------------#
                fileNameContent = inputPath & "\" & rFile.Text

               #--------------------------------------------------------------#
               # Get the discipline from the second cell:                     #
               #--------------------------------------------------------------#
                Set rFile = tTable.Cell(i, 2).Range
                rFile.End = rFile.End - 1
                documentDiscipline = rFile.Text

               #--------------------------------------------------------------#
               # Get the document number from the third cell:                 #
               #--------------------------------------------------------------#
                Set rFile = tTable.Cell(i, 3).Range
                rFile.End = rFile.End - 1
                documentNumber = rFile.Text

               #--------------------------------------------------------------#
               # Get the document title from the fourth cell:                 #
               #--------------------------------------------------------------#
                Set rFile = tTable.Cell(i, 4).Range
                rFile.End = rFile.End - 1
                documentTitle = rFile.Text

               #--------------------------------------------------------------#
               # Get the author from the fifth cell:                          #
               #--------------------------------------------------------------#
                Set rFile = tTable.Cell(i, 5).Range
                rFile.End = rFile.End - 1
                documentAuthor = rFile.Text

               #--------------------------------------------------------------#
               # Get the format template file from the sixth cell:            #
               #--------------------------------------------------------------#
                Set rFile = tTable.Cell(i, 6).Range
                rFile.End = rFile.End - 1
                fileNameFormat = fileNameFormatPath & "\" & rFile.Text

                #--------------------------------------------------------------#
                # Get the deletion bookmarks from the eighth cell:             #
                #--------------------------------------------------------------#
                Set rFile = tTable.Cell(i, 8).Range
                rFile.End = rFile.End - 1
                documentDelete = rFile.Text

                #--------------------------------------------------------------#
                # Generate the document:                                       #
                #--------------------------------------------------------------#
                If (documentGenerate(fileNameFormat, fileNameContent, documentType, _
                                     documentDiscipline, documentNumber, documentTitle, _
                                     documentAuthor, documentDelete) <> 0) Then
                    Exit For
                Else
                   #----------------------------------------------------------#
                   # Print the first page for signing if requested:           #
                   #----------------------------------------------------------#
                    wdDoc.Activate
                    Selection.HomeKey Unit:=wdStory
                    If (bPrint) Then
                        Application.PrintOut fileName:="", Range:=wdPrintCurrentPage, Item:= _
                            wdPrintDocumentWithMarkup, Copies:=1, Pages:="", PageType:= _
                            wdPrintAllPages, Collate:=True, Background:=True, PrintToFile:=False, _
                            PrintZoomColumn:=0, PrintZoomRow:=0, PrintZoomPaperWidth:=0, _
                            PrintZoomPaperHeight:=0
                    End If

                   #----------------------------------------------------------#
                   # Save the file to the output path:                        #
                   #----------------------------------------------------------#
                    ActiveDocument.SaveAs2 fileName:=outputPath & "\" & documentNumber & ".docx", _
                        FileFormat:=wdFormatXMLDocument, LockComments:=False, Password:="", _
                        AddToRecentFiles:=True, WritePassword:="", ReadOnlyRecommended:=False, _
                        EmbedTrueTypeFonts:=False, SaveNativePictureFormat:=False, SaveFormsData _
                        :=False, SaveAsAOCELetter:=False, CompatibilityMode:=15

                   #----------------------------------------------------------#
                   # Save the file as a PDF to the output path:               #
                   #----------------------------------------------------------#
                    ActiveDocument.ExportAsFixedFormat OutputFileName:=outputPath & "\" & documentNumber & ".pdf", _
                        ExportFormat:=wdExportFormatPDF, OpenAfterExport:=False, _
                        OptimizeFor:=wdExportOptimizeForPrint, Range:=wdExportAllDocument, _
                        Item:=wdExportDocumentContent, IncludeDocProps:=True, KeepIRM:=True, _
                        CreateBookmarks:=wdExportCreateNoBookmarks, DocStructureTags:=True, _
                        BitmapMissingFonts:=True, UseISO19005_1:=False

                   #----------------------------------------------------------#
                   # Close the document:                                      #
                   #----------------------------------------------------------#
                    ActiveDocument.Close False
                End If

               #--------------------------------------------------------------#
               # Highlight the row green now that it has been processed:      #
               #--------------------------------------------------------------#
                Set rFile = ActiveDocument.Range(Start:=tTable.Cell(i, 2).Range.Start, End:=tTable.Cell(i, 8).Range.End)
                rFile.Shading.BackgroundPatternColor = WdColor.wdColorLightGreen
            End If
        Next i
    End If

   #--------------------------------------------------------------------------#
   # Return completion status:                                                #
   #--------------------------------------------------------------------------#
ExitFunction:
    If (iErr = CS_ERR.userCancel) Then
    ElseIf (iErr <> 0) Then
        MsgBox DeclareGetMessage(iErr) & " " & sErr(0), vbOKOnly, "Error - something went wrong because of Hisham"
    Else
        MsgBox "Succesfully Complete :O)", vbOKOnly, "All documents processed"
    End If
    processTables = iErr
    Exit Function

   #--------------------------------------------------------------------------#
   # Output the unspecified error message:                                    #
   #--------------------------------------------------------------------------#
Err_processTables:
    iErr = Err.Number: sErrProc = ERR_PROC
    ReDim sErr(0)
    sErr(0) = Err.Description
    Resume ExitFunction
End Function

#------------------------------------------------------------------------------#
# Function: documentGenerate                                                   #
#                                                                              #
# Description:                                                                 #
# Generates the document from the format and content templates.                #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# fileNameFormat              The format template.                             #
# fileNameContent             The content template.                            #
# documentType                The type of document, such as URS.               #
# documentDisciplinke         The discipline, such as Architectural.           #
# documentTitle               The title of the document.                       #
# documentAuthor              The author name.                                 #
# documentDelete              The csv deletion bookmark list.                  #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# documentNumber              The document number.                             #
#------------------------------------------------------------------------------#
Private Function documentGenerate(ByVal fileNameFormat As String, _
                                  ByVal fileNameContent As String, _
                                  ByVal documentType As String, ByVal documentDiscipline As String, _
                                  ByRef documentNumber As String, ByVal documentTitle As String, _
                                  ByVal documentAuthor As String, ByVal documentDelete As String) As Integer
   #--------------------------------------------------------------------------#
   # Declare local variables:                                                 #
   #--------------------------------------------------------------------------#
    Dim i As Integer
    Dim propertyValue As String
    Dim s() As String
    Dim propertyName As Variant
    Dim wdTemplate As Word.Document

   #--------------------------------------------------------------------------#
   # Define the procedure name and trap any programming errors:               #
   #--------------------------------------------------------------------------#
On Error GoTo Err_documentGenerate
    Const ERR_PROC = "documentGenerate"

   #--------------------------------------------------------------------------#
   # Create a new document from the format template:                          #
   #--------------------------------------------------------------------------#
    Set wdDoc = Application.Documents.Add(Template:=fileNameFormat, NewTemplate:=False, documentType:=0, Visible:=True)
    wdDoc.Activate

   #--------------------------------------------------------------------------#
   # Insert the content template at the end:                                  #
   #--------------------------------------------------------------------------#
    Selection.EndKey Unit:=wdStory
    Selection.InsertFile fileName:=fileNameContent, Range:="", ConfirmConversions:=False, Link:=False, Attachment:=False

   #--------------------------------------------------------------------------#
   # Open the content template:                                               #
   #--------------------------------------------------------------------------#
    Documents.Open fileName:=fileNameContent, _
        ConfirmConversions:=False, ReadOnly:=False, AddToRecentFiles:=False, _
        PasswordDocument:="", PasswordTemplate:="", Revert:=False, _
        WritePasswordDocument:="", WritePasswordTemplate:="", Format:= _
        wdOpenFormatAuto, XMLTransform:=""
    Set wdTemplate = Application.ActiveDocument

   #--------------------------------------------------------------------------#
   # Copy the document properties from the content template to the format     #
   # template:                                                                #
   #--------------------------------------------------------------------------#
'    propertyName = WdBuiltInProperty.wdPropertyTitle
'    propertyValue = wdTemplate.BuiltInDocumentProperties(propertyName).Value
'    wdDoc.BuiltInDocumentProperties(propertyName).Value = propertyValue
    wdDoc.BuiltInDocumentProperties(WdBuiltInProperty.wdPropertyTitle).Value = documentTitle

'    propertyName = WdBuiltInProperty.wdPropertyCategory
'    propertyValue = wdTemplate.BuiltInDocumentProperties(propertyName).Value
'    wdDoc.BuiltInDocumentProperties(propertyName).Value = propertyValue
    wdDoc.BuiltInDocumentProperties(WdBuiltInProperty.wdPropertyCategory).Value = documentType

'    propertyName = WdBuiltInProperty.wdPropertyManager
'    propertyValue = wdTemplate.BuiltInDocumentProperties(propertyName).Value
'    wdDoc.BuiltInDocumentProperties(propertyName).Value = propertyValue
    wdDoc.BuiltInDocumentProperties(WdBuiltInProperty.wdPropertyManager).Value = documentAuthor

'    propertyName = WdBuiltInProperty.wdPropertySubject
'    propertyValue = wdTemplate.BuiltInDocumentProperties(propertyName).Value
'    documentNumber = wdDoc.BuiltInDocumentProperties(propertyName).Value & propertyValue
'    wdDoc.BuiltInDocumentProperties(propertyName).Value = documentNumber
    documentNumber = wdDoc.BuiltInDocumentProperties(WdBuiltInProperty.wdPropertySubject).Value & documentNumber
    wdDoc.BuiltInDocumentProperties(WdBuiltInProperty.wdPropertySubject).Value = documentNumber

'    propertyName = WdBuiltInProperty.wdPropertyCompany
'    propertyValue = wdTemplate.BuiltInDocumentProperties(propertyName).Value
'    propertyName = WdBuiltInProperty.wdPropertyKeywords
'    wdDoc.BuiltInDocumentProperties(propertyName).Value = propertyValue
    wdDoc.BuiltInDocumentProperties(WdBuiltInProperty.wdPropertyCompany).Value = documentDiscipline

   #--------------------------------------------------------------------------#
   # Get the list of deletion bookmarks if any:                               #
   #--------------------------------------------------------------------------#
    If (Len(documentDelete) = 0) Then
    ElseIf (Len(documentDelete) = 2 And Asc(Right(documentDelete, 1)) = 7 And Asc(Right(documentDelete, 2)) = 13) Then
    Else
        s = Split(documentDelete, ",")
        For i = 0 To UBound(s)
            If (DeleteBookmarks(Trim(s(i)), 20) <> 0) Then
            End If
        Next i
    End If

   #--------------------------------------------------------------------------#
   # Close the content template:                                              #
   #--------------------------------------------------------------------------#
    wdTemplate.Close False
    wdDoc.Activate

   #--------------------------------------------------------------------------#
   # Update the header field codes in the new document:                       #
   #--------------------------------------------------------------------------#
    ActiveWindow.ActivePane.View.SeekView = wdSeekCurrentPageHeader
    Selection.WholeStory
    Selection.Fields.Update

    If ActiveWindow.View.SplitSpecial <> wdPaneNone Then
        ActiveWindow.Panes(2).Close
    End If
    If ActiveWindow.ActivePane.View.Type = wdNormalView Or ActiveWindow. _
        ActivePane.View.Type = wdOutlineView Then
        ActiveWindow.ActivePane.View.Type = wdPrintView
    End If

   #--------------------------------------------------------------------------#
   # Update the main body of the new document including explicity update      #
   # of the table of contents:                                                #
   #--------------------------------------------------------------------------#
    ActiveWindow.ActivePane.View.SeekView = wdSeekMainDocument
    Selection.HomeKey Unit:=wdStory
    Selection.WholeStory
    Selection.Fields.Update
    ActiveDocument.TablesOfContents(1).Update
    Selection.HomeKey Unit:=wdStory

   #--------------------------------------------------------------------------#
   # Renumber any requirement reference tag numbers:                          #
   #--------------------------------------------------------------------------#
    If (tagRenumber <> 0) Then
    End If

   #--------------------------------------------------------------------------#
   # Return completion status:                                                #
   #--------------------------------------------------------------------------#
ExitFunction:
    documentGenerate = iErr
    Exit Function

   #--------------------------------------------------------------------------#
   # Output the unspecified error message:                                    #
   #--------------------------------------------------------------------------#
Err_documentGenerate:
    iErr = Err.Number: sErrProc = ERR_PROC
    ReDim sErr(0)
    sErr(0) = Err.Description
    Resume ExitFunction
End Function

#------------------------------------------------------------------------------#
# Function: tagRenumber                                                        #
#                                                                              #
# Description:                                                                 #
# Resequences reference numbers.                                               #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# none                                                                         #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# none                                                                         #
#------------------------------------------------------------------------------#
Private Function tagRenumber() As Integer
   #--------------------------------------------------------------------------#
   # Declare local variables:                                                 #
   #--------------------------------------------------------------------------#
    Dim i As Integer               # Basic counter                            #
    Dim iTagNum As Integer
    Dim j As Integer               # Basic counter                            #
    Dim s As String
    Dim rTag As Word.Range
    Dim tTable As Word.Table

   #--------------------------------------------------------------------------#
   # Define the procedure name and trap any programming errors:               #
   #--------------------------------------------------------------------------#
On Error GoTo Err_tagRenumber
    Const ERR_PROC = "tagRenumber"

   #--------------------------------------------------------------------------#
   # Loop through all the tables in the document's table collection from      #
   # bottom up:                                                               #
   #--------------------------------------------------------------------------#
    iTagNum = 1
    For i = 1 To wdDoc.Tables.Count
       #----------------------------------------------------------------------#
       # Loop through the current table's rows:                               #
       #----------------------------------------------------------------------#
        Set tTable = wdDoc.Tables(i)
        For j = 1 To tTable.Rows.Count
           #------------------------------------------------------------------#
           # Get the text from the first cell:                                #
           #------------------------------------------------------------------#
            Set rTag = tTable.Cell(j, 1).Range
            rTag.End = rTag.End - 1
            s = rTag.Text

           #------------------------------------------------------------------#
           # Check if the cell is blank:                                      #
           #------------------------------------------------------------------#
            If (Len(s) = 0) Then

           #------------------------------------------------------------------#
           # Check if the current text cannot be a test tag:                  #
           #------------------------------------------------------------------#
            ElseIf (Len(s) < 2) Then

           #------------------------------------------------------------------#
           # Check if the current text is a test tag number:                  #
           #------------------------------------------------------------------#
            ElseIf ((Left(s, 1) = "U" Or Left(s, 1) = "F" Or _
                     Left(s, 1) = "D" Or Left(s, 1) = "R") And _
                    IsNumeric(Mid(s, 2, Len(s) - 1))) Then
               #--------------------------------------------------------------#
               # This is a valid prefix and tag. Unlink it:                   #
               #--------------------------------------------------------------#
                rTag.Text = Left(s, 1) & iTagNum
                iTagNum = iTagNum + 1
            End If
        Next j
    Next i

   #--------------------------------------------------------------------------#
   # Return completion status:                                                #
   #--------------------------------------------------------------------------#
ExitFunction:
    tagRenumber = iErr
    Exit Function

   #--------------------------------------------------------------------------#
   # Output the unspecified error message:                                    #
   #--------------------------------------------------------------------------#
Err_tagRenumber:
    iErr = CS_ERR.tableFormatBad: sErrProc = ERR_PROC
    ReDim sErr(0)
    sErr(0) = Err.Description
    Resume ExitFunction
End Function


#------------------------------------------------------------------------------#
# Function: DeleteBookmarks                                                    #
#                                                                              #
# Description:                                                                 #
# Deletes any names bookmarks.                                                 #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# sFieldName            The field name being looked at.                        #
# iCount                The number of bookmark names to check for.             #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# none                                                                         #
#------------------------------------------------------------------------------#
Public Function DeleteBookmarks(ByVal sFieldName As String, ByVal iCount As Integer) As Long
   #--------------------------------------------------------------------------#
   # Declare local variables:                                                 #
   #--------------------------------------------------------------------------#
    Dim i As Integer
    Dim rBookmark As Word.Range

   #--------------------------------------------------------------------------#
   # Define the procedure name and trap any programming errors:               #
   #--------------------------------------------------------------------------#
On Error GoTo Err_DeleteBookmarks
    Const ERR_PROC = "DeleteBookmarks"

   #--------------------------------------------------------------------------#
   # Enter a loop to process all deletion bookmarks (if any):                 #
   #--------------------------------------------------------------------------#
    For i = 1 To iCount
       #----------------------------------------------------------------------#
       # Get the deletion bookmark range if there is one. Will cause an       #
       # error if not and exit the loop:                                      #
       #----------------------------------------------------------------------#
On Error GoTo Missing_Field_Bookmark:
        Set rBookmark = wdDoc.Bookmarks(sFieldName & "_" & i).Range
On Error GoTo Err_DeleteBookmarks

       #----------------------------------------------------------------------#
       # Delete the unwanted range:                                           #
       #----------------------------------------------------------------------#
        rBookmark.Delete
'        If (DeleteUnwantedRange(rBookmark) <> 0) Then
'            Exit For
'        End If
CheckNextBookmark:
    Next i

   #--------------------------------------------------------------------------#
   # Clear the object references:                                             #
   #--------------------------------------------------------------------------#
ExitFunction:
    DeleteBookmarks = iErr
    Set rBookmark = Nothing
    Exit Function

   #--------------------------------------------------------------------------#
   # Ignore missing bookmarks. Check for the next one:                        #
   #--------------------------------------------------------------------------#
Missing_Field_Bookmark:
    Resume CheckNextBookmark

   #--------------------------------------------------------------------------#
   # Output the error message:                                                #
   #--------------------------------------------------------------------------#
Err_DeleteBookmarks:
    iErr = Err.Number: sErrProc = ERR_PROC
    ReDim sErr(0)
    sErr(0) = Err.Description
    Resume ExitFunction
End Function

#------------------------------------------------------------------------------#
# Function: DeleteUnwantedRange                                                #
#                                                                              #
# Description:                                                                 #
# Deletes unwanted range. The whole paragraph will be deleted it it can,       #
# so deletion range placeholders must always be in their own paragraph.        #
#------------------------------------------------------------------------------#
# Calling parameters:                                                          #
#                                                                              #
# rDelete               The unwanted document range.                           #
#------------------------------------------------------------------------------#
# Returned parameters:                                                         #
#                                                                              #
# none                                                                         #
#------------------------------------------------------------------------------#
Private Function DeleteUnwantedRange(ByRef rDelete As Word.Range) As Long
   #--------------------------------------------------------------------------#
   # Declare local variables:                                                 #
   #--------------------------------------------------------------------------#
    Dim bCellIsEmpty As Boolean
    Dim bEndofCell As Boolean
    Dim bRowIsEmpty As Boolean
    Dim i As Integer
    Dim j As Integer
    Dim iNumColumns As Integer
    Dim iNumRows As Integer
    Dim lngCharMoved As Long
    Dim rCell As Word.Range

   #--------------------------------------------------------------------------#
   # Define the procedure name and trap any programming errors:               #
   #--------------------------------------------------------------------------#
On Error GoTo Err_DeleteUnwantedRange
    Const ERR_PROC = "DeleteUnwantedRange"

   #--------------------------------------------------------------------------#
   # Try to select the entire paragraph:                                      #
   #--------------------------------------------------------------------------#
    rDelete.Shading.BackgroundPatternColor = WdColor.wdColorLightOrange
    lngCharMoved = rDelete.StartOf(wdParagraph, wdExtend)
    lngCharMoved = rDelete.EndOf(wdParagraph, wdExtend)

   #--------------------------------------------------------------------------#
   # Check if at the end of the table cell (end of cell marker):              #
   #--------------------------------------------------------------------------#
    bCellIsEmpty = False
    bEndofCell = False
    If (rDelete.Information(wdWithInTable) And _
        Asc(Right(rDelete.Text, 1)) = 7 And _
        Asc(Right(rDelete.Text, 2)) = 13) Then
        bEndofCell = True
    End If

   #--------------------------------------------------------------------------#
   # Get the number of rows and columns selected if in a table:               #
   #--------------------------------------------------------------------------#
    If (rDelete.Information(wdWithInTable)) Then
        iNumColumns = rDelete.Columns.Count
        iNumRows = rDelete.Rows.Count
    End If

   #--------------------------------------------------------------------------#
   # Delete the row of characters:                                            #
   #--------------------------------------------------------------------------#
    rDelete.MoveEnd Unit:=WdUnits.wdCharacter, Count:=-1
    If (bDeleteUnwanted) Then
        rDelete.Delete
    Else
        rDelete.Shading.BackgroundPatternColor = WdColor.wdColorLightOrange
        rDelete.Text = "DEL"
    End If

   #--------------------------------------------------------------------------#
   # Check if the cell is now empty:                                          #
   #--------------------------------------------------------------------------#
    rDelete.MoveEnd Unit:=WdUnits.wdCharacter, Count:=1
    If (rDelete.Information(wdWithInTable) And _
        Asc(Right(rDelete.Text, 1)) = 7 And _
        Asc(Right(rDelete.Text, 2)) = 13 And _
        Len(rDelete.Cells(1).Range.Text) = 2) Then
        rDelete.Cells(1).Shading.BackgroundPatternColor = WdColor.wdColorLightOrange
'        rDelete.Collapse
    Else
       #----------------------------------------------------------------------#
       # Delete any CR LF if there is one:                                    #
       #----------------------------------------------------------------------#
        rDelete.Collapse
        If (bEndofCell) Then
            lngCharMoved = rDelete.Move(wdCharacter, -1)
        End If
        If (bDeleteUnwanted) Then
            rDelete.Delete
        End If
    End If

   #--------------------------------------------------------------------------#
   # Process all of the rows if within a table:                               #
   #--------------------------------------------------------------------------#
    If (rDelete.Information(wdWithInTable)) Then
        For i = 1 To iNumRows
           #------------------------------------------------------------------#
           # Assume the row is empty unless some text found. Enter a          #
           # another loop to check all the cells:                             #
           #------------------------------------------------------------------#
            bRowIsEmpty = True
            For j = 1 To iNumColumns
               #--------------------------------------------------------------#
               # Check if the end of cell marker is all that is in the        #
               # cell. If not, there is other text and the row should not     #
               # be deleted. Exit on error if no more cells as the table      #
               # may have split cells elsewhere and hence a higher            #
               # column count than the particular row being traversed:        #
               #--------------------------------------------------------------#
On Error GoTo noMoreCells
                Set rCell = rDelete.Rows(1).Cells(j).Range
                If (Asc(Right(rCell.Text, 1)) = 7 And _
                    Asc(Right(rCell.Text, 2)) = 13 And _
                    Len(rCell.Cells(1).Range.Text) = 2) Then
                Else
                    bRowIsEmpty = False
                    Exit For
                End If
            Next j

           #------------------------------------------------------------------#
           # Delete the entire row if cells are empty:                        #
           #------------------------------------------------------------------#
checkRowDeleted:
            If (bRowIsEmpty And bDeleteUnwanted) Then
                rDelete.Rows(1).Delete
            End If
        Next i
    End If

   #--------------------------------------------------------------------------#
   # Clear the object references:                                             #
   #--------------------------------------------------------------------------#
ExitFunction:
    DeleteUnwantedRange = iErr
    Exit Function

   #--------------------------------------------------------------------------#
   # No more field area deletion bookmarks:                                   #
   #--------------------------------------------------------------------------#
noMoreCells:
    Resume checkRowDeleted

   #--------------------------------------------------------------------------#
   # Output the error message:                                                #
   #--------------------------------------------------------------------------#
Err_DeleteUnwantedRange:
    iErr = Err.Number: sErrProc = ERR_PROC
    ReDim sErr(0)
    sErr(0) = Err.Description
    Resume ExitFunction
End Function
