"""
Script for converting Markdown files
(possibly with LaTeX) into Anki decks.

Usage:
python3 convert_md_to_anki.py "../input_decks/test_deck.md"
"Understanding_Analysis" "../output_decks/math_deck.apkg"

"""

# %% LIBRARIES

import argparse
import os
import re

import genanki

# %% FUNCTIONS


def parse_markdown(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    # split questions and answers
    pattern = r"##\s*(.+?)\n(.+?)(?=\n##|$)"
    matches = re.findall(pattern, content, re.DOTALL)
    cards = [(q.strip(), a.strip()) for q, a in matches]
    return cards


def create_anki_deck(cards, deck_name):
    model = genanki.Model(
        1607392319,
        "Simple Model",
        fields=[{"name": "Question"}, {"name": "Answer"}],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
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
    deck = genanki.Deck(2059400110, deck_name)
    for question, answer in cards:
        note = genanki.Note(model=model, fields=[question, answer])
        deck.add_note(note)
    return deck


def save_deck(deck, output_path):
    """
    Saves the Anki deck to an .apkg file.
    """
    genanki.Package(deck).write_to_file(output_path)


# %% EXECUTION


def main():

    parser = argparse.ArgumentParser(
        description="Convert a Markdown file into an Anki deck."
    )
    parser.add_argument("md_file", help="Path to the Markdown file.")
    parser.add_argument("deck_name", help="Name of the Anki deck.")
    parser.add_argument("out_file", help="Path to save the .apkg file.")
    args = parser.parse_args()
    if not os.path.isfile(args.md_file):
        raise FileNotFoundError(
            f"The input file '{args.md_file}' does not exist."
        )
    output_dir = os.path.dirname(args.out_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"Created output directory: {output_dir}")
    cards = parse_markdown(args.md_file)
    anki_deck = create_anki_deck(cards, deck_name=args.deck_name)
    save_deck(anki_deck, args.out_file)
    print(f"Deck saved to {args.out_file}")


if __name__ == "__main__":
    main()
