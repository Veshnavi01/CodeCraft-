import pytesseract
from PIL import Image
import requests

def extract_text_from_receipt(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url).json()
    rate = response["rates"].get(to_currency, 1)
    return round(amount * rate, 2)
