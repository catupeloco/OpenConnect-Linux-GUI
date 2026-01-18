#!/bin/bash
#set -x
# Exit codes
# Start:
#	- CODE 11: Can't resolve server ip address.
#	- CODE 12: Openconnect is not running after starting it.
# Status:
#	- CODE 21: There isn't a Openconnect process running.
#	- CODE 22: Process is running but tunnel isn't up.

###########################################
VPNUSER=$2
PASSWORD=$3
SERVER=$4
. $(dirname ${0})/oc-gui-variables.sh

###########################################
function start () {
# If SERVER is not resolvable
if ! host ${SERVER} >/dev/null 2>&1 ; then
	echo No se puede determinar la ip del servidor, saliendo
	exit 11
fi
echo --------Starting---------------
echo $PASSWORD | sudo openconnect --background  --server=${SERVER} --user=${VPNUSER} --passwd-on-stdin --protocol=anyconnect \
                                  --reconnect-timeout=30 --pid-file=/tmp/pid_openconnect -s "vpn-slice $DESTINYS" >/dev/null 2>&1
echo --------Waiting----------------
#ps -fea | grep openconnect | grep -v grep 
if pgrep openconnect; then
	while [ -z "$(ip -br a | grep tun | grep $VPNNET)" ] ; do echo -n . ; done
	echo "."
else
	echo No se detectaron procesos de openconnect corriendo, saliendo.
	exit 12
fi

echo --------Tunneling--------------
. $(dirname ${0})/oc-gui-tunnels.sh
echo --------Done-------------------
}
###########################################
function status () {
pgrep openconnect >/dev/null
if [ "$?" != "0" ] ; then 
        echo -----There are not processes running left-----
	exit 21
else
        echo -----There are processes running--------------
        ip -br a | grep tun >/dev/null
        if [ "$?" != "0" ] ; then
                echo --------But there is no tunnel up-------
		exit 22
	else
		echo --------Even there is a tunnen up-------
        fi
fi
echo -------These are the current routes-----------
	ip route show
}
###########################################
function stop () {
echo ---------Stopping process---------------------
	sudo pkill -9 openconnect
echo ---------Checking if process is active--------
	if pgrep openconnect; then
		exit 31
	fi
}
###########################################

###########MAIN####################################################
case $1 in                              			###
        start) start ;;                 			###
        status) status ;;               			###
        stop) stop ;;                   			###
        *) echo opcion desconocida      			###
           echo uso:                    			###
           echo - $0 status             			###
           echo - $0 stop               			###
           echo - $0 start username password server 		###
	   exit 22 				;;		###
esac                                    			###
###################################################################
exit 0
