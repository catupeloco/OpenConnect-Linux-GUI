#!/bin/bash
export JUMPSERVER=#JUMPSERVER#
export DNSs='#IPDNSVPN1# #IPDNSVPN2#'
export VPNNET=#SUBNETVPN#
export DESTINYS='#SUBNETTARGET1# #SUBNETTARGET2# #SUBNETTARGET3# #SUBNETTARGET4# #HOSTTARGET1# #HOSTTARGET2#'

# IF JUMPSERVER ONLY SUPPORTS RSA/DSA
	#export SSH=$(dirname ${0})/openssh-client_9.2p1-2+deb12u7_amd64/ssh
	#export SSH_COPY_ID=$(dirname ${0})/openssh-client_9.2p1-2+deb12u7_amd64/ssh-copy-id
	#export SSH_KEY="-o HostKeyAlgorithms=+ssh-rsa,ssh-dss -o PubkeyAcceptedAlgorithms=+ssh-rsa,ssh-dss -i $HOME/.ssh/id_dsa"
# FOR EVERY OTHER CASE
	export SSH=/usr/bin/ssh
	export SSH_COPY_ID=/usr/bin/ssh-copy-id
	export SSH_KEY="-i $HOME/.ssh/#SSHKEY#"

tunnel_hosts=""
tunnel_hosts+=("#NONREACHABLEHOST1#"	"#REMOTEPORT1#"	"#LOCALPORT1#")
tunnel_hosts+=("#NONREACHABLEHOST2#"	"#REMOTEPORT2#"	"#LOCALPORT2#")
tunnel_hosts+=("#NONREACHABLEHOST3#"	"#REMOTEPORT3#"	"#LOCALPORT3#")
tunnel_hosts+=("#NONREACHABLEHOST4#"	"#REMOTEPORT4#"	"#LOCALPORT4#")
tunnel_hosts+=("#NONREACHABLEHOST5#"	"#REMOTEPORT5#"	"#LOCALPORT5#")


