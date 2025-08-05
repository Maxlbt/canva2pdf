import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fpdf import FPDF
from pptx import Presentation
from pptx.util import Inches
from PIL import Image
import requests
from io import BytesIO

def generate_pdf_and_ppt(canva_url, num_slides, output_folder, pdf_filename, ppt_filename):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(canva_url)

    time.sleep(5)

    images = []

    for i in range(int(num_slides)):
        time.sleep(0.5)
        image_url = f"https://fakeimage.canva.com/slide{i+1}.png"
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            images.append(img)

    pdf = FPDF()
    for img in images:
        img_path = os.path.join(output_folder, "temp_img.jpg")
        img.save(img_path)
        pdf.add_page()
        pdf.image(img_path, x=10, y=10, w=190)
    pdf_output_path = os.path.join(output_folder, pdf_filename)
    pdf.output(pdf_output_path, "F")

    prs = Presentation()
    blank_slide_layout = prs.slide_layouts[6]
    for img in images:
        slide = prs.slides.add_slide(blank_slide_layout)
        image_stream = BytesIO()
        img.save(image_stream, format='PNG')
        image_stream.seek(0)
        slide.shapes.add_picture(image_stream, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)
    ppt_output_path = os.path.join(output_folder, ppt_filename)
    prs.save(ppt_output_path)

    driver.quit()
