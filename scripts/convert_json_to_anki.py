"""
This script allows the user to create an Anki deck from
a json file formatted in a particular manner. The user
provides command line arguments for the path of the json
file, a deck ID (which must be unique, relative to the
other decks), and the Anki package output path.
"""

import argparse
import json

import genanki


def convert_json_to_anki(in_path: str, out_path: str) -> None:
    """
    Parameters
    ----------
    in_path : str
        Path to Anki decked formatted json file for ingestion.
    out_path : str
        Output path for Anki deck rendered from json file.
    """

    # ingest anki-ready json file
    with open(in_path, encoding="utf-8") as f:
        deck = json.load(f)
    # retrieve deck name and deck ID from file
    deck_name = deck.get("deck_name")
    deck_id = deck.get("deck_id")
    # create base genanki model w/ Question/Answer fields
    model = genanki.Model(
        deck_id,
        f"{deck_name} Model",
        fields=[{"name": "Question"}, {"name": "Answer"}],
    )
    print(f"Genanki model created: {deck_name} Model")
    # iterate through json rows and input entries
    for entry in deck.get("entries", []):
        note = genanki.Note(
            model=model,
            fields=[entry["question"], entry["answer"]],
            guid=str(entry["id"]),
        )
        deck.add_note(note)
    # create the deck from genanki notes
    genanki.Package(deck).write_to_file(out_path)
    print(f"The genanki deck {deck_name} has been written to:\n{out_path}")


def main(
    in_path: str,
    out_path: str,
) -> None:
    convert_json_to_anki(in_path, out_path)


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
