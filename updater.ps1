Stop-process -Name HymnOS

Start-Sleep 5s

rm .\dist\ -r

$currentDirectory = pwd
cd $currentDirectory

$updating = git pull

if($updating -like '* up to date*'){
  Write-Host "App is already up to date"
}elseif(err){
  Write-Host "Updated has failed"
}else{
  Write-Host "App has been updated successfully"
}

Start-Sleep 5s

cxfreeze --script main.py --target-dir dist --target-name HymnOS --base gui

Start-Sleep 5s

$csvFile = $currentDirectory.path + "\hymnlist.csv"
Write-Host $csvFile
$jsonFile = $currentDirectory.path + "\Setting.json"
Write-Host $csvFile
$picFile = $currentDirectory.path + "\jg.jpg"
Write-Host $picFile
$picFile2 = $currentDirectory.path + "\1000014238.png"
Write-Host $picFile
$destinationFile = $currentDirectory.path + "\dist"
Write-Host $destinationFileFile

Copy-Item -Path $csvFile -Destination $destinationFile
Copy-Item -Path $picFile -Destination $destinationFile
Copy-Item -Path $picFile2 -Destination $destinationFile

Start-Sleep 5s

$exeFile = $currentDirectory.path + "\dist\HymnOS.exe"
start $exeFile
