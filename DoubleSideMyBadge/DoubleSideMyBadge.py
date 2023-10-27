# ASCII Art at the start of the script
ASCII_ART = r"""

█████████████████████████████████████████████████████████████
█▄─▄▄▀█─▄▄─█▄─██─▄█▄─▄─▀█▄─▄███▄─▄▄─███─▄▄▄▄█▄─▄█▄─▄▄▀█▄─▄▄─█
██─██─█─██─██─██─███─▄─▀██─██▀██─▄█▀███▄▄▄▄─██─███─██─██─▄█▀█
▀▄▄▄▄▀▀▄▄▄▄▀▀▄▄▄▄▀▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▄▄▄▀▀▀▄▄▄▄▄▀▄▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀
███████████████████████████████████████▀███████
█▄─▀█▀─▄█▄─█─▄███▄─▄─▀██▀▄─██▄─▄▄▀█─▄▄▄▄█▄─▄▄─█
██─█▄█─███▄─▄█████─▄─▀██─▀─███─██─█─██▄─██─▄█▀█
▀▄▄▄▀▄▄▄▀▀▄▄▄▀▀▀▀▄▄▄▄▀▀▄▄▀▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀▄▄▄▄▄▀
                    
"""
print(ASCII_ART)

from fpdf import FPDF
import pdf2image
import sys
from tqdm import tqdm
from io import BytesIO
import os
from datetime import datetime


def make_double_sided_fpdf(input_pdf_path, output_pdf_path):
    # Ensure the /tmp subfolder exists
    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    # Convert PDF pages to images with high DPI
    pages = pdf2image.convert_from_path(input_pdf_path, dpi=300)
    print(f"Number of pages detected: {len(pages)}")

    # Create a new PDF instance
    pdf = PDF(unit='mm')
    image_counter = 0

    # Loop through pages with progress bar
    for image in tqdm(pages, desc="Processing pages", ncols=100):

        # Calculate the dimensions in mm (considering DPI)
        new_width = image.width * 25.4 / 300  # assuming 300 DPI
        new_height = image.height * 25.4 / 300  # assuming 300 DPI

        # Set the PDF page size based on the image dimensions
        pdf.add_page(format=(new_width, 2 * new_height))

        # Convert the image to PNG (lossless format) and save temporarily
    
        temp_image_path_upper = f"tmp/temp_image_upper_{image_counter}.png"
        temp_image_path_lower = f"tmp/temp_image_lower_{image_counter}.png"

        
        image.save(temp_image_path_upper, format="PNG")
        image.rotate(180).save(temp_image_path_lower, format="PNG")

        # Place the original image on the upper half and the rotated image on the lower half
        pdf.image(name=temp_image_path_upper, x=0, y=0, w=new_width, h=new_height, link='')
        pdf.image(name=temp_image_path_lower, x=0, y=new_height, w=new_width, h=new_height, link='')

        # Remove the temporary images
        os.remove(temp_image_path_upper)
        os.remove(temp_image_path_lower)

        image_counter += 1


    # Save the resulting double-sided PDF
    pdf.output(output_pdf_path)

class PDF(FPDF):
    def header(self):
        pass  # No header

    def footer(self):
        pass  # No footer

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 DoubleSideMyBadge.py input.pdf")
        sys.exit(1)

    # Get the current timestamp in the desired format
    timestamp = datetime.now().strftime('%y%m%d%H%M')
    
    input_pdf_path = sys.argv[1]
    output_pdf_path = f"{timestamp}_DoubleSided_{input_pdf_path.split('/')[-1]}"
    make_double_sided_fpdf(input_pdf_path, output_pdf_path)

    print(f"\nDouble-sided PDF saved as {output_pdf_path}")
