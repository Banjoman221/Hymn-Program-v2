Stop-process -Name HymnOS

Start-Sleep -seconds 5

rm .\HymnOS\ -r -Force

$currentDirectory = pwd
cd $currentDirectory

git add .

git status
$gitStatus = git status
if($gitStatus -notlike '* nothing to commit *'){
  $commitMessage = Read-Host "Please enter a commit message" 

  git commit -m $commitMessage

  git push
}
Start-Sleep -seconds 5

$updating = git pull

if($updating -like '* up to date*'){
  Write-Host "App is already up to date"
}elseif(err){
  Write-Host "Updated has failed"
}else{
  Write-Host "App has been updated successfully"
}

Start-Sleep -seconds 5

cxfreeze --script main.py --target-dir HymnOS --target-name HymnOS --base gui --icon gospel 

Start-Sleep -seconds 5

$csvFile = $currentDirectory.path + "\hymnlist.csv"
Write-Host $csvFile
$jsonFile = $currentDirectory.path + "\Setting.json"
Write-Host $jsonFile
$picFile = $currentDirectory.path + "\jg.jpg"
Write-Host $picFile
$picFile2 = $currentDirectory.path + "\1000014238.png"
Write-Host $picFile2
$destinationFile = $currentDirectory.path + "\HymnOS"
Write-Host $destinationFileFile

Copy-Item -Path $csvFile -Destination $destinationFile
Copy-Item -Path $jsonFile -Destination $destinationFile
Copy-Item -Path $picFile -Destination $destinationFile
Copy-Item -Path $picFile2 -Destination $destinationFile

Start-Sleep -seconds 5

$exeFile = $currentDirectory.path + "\HymnOS\HymnOS.exe"
start $exeFile
