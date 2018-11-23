#!/bin/bash 

GPKG_PATH="out/cshapes.gpkg"

first=0
for geojson in out/*geojson; do 
    echo $geojson
    tab_name=$(basename $geojson)
    tab_name=${tab_name%%.geojson}
    echo $tab_name
    if [ $first -eq 0 ]; then
        mode="-overwrite"
        first=1
    else 
        mode="-append"
    fi 
    ogr2ogr -f GPKG -nln $tab_name $mode $GPKG_PATH $geojson
done 