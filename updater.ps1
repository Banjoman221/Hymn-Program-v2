Stop-process -Name main


rm .\build\ -r
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

pyinstaller main.py --clean --onefile --noconsole

$csvFile = $currentDirectory.path + "\hymnlist.csv"
Write-Host $csvFile
$picFile = $currentDirectory.path + "\jg.jpg"
Write-Host $picFile
$destinationFile = $currentDirectory.path + "\dist"
Write-Host $destinationFileFile

Copy-Item -Path $csvFile -Destination $destinationFile
Copy-Item -Path $picFile -Destination $destinationFile

$exeFile = $currentDirectory.path + "\dist\main.exe"
start $exeFile
