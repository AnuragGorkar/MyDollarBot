import google.generativeai as genai
from PIL import Image
import json
import ast
from datetime import datetime
import helper
from jproperties import Properties
import requests
from io import BytesIO

configs = Properties()

with open('user.properties', 'rb') as read_prop:
    configs.load(read_prop)

api_token = str(configs.get('api_token').data)
gemini_api_key = str(configs.get('gemini_api_key').data)

_gemini_model = None

def initialize_gemini():
    """Initialize Gemini AI model"""
    global _gemini_model
    if not _gemini_model:
        genai.configure(api_key=gemini_api_key)
        _gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    return _gemini_model

def process_receipt_image(file_url):
    """Process receipt image using Gemini AI"""
    try:
        model = initialize_gemini()

        # Download and convert to PIL Image
        response = requests.get(file_url)
        img = Image.open(BytesIO(response.content))

        current_date = datetime.now()

        # Format it to YYYY-MM-DD
        formatted_date = current_date.strftime('%Y-%m-%d')

        print(helper.getSpendCategories())
        prompt = (
            "You will be given an image of a receipt. Please analyze it and extract the following information:\n"
            f"1. Date of the receipt (format: YYYY-MM-DD) if there is no date, use the current date: {formatted_date}\n"
            "2. Total amount (numeric value only, with two decimal places if applicable)\n"
            f"3. Analyse the receipt and check for keywords to determine the category of the bill (choose from the following options with brief descriptions): {helper.getSpendCategories()}\n"
            "If the image is not a receipt, return this exact JSON format: {'is_receipt': False}.\n"
            "If it is a receipt but any information is unclear, use the following defaults:\n"
            f"   - For unclear date: use the current date.{formatted_date}\n"
            "   - For unclear category: use 'Miscellaneous'.\n\n"
            "Return the data in this exact JSON format:\n"
            "{'is_receipt': True, 'date': 'YYYY-MM-DD', 'amount': float_value, 'category': 'category_name'}\n"
            "Ensure there are no extra characters, spaces, or formatting issues outside the JSON structure."
        )

            
        response = model.generate_content([prompt, img])
        response_text = response.text.strip()
        print("Gemini response text:", response_text)
        
        # Ensure response is JSON-compatible
        if not (response_text.startswith("{") and response_text.endswith("}")):
            return None, "Invalid response format from Gemini. Ensure output is JSON-compatible."

        
        try:
            # Attempt fallback parsing using ast.literal_eval
            result = ast.literal_eval(response_text)
            # print("Parsed using ast.literal_eval:", result)
        except (ValueError, SyntaxError):
            return None, "Image cannot be processed. Please upload again or try with a different image."
                
        # Validate parsed data structure
        if not result.get('is_receipt', False):
            return None, "Image does not appear to be a receipt"
        
        # Validate and correct the category if needed
        if result['category'] not in helper.getSpendCategories():
            result['category'] = 'Miscellaneous'
        
        return result, None

    except Exception as e:
        return None, f"Error processing receipt: {str(e)}"
