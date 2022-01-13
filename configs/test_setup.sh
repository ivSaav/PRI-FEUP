#!/bin/bash

set +v

./load_sys2.sh & ./load_sys3.sh ;

./index.sh -c netflix & ./index.sh -c netflix_ml2

echo "Done."