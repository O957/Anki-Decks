"""
Tests the formatting of Anki decks (as json or parquet) to
ensure that there are not issues on the Anki platform.
"""

import pathlib

DECK_DIR = pathlib.Path(__file__).parent.parent / "raw_decks"
MEDIA_DIR = pathlib.Path(__file__).parent.parent.parent / "Anki-Decks-Media"

deck_files = list(DECK_DIR.rglob("*.json")) + list(DECK_DIR.rglob("*.parquet"))
assert deck_files, f"No deck files found in {DECK_DIR}."


def test_no_missing_ids():
    """
    Tests each deck to ensure that there are no missing
    ids across entries.
    """
    pass


def test_no_duplicate_ids():
    """
    Tests each deck to ensure that there are no duplicate
    ids across entries.
    """
    pass


def test_entries_have_sources():
    """
    Tests each deck to ensure that all entries have sources.
    """
    pass
