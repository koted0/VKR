from typing import Dict, List
from ocr_text_corrector import CorrectOCR


def process_text(json_data: Dict[str, List[Dict[str, List]]]) -> str:
    """
    Processes OCR data obtained from PaddleOCR and stored in a JSON file.

    This function takes a dictionary loaded from a JSON file as input. The dictionary should have the following structure:
    {
        "page1": [
            {
                "text": "Line 1 text",
                "confidence": 0.99,
                "position": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            },
            ...
        ],
        ...
    }

    The function processes the OCR data and merges lines that are a continuation of each other to preserve the
    original structure of the text. If the confidence of a line is below 0.95, the text is checked for spelling
    errors using the CorrectOCR class.

    :param json_data: A dictionary loaded from a JSON file containing OCR data obtained from PaddleOCR.
    :return: A string containing the processed text with preserved original structure.
    """
    threshold = 50
    result = []
    for page in json_data.values():
        page_result = []
        prev_line = page[0]['text']
        if page[0]['confidence'] < 0.95:
            prev_line = CorrectOCR.check_spelling(prev_line)
        for i in range(1, len(page)):
            current_line = page[i]['text']
            if page[i]['confidence'] < 0.95:
                current_line = CorrectOCR.check_spelling(current_line)
            prev_end_x = page[i - 1]['position'][1][0]
            current_start_x = page[i]['position'][0][0]
            prev_y = page[i - 1]['position'][0][1]
            current_y = page[i]['position'][0][1]
            if abs(current_start_x - prev_end_x) < threshold and abs(current_y - prev_y) < threshold:
                if prev_line.endswith('-'):
                    prev_line = prev_line.removesuffix('-') + current_line
                else:
                    prev_line += ' ' + current_line
            else:
                page_result.append(prev_line)
                prev_line = current_line
        page_result.append(prev_line)
        result.append('\n'.join(page_result))
    return '\n\n'.join(result)