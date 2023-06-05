from paddleocr import PaddleOCR
import json


class OCR:
    def __init__(self, path_to_pdf: str):
        self.path_to_pdf = path_to_pdf

    def extract_text_from_pdf(self) -> list:
        ocr = PaddleOCR(lang='en', cpu_threads='8', use_mp=True)
        extracted_text: list = []
        result = ocr.ocr(self.path_to_pdf, cls=True)
        for page, line_data in enumerate(result):
            extracted_text.append(
                [{"text": line[1][0], "confidence": line[1][1], "position": line[0]} for line in line_data]
            )

        return extracted_text

    def save_extracted_text_to_json(self, output_file: str = 'output.json') -> None:
        print('saving results to JSON')
        transformed_data = {}

        for page, page_data in enumerate(self.extract_text_from_pdf()):
            transformed_data[f"page{page + 1}"] = page_data

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transformed_data, f, ensure_ascii=False, indent=4)
