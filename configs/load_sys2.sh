#!/bin/bash

set +v

conf_folder="milestone2"
core_name="netflix_ml2"

# Add schema filename to this array
# If the schema requires a xml config add -x <path/to/config.xml>
schema_arr=(
    "schema_member.json -x $conf_folder/name_synonyms.txt"
    #"schema_enums.json -x $conf_folder/enumsConfig.xml"
    "schema_genre_type.json"
    "schema_numeric.json"
    "schema_country_lang.json"
    "schema_title.json -x $conf_folder/stopwords_simple.txt"
    "schema_plot.json -x $conf_folder/stopwords_en.txt"
)

# reset core
./delete.sh $core_name
./create_core.sh $core_name

# load init paramns config
./load_conf.sh -f $conf_folder/init_params.json -a config -c $core_name

# load schema configs
for cmd in "${schema_arr[@]}"
do
    ./load_conf.sh -f $conf_folder/$cmd -c $core_name
done

echo "Done."