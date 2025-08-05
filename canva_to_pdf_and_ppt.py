import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PIL import Image
from fpdf import FPDF
from pptx import Presentation
from pptx.util import Inches

# Créer un dossier temporaire pour stocker les captures
OUTPUT_DIR = "screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_pdf_and_ppt(canva_url):
    # Options pour exécution dans un environnement serveur
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Lancer le navigateur
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(canva_url)

    time.sleep(5)  # Laisse le temps à la page de charger

    # Capture d'écran de la page entière
    screenshot_path = os.path.join(OUTPUT_DIR, "canva_capture.png")
    driver.save_screenshot(screenshot_path)

    driver.quit()

    # --- PDF ---
    pdf = FPDF()
    pdf.add_page()
    pdf.image(screenshot_path, x=10, y=10, w=pdf.w - 20)
    pdf_path = os.path.join(OUTPUT_DIR, "output.pdf")
    pdf.output(pdf_path)

    # --- PPTX ---
    prs = Presentation()
    slide_layout = prs.slide_layouts[6]  # slide vide
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.add_picture(screenshot_path, Inches(0), Inches(0), width=prs.slide_width)
    pptx_path = os.path.join(OUTPUT_DIR, "output.pptx")
    prs.save(pptx_path)

    return pdf_path, pptx_path
