#!/bin/bash
set -e
function install_elasticsearch()
{
    cluster_name=$1
    ctx logger info  "installing elasticsearch"
    sudo wget https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.5.2.deb -O /opt/elasticsearch.deb
    sudo dpkg -i /opt/elasticsearch.deb
    sudo update-rc.d elasticsearch defaults 95 10
    sudo rm /opt/elasticsearch.deb
    ctx logger info  "Setting cluster name"
    echo "cluster.name: ${cluster_name}" | sudo tee --append /etc/elasticsearch/elasticsearch.yml
    sudo /etc/init.d/elasticsearch start
    # install plugins
    sudo /usr/share/elasticsearch/bin/plugin --install mobz/elasticsearch-head
    sudo /usr/share/elasticsearch/bin/plugin --install lmenezes/elasticsearch-kopf/1.2
    sudo /usr/share/elasticsearch/bin/plugin --install lukas-vlcek/bigdesk
}


function main()
{

    CLUSTER_NAME=$(ctx node properties "clusterName")
    
    if [ -z "$CLUSTER_NAME" ]
     then
        ctx logger info "CLUSTER_NAME is null."
        exit 1
    fi
    
    ctx logger info  "bootstrapping..."

    ctx logger info  "updating db cache"
    sudo apt-get -y update &&
    ctx logger info  "installing dependencies"
    sudo apt-get install -y vim openjdk-7-jdk &&
    #sudo apt-get install -y vim openjdk-7-jdk python-dev curl git &&
   
    # go home
    cd ~
    
    mkdir -p elk &&
    cd elk &&
    install_elasticsearch ${CLUSTER_NAME} &&
    #Set the ElasticSearch IP runtime property
    ctx logger info "Set the ElasticSearch IP runtime property"
    ELASTIC=$(ctx instance host_ip) 
    ctx logger info "ElasticSearch IP is ${ELASTIC} "    
    ctx instance runtime_properties elasticsearch_ip_address $(ctx instance host_ip)
        
    ctx logger info  "bootstrap done"
}

main
