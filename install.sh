#!/bin/bash


# reset core
./root_scripts/delete.sh netflix_base
./root_scripts/create_core.sh netflix_base

./root_scripts/index.sh -c netflix_base