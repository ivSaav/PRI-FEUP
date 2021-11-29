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
   echo "Syntax: create_core [-h|c|f|p]"
   echo "options:"
   echo "h     help."
   echo "c     core name."
   echo "f     input file."
   echo "p     populate core (0|1)"
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
populate=1


############################################################
# Process the input options. Add options as needed.        #
############################################################
# Get the options
while getopts ":h:c:f:p:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      c) # Enter a name
         core_name=$OPTARG;;
      f) # Enter a name
         in_file=$OPTARG;;
      p)
         populate=0;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

echo ""
echo "[!] Creating $core_name core..."
docker exec pri_proj bin/solr create_core -c $core_name ;

if (( populate ))
then
    echo ""
    echo "[!] Populating $core_name with $in_file"
    curl -X POST -H "Content-type:application/json" --data-binary @${in_file}  "http://localhost:8983/solr/${core_name}/update?commit=true"
fi