# app/services/selenium_script.py
import os
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import time

EXTERNAL_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"
MAX_YEAR_DATE=2023

def get_file_path(file_name):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    tmp_dir = os.path.join(project_root, 'tmp')

    os.makedirs(tmp_dir, exist_ok=True)

    return os.path.join(tmp_dir, file_name)

def write_to_csv(data, file_name):
    """
    Escreve uma lista de dicionários em um arquivo CSV.

    :param data: Lista de dicionários com os dados a serem escritos
    :param file_name: Nome do arquivo CSV a ser criado
    """
    if not data:
        print("Nenhum dado para escrever.")
        return

    headers = data[0].keys()

    file_path = get_file_path(file_name)

    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for entry in data:
            writer.writerow(entry)

    return file_path

def get_selenium_drive():
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_generic_table(tab, file_name):
    if not tab or not file_name:
        print("Erro: 'tab' and 'file_name' are required.")
        return

    year = 1970
    category = ""
    data = []

    driver = get_selenium_drive()

    while (year <= MAX_YEAR_DATE):
        driver.get(f"{EXTERNAL_URL}?ano={year}&opcao={tab}")
        time.sleep(3)

        try:
            table = driver.find_element(By.CSS_SELECTOR, 'table.tb_base.tb_dados')
            print("Tabela encontrada!")
        except Exception as e:
            print(f"Erro ao encontrar a tabela: {e}")

        if 'table' in locals():
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")

                if not cells:
                    continue

                class_name = cells[0].get_attribute('class') if cells else "Element not found"

                if (class_name == "Element not found"):
                    continue

                if (class_name == "tb_item"):
                    category = cells[0].text

                data.append({
                    "name": cells[0].text,
                    "category": "Total" if cells[0].text == "Total" else category,
                    "amount": cells[1].text,
                    "date": datetime.strptime(f"{year}-12-21", "%Y-%m-%d").date(),
                    "created_at": datetime.utcnow(),
                })

        year += 1

    write_to_csv(data, file_name)
    driver.quit()

def get_products():
    print("Start get_products web scraping...")
    get_generic_table(tab="opt_02", file_name="commercialization.csv")
    print("Finish get_products web scraping...")

def get_commercialization():
    print("Start get_commercialization web scraping...")
    get_generic_table(tab="opt_04", file_name="products.csv")
    print("Finish get_commercialization web scraping...")

def scrape_data():
    with ThreadPoolExecutor() as executor:
        executor.submit(get_products)
        executor.submit(get_commercialization)