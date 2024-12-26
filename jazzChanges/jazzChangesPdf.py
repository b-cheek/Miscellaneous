from PIL import Image
import io
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"

import pymupdf # imports the pymupdf library
doc = pymupdf.open("JazzChanges.pdf") # open a document
for page in doc: # iterate the document pages
    text = page.get_text() # get plain text encoded as UTF-8
    img = Image.open(io.BytesIO(page.get_pixmap().pil_tobytes(format="WEBP"))) # get an image of the page
    print(text) # print the text
    # img.show() # show the image
    ocr_text = pytesseract.image_to_string(img) # perform OCR on the image
    print(ocr_text) # print the OCR text
    input("Press Enter to continue...") # wait for the user to press Enter

    # Debugging
    # Save the image
    # img.save("page.png") # save the image as a PNG file