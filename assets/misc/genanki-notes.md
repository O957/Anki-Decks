### 1. Basic Flashcards
- **Front:** A question or term.
- **Back:** The answer or definition.

```python
model = genanki.Model(
    1607392319,
    'Basic Model',
    fields=[{'name': 'Question'}, {'name': 'Answer'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    }],
)
```

---

### 2. Cloze Deletion Cards
s
- Fill-in-the-blank style cards where parts of a sentence are hidden.

```python
model = genanki.Model(
    1607392320,
    'Cloze Model',
    fields=[{'name': 'Text'}],
    templates=[{
        'name': 'Cloze',
        'qfmt': '{{cloze:Text}}',
        'afmt': '{{cloze:Text}}',
    }],
    css=".cloze { font-weight: bold; color: blue; }",
)

note = genanki.Note(
    model=model,
    fields=["The capital of France is {{c1::Paris}}."]
)
```

---

### 3. Image-Based Cards

- Cards where the front shows an image, and the back provides an explanation.

```python
model = genanki.Model(
    1607392321,
    'Image Model',
    fields=[{'name': 'Image'}, {'name': 'Explanation'}],
    templates=[{
        'name': 'Image Card',
        'qfmt': '<img src="{{Image}}">',
        'afmt': '<img src="{{Image}}"><hr id="answer">{{Explanation}}',
    }],
)

note = genanki.Note(
    model=model,
    fields=["example_image.png", "This is an example image."]
)
```

---

### 4. Audio Cards

- Cards with an audio prompt or answer.

```python
model = genanki.Model(
    1607392322,
    'Audio Model',
    fields=[{'name': 'Audio'}, {'name': 'Answer'}],
    templates=[{
        'name': 'Audio Card',
        'qfmt': '{{Audio}}',
        'afmt': '{{Audio}}<hr id="answer">{{Answer}}',
    }],
)

note = genanki.Note(
    model=model,
    fields=["[sound:example_audio.mp3]", "The answer to the audio prompt."]
)
```

---

### 5. Multi-Field Cards

- Cards with multiple fields (e.g., term, definition, example sentence).

```python
model = genanki.Model(
    1607392323,
    'Multi-Field Model',
    fields=[{'name': 'Term'}, {'name': 'Definition'}, {'name': 'Example'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Term}}',
        'afmt': '{{Term}}<hr id="answer">{{Definition}}<br>{{Example}}',
    }],
)

note = genanki.Note(
    model=model,
    fields=["Photosynthesis", "The process by which green plants use sunlight to synthesize food.", "Example: Plants perform photosynthesis to produce glucose."]
)
```

---

### 6. Reversible Cards

- Cards where both sides can serve as the question.

```python
model = genanki.Model(
    1607392324,
    'Reversible Model',
    fields=[{'name': 'Front'}, {'name': 'Back'}],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
        {
            'name': 'Card 2',
            'qfmt': '{{Back}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Front}}',
        },
    ],
)

note = genanki.Note(
    model=model,
    fields=["What is the capital of France?", "Paris"]
)
```

---

### 7. Diagram Labeling Cards

- Cards that ask for labeling parts of a diagram.

```python
model = genanki.Model(
    1607392325,
    'Diagram Label Model',
    fields=[{'name': 'Image'}, {'name': 'Label'}],
    templates=[{
        'name': 'Label Card',
        'qfmt': '<img src="{{Image}}">',
        'afmt': '<img src="{{Image}}"><br><hr>{{Label}}',
    }],
)

note = genanki.Note(
    model=model,
    fields=["labeled_diagram.png", "Label: mitochondria"]
)
```

---

### 8. Cards with LaTeX

- Cards with math or scientific equations rendered via LaTeX.

```python
model = genanki.Model(
    1607392326,
    'LaTeX Model',
    fields=[{'name': 'Question'}, {'name': 'Answer'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    }],
)

note = genanki.Note(
    model=model,
    fields=["What is the integral of \\(x^2\\)?", "\\(\\int x^2 dx = \\frac{x^3}{3} + C\\)"]
)
```

---

### 9. Multiple Choice Cards

- Cards that include multiple-choice questions.

```python
model = genanki.Model(
    1607392327,
    'Multiple Choice Model',
    fields=[{'name': 'Question'}, {'name': 'Options'}, {'name': 'Answer'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Question}}<br>{{Options}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    }],
)

note = genanki.Note(
    model=model,
    fields=[
        "Which of the following is the capital of France?",
        "A) Berlin<br>B) Paris<br>C) Madrid<br>D) Rome",
        "B) Paris"
    ]
)
```

---

### 10. Custom HTML/CSS Cards

- Cards styled with custom HTML/CSS for unique layouts.

```python
model = genanki.Model(
    1607392328,
    'Custom HTML Model',
    fields=[{'name': 'Front'}, {'name': 'Back'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '<div style="color: blue;">{{Front}}</div>',
        'afmt': '<div style="color: green;">{{Back}}</div>',
    }],
)

note = genanki.Note(
    model=model,
    fields=["What is the chemical formula of water?", "H₂O"]
)
```

---

### 11. Conditional Formatting Cards

- Cards where the appearance changes based on field content.

```python
model = genanki.Model(
    1607392329,
    'Conditional Model',
    fields=[{'name': 'Question'}, {'name': 'Hint'}, {'name': 'Answer'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Question}}<br>{{#Hint}}<small>{{Hint}}</small>{{/Hint}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    }],
)

note = genanki.Note(
    model=model,
    fields=["What is the speed of light?", "Hint: It's in m/s", "299,792,458 m/s"]
)
```
