"""
This script allows the user to create an Anki deck from
a json file formatted in a particular manner. The user
provides command line arguments for the path of the json
file, a deck ID (which must be unique, relative to the
other decks), and the Anki package output path.
"""

import argparse
import json
import re

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
        json_deck = json.load(f)
    # retrieve deck name and deck ID from file
    deck_name = json_deck.get("deck_name")
    deck_id = json_deck.get("deck_id")
    # define the empty anki deck
    deck = genanki.Deck(deck_id=deck_id, name=deck_name)
    # create base genanki model w/ Question/Answer fields
    model = genanki.Model(
        deck_id,
        f"{deck_name} Model",
        fields=[{"name": "Question"}, {"name": "Answer"}],
        # see https://github.com/kerrickstaley/genanki for more on this
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": "{{FrontSide}}<hr id='answer'>{{Answer}}",
            },
        ],
        # copied from another answer, so might be incorrect
        css="""
            .card {
                font-family: arial;
                font-size: 20px;
                text-align: left;
                color: black;
                background-color: white;
            }
            .latex {
                font-size: 18px;
            }
        """,
    )
    print(f"Genanki model created: {deck_name} Model")
    # iterate through json rows and input entries
    for entry in json_deck.get("entries", []):
        # get question and answer from json
        question = entry["question"]
        answer = entry["answer"]

        # apply latex conversion from $ to Anki supported tex
        question = re.sub(
            r"\$\$(.+?)\$\$", r"\\[\1\\]", question, flags=re.DOTALL
        )
        question = re.sub(r"\$(.+?)\$", r"\\(\1\\)", question, flags=re.DOTALL)
        answer = re.sub(r"\$\$(.+?)\$\$", r"\\[\1\\]", answer, flags=re.DOTALL)
        answer = re.sub(r"\$(.+?)\$", r"\\(\1\\)", answer, flags=re.DOTALL)
        # make into genanki note
        note = genanki.Note(
            model=model,
            fields=[question, answer],
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
