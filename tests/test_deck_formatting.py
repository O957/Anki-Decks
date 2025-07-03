"""
Tests the formatting of Anki decks (as json or parquet) to
ensure that there are not issues on the Anki platform.
"""

import json
import pathlib

import polars as pl

DECK_DIR = pathlib.Path(__file__).parent.parent / "raw_decks"
MEDIA_JSON = (
    pathlib.Path(__file__).parent.parent / "assets" / "media_files.json"
)

deck_files = list(DECK_DIR.rglob("*.json")) + list(DECK_DIR.rglob("*.parquet"))
assert deck_files, f"No deck files found in {DECK_DIR}."


def _load_entries(path):
    """
    Load entries from a deck file. Supports two JSON formats:
      - A list of entry dicts at the root, or
      - A dict with keys 'deck_name', 'deck_id', and 'entries'.
    Also supports Parquet files where each row is an entry.
    Returns a list of entry dicts.
    """
    if path.suffix == ".json":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "entries" in data:
            return data["entries"]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError(
                f"Unexpected JSON structure in {path}: root should be a "
                "list or a dict with 'entries'."
            )
    else:
        df = pl.read_parquet(path)
        return df.to_dicts()


def _load_deck_id(path):
    """
    Extracts the top-level deck_id from a JSON or Parquet
    deck file. Returns the deck_id as an int, or None if
    not present.
    """
    if path.suffix == ".json":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "deck_id" in data:
            return int(data["deck_id"])
        return None


def test_no_missing_ids():
    """
    Tests each deck to ensure that there are no missing
    ids across entries.
    """
    for deck in deck_files:
        entries = _load_entries(deck)
        ids = sorted(int(e["id"]) for e in entries)
        if not ids:
            continue
        start, end = ids[0], ids[-1]
        full = set(range(start, end + 1))
        missing = full - set(ids)
        assert not missing, (
            f"Missing id(s) in deck {deck.name}: {sorted(missing)}"
        )


def test_no_duplicate_ids():
    """
    Tests each deck to ensure that there are no duplicate
    ids across entries.
    """
    for deck in deck_files:
        entries = _load_entries(deck)
        ids = [e["id"] for e in entries]
        dupes = {x for x in ids if ids.count(x) > 1}
        assert not dupes, (
            f"Duplicate id(s) in deck {deck.name}: {sorted(dupes)}"
        )


def test_entries_have_sources():
    """
    Tests each deck to ensure that all entries have sources.
    """
    for deck in deck_files:
        entries = _load_entries(deck)
        for e in entries:
            sid = e.get("id", "<no-id>")
            assert e.get("source_abbr"), (
                f"Entry {sid} in {deck.name} missing source_abbr"
            )


def test_no_unused_media_file():
    """
    Tests each media listed in the manifest is associated
    with some entry across decks.
    """
    # load the media manifest
    with open(MEDIA_JSON, encoding="utf-8") as mf:
        media_files = set(json.load(mf))

    referenced = set()
    for deck in deck_files:
        entries = _load_entries(deck)
        for e in entries:
            name = e.get("image_name")
            if name:
                referenced.add(name)

    unused = media_files - referenced
    assert not unused, (
        f"Unused media files found in manifest: {sorted(unused)}"
    )


def test_no_nonexistent_media_file():
    """
    Tests each entry with a media file to ensure that the
    media file actually exists in the manifest.
    """
    with open(MEDIA_JSON, encoding="utf-8") as mf:
        media_files = set(json.load(mf))

    for deck in deck_files:
        entries = _load_entries(deck)
        for e in entries:
            name = e.get("image_name")
            if name:
                assert name in media_files, (
                    f"Entry {e.get('id', '<no-id>')} in {deck.name} "
                    f"references missing media '{name}' not listed in "
                    "media_manifest"
                )


def test_both_image_name_and_mode():
    """
    Tests each entry has either no image name and mode or
    has both an image name and mode.
    """
    for deck in deck_files:
        entries = _load_entries(deck)
        for e in entries:
            name = e.get("image_name", "")
            mode = e.get("image_mode", "")
            assert bool(name) == bool(mode), (
                f"Entry {e.get('id', '<no-id>')} in {deck.name} "
                "must have both image_name and image_mode or neither"
            )


def test_verify_image_modes():
    """
    Ensures that if image_mode is nonempty, then it is one
    of back, front, back_text.
    """
    valid = {"back", "front", "back_text"}
    for deck in deck_files:
        entries = _load_entries(deck)
        for e in entries:
            mode = e.get("image_mode", "")
            if mode:
                assert mode in valid, (
                    f"Entry {e.get('id', '<no-id>')} in {deck.name} "
                    f"has invalid image_mode '{mode}'"
                )


def test_unique_deck_ids():
    """
    Ensures that each deck file has a unique top-level
    deck_id.
    """
    deck_ids = []
    for deck in deck_files:
        did = _load_deck_id(deck)
        if did is not None:
            deck_ids.append(did)
    dupes = {x for x in deck_ids if deck_ids.count(x) > 1}
    assert not dupes, (
        f"Duplicate deck_id(s) across deck files: {sorted(dupes)}"
    )
