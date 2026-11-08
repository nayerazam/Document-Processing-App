"""Basic Word replacement engine. Complex document elements may not be covered."""
from datetime import datetime
from pathlib import Path
import re
from docx import Document


def replace_in_paragraph(paragraph, old_text: str, new_text: str) -> int:
    # Using paragraph.text catches words split across runs, but rebuilding
    # the paragraph can discard run-level formatting and inline objects.
    pattern = re.compile(re.escape(old_text), re.IGNORECASE)
    updated, count = pattern.subn(lambda _: new_text, paragraph.text)
    if count:
        paragraph.text = updated
    return count


def replace_in_container(container, old_text: str, new_text: str) -> int:
    count = sum(replace_in_paragraph(p, old_text, new_text)
                for p in container.paragraphs)
    for table in container.tables:
        for row in table.rows:
            for cell in row.cells:
                count += replace_in_container(cell, old_text, new_text)
    return count


def process_word_file(input_path: str, instruction: str, output_folder='output') -> str:
    match = re.fullmatch(r'\s*replace\s+(.+?)\s+with\s+(.+?)\s*', instruction,
                         flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return 'No changes made. Use: replace old text with new text'
    old_text, new_text = match.group(1).strip(), match.group(2).strip()
    if not old_text:
        return 'No changes made: search text is empty.'

    doc = Document(input_path)
    count = replace_in_container(doc, old_text, new_text)
    for section in doc.sections:
        count += replace_in_container(section.header, old_text, new_text)
        count += replace_in_container(section.footer, old_text, new_text)

    if count == 0:
        return (f'No changes made: "{old_text}" was not found in supported '
                'paragraphs, tables, headers, or footers. Text in shapes/text boxes '
                'may require Microsoft Word automation.')

    folder = Path(output_folder)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    destination = folder / f'edited_{stamp}_{Path(input_path).name}'
    try:
        doc.save(destination)
    except PermissionError:
        return 'Could not save: close the output document in Microsoft Word and retry.'
    return (f'Word file saved at: {destination.resolve()}\n'
            f'Text searched: {old_text}\nReplacement text: {new_text}\n'
            f'Replacements made: {count}\n'
            'Note: formatting in edited paragraphs may change.')
