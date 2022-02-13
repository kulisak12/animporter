#!/usr/bin/env python3

from animporter.create_files import create_template_file
from animporter.import_file import import_file, print_error
import argparse
import json


def main():
    # parse CLI arguments
    parser = argparse.ArgumentParser(
        description="Import NPCs from Mine-imator to Minecraft.")
    parser.add_argument("-o", "--output-dir", default=".",
                        help="directory where functions should be created")
    parser.add_argument("FILE", nargs="*", help="Mine-imator project file")
    parser.add_argument("-t", "--template", action='store_true',
                        help="create a template function to spawn the NPC")

    args = parser.parse_args()
    for filename in args.FILE:
        try:
            import_file(filename, args.output_dir)
        except FileNotFoundError as e:
            print_error(e.filename + ": No such file or directory")
        except json.decoder.JSONDecodeError:
            print_error(filename + ": Not a valid Mine-imator file")
        except KeyError as e:
            print_error(filename + ": Not a recognized Mine-imator file (missing entry: '" + e.args[0] + "')")

    if args.template:
        try:
            create_template_file(args.output_dir)
        except FileNotFoundError as e:
            print_error(e.filename + ": No such file or directory")


if __name__ == '__main__':
    main()
