#!/bin/bash

set +v

############################################################
############################################################
# Main program                                             #
############################################################
############################################################

# Set variables

argc=$#

if (( argc < 1 )) 
then
    core_name="netflix"
else
    core_name=$1
fi

echo "[!] Deleting previous core"
docker exec pri_proj bin/solr delete -c $core_name ;