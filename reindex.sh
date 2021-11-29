#!/bin/bash

set +v

#!/bin/bash
############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo
   echo "Syntax: reindex [-h|c|s]"
   echo "options:"
   echo "h     help."
   echo "s     schema file (json)."
   echo
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################

# Set variables
core_name="netflix"
in_file="data/imdb_final.json"
schema=0


############################################################
# Process the input options. Add options as needed.        #
############################################################
# Get the options
while getopts ":h:s:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      s)
         schema=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         Help
         exit;;
   esac
done

echo "[!] Deleting previous core"
docker exec pri_proj bin/solr delete -c $core_name ;

# creating core without populating
./create_core.sh -c $core_name -p 0;

if (( $schema ))
then
    # load schema
    echo ""
    echo "[!] Loading schema from ${schema}"
    curl -X POST -H "Content-type:application/json" --data-binary @${schema}  "http://localhost:8983/solr/${core}/schema"
fi

# repopulating core
echo ""
echo "[!] Populating $core_name with $in_file"
curl -X POST -H "Content-type:application/json" --data-binary @${in_file}  "http://localhost:8983/solr/${core_name}/update?commit=true"


echo "Done."