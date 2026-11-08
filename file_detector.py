from pathlib import Path


def detect_file_type(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext in {'.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'}:
        return 'image'
    if ext == '.pdf':
        return 'pdf'
    if ext == '.docx':
        return 'docx'
    if ext == '.xlsx':
        return 'xlsx'
    return 'unsupported'
