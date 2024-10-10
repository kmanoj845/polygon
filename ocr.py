import os
import io
from PIL import Image
import cv2
import numpy as np
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

# Load environment variables from .env file
load_dotenv()

# Access the variables
OCR_KEY = os.getenv('OCR_KEY')
ocr_endpoint = "https://cbse-marksocr.cognitiveservices.azure.com/"

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])

# Open the image file and encode it as BytesIO
def imagepath_to_bytes (image):
    with open(image, 'rb' ) as image_file:
        return io.BytesIO(image_file.read())
    
def pil_image_to_bytes(image):
    byte_io = io.BytesIO()
    image.save(byte_io, format='PNG')  # or 'JPEG' if preferred
    byte_io.seek(0)  # Move to the beginning of the BytesIO object
    return byte_io

def validate_image_input(image):
    if isinstance(image, str):  # Image path
        return "imagepath"
    elif isinstance(image, Image.Image):    # image as PIL Image
        return "pilimage"
    else:
        raise TypeError("Input must be a valid image path (string), or a PIL image.")


def get_ocr_data(image):
    image_type = validate_image_input(image)
    if image_type == 'pilimage':
        image = pil_image_to_bytes(image)
    else:
        image = imagepath_to_bytes(image)

    document_analysis_client = DocumentAnalysisClient(
        endpoint=ocr_endpoint, credential=AzureKeyCredential(OCR_KEY)
    )
    poller = document_analysis_client.begin_analyze_document(
            "prebuilt-read", image)
    result = poller.result()

    print("---OCR done---")
    return result

