#!/bin/bash

git pull

rm ./backend/ -read -r 
mkdir backend

desktopLocation=$(xdg-user-dir DESKTOP)
file=$desktopLocation'/HymnsOS.desktop'
echo $file 
python3C=$(which python3)
pythonC=$(which python)
if [ -e $pythonC ]; then
  pythonCommad=$(which python3)
elif [ -e $python3C ]; then
  pythonCommad=$(which python)
fi
# pythonCommad=$(which python)
echo $pythonCommad

cat << EOF > $file
[Desktop Entry]
Type=Application
Terminal=false
Name=HymnOS
Path=$PWD
Exec=$pythonCommad 'main.py'
EOF
