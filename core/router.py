def select_route(input_type: str, output_type: str) -> str:
    output = output_type.lower()
    if input_type in ('image', 'pdf') and output == 'word':
        return 'image_to_word'
    if input_type in ('image', 'pdf') and output == 'excel':
        return 'image_to_excel'
    if input_type == 'docx' and output == 'word':
        return 'edit_word'
    if input_type == 'xlsx' and output == 'excel':
        return 'edit_excel'
    return 'unsupported'
