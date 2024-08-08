# pre-clean-disk
A quick and dirty way to always ensure the target disk 0 is cleaned when running a MDT deploy

Outline:
1. copy pre-clean-disk.exe to wim-image.
2. make winpeshl.ini run this app at startup.
3. commit wim-image.
4. update MDT iso file.
5. Profits.

```powershell
Add-Type -AssemblyName PresentationCore,PresentationFramework,System.Windows.Forms

function DPcommand {

   powershell.exe -ep bypass -c "echo 'select disk 0', 'clean' | diskpart"

}

function cleaned {

    $ButtonType = [System.Windows.MessageBoxButton]::OK
    $MessageIcon = [System.Windows.MessageBoxImage]::Information
    $MessageBody = "Disk 0 has been completely wiped."
    $MessageTitle = "INFO"
    [System.Windows.Forms.MessageBox]::Show($MessageBody, $MessageTitle, $ButtonType, $MessageIcon)

}

function DoNothing {

     $ButtonType = [System.Windows.MessageBoxButton]::OK
     $MessageIcon = [System.Windows.MessageBoxImage]::Information
     $MessageBody = "Disk 0 has been left alone."
     $MessageTitle = "INFO"
     [System.Windows.Forms.MessageBox]::Show($MessageBody, $MessageTitle, $ButtonType, $MessageIcon)

}

# Define message box parameters
$ButtonType = [System.Windows.MessageBoxButton]::YesNo
$MessageIcon = [System.Windows.MessageBoxImage]::Warning
$MessageBody = "Do you want to manually erase disk 0?"
$MessageTitle = "WARNING!?"

# Show the message box and capture the result
$Result = [System.Windows.MessageBox]::Show($MessageBody, $MessageTitle, $ButtonType, $MessageIcon)


if ($Result -eq [System.Windows.MessageBoxResult]::Yes) {

    DPcommand
    cleaned

} else {

    DoNothing
}
```

compile said script with the help of PS2EXE:  
```powershell
Invoke-PS2EXE -inputFile .\pre-clean-disk.ps1 -outputFile .\pre-clean-disk.exe -NoOutput -NoConsole -Icon D:\system\icons\mdt.ico -title 'PCD v0.1' -description 'Simple binary to ask user at start of MDT deploy to erase disk 0' -company 'JML - @jockemedlinux' -product "PCD v0.1" -version "0.1" -copyright "COPYRIGHT" -trademark 'SE' -verbose
```

winpeshl.ini settings:  
```
[LaunchApps]
X:\TOOLS\pre-clean-disk.exe
```
