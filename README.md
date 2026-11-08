# Document Processing App

Early-stage Python desktop application for document conversion and editing.

## Currently working
- Tkinter interface: select input, choose Word or Excel output, enter instruction.
- File-type detection and routing.
- Basic Word `.docx` case-insensitive find/replace in paragraphs, tables, headers and footers.
- Unique output filenames and replacement counts.

## Not yet implemented
- Image/PDF to Word or Excel (OCR integration).
- Excel editing.
- Natural-language instruction understanding beyond `replace X with Y`.
- Faithful formatting preservation. Replacement may remove character formatting in changed paragraphs.
- Word text boxes, shapes and other advanced document elements.

## Run on Windows
Install Python 3.11+, then from the project directory:

```bat
python -m pip install -r requirements.txt
python app.py
```

For Word editing, choose a `.docx` input and Word output, then enter an instruction such as:

```text
replace Nayer with Ahmed
```

Check the `output` folder for the edited document. A zero-match result does **not** imply the word is absent from every part of the document; advanced Word elements may not be accessible through this basic engine.

## GitHub upload without Git
Create an empty GitHub repository and upload the files and `core`/`gui` folders using **Add file → Upload files**. Do not upload private documents, virtual environments or test data.
