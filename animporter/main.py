#!/usr/bin/env python3

from animporter.import_file import import_file
import argparse
import os

def main():
	# parse CLI arguments
	parser = argparse.ArgumentParser(description="Import NPCs from Mine-imator to Minecraft.")
	parser.add_argument("-o", "--output-dir", default=".", help="namespace directory in the datapack")
	parser.add_argument("FILE", nargs="+", help="Mine-imator project file")

	args = parser.parse_args()
	for filename in args.FILE:
		import_file(filename, os.path.realpath(args.output_dir))
	
if __name__ == '__main__':
	main()
