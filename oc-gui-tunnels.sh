#!/bin/bash

. $(dirname ${0})/oc-gui-variables.sh

###########################################
tunnel_set (){
        local DESTINY_HOST=$1
        local DESTINY_PORT=$2
        local LOCAL_PORT=$3
        ps -fea | grep -v grep | grep $DESTINY_HOST >/dev/null
        if [ $? != 0 ] ; then
               $SSH_COPY_ID $SSH_KEY -o StrictHostKeyChecking=no $VPNUSER@$JUMPSERVER >/dev/null 2>&1
               $SSH -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -L ${LOCAL_PORT}:${DESTINY_HOST}:${DESTINY_PORT} -f -N $SSH_KEY $VPNUSER@$JUMPSERVER
        fi
}
###########################################
tunnel_check (){
        local DESTINY_HOST=$1
        ps -fea | grep -v grep | grep $DESTINY_HOST | awk '{print $14}'
        if [ "$?" != "0" ] ; then echo $DESTINY_HOST no tuneleado; fi
}

###########################################

tunnel_elements=${#tunnel_hosts[@]}
tunnel_columns=3
tunnel_rows=$((tunnel_elements / tunnel_columns))

###########################################
echo --------tunnel_set------------
for ((i=0; i<tunnel_rows; i++)); do
	base=$((i * tunnel_columns))
	tunnel_set ${tunnel_hosts[base+1]} ${tunnel_hosts[base+2]} ${tunnel_hosts[base+3]}
done

###########################################

echo --------tunnel_check---------
for ((i=0; i<tunnel_rows; i++)); do
	base=$((i * tunnel_columns))
	tunnel_check ${tunnel_hosts[base+1]}
done
