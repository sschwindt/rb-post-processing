**Requirements**: *Python3 conda* environment of [*ArcGIS Pro*](https://www.esri.com/en-us/arcgis/products/arcgis-pro/resources) with *Advanced license*, *Spatial Analyst*, and *3D* extensions. With the *ArcGIS Pro* dependency, the codes can only be run on Windows.

***

Folder and file summary:

 - **/input/**
	 + Store here River Builder *.csv* output files with XYZ coordinates.
	 + The standard download includes a sample file called *SRVtopo.csv*.
 - **/output/**
	 + Results will be produced in a subfolder named after the provided *.csv* file.
	 + *Visualize.aprx* enables the visualization of output geodata with [*ArcGIS Pro*](https://www.esri.com/en-us/arcgis/products/arcgis-pro/resources).
 - **cArcPyContainer.py** runs `arcpy` routines for converting *.csv* XYZ point files to geospatial data.
 - **fGlobal** provides folder management and envelop functions.
 - **rb-post-processor.py** runs the program.


***


## Usage
There are several options to run the code and here is one of them.

1. Download the repository and save the contents to a local folder (e.g., *D:\Python\rb-post-processing*).
2. Store the River Builder *.csv* output file in the */input/* folder (e.g., *D:\Python\rb-post-processing/SRVtopo.csv*).
3. Open *ArcGIS Pro*'s *Python3 conda* environment (typical location: *C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe*).
4. In the Python window, enter:

``` python
import os, sys
code_folder = "D:/Python/rb-post-processing/"  # REPLACE WITH FOLDER WHERE THIS REPOSITORY IS STORED
sys.path.append(code_folder)
import rb_post_processor
rb_post_processor.run("SRVtopo.csv")  # REPLACE SRVtopo.csv WITH THE PROVIDED .CSV FILE NAME
```

If *ArcGIS Pro*'s *Python3 conda* is defined as the standard application for running (opening) *.py* files, alternatively, steps 3. and 4. can be replaced with just double-clicking on *D:\Python\rb-post-processing/rb_post_processor.py* (or wherever the repository is locally stored). The code will then prompt a request for entering the *.csv* file name in the *Python* window.

***

## Output

*`rb_post_processor.run("CSV_NAME.csv")`* produces geospatial data files, named after the provided *.csv* file in the folder */output/CSV_NAME/*. For example, if the *.csv* file name is *SRVtopo.csv*, then *`CSV_NAME=SRVtopo`*. The following files are subsequently produced:

1. *CSV_NAME_pts.shp*: A point shapefile containing the points provided in *CSV_NAME.csv*.
2. *boundary.shp*: A polygon shapefile containing the minimum outer boundary of the provided points. The file is produced using the [`Convex_Hull` argument in `arcpy`'s Minimum Bounding Geometry](https://pro.arcgis.com/en/pro-app/tool-reference/data-management/minimum-bounding-geometry.htm). *Note: This method works not satisfactorily. Consider using a CONCAVE HULL method instead, as provided [here](https://community.esri.com/blogs/richard_fairhurst/2015/06/11/bruce-harolds-concave-hull-estimator-tool-enhanced). Programmatic CONCAVE HULL methods are available for [QGIS and the `gdal` package](https://docs.qgis.org/3.4/de/docs/user_manual/processing_algs/qgis/vectorgeometry.html#concave-hull-alpha-shapes).*
3. *CSV_NAME_tin/*: A TIN object created from *CSV_NAME_pts.shp*, where all perimeter edges with a length of more than 400 (meters) are removed. To modify the default value, please refer to the [Options](#Options) section. *Note: The `Convex_Hull` is not able to clip a TIN better than the clip method itself. Therefore, the code uses `arcpy.DelineateTinDataArea_3d` to remove long, unwanted edges.*
5. *CSV_NAME.tif*: A *GeoTIFF* raster created from *CSV_NAME_tin/*.

*Note: Re-running `rb_post_processor.run("CSV_NAME.csv")` for the same shapefile will overwrite previous results.*

The results can be visualized by opening the *ArcGIS Pro* project */output/Visualize.aprx*.

***

## Options
The functions of the `ArcPyContainer` class (*cArcPyContainer.py*) enable adaptive usage of the code. To modify default values (e.g., for the spatial reference or the TIN edge cropping length), open *rb_post_processor.py* in an editor. Here are some options for adapting variables:

|VARIABLE| USAGE| EXPLANATION |
|:-------|:----:|:------------|
|Spatial reference|`post_processor.csv2points(spatial_ref=INT)`| An *Integer* number of a [projected coordinate system](http://desktop.arcgis.com/en/arcmap/10.3/guide-books/map-projections/about-projected-coordinate-systems.htm). Use the *WKID* number listed in this [PDF document](http://desktop.arcgis.com/en/arcmap/10.3/guide-books/map-projections/pdf/projected_coordinate_systems.pdf) to set the `spatial_ref` variable. The default value is `spatial_ref=26942` (i.e., the metric `NAD_1983_StatePlane_California_II_FIPS_0402`).|
|TIN crop edge length|`post_processor.points2tin(edge_length=Double)`| Define the edge lengths that will be deleted from the TIN. The default value is 400 (meters). If you are unsure which value to use, open the output TIN in *ArcGIS Pro* and measure the lengths of edges you want to keep or delete. Define the desired threshold value and re-run `rb_post_processor.run("CSV_NAME.csv")`.|
|Field names|`post_processor.csv2points(x_field_name='X', y_field_name='Y', z_field_name='Z')` and `post_processor.points2tin(self, field_name="Z")`| Modify the field names according to the column names of *CSV_NAME.csv*.|




