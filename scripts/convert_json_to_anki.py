"""
This script allows the user to create an Anki deck from
a formatted `json` file. The `json` file path, unique deck
ID, and Anki deck output path must be provided as command
line arguments. Many of the templates used below come from:
https://github.com/kerrickstaley/genanki (2025-06-15).
Image mode options include "back, back_text, front"
"""

import argparse
import json
import logging
import pathlib
import re

import genanki

# initiate logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def anki_note(question, answer, model, entry, image_name):
    # apply latex conversion from $ to Anki supported tex
    question = re.sub(r"\$\$(.+?)\$\$", r"\\[\1\\]", question, flags=re.DOTALL)
    question = re.sub(r"\$(.+?)\$", r"\\(\1\\)", question, flags=re.DOTALL)
    answer = re.sub(r"\$\$(.+?)\$\$", r"\\[\1\\]", answer, flags=re.DOTALL)
    answer = re.sub(r"\$(.+?)\$", r"\\(\1\\)", answer, flags=re.DOTALL)

    # make into genanki note
    if image_name == "":
        note = genanki.Note(
            model=model,
            fields=[question, answer],
            guid=str(entry["id"]),
        )
    else:
        note = genanki.Note(
            model=model,
            fields=[question, answer, f"<img src={image_name}>"],
            guid=str(entry["id"]),
        )

    return note


def get_media_file_names(media_path):
    if not media_path.exists() or not media_path.is_dir():
        raise ValueError(
            f"Media path does not exist or is not a directory: {media_path}"
        )
    media_files = [
        str(file) for file in media_path.iterdir() if file.is_file()
    ]
    return media_files


def convert_json_to_anki(in_path: str, out_path: str, media_path: str) -> None:
    """
    Parameters
    ----------
    in_path : str
        Path to Anki decked formatted json file for ingestion.
    out_path : str
        Output path for Anki deck rendered from json file.
    """

    # as pathlib
    file_path = pathlib.Path(in_path)
    out_path = pathlib.Path(out_path)
    media_path = pathlib.Path(media_path)

    # ingest anki-ready json file
    with open(in_path, encoding="utf-8") as f:
        json_deck = json.load(f)
        logger.info(f"Uploaded:\n{file_path.name}")

    # retrieve deck name and deck ID from file
    deck_name = json_deck.get("deck_name")
    deck_id = json_deck.get("deck_id")
    logger.info(f"Deck Named: {deck_name}")

    # define the empty anki deck
    deck = genanki.Deck(deck_id=deck_id, name=deck_name)
    logger.info("Created GenAnki Deck.")

    # get media files and add to deck
    media_files = get_media_file_names(media_path)
    anki_pkg = genanki.Package(deck)
    anki_pkg.media_files = media_files

    # define css for all decks (copied from somewhere I can't recall)
    deck_css = """
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
    """

    # define genanki non-image deck model
    non_image_model = genanki.Model(
        deck_id + 1,
        f"Non-Image {deck_name} Model",
        fields=[{"name": "Question"}, {"name": "Answer"}],
        templates=[
            {
                "name": "Default",
                "qfmt": "{{Question}}",
                "afmt": "{{FrontSide}}<hr id='answer'>{{Answer}}",
            },
        ],
        css=deck_css,
    )
    logger.info("Non-Image Deck Model Created.")

    # define genanki image (on front) deck model
    image_front_model = genanki.Model(
        deck_id + 2,
        f"Image {deck_name} Model",
        fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Media"}],
        templates=[
            {
                "name": "Image On Front",
                "qfmt": "{{Question}}<br>{{Media}}",
                "afmt": "{{FrontSide}}<hr id='answer'>{{Answer}}",
            },
        ],
    )

    # define genanki image (on front) deck model
    image_back_model = genanki.Model(
        deck_id + 3,
        f"Image {deck_name} Model",
        fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Media"}],
        templates=[
            {
                "name": "Image On Back",
                "qfmt": "{{Question}}",
                "afmt": "{{FrontSide}}<hr id='answer'>{{Media}}",
            },
        ],
    )

    # define genanki image (on front) deck model
    image_back_text_model = genanki.Model(
        deck_id + 4,
        f"Image {deck_name} Model",
        fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Media"}],
        templates=[
            {
                "name": "Image On Back With Text",
                "qfmt": "{{Question}}",
                "afmt": "{{FrontSide}}<hr id='answer'>{{Answer}}<br>{{Media}}",
            },
        ],
    )

    # image model for use in note creation
    image_models = {
        "front": image_front_model,
        "back": image_back_model,
        "back_text": image_back_text_model,
    }

    # iterate through json rows and input entries
    for entry in json_deck.get("entries", []):
        if entry.get("include", True):
            # get question and answer from json
            question = entry["question"]
            answer = entry["answer"]
            image_name = entry.get("image_name", "")

            if image_name == "":
                note = anki_note(
                    question=question,
                    answer=answer,
                    model=non_image_model,
                    entry=entry,
                    image_name=image_name,
                )
            else:
                image_mode = entry.get("image_mode", "front")
                note = anki_note(
                    question=question,
                    answer=answer,
                    model=image_models[image_mode],
                    entry=entry,
                    image_name=image_name,
                )
            deck.add_note(note)

    # create the deck from genanki notes
    anki_pkg.write_to_file(out_path)
    logger.info(f"Deck {deck_name} Written To {out_path}.")


def main(in_path: str, out_path: str, media_path: str) -> None:
    convert_json_to_anki(in_path, out_path, media_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Argument parser for converting a `json` file to an Anki deck."
        )
    )
    parser.add_argument(
        "--in-path",
        type=str,
        help="Path to Anki decked formatted `json` file for ingestion.",
    )
    parser.add_argument(
        "--out-path",
        type=str,
        help="Output path for Anki deck rendered from `json` file.",
    )
    parser.add_argument(
        "--media-path",
        type=str,
        help="Path to any media files used in the deck.",
    )
    args = parser.parse_args()
    main(**vars(args))
