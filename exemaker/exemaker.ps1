Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Create the form
$form = New-Object System.Windows.Forms.Form
$form.Text = 'PowerShell Script to EXE Converter'
$form.Size = New-Object System.Drawing.Size(450, 400)
$form.StartPosition = 'CenterScreen'
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false

# Create a TableLayoutPanel for better layout
$tableLayout = New-Object System.Windows.Forms.TableLayoutPanel
$tableLayout.Dock = 'Fill'
$tableLayout.ColumnCount = 2
$tableLayout.RowCount = 11  # Increased row count for additional text fields
$tableLayout.AutoSize = $true
$form.Controls.Add($tableLayout)

# Select PowerShell Script Button
$scriptPath = ''
$scriptPathTextBox = New-Object System.Windows.Forms.TextBox
$scriptPathTextBox.ReadOnly = $true
$scriptPathTextBox.Width = 250
$tableLayout.Controls.Add($scriptPathTextBox, 1, 0)

$selectScriptButton = New-Object System.Windows.Forms.Button
$selectScriptButton.Text = 'Select PowerShell Script'
$selectScriptButton.Width = 200
$selectScriptButton.Add_Click({
    $fileDialog = New-Object System.Windows.Forms.OpenFileDialog
    $fileDialog.Filter = 'PowerShell Scripts (*.ps1)|*.ps1'
    if ($fileDialog.ShowDialog() -eq 'OK') {
        $scriptPath = $fileDialog.FileName
        $scriptPathTextBox.Text = $scriptPath  # Update the text box with the selected path
    }
})
$tableLayout.Controls.Add($selectScriptButton, 0, 0)

# Select Output Location Button
$outputPath = ''
$outputPathTextBox = New-Object System.Windows.Forms.TextBox
$outputPathTextBox.ReadOnly = $true
$outputPathTextBox.Width = 250
$tableLayout.Controls.Add($outputPathTextBox, 1, 1)

$selectOutputButton = New-Object System.Windows.Forms.Button
$selectOutputButton.Text = 'Select Output Location'
$selectOutputButton.Width = 200
$selectOutputButton.Add_Click({
    $folderDialog = New-Object System.Windows.Forms.FolderBrowserDialog
    if ($folderDialog.ShowDialog() -eq 'OK') {
        $outputPath = $folderDialog.SelectedPath
        $outputPathTextBox.Text = $outputPath  # Update the text box with the selected path
    }
})
$tableLayout.Controls.Add($selectOutputButton, 0, 1)

# Create input fields with labels
$labels = @('Title:', 'Description:', 'Company:', 'Product:', 'Copyright:', 'Trademark:', 'Version:')
$inputs = @()

for ($i = 0; $i -lt $labels.Length; $i++) {
    $label = New-Object System.Windows.Forms.Label
    $label.Text = $labels[$i]
    $label.AutoSize = $true
    $tableLayout.Controls.Add($label, 0, $i + 2)  # Adjusted row index

    $textBox = New-Object System.Windows.Forms.TextBox
    $textBox.Width = 250
    $tableLayout.Controls.Add($textBox, 1, $i + 2)  # Adjusted row index
    $inputs += $textBox
}

# Hidden Checkbox
$hiddenCheckbox = New-Object System.Windows.Forms.CheckBox
$hiddenCheckbox.Text = 'Run Hidden'
$tableLayout.Controls.Add($hiddenCheckbox, 0, 9)

# Convert Button
$convertButton = New-Object System.Windows.Forms.Button
$convertButton.Text = 'Convert'
$convertButton.Width = 100
$convertButton.Add_Click({
    if (-not [string]::IsNullOrEmpty($scriptPath) -and -not [string]::IsNullOrEmpty($outputPath)) {
        $exeName = Join-Path -Path $outputPath -ChildPath "$($inputs[0].Text).exe"
        
        # C# code to create the EXE
        $csharpCode = @"
using System;
using System.Diagnostics;

namespace ScriptRunner
{
    class Program
    {
        static void Main(string[] args)
        {
            string scriptPath = @"$scriptPath";
            ProcessStartInfo startInfo = new ProcessStartInfo("powershell.exe", "-ExecutionPolicy Bypass -File \"" + scriptPath + "\"");
            startInfo.UseShellExecute = false;
            startInfo.CreateNoWindow = $hiddenCheckbox.Checked;
            Process.Start(startInfo);
        }
    }
}
"@

        # Create a temporary C# file
        $tempCSharpFile = Join-Path -Path $outputPath -ChildPath "ScriptRunner.cs"
        Set-Content -Path $tempCSharpFile -Value $csharpCode

        # Compile the C# code to EXE
        $cscPath = Join-Path -Path $env:windir -ChildPath "Microsoft.NET\Framework\v4.0.30319\csc.exe"
        & $cscPath /out:$exeName $tempCSharpFile

        # Clean up the temporary C# file
        Remove-Item -Path $tempCSharpFile

        [System.Windows.Forms.MessageBox]::Show("Conversion complete: $exeName", "Success", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
    } else {
        [System.Windows.Forms.MessageBox]::Show("Please select a script and output location.", "Error", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
    }
})
$tableLayout.Controls.Add($convertButton, 0, 30)

# Cancel Button
$cancelButton = New-Object System.Windows.Forms.Button
$cancelButton.Text = 'Cancel'
$cancelButton.Width = 100
$cancelButton.Add_Click({
    $form.Close()
})
$tableLayout.Controls.Add($cancelButton, 1, 30)

# Show the form
$form.Add_Shown({$form.Activate()})
[void]$form.ShowDialog()
