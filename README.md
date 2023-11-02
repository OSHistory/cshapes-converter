# DEPRECATED

**Functionality provided by cshapes maintainers at https://cshapes.ethz.ch/**

# README 

This project generates snapshots from the GIS-Data provided 
by the [cshapes project](http://nils.weidmann.ws/projects/cshapes.html),
see also [this article](
https://www.tandfonline.com/doi/abs/10.1080/03050620903554614).

The cshapes project aims to map the territoriality of sovereign 
states from past-WWII to the present (2016).

The original data is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Please follow the citation guidelines of the cshape project. 

## C-Shape Version 

The data originates from the shape-files provided with 
the [R-package](http://nils.weidmann.ws/projects/cshapes/r-package.html).

Current Version is 0.6

## Examples 

Export all differing timestamps in the default output-directory, using 
default mode "Correlates of War" (roughly 1.3 Gb)

~~~
python3 slice-geojson-by-time.py
~~~

Write a geojson file to `/tmp` with the second of march, 1978 as 
timestamp. Use the "Gleditsch and Ward (1999), GW" mode. 

~~~
python3 slice-geojson-by-time.py -m "GW" -f "/tmp/cow-1978-03-02.geojson" -d "1978-03-02"
~~~
