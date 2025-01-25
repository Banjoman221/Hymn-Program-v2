$updating = git pull

  if($updating -like '* up to date*'){
    Write-Host "App is already up to date"
  }elseif(err){
    Write-Host "Updated has failed"
  }else{
    Write-Host "App has been updated successfully"
  }

Start-Sleep -seconds 5

cd ..

cxfreeze --script main.py --target-dir HymnOS --target-name HymnOS --base gui --icon gospel 

