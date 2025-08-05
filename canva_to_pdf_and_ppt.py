import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
from fpdf import FPDF
from pptx import Presentation
from pptx.util import Inches

def generate_pdf_and_ppt(canva_url, output_format, pdf_path=None, ppt_path=None, num_slides=30):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(canva_url)
    time.sleep(10)

    images = []
    for i in range(int(num_slides)):
        image_path = f"/tmp/slide_{i + 1}.png"
        driver.save_screenshot(image_path)
        images.append(image_path)
        driver.execute_script("document.dispatchEvent(new KeyboardEvent('keydown', {'key': 'ArrowRight'}));")
        time.sleep(0.5)

    driver.quit()

    if output_format == "pdf" and pdf_path:
        pdf = FPDF()
        for image in images:
            pdf.add_page()
            pdf.image(image, x=0, y=0, w=210, h=297)
        pdf.output(pdf_path)

    if output_format == "pptx" and ppt_path:
        prs = Presentation()
        blank_slide_layout = prs.slide_layouts[6]

        for image in images:
            slide = prs.slides.add_slide(blank_slide_layout)
            slide.shapes.add_picture(image, Inches(0), Inches(0), width=prs.slide_width)
        prs.save(ppt_path)

    for image in images:
        os.remove(image)
