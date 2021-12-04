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
conf_file=""
xml_file=""
api="schema"

############################################################
# Process the input options. Add options as needed.        #
############################################################
# Get the options
while getopts ":h:c:f:x:a:" option; do
   case $option in
      h)
         Help
         exit;;
      c) # core name
         core_name=$OPTARG;;
      f) # input file
         conf_file=$OPTARG;;
      x)
         xml_file=$OPTARG;;
      a)
         api=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

if [ -n "$xml_file" ];
then
   echo "[!] Copying $xml_file file to solrdata/data/$core_name/conf/"
   cp $xml_file solrdata/data/${core_name}/conf/
fi

# load config
if [ -n "$conf_file" ];
then
   echo ""
   echo "[!] Loading config from ${conf_file}"
   curl -X POST -H "Content-type:application/json" --data-binary @${conf_file}  "http://localhost:8983/solr/${core_name}/${api}"
fi