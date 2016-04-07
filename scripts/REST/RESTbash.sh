#!/bin/bash -v

SBCIP=$1

url_basic="http://$SBCIP/api/v1"
rest_header="Content-Type:application/json "
get_action="-X GET"
put_action="-X PUT"
post_action="-X POST"

curl -v -H \"${rest_header}\" ${get_action} ${url_basic}/status


#curl -v -H \"${rest_header}\" ${rest_action} --data "@SetInterfaces-new.json" ${url_basic}/3.5/config/active/traffic_managers/172.30.0.10
#
#curl -v -H \"${rest_header}\" ${rest_action} --data "@AddPool.json" ${url_basic}/3.5/config/active/pools/CFY-Pool
#
#curl -v -H \"${rest_header}\" ${rest_action} --data "@CreatingTrafficIPGroup.json" ${url_basic}/2.0/config/active/traffic_ip_groups/CFY-TIP

#curl -v -H ${rest_header} ${rest_action} \
#     --data "@CreateSessionPersistence.json" \
#     ${url_basic}/2.0/config/active/persistence/Persistence

#curl -v -H ${rest_header} ${rest_action} \
#     --data "@AssigningSessionPersistence.json" \
#     ${url_basic}/3.5/config/active/pools/CFY-Pool

#curl -v -H ${rest_header} ${rest_action} \
#     --data "@CreatingVirtualServer.json" \
#     ${url_basic}/2.0/config/active/virtual_servers/CFY-VS

#-------------------------------------------------------------

## Create/update Configure LB traffic manager and interfaces,
#curl -v -H "Content-Type: application/json" -u admin:admin  -k -X PUT --data "@SetInterfaces.json" \
#     https://192.168.122.84:9070/api/tm/3.5/config/active/traffic_managers/192.168.122.84
#
#curl -v -H "Content-Type: application/json" -u admin:admin  -k -X PUT --data "@AddPool.json" \
#  https://192.168.122.84:9070/api/tm/3.5/config/active/pools/CFY-Pool
#
#curl -v -H "Content-Type: application/json" -u admin:admin  -k -X PUT --data "@CreatingTrafficIPGroup.json" \
#  https://192.168.122.84:9070/api/tm/2.0/config/active/traffic_ip_groups/CFY-TIP
#
#curl -v -H "Content-Type: application/json" -u admin:admin  -k -X PUT --data "@CreateSessionPersistence.json" \
#  https://192.168.122.84:9070/api/tm/2.0/config/active/persistence/Persistence
#
#curl -v -H "Content-Type: application/json" -u admin:admin  -k -X PUT --data "@AssigningSessionPersistence.json" \
#  https://192.168.122.84:9070/api/tm/3.5/config/active/pools/CFY-Pool
#
#curl -v -H "Content-Type: application/json" -u admin:admin  -k -X PUT --data "@CreatingVirtualServer.json" \
#  https://192.168.122.84:9070/api/tm/2.0/config/active/virtual_servers/CFY-VS

