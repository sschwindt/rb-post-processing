try:
    import sys, os
    import numpy as np
except:
    print("ExceptionERROR: Missing fundamental packages (required: os, sys, logging, random, shutil).")
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import fGlobal as fGl
except:
    print("ExceptionERROR: Cannot find riverpy.")
try:
    import arcpy
except:
    print("ExceptionERROR: arcpy is not available (check license connection?)")
try:
    from arcpy.sa import *
except:
    print("ExceptionERROR: Spatial Analyst (arcpy.sa) is not available (check license?)")


class ArcPyContainer:
    def __init__(self, input_csv=str()):
        """
        :param input_csv: STR of full dir to input csv
        """
        self.csv_file = input_csv
        self.cache = os.path.dirname(os.path.abspath(__file__)) + "/.cache/"
        fGl.chk_dir(self.cache)
        self.csv_name = input_csv.split("\\")[-1].split("/")[-1].split(".csv")[0]
        self.out_dir = os.path.dirname(os.path.abspath(__file__)) + "/output/" + self.csv_name + "/"
        print(" * creating output dir (%s) ..." % self.out_dir)
        fGl.chk_dir(self.out_dir)
        print(" * cleaning output dir ...")
        fGl.clean_dir(self.out_dir)
        self.boundary_shp = self.out_dir + "boundary.shp"
        self.point_shp = self.out_dir + self.csv_name + "_pts.shp"
        self.raster_tif = self.out_dir + self.csv_name + ".tif"
        self.tin = self.out_dir + self.csv_name + "_tin"
        self.sr = arcpy.SpatialReference(26942)

    @fGl.err_info
    @fGl.spatial_license
    def csv2points(self, spatial_ref=26942, x_field_name='X', y_field_name='Y', z_field_name='Z'):
        """
        Converts csv file to point shapefile
        :param spatial_ref: INT of factory code of a SpatialReference. DEFAULT = 26942 (NAD83 California II)
                                > must be a PROJECTED COORDINATE SYSTEM
                                > check docs/projected_coordinate_systems.pdf for more
        :param x_field_name: STR
        :param y_field_name: STR
        :param z_field_name: STR
        :return: None
        """
        print(" * setting spatial reference ...")
        self.sr = arcpy.SpatialReference(spatial_ref)
        arcpy.env.outputCoordinateSystem = self.sr
        print(" * reading %s and creating XYEvent layer ..." % self.csv_file)
        arcpy.MakeXYEventLayer_management(table=self.csv_file, in_x_field=x_field_name, in_y_field=y_field_name,
                                          out_layer=self.csv_name + "_pts",
                                          spatial_reference=self.sr,
                                          in_z_field=z_field_name)
        print(" * converting XYEvent layer to %s ..." % self.point_shp)
        arcpy.FeatureClassToShapefile_conversion(self.csv_name + "_pts", self.out_dir)
        print("   - OK")

    @fGl.err_info
    def make_boundary_shp(self):
        print(" * creating boundary shapefile (%s) ..." % self.boundary_shp)
        print("   - source file: %s" % self.point_shp)
        arcpy.env.workspace = self.out_dir
        arcpy.env.outputCoordinateSystem = self.sr
        arcpy.MinimumBoundingGeometry_management(in_features=self.point_shp, out_feature_class=self.boundary_shp,
                                                 geometry_type="CONVEX_HULL", group_option="ALL")
        print("   - OK")

    @fGl.err_info
    @fGl.threeD_license
    def points2tin(self, field_name="Z", edge_length=200):
        """
        Converts point shapefile to TIN
        :param field_name: STR
        :param edge_length: maximum length of TIN edges
        :return: None
        """
        print(" * converting points to TIN...")
        arcpy.env.workspace = self.out_dir
        arcpy.env.outputCoordinateSystem = self.sr
        arcpy.CreateTin_3d(out_tin=self.tin, in_features=[[self.point_shp, field_name]])
        print(" * clipping edges longer than %s ..." % str(edge_length))
        arcpy.DelineateTinDataArea_3d(in_tin=self.tin, max_edge_length=edge_length, method="PERIMETER_ONLY")
        arcpy.TinDomain_3d(in_tin=self.tin, out_feature_class=self.boundary_shp, out_geometry_type="POLYGON")
        print("   - OK (saved as %s)" % self.tin)

    @fGl.err_info
    @fGl.threeD_license
    def tin2raster(self, interpolation_method="LINEAR", sampling_method="OBSERVATIONS"):
        print(" * converting tin to raster ...")
        arcpy.env.outputCoordinateSystem = self.sr
        arcpy.TinRaster_3d(self.tin, self.raster_tif, data_type="FLOAT", method=interpolation_method,
                           sample_distance=sampling_method, z_factor=1)
        print("   - OK")

    def clean_up(self):
        try:
            print(" * cleaning up ...")
            fGl.clean_dir(self.cache)
            fGl.rm_dir(self.cache)
            print("   - OK")
        except:
            print("WARNING: Failed to clean up .cache folder.")

    def __call__(self, *args, **kwargs):
        print("Class Info: <type> = ArcPyContainer")
        print(dir(self))
