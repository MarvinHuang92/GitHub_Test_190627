VERSION 5.00
Begin VB.Form Form1 
   BackColor       =   &H00000000&
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Attributes to Excel"
   ClientHeight    =   1530
   ClientLeft      =   45
   ClientTop       =   435
   ClientWidth     =   9180
   Icon            =   "AR_2EForm1.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   ScaleHeight     =   1530
   ScaleWidth      =   9180
   StartUpPosition =   3  '窗口缺省
   Begin VB.CommandButton Command1 
      Caption         =   "Select Blocks"
      Height          =   615
      Left            =   750
      TabIndex        =   0
      Top             =   720
      Width           =   2265
   End
   Begin VB.Image Image1 
      Height          =   1410
      Left            =   3870
      Picture         =   "AR_2EForm1.frx":0CCA
      Stretch         =   -1  'True
      Top             =   90
      Width           =   5250
   End
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "Rip attributes per block selected. 16 attributes per block. Excel and AutoCAD must be running."
      ForeColor       =   &H00FFC0C0&
      Height          =   465
      Left            =   240
      TabIndex        =   1
      Top             =   120
      Width           =   3555
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub M222_Command1_Click()

Dim AutoCAD As Object
Dim activedocument As Object
'Dim modelspace As AcadModelSpace 'not used
'Dim paperspace As AcadPaperSpace 'not used
Dim SSET2 As Object
'Dim insertionPoint(0 To 2) As Variant 'not used
'Dim ent As AcadEntity 'as Object
Dim Excel As Object
Dim excelSheet As Object
Dim application As Object
Dim C As Integer, R As Integer
Dim entLayer As String
Dim entTextString As String
Dim entColor As Variant
Dim entName As String
Dim entName2
Dim entHandle As String

On Error Resume Next
    Set AutoCAD = GetObject(, "AutoCAD.Application")
    If Err Then
        Err.Clear
        Set AutoCAD = CreateObject("AutoCAD.Application")
        AutoCAD.Visible = True
        If Err Then
            MsgBox Err.Description
            Exit Sub
        End If
    End If

  On Error GoTo prcERR
  AutoCAD.Visible = True '显示CAD
  
  
  Set activeDoc = AutoCAD.AcadDocuments
  Dim startPoint(0 To 2) As Double
  Dim endPoint(0 To 2) As Double
  Dim LineObj As AcadLine '如果画图时出错，改为Dim LineObj As Object
  startPoint(0) = 0: startPoint(1) = 0: startPoint(2) = 0
  endPoint(0) = 30: endPoint(1) = 20: endPoint(2) = 0
  Set LineObj = activeDoc.modelspace.AddLine(startPoint, endPoint) '画线
  
prcExit:
  Set activeDoc = Nothing
  Set AutoCAD = Nothing
  Exit Sub
prcERR:
  MsgBox Err.Number & ":" & Err.Description, vbCritical, "错误"
  Resume prcExit
End Sub

Sub M2()


'Dim AutoCAD As AcadApplication
Dim Thisdrawing As AcadDocument  'as Object
Dim activedocument As Object
Dim modelspace As AcadModelSpace 'not used
Dim paperspace As AcadPaperSpace 'not used
Dim SSET2 As Object
Dim insertionPoint(0 To 2) As Variant 'not used
Dim ent As AcadEntity 'as Object
Dim Excel As Object
Dim excelSheet As Object
Dim application As Object
Dim C As Integer, R As Integer
Dim entLayer As String
Dim entTextString As String
Dim entColor As Variant
Dim entName As String
Dim entName2
Dim entHandle As String

    On Error Resume Next
    
    Set Excel = GetObject(, "Excel.Application")
    If Err <> 0 Then
      Err.Clear
        Set Excel = CreateObject("Excel.Application")
        If Err <> 0 Then
            MsgBox "Could not load Excel.", vbExclamation
            End
        End If
    End If
    On Error GoTo 0
    
    Excel.Visible = True
    Excel.Workbooks.Add
    Excel.Sheets("Sheet1").Select
    Set excelSheet = Excel.ActiveWorkbook.Sheets("Sheet1")
    
On Error Resume Next
Set acadapp = GetObject(, "autocad.application")
Set Thisdrawing = acadapp.activedocument
Set acadapp = GetObject(, "AutoCAD.Application")
Set Thisdrawing = acadapp.activedocument
Dim Count
Apptivate

On Error Resume Next
    
   Set SSET2 = Thisdrawing.SelectionSets.Add("strSet3")

R = 1
SSET2.SelectOnScreen

    AppActivate ("Microsoft Excel")
    
    For Each ent In SSET2
    
    If ent.EntityName = "AcDbBlockReference" Then
        
            array1 = ent.GetAttributes
                
        For Count = LBound(array1) To UBound(array1)

          
        ipos = InStr(1, array1(3).TextString, ".")
        tag1 = array1(0).TagString
        tag2 = array1(1).TagString
        tag3 = array1(2).TagString
        tag4 = array1(3).TagString
        tag5 = array1(4).TagString
        tag6 = array1(5).TagString
        tag7 = array1(6).TagString
        tag8 = array1(7).TagString
        tag9 = array1(8).TagString
        tag10 = array1(9).TagString
        tag11 = array1(10).TagString
        tag12 = array1(11).TagString
        tag13 = array1(12).TagString
        tag14 = array1(13).TagString
        tag15 = array1(14).TagString
        tag16 = array1(15).TagString
        
        If array1(0).TextString = "" Then
        ent1 = ""
        End If
        If array1(1).TextString = "" Then
        ent2 = ""
        End If
        If array1(2).TextString = "" Then
        ent3 = ""
        End If
        If array1(3).TextString = "" Then
        ent4 = ""
        End If
        If array1(4).TextString = "" Then
        ent5 = ""
        End If
        
        If array1(5).TextString = "" Then
        ent6 = ""
        End If
        If array1(6).TextString = "" Then
        ent7 = ""
        End If
        If array1(7).TextString = "" Then
        ent8 = ""
        End If
        If array1(8).TextString = "" Then
        ent9 = ""
        End If
        If array1(9).TextString = "" Then
        ent10 = ""
        End If
        If array1(10).TextString = "" Then
        ent11 = ""
        End If
        If array1(11).TextString = "" Then
        ent12 = ""
        End If
        If array1(12).TextString = "" Then
        ent13 = ""
        End If
        If array1(13).TextString = "" Then
        ent14 = ""
        End If
        If array1(14).TextString = "" Then
        ent15 = ""
        End If
        If array1(15).TextString = "" Then
        ent16 = ""
        End If
        
        ent1 = array1(0).TextString
        ent2 = array1(1).TextString
        ent3 = array1(2).TextString
        ent4 = array1(3).TextString
        ent5 = array1(4).TextString
        ent6 = array1(5).TextString
        ent7 = array1(6).TextString
        ent8 = array1(7).TextString
        ent9 = array1(8).TextString
        ent10 = array1(9).TextString
        ent11 = array1(10).TextString
        ent12 = array1(11).TextString
        ent13 = array1(12).TextString
        ent14 = array1(13).TextString
        ent15 = array1(14).TextString
        ent16 = array1(15).TextString
        
        excelSheet.Cells(R, 1).Value = ent1
        excelSheet.Cells(R, 2).Value = ent2
        excelSheet.Cells(R, 3).Value = ent3
        excelSheet.Cells(R, 4).Value = ent4
        excelSheet.Cells(R, 5).Value = ent5
        excelSheet.Cells(R, 6).Value = ent6
        excelSheet.Cells(R, 7).Value = ent7
        excelSheet.Cells(R, 8).Value = ent8
        excelSheet.Cells(R, 9).Value = ent9
        excelSheet.Cells(R, 10).Value = ent10
        excelSheet.Cells(R, 11).Value = ent11
        excelSheet.Cells(R, 12).Value = ent12
        excelSheet.Cells(R, 13).Value = ent13
        excelSheet.Cells(R, 14).Value = ent14
        excelSheet.Cells(R, 15).Value = ent15
        excelSheet.Cells(R, 16).Value = ent16
        
        
    Next Count
    
    R = R + 1
    
    entArea = 0
    End If
    Next ent
    
    
    SSET2.Delete
    
    
    excelSheet.Range("A1").Select
    
    
    Excel.Selection.EntireRow.Insert
    
    excelSheet.Range("A1:P1").Select
    
    Excel.Selection.AutoFilter
    
    excelSheet.Range("A1").Select
    Excel.ActiveCell.FormulaR1C1 = tag1
   
    excelSheet.Range("B1").Select
    Excel.ActiveCell.FormulaR1C1 = tag2
   
    excelSheet.Range("C1").Select
    Excel.ActiveCell.FormulaR1C1 = tag3
    
    excelSheet.Range("D1").Select
    Excel.ActiveCell.FormulaR1C1 = tag4
    
    excelSheet.Range("E1").Select
    Excel.ActiveCell.FormulaR1C1 = tag5
    
    excelSheet.Range("F1").Select
    Excel.ActiveCell.FormulaR1C1 = tag6
    
    excelSheet.Range("G1").Select
    Excel.ActiveCell.FormulaR1C1 = tag7
    
    excelSheet.Range("H1").Select
    Excel.ActiveCell.FormulaR1C1 = tag8
    
   '--------------
   excelSheet.Range("I1").Select
    Excel.ActiveCell.FormulaR1C1 = tag9
   
    excelSheet.Range("J1").Select
    Excel.ActiveCell.FormulaR1C1 = tag10
   
    excelSheet.Range("K1").Select
    Excel.ActiveCell.FormulaR1C1 = tag11
    
    excelSheet.Range("L1").Select
    Excel.ActiveCell.FormulaR1C1 = tag12
    
    excelSheet.Range("M1").Select
    Excel.ActiveCell.FormulaR1C1 = tag13
    
    excelSheet.Range("N1").Select
    Excel.ActiveCell.FormulaR1C1 = tag14
    
    excelSheet.Range("O1").Select
    Excel.ActiveCell.FormulaR1C1 = tag15
    
    excelSheet.Range("P1").Select
    Excel.ActiveCell.FormulaR1C1 = tag16
    
    
    excelSheet.Range("A1:P1").Select
    Excel.Selection.Font.Bold = True
    
    
    C = 1
    excelSheet.Columns(C).AutoFit
    C = 2
    excelSheet.Columns(C).AutoFit
    C = 3
    excelSheet.Columns(C).AutoFit
    C = 4
    excelSheet.Columns(C).AutoFit
    C = 5
    excelSheet.Columns(C).AutoFit
    C = 6
    excelSheet.Columns(C).AutoFit
    C = 7
    excelSheet.Columns(C).AutoFit
     C = 8
    excelSheet.Columns(C).AutoFit
    C = 9
    excelSheet.Columns(C).AutoFit
    C = 10
    excelSheet.Columns(C).AutoFit
    C = 11
    excelSheet.Columns(C).AutoFit
    C = 12
    excelSheet.Columns(C).AutoFit
    C = 13
    excelSheet.Columns(C).AutoFit
    C = 14
    excelSheet.Columns(C).AutoFit
    C = 15
    excelSheet.Columns(C).AutoFit
    C = 16
    excelSheet.Columns(C).AutoFit
    
    excelSheet.Rows("1:1").Select
    'excelSheet.Selection.RowHeight = 22.5
    excelSheet.Range("A1:P1").Select
    With excelSheet.Selection.Interior
        .ColorIndex = 37
        .Pattern = xlSolid
    End With
    
    excelSheet.Cells.Select
    With excelSheet.Selection
        .HorizontalAlignment = xlLeft
        .VerticalAlignment = xlBottom
        .WrapText = False
        .Orientation = 0
        .AddIndent = False
        .IndentLevel = 0
        .ShrinkToFit = False
        .MergeCells = False
    End With
    excelSheet.Range("A1").Select
End Sub


Sub Command1_Click()

Dim myAcadApp As AutoCAD.AcadApplication, activeDoc As AutoCAD.AcadDocument, acMS As AutoCAD.AcadModelSpace
Set myAcadApp = CreateObject("Autocad.Application")
Set activeDoc = myAcadApp.activedocument

Dim I%
Dim entry As AcadEntity, blk1 As AcadBlockReference, att1 As AcadAttributeReference
Dim varAttributes As Variant
Dim strAttributes As String
For Each entry In activeDoc.modelspace
If entry.ObjectName = "AcDbBlockReference" Then
Set blk1 = entry
If blk1.Name = "?????" Then '你的块名
varAttributes = entry.GetAttributes
strAttributes = ""
For I = LBound(varAttributes) To UBound(varAttributes)
Set att1 = varAttributes(I)
strAttributes = strAttributes & "标记：" & att1.TagString & "，值：" & att1.TextString & "。"
'自己想怎么用就怎么用^_^
Next
End If
End If

Next
End Sub
