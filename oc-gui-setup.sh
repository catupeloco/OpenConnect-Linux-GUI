#!/bin/bash
echo instalando dependencias apt
sudo apt install openconnect python3-pip pipx python3-tk sqlite3 -y

echo Instalando dependencias python
sudo pip install "vpn-slice[dnspython,setproctitle]" tkterminal #--break-system-packages

if [ ! -d $HOME/.local/share/applications/ ] ; then
	mkdir -p $HOME/.local/share/applications
fi
cat << EOF > $HOME/.local/share/applications/oc-gui.desktop
[Desktop Entry]
Type=Application
Icon=utilities-terminal
Exec=python3 ${PWD}/oc-gui.py
Terminal=false
Categories=System
Name=OpenConnect GUI
Comment=Visual Client for OpenConnect VPN with vpn-slice
Path=${PWD}
StartupNotify=false
EOF

if [ -d $HOME/Desktop ] ; then
	cp $HOME/.local/share/applications/oc-gui.desktop $HOME/Desktop
fi
if [ -d $HOME/Escritorio ] ; then
	cp $HOME/.local/share/applications/oc-gui.desktop $HOME/Escritorio
fi
