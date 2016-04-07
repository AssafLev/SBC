#!/bin/bash -x

SBCIP=$1
command=$2

url_basic="http://$SBCIP/api/v1"
rest_header="Content-Type:application/json "
get_action="-X GET"
put_action="-X PUT"
post_action="-X POST"
auth_key="-uAdmin:Admin"

curl -v -H ${rest_header} ${auth_key} ${get_action} ${url_basic}/${command}


#curl -v -H \"${rest_header}\" ${rest_action} --data "@SetInterfaces-new.json" ${url_basic}/3.5/config/active/traffic_managers/172.30.0.10

