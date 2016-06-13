import argparse
parser = argparse.ArgumentParser(description='UpFrac: An Up-Scaling Utility for DEM Simulations')
parser.add_argument('-n', '--name', required=True ,help='Name of the file containing the model data without the extension')

args = parser.parse_args()
print(args.name)
