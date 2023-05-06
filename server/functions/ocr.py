from bisect import insort

import pytesseract
from PIL import Image
from io import BytesIO


def _is_empty_string(s):
    return len(s) == 0 or s.isspace()


def pytesseract_read_image(image):

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    raw_data = pytesseract.image_to_data(
        image,
        config=r"-c tessedit_char_whitelist=\"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@$%&()-_+=[];:,.?\ \'\"")
    raw_data = [d.split("\t") for d in raw_data.split("\n")[1:] if not _is_empty_string(d.split("\t")[-1])]

    raw_data.sort(key=lambda x: int(x[7]))

    data = {}
    for row in raw_data:
        key = row[2]
        if key not in data:
            data[key] = []
        insort(data[key], (int(row[4]), int(row[5]), row[-1]))

    sentences = []
    for sentence in data.values():
        print(" ".join(word[2] for word in sentence))
        sentences.append(" ".join(word[2] for word in sentence))

    result = ". ".join(sentences)

    if _is_empty_string(result):
        return "No string detected. Maybe try again."
    return result