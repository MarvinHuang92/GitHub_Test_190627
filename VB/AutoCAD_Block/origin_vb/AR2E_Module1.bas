Attribute VB_Name = "Module1"
Public Function Apptivate()
Dim Thisdrawing As Object
Dim modelspace As Object
Dim strCaption As String
'Dim modelspace As ACADMODELSPACE
'Dim paperspace As AcadPaperSpace


On Error GoTo ZOOP:

Set acadapp = GetObject(, "AutoCAD.Application")
        If Err Then
            Err.Clear
        Set acadapp = CreateObject("AutoCAD.Application")
            acadapp.Visible = True
                If Err Then
            
       End If
    End If
   strCaption = acadapp.Caption
    
ipos = InStr(1, strCaption, " -")
ipos2 = InStr(1, strCaption, " [")
ipos3 = InStr(1, strCaption, " 2000")


If ipos > 0 Then
strStripCaption = Mid(strCaption, 1, ipos)
End If
If ipos2 > 0 Then
strStripCaption = Mid(strCaption, 1, ipos2)
End If
If ipos3 > 0 Then
strStripCaption = Mid(strCaption, 1, ipos3)
End If


    
    
    Set acadapp = GetObject(, "autocad.application")
        Set Thisdrawing = acadapp.activedocument
            acadapp.Visible = True
    'AppActivate "autocad"
    AppActivate Trim(strStripCaption)
    
    Exit Function
ZOOP:

End Function

