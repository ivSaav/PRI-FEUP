#!/bin/bash

set +v

schema_folder="schema_conf"

# Add schema filename to this array
# If the schema requires a xml config add -x <path/to/config.xml>
cmdarr=(
    "schema_cast.json"
    "schema_enums.json -x $schema_folder/enumsConfig.xml"
    "schema_numeric.json"
)

# reset core
./root_scripts/delete.sh netflix
./root_scripts/create_core.sh netflix

for cmd in "${cmdarr[@]}"
do
    ./root_scripts/load_conf.sh -s $schema_folder/$cmd
done

echo "Done."