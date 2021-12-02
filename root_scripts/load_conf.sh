#!/bin/bash

set +v

Help()
{
   # Display Help
   echo
   echo "Syntax: load_conf [-h|c|s|x]"
   echo "options:"
   echo "h     help."
   echo "c     core name."
   echo "s     schema config file."
   echo "x     xml to be copied to conf dir"
   echo
}


############################################################
############################################################
# Main program                                             #
############################################################
############################################################

argc=$#

if (( argc < 1 )) 
then
    Help
    exit 1
fi

# Set variables
core_name="netflix"
schema=""
xml_file=""

############################################################
# Process the input options. Add options as needed.        #
############################################################
# Get the options
while getopts ":h:c:s:x:p:" option; do
   case $option in
      h)
         Help
         exit;;
      c) # core name
         core_name=$OPTARG;;
      s) # input file
         schema=$OPTARG;;
      x)
         xml_file=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

if [ -n "$xml_file" ];
then
   echo "[!] Copying $xml_file file to solrdata/data/$core_name/conf/$xml_file"
   cp $xml_file solrdata/data/${core_name}/conf/
fi

# load schema
if [ -n "$schema" ];
then
   echo ""
   echo "[!] Loading schema from ${schema}"
   curl -X POST -H "Content-type:application/json" --data-binary @${schema}  "http://localhost:8983/solr/${core_name}/schema"
fi