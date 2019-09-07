try:
    import os, sys, glob
except:
    print("ExceptionERROR: Missing fundamental packages (required:  os, sys, glob).")
try:
    import arcpy
except:
    print("ExceptionERROR: arcpy is not available (check license connection?)")
try:
    from arcpy.sa import *
except:
    print("ExceptionERROR: Spatial Analyst (arcpy.sa) is not available (check license?)")


def threeD_license(func):
    """
    Checks out 3D license and sets workspace to .cache
    :param func: function using arcpy.sa
    :return: wrapper
    """
    def wrapper(*args, **kwargs):
        arcpy.CheckOutExtension('3D')
        chk_dir(os.path.dirname(os.path.abspath(__file__)) + "/.cache/")
        func(*args, **kwargs)
        arcpy.CheckInExtension('3D')
    return wrapper


def chk_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def clean_dir(directory):
    # Delete everything reachable IN the directory named in 'directory',
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if directory == '/', it
    # could delete all your disk files.
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def err_info(func):
    def wrapper(*args, **kwargs):
        arcpy.gp.overwriteOutput = True
        try:
            func(*args, **kwargs)
        except arcpy.ExecuteError:
            print("ExecuteERROR: (arcpy).")
            print(arcpy.GetMessages(2))
            arcpy.AddError(arcpy.GetMessages(2))
        except Exception as e:
            print("ExceptionERROR: (arcpy).")
            print(e.args[0])
            arcpy.AddError(e.args[0])
        except:
            print("ERROR: (arcpy).")
            print(arcpy.GetMessages())
    return wrapper


def rm_dir(directory):
    # Deletes everything reachable from the directory named in 'directory', and the directory itself
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if directory == '/' deletes all disk files
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(directory)


def rm_file(full_name):
    # fullname = str of directory + file name
    try:
        os.remove(full_name)
    except:
        pass


def spatial_license(func):
    """
    Checks out spatial license and sets workspace to .cache
    :param func: function using arcpy.sa
    :return: wrapper
    """
    def wrapper(*args, **kwargs):
        arcpy.CheckOutExtension('Spatial')
        chk_dir(os.path.dirname(os.path.abspath(__file__)) + "/.cache/")
        arcpy.env.workspace = os.path.dirname(os.path.abspath(__file__)) + "/.cache/"
        func(*args, **kwargs)
        arcpy.CheckInExtension('Spatial')
    return wrapper


def verify_shp_file(shapefile):
    # shapefile = STR (full path) of shapefile
    # returns TRUE if the shapefile is NOT EMPTY (has at least one polygon or line)
    try:
        item_number = arcpy.GetCount_management(shapefile)
    except:
        return False
    if item_number > 0:
        return True
    else:
        return False
