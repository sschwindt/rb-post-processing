try:
    import os, sys
except:
    print("ExceptionERROR: Missing fundamental packages (required: os, sys).")

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import cArcPyContainer as cAPC
except:
    print("ExceptionERROR: Cannot find riverpy.")

# define global variables
global own_dir
own_dir = os.path.dirname(os.path.abspath(__file__)) + "/"


def run(input_csv="SRVtopo.csv"):
    """
    :param input_csv: STR of csv file with XYZ data
                        > example: input_csv="SRVtopo.csv" (default example)
                        > csv file MUST BE STORED IN /input/ folder
    :return: None
    """
    post_processor = cAPC.ArcPyContainer(own_dir + "input/" + input_csv)
    post_processor.csv2points()
    post_processor.make_boundary_shp()
    post_processor.points2tin()
    post_processor.tin2raster()
    post_processor.clean_up()
    print("Finished.")


if __name__ == '__main__':
    csv_name = str(input(" Please enter csv file name with XYZ data (e.g., \'SRVtopo.csv\')\n >> "))
    run()
