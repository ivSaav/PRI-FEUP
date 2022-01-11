#!/bin/bash

set +v

conf_folder="solr_conf"

# Add schema filename to this array
# If the schema requires a xml config add -x <path/to/config.xml>
schema_arr=(
    "schema_member.json -x $conf_folder/name_synonyms.txt"
    #"schema_enums.json -x $conf_folder/enumsConfig.xml"
    "schema_genre_type.json"
    "schema_kind.json -x $conf_folder/kind_synonyms.txt"
    "schema_numeric.json"
    "schema_country_lang.json"
    "schema_title.json -x $conf_folder/dims_synonyms.txt"
    "schema_plot.json -x $conf_folder/stopwords_en.txt"
    "suggest_field.json"
)

# reset core
./root_scripts/delete.sh netflix
./root_scripts/create_core.sh netflix



# load schema configs
for cmd in "${schema_arr[@]}"
do
    ./root_scripts/load_conf.sh -f $conf_folder/$cmd
done

# load init paramns config
./root_scripts/load_conf.sh -f $conf_folder/init_params.json -a config

echo "Done."