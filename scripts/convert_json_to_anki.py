"""
This script allows the user to create an Anki deck from
a json file formatted in a particular manner. The user
provides command line arguments for the path of the json
file, a deck ID (which must be unique, relative to the
other decks), and the Anki package output path.
"""

import argparse


def convert_json_to_anki(in_path: str, out_path: str):
    """
    Parameters
    ----------
    in_path : str
        Path to Anki decked formatted json file for ingestion.
    out_path : str
        Output path for Anki deck rendered from json file.
    """
    pass


def main(
    in_path: str,
    out_path: str,
) -> None:
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Argument parser for converting a json file to an Anki deck."
        )
    )
    parser.add_argument(
        "--in-path",
        type=str,
        help="Path to Anki decked formatted json file for ingestion.",
    )
    parser.add_argument(
        "--out-path",
        type=str,
        help="Output path for Anki deck rendered from json file.",
    )
    args = parser.parse_args()
    main(**vars(args))
