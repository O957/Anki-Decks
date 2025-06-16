# Personal Anki Decks

_The author's personal Anki workflow, making use of genanki._

NOTE:

* This repository is a work in progress.
* This repository has been made by the author mostly for the author.

## Basic Usage

Create, within `raw_decks`, a `json` file in the following format:

```json
{
  "deck_name": "2020_ITPATFR_Benton",
  "deck_id": 2000,
  "entries": [
    {
      "id": "0001",
      "question": "What are fossils?",
      "answer": "The remains or traces of any organism that lived in the geological past. In general only the hard parts of organisms become fossilized (e.g. bones, teeth, shells, and wood) but under certain circumstances the entire organism is preserved."
    }
  ]
}
```

```
python3 ./scripts/convert_json_to_anki.py
--in-path  "./raw_decks/2020_ITPATFR_Benton.json"
--out-path "./output/2020_ITPATFR_Benton.apkg"
```

## Standards

* The author uses the folder `raw_decks` for deck `json` files.
* The author uses the folder `rendered_decks` for `.apkg` files.
* The author names Anki deck files the most recent publish or copyright date with the first letter of every word followed by the last name of the first author.[^example]
* The author does not change the deck name or IDs but does change the question and answer content (which Anki will update).
* The author only uses the fields Question and Answer, for now.

[^example]: For example, Introduction To Paleobiology And The Fossil Record Edition 2, which was produced in 2020 and written by Benton, Michael J and Harper, David AT, would be `2020_ITPATFR_Benton.json`.


## Deck List (Books)

(all decks at present are pending)

* Introduction To Paleobiology And The Fossil Record Edition 2
* Forecasting Principles And Practice Edition 3
* Basic Mathematics

## Deck List (Papers)

(all decks at present are pending)
