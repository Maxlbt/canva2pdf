import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pptx import Presentation
from pptx.util import Inches
from fpdf import FPDF
from PIL import Image

def generate_pdf_and_ppt(canva_url, num_slides, output_folder, pdf_filename, ppt_filename):
    # 1. Configuration du navigateur headless
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    try:
        # 2. Accès à l’URL Canva
        driver.get(canva_url)
        time.sleep(5)

        # 3. Activation du mode plein écran si besoin (facultatif selon Canva)
        # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.F11)

        # 4. Capture des captures d’écran
        image_paths = []
        for i in range(num_slides):
            image_path = os.path.join(output_folder, f"slide_{i+1}.png")
            driver.save_screenshot(image_path)
            image_paths.append(image_path)

            # Simule flèche droite pour passer au slide suivant
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)
            time.sleep(1)

        # 5. Création du PDF
        pdf = FPDF()
        for image in image_paths:
            img = Image.open(image)
            width, height = img.size
            pdf.add_page()
            pdf.image(image, x=0, y=0, w=210, h=297)
        pdf.output(os.path.join(output_folder, pdf_filename))

        # 6. Création du PowerPoint
        prs = Presentation()
        blank_slide_layout = prs.slide_layouts[6]
        for image in image_paths:
            slide = prs.slides.add_slide(blank_slide_layout)
            left = top = Inches(0)
            pic = slide.shapes.add_picture(image, left, top, width=prs.slide_width, height=prs.slide_height)
        prs.save(os.path.join(output_folder, ppt_filename))

    finally:
        driver.quit()
