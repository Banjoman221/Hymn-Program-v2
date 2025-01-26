Stop-process -Name HymnOS

Start-Sleep -seconds 5

rm .\HymnOS\ -r -Force

$currentDirectory = pwd
cd $currentDirectory

$continueing = Read-Host "Would you like to commit changes? enter c for commit or press enter to pull changes(default)"

if($continueing -ne 'c'){
 git pull
}elseif ($continueing -eq 'c') {
  git add .

  git status

  $gitStatus = git status

  if($gitStatus -like "*changes*"){
    $commitMessage = Read-Host "Please enter a commit message or enter 'c' to continue" 
    if($commitMessage -ne 'c'){
      git commit -m $commitMessage

      git push
    }
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
}

Start-Sleep -seconds 5

cxfreeze --script /public/main.py --target-dir HymnOS --target-name HymnOS --base gui --icon gospel 

Start-Sleep -seconds 5

# $csvFile = $currentDirectory.path + "\resources\hymnlist.csv"
# Write-Host $csvFile
# $picFile = $currentDirectory.path + "\resources\jg.jpg"
# Write-Host $picFile
# $picFile2 = $currentDirectory.path + "\resources\1000014238.png"
# Write-Host $picFile2
$resources = $currentDirectory.path + "\resources\hymnlist.csv"
$destinationFile = $currentDirectory.path + "\HymnOS"
Write-Host $destinationFileFile
Copy-Item -Path $resources -Destination $destinationFile

# Copy-Item -Path $csvFile -Destination $destinationFile
# Copy-Item -Path $picFile -Destination $destinationFile
# Copy-Item -Path $picFile2 -Destination $destinationFile

