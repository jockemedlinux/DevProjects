# Load the Windows Forms assembly
Add-Type -AssemblyName System.Windows.Forms

# Get the .NET Framework versions
$dotNetVersions = Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP' -Recurse | 
    Get-ItemProperty -Name version -ErrorAction SilentlyContinue | 
    Where-Object { $_.PSChildName -Match '^(?!S)\p{L}' } | 
    Select-Object PSChildName, version

# Create a formatted output string
$output = "Installed .NET Framework Versions:`n`n"
$output += "Name`tVersion`n"
$output += "----`t-------`n"

foreach ($version in $dotNetVersions) {
    $output += "{0}`t{1}`n" -f $version.PSChildName, $version.version
}

# Show the output in a message box
[System.Windows.Forms.MessageBox]::Show($output, "Installed .NET Framework Versions")
