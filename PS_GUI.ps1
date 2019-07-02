# This function must be defined bofore called, or it will cause an error.
function _add_test_to_listbox([string]$txt){
$txt = $txt.trim()
if ($txt -ne ""){	
	[void] $listbox_build.Items.Add($txt)
	}
}

[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing") 
[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") 


$objForm = New-Object System.Windows.Forms.Form 
$objForm.Text = "Data Entry Form"
$objForm.Size = New-Object System.Drawing.Size(300,370) 
$objForm.StartPosition = "CenterScreen"

$objForm.KeyPreview = $True
$objForm.Add_KeyDown({if ($_.KeyCode -eq "Enter") 
    {$x=$objTextBox.Text;$objForm.Close()}})
$objForm.Add_KeyDown({if ($_.KeyCode -eq "Escape") 
    {$objForm.Close()}})

$OKButton = New-Object System.Windows.Forms.Button
$OKButton.Location = New-Object System.Drawing.Size(75,220)
$OKButton.Size = New-Object System.Drawing.Size(75,23)
$OKButton.Text = "Add"
$OKButton.Add_Click({$x=$objTextBox.Text;& _add_test_to_listbox($x);$objTextBox.Text = ""})
$objForm.Controls.Add($OKButton)

$CancelButton = New-Object System.Windows.Forms.Button
$CancelButton.Location = New-Object System.Drawing.Size(150,220)
$CancelButton.Size = New-Object System.Drawing.Size(75,23)
$CancelButton.Text = "Cancel"
$CancelButton.Add_Click({$objForm.Close()})
$objForm.Controls.Add($CancelButton)

$objLabel = New-Object System.Windows.Forms.Label
$objLabel.Location = New-Object System.Drawing.Size(10,20) 
$objLabel.Size = New-Object System.Drawing.Size(280,20) 
$objLabel.Text = "Please enter the information in the space below:"
$objForm.Controls.Add($objLabel) 

$objTextBox = New-Object System.Windows.Forms.TextBox 
$objTextBox.Location = New-Object System.Drawing.Size(10,40) 
$objTextBox.Size = New-Object System.Drawing.Size(260,20) 
$objForm.Controls.Add($objTextBox)

$listbox_build = New-Object System.Windows.Forms.ListBox 
$listbox_build.Location = New-Object System.Drawing.Size(10,75) 
$listbox_build.Size = New-Object System.Drawing.Size(260,20) 
$listbox_build.Height = 100
[void] $listbox_build.Items.Add("Item1")
$objForm.Controls.Add($listbox_build)

$objForm.Topmost = $True

$objForm.Add_Shown({$objForm.Activate()})
[void] $objForm.ShowDialog()
