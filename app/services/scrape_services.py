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
import pandas as pd
from .production_service import ProductionService
from app.db.db import SessionLocal

# Configuração manual para criar e fechar a sessão
def get_session_local():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

EXTERNAL_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"
MAX_YEAR_DATE=2023
PAGE_LOADING_WAITING_TIME_IN_SECONDS=3

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

def get_generic_tables(tab, dynamic_fields):
    if not tab:
        print("Error: 'tab' is required!")
        return
    
    if not len(dynamic_fields):
        print("Error: 'dynamic_fields = []' is required!")
        return

    year = 1970
    csv_itens = []
    last_category=""

    driver = get_selenium_drive()

    while (year <= MAX_YEAR_DATE):
        sub_tab = 1

        while True:
            driver.get(f"{EXTERNAL_URL}?ano={year}&opcao={tab}&subopcao=subopt_0{sub_tab}")
            time.sleep(PAGE_LOADING_WAITING_TIME_IN_SECONDS)

            total_btn_on_page = driver.find_elements(By.CSS_SELECTOR, '.btn_sopt')

            if len(total_btn_on_page) > 0:
                last_category = total_btn_on_page[sub_tab - 1].text

            try:
                table = driver.find_element(By.CSS_SELECTOR, 'table.tb_base.tb_dados')
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

                    if (class_name == "tb_item" and len(total_btn_on_page) == 0):
                        last_category = cells[0].text

                    current_category = last_category

                    if cells[0].text == "Total" and len(total_btn_on_page) == 0:
                        current_category = "Total"

                    csv_element_item = {
                        "category": current_category,
                        "date": datetime.strptime(f"{year}-12-21", "%Y-%m-%d").date(),
                        "created_at": datetime.utcnow(),
                    }

                    for index, _ in enumerate(dynamic_fields):
                        csv_element_item[dynamic_fields[index]] = cells[index].text

                    csv_itens.append(csv_element_item)

            if len(total_btn_on_page) == 0 or sub_tab >= len(total_btn_on_page):
                break

            sub_tab += 1

        year += 1

    driver.quit()
    return csv_itens

def get_productions():
    try:
        print("Start get_productions web scraping...")
        db = next(get_session_local())

        productions = get_generic_tables(tab="opt_02", dynamic_fields=["name", "amount_liters"])
        df = pd.DataFrame(productions[0:], columns=productions[0])
        df.to_csv("./tmp/productions.csv", index=False, header=True, sep=',', encoding='utf-8')

        ProductionService.insert_many(db, productions)

        print("Finish get_productions web scraping...")
    except Exception as e:
        print(f"Error to get_productions: {e}")

def get_processingn():
    print("Start get_processingn web scraping...")
    get_generic_tables(tab="opt_03", dynamic_fields=["name", "amount_kg"], file_name="processingn.csv")
    print("Finish get_processingn web scraping...")

def get_commercialization():
    print("Start get_commercialization web scraping...")
    get_generic_tables(tab="opt_04", dynamic_fields=["name", "amount_liters"], file_name="commercialization.csv")
    print("Finish get_commercialization web scraping...")

def get_importation():
    print("Start get_importation web scraping...")
    get_generic_tables(tab="opt_05", dynamic_fields=["country", "amount_kg", "price_us"], file_name="importation.csv")
    print("Finish get_importation web scraping...")

def get_exportation():
    print("Start get_exportation web scraping...")
    get_generic_tables(tab="opt_06", dynamic_fields=["country", "amount_kg", "price_us"], file_name="exportation.csv")
    print("Finish get_exportation web scraping...")

def scrape_data():
    with ThreadPoolExecutor() as executor:
        executor.submit(get_productions)
        # executor.submit(get_commercialization)
        # executor.submit(get_processingn)
        # executor.submit(get_importation)
        # executor.submit(get_exportation)
