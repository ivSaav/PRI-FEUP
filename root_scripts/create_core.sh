#!/bin/bash

set +v

argc=$#

if (( argc < 1 ))
then 
   core_name="netflix"
else
   core_name=$1
fi

echo ""
echo "[!] Creating $core_name core..."
docker exec pri_proj bin/solr create_core -c $core_name ;