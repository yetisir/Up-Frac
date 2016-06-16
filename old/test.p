parser = argparse.ArgumentParser(description='UpFrac: An Up-Scaling Utility for DEM Simulations')
parser.add_argument('--name', metavar='-n', type=str, nargs='+',
					help='Name of the file containing the model data without the extension')
parser.add_argument('--MPI', dest='accumulate', action='store_const',
					const=sum, default=max,
					help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
