from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fpdf import FPDF
from pptx import Presentation
from pptx.util import Inches
import time
import os


def generate_pdf_and_ppt(canva_url, output_folder, pdf_filename="output.pdf", ppt_filename="output.pptx"):
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"  # ✅ chemin requis sur Render
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    # Lance le navigateur
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Charge la page Canva
    driver.get(canva_url)
    time.sleep(5)  # ⏳ laisse le temps à Canva de charger les éléments

    # Capture des screenshots des slides
    slides = driver.find_elements("css selector", '[data-testid="page"]')
    screenshots = []
    for i, slide in enumerate(slides):
        driver.execute_script("arguments[0].scrollIntoView(true);", slide)
        time.sleep(1)
        path = os.path.join(output_folder, f"slide_{i+1}.png")
        slide.screenshot(path)
        screenshots.append(path)

    driver.quit()

    # Génère le PDF
    pdf = FPDF()
    for img_path in screenshots:
        pdf.add_page()
        pdf.image(img_path, x=10, y=10, w=190)
    pdf_output_path = os.path.join(output_folder, pdf_filename)
    pdf.output(pdf_output_path)

    # Génère le PPTX
    ppt = Presentation()
    blank_slide_layout = ppt.slide_layouts[6]
    for img_path in screenshots:
        slide = ppt.slides.add_slide(blank_slide_layout)
        slide.shapes.add_picture(img_path, Inches(0), Inches(0), width=Inches(10))
    ppt_output_path = os.path.join(output_folder, ppt_filename)
    ppt.save(ppt_output_path)
