Add-Type -AssemblyName PresentationCore,PresentationFramework,System.Windows.Forms

function DPcommand {

   powershell.exe -ep bypass -windowstyle hidden -c "echo 'select disk 0', 'clean' | diskpart"

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