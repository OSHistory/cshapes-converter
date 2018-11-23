
"""
Iterate over all features and create a timestamp 
for start and end date. Also records each 
date change to create a list of date 
snapshots for output.
"""

import argparse
import datetime
import os
import json 
import sys 

# props: property dict from feature 
# mode: COW or GW (see below)
# _type: s (start) or e (end)
def create_datetime(props, mode, _type):
    try:
        return datetime.date(
            props[mode + _type.upper() + "YEAR"],
            props[mode + _type.upper() + "MONTH"],
            props[mode + _type.upper() + "DAY"]
        )
    except ValueError:
        return None
        # return datetime.date(1900,1,1)

def find_nearest_date_cut(date_cuts, target_date):
    # Check if target date in range
    if target_date > date_cuts[0] or target_date < date_cuts[len(date_cuts)-1]:
        # return value before first date_cut greater than target (or last item)
        for idx, date_cut in enumerate(date_cuts):
            if date_cut > target_date:
                return date_cuts[idx - 1]
        return date_cuts[len(date_cuts) - 1]

    else: 
        print("Target date out of range {start} - {end}".format(
            start=date_cuts[0], 
            end=date_cuts[len(date_cuts)-1]
        ))
        sys.exit(1)

def get_matching_feature(feature_list, date_cut):
    return [
        feature["orig"] for feature in feature_list 
            if feature["start"] <= date_cut 
                and
            feature["end"] >= date_cut 
    ]

def write_to_geojson(out_path, name, match_features):
    with open(out_path, "w+") as fh_out:
        json.dump({
            "type": "FeatureCollection",
            "name": "cshapes " + name,
            "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
            "features": match_features
        },
        fh_out)
        print("Written {num} features to {path}.".format(
            num=len(match_features),
            path=out_path)
        )

ap = argparse.ArgumentParser(
    description="Generate easy to use geofiles from the cshapes-project data",
)

ap.add_argument("-d", "--date", default=None, 
    help="Date formatted as YYYY-MM-DD. If not set all timestamps will be exported (roughly 1.3 GB)")
ap.add_argument("-m", "--mode", default="COW",
    help="COW ('Correlates of War') or GW (Gleditsch and Ward (1999)), refer to the cshapes documentation")
ap.add_argument("-f", "--file", default=None,
    help="Write result to file (overrides option base-dir)")
ap.add_argument("-b", "--base-dir", default="out/",
    help="Output directory")

args = ap.parse_args()

# MODE (either COW or GW)
# See original dataset description for details
MODE = args.mode


with open("data/cshapes.geojson") as fh:
    geo_data = json.load(fh)

# a list of all date-cuts (will create the 
# timestamp layers)
date_cuts = []

# a list of features (objects)
# with start and end datetime objects 
# to filter the original geojson 
# for later reexport
feature_list = []

for feature in geo_data["features"]:
    props = feature["properties"]
    start_dt = create_datetime(props, MODE, 'S')
    end_dt = create_datetime(props, MODE, 'E')

    if start_dt is not None and start_dt not in date_cuts:
        date_cuts.append(start_dt)
    if end_dt is not None and end_dt not in date_cuts:
        date_cuts.append(end_dt)
    if start_dt is not None and end_dt is not None:
        feature_obj = {
            "orig": feature,
            "start": start_dt,
            "end": end_dt
        }
        feature_list.append(feature_obj)

date_cuts.sort()

if args.date is not None:
    try:
        date_parts = args.date.split("-")
        target_date = datetime.date(
            int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
        )
    except:
        print("Failed to parse date: " + args.date)
        print("Exiting")
        sys.exit(1)

    date_cut = find_nearest_date_cut(date_cuts, target_date)
    match_features = get_matching_feature(feature_list, date_cut)
    if args.file is None:
        name = str(date_cut).replace("-", "_")
        out_path = os.path.join(
            args.base_dir, name + ".geojson"
        )

    else: 
        out_path = args.file
        name = os.path.basename(out_path).replace(".geojson", "")

    write_to_geojson(out_path, name, match_features)

# No date set => iterate over all breakpoints
else:
    for date_cut in date_cuts:
        print("Generating " + str(date_cut))
        match_features = get_matching_feature(feature_list, date_cut)
        name = str(date_cut).replace("-", "_")
        out_path = os.path.join(args.base_dir, name + ".geojson")
        write_to_geojson(out_path, name, match_features)