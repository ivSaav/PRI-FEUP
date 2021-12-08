#!/bin/bash

set +v

############################################################
############################################################
# Main program                                             #
############################################################
############################################################

# Set variables
core_name="netflix"
in_file="data/imdb_final.json"


############################################################
# Process the input options. Add options as needed.        #
############################################################
# Get the options
while getopts ":c:f:" option; do
   case $option in
      c) # core name
         core_name=$OPTARG;;
      f) # input file
         in_file=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done


echo ""
echo "[!] Populating $core_name with $in_file"
curl -X POST -H "Content-type:application/json" --data-binary @${in_file}  "http://localhost:8983/solr/${core_name}/update?commit=true"