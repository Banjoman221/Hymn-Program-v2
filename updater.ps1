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
cd ./public/

cxfreeze --script main.py --target-dir ../HymnOS --target-name HymnOS --base gui --icon ../resources/gospel 

Start-Sleep -seconds 5
cd ..

rm .\backend -r -Force

Start-Sleep -seconds 5

mkdir backend

start HymnOS
