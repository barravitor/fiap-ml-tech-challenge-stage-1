# app/services/selenium_script.py
import ast
import asyncio
import time
import pandas as pd
from datetime import datetime, timezone
from requests import Session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from concurrent.futures import ThreadPoolExecutor
from .file_service import remove_file_by_path, check_if_file_exists, create_folder_does_not_exist
from .productions_service import ProductionsService
from .processingn_service import ProcessingnService
from .commercialization_service import CommercializationService
from .exportation_service import ExportationService
from .importation_service import ImportationService
from .scrapre_status_service import ScrapeStatusService
from app.db.db import SessionLocal
from app.config import EXTERNAL_URL, SELENIUM_DRIVE_ARGS, MAX_YEAR_DATE, PAGE_LOADING_WAITING_TIME_IN_SECONDS, PAGE_MAX_RETRY, PAGE_RETRY_DELAY_TIME_IN_SECONDS, PRODUCTION

# Configuração manual para criar e fechar a sessão
def get_session_local():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_selenium_drive():
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'

    try:
        args = ast.literal_eval(SELENIUM_DRIVE_ARGS)
    except:
        args = []

    for arg in args:
        options.add_argument(arg)

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_generic_tables(tab, dynamic_fields, startingYear = 1970):
    if not tab:
        print("Error: 'tab' is required!")
        return
    
    if not len(dynamic_fields):
        print("Error: 'dynamic_fields = []' is required!")
        return
    
    start_time = time.time()
    current_time = datetime.now()
    csv_file_path = f"./tmp/{tab}-{str(current_time.timestamp())}.csv"

    if not check_if_file_exists("./tmp"):
        create_folder_does_not_exist("./tmp")

    attempt = 0
    year = startingYear
    last_category=""

    driver = get_selenium_drive()

    while (year <= int(MAX_YEAR_DATE)):
        sub_tab = 1
        csv_itens = []

        print(f"Processing data from tab {tab}, subtab {sub_tab}, of year {year}")

        if attempt >= int(PAGE_MAX_RETRY):
            break

        while True:
            try:
                driver.get(f"{EXTERNAL_URL}?ano={year}&opcao={tab}&subopcao=subopt_0{sub_tab}")

                time.sleep(float(PAGE_LOADING_WAITING_TIME_IN_SECONDS))

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
                            "created_at": datetime.now(timezone.utc),
                        }

                        for index, _ in enumerate(dynamic_fields):
                            csv_element_item[dynamic_fields[index]] = cells[index].text

                        csv_itens.append(csv_element_item)

                attempt = 0
                if len(total_btn_on_page) == 0 or sub_tab >= len(total_btn_on_page):
                    break

                sub_tab += 1
            except WebDriverException as e:
                if attempt >= int(PAGE_MAX_RETRY):
                    break

                attempt += 1
                print(f"Tentativa {attempt} falhou: {e}. Tentando novamente em {PAGE_RETRY_DELAY_TIME_IN_SECONDS} segundos...")
                time.sleep(float(PAGE_RETRY_DELAY_TIME_IN_SECONDS))

        df = pd.DataFrame(csv_itens)

        if year == startingYear:
            df.to_csv(csv_file_path, mode='w', index=False, header=True)
        else:
            df.to_csv(csv_file_path, mode='a', index=False, header=False)

        year += 1

    driver.quit()

    if attempt >= int(PAGE_MAX_RETRY):
        return

    print(f"Time to run: {(time.time() - start_time):.2f} in seconds")

    return csv_file_path

def run_scrape(name: str, tab, dynamic_fields, db: Session):
    scrape = ScrapeStatusService.get_document_by_name(db=db, name=name)

    if scrape.running:
        return None

    ScrapeStatusService.start_scrape(db=db, name=name)

    csv_file_path = get_generic_tables(tab=tab, dynamic_fields=dynamic_fields)

    if not csv_file_path:
        return

    ScrapeStatusService.finished_scrape(db=db, name=name)

    return csv_file_path

def get_productions():
    try:
        key = "productions"
        tab="opt_02"
        dynamic_fields=["name", "amount_liters"]

        print(f"Start get_{key} web scraping...")

        db = next(get_session_local())

        csv_file_path = run_scrape(key, tab, dynamic_fields, db=db)

        if csv_file_path != None:
            df = pd.read_csv(csv_file_path)

            if df.empty:
                print("Data not found")
                return
            
            print("Update data on database...")
            ProductionsService.delete_documents(db)
            ProductionsService.insert_many_documents(db, df.to_dict(orient='records'))
            remove_file_by_path(csv_file_path)

        db.close()

        print(f"Finish get_{key} web scraping...")
    except Exception as e:
        print(f"Error to scrape data: {e}")

def get_processingn():
    try:
        key = "processingn"
        tab="opt_03"
        dynamic_fields=["name", "amount_kg"]

        print(f"Start get_{key} web scraping...")

        db = next(get_session_local())

        csv_file_path = run_scrape(key, tab, dynamic_fields, db=db)

        if csv_file_path != None:
            df = pd.read_csv(csv_file_path)

            if df.empty:
                print("Data not found")
                return
            
            print("Update data on database...")
            ProcessingnService.delete_documents(db)
            ProcessingnService.insert_many_documents(db, df.to_dict(orient='records'))
            remove_file_by_path(csv_file_path)

        db.close()

        print(f"Finish get_{key} web scraping...")
    except Exception as e:
        print(f"Error to scrape data: {e}")

def get_commercialization():
    try:
        key = "commercialization"
        tab="opt_04"
        dynamic_fields=["name", "amount_liters"]

        print(f"Start get_{key} web scraping...")

        db = next(get_session_local())

        csv_file_path = run_scrape(key, tab, dynamic_fields, db=db)

        if csv_file_path != None:
            df = pd.read_csv(csv_file_path)

            if df.empty:
                print("Data not found")
                return
            
            print("Update data on database...")
            CommercializationService.delete_documents(db)
            CommercializationService.insert_many_documents(db, df.to_dict(orient='records'))
            remove_file_by_path(csv_file_path)

        db.close()

        print(f"Finish get_{key} web scraping...")
    except Exception as e:
        print(f"Error to scrape data: {e}")

def get_importation():
    try:
        key = "importation"
        tab="opt_05"
        dynamic_fields=["country", "amount_kg", "price_us"]

        print(f"Start get_{key} web scraping...")

        db = next(get_session_local())

        csv_file_path = run_scrape(key, tab, dynamic_fields, db=db)

        if csv_file_path != None:
            df = pd.read_csv(csv_file_path)

            if df.empty:
                print("Data not found")
                return
            
            print("Update data on database...")
            ImportationService.delete_documents(db)
            ImportationService.insert_many_documents(db, df.to_dict(orient='records'))
            remove_file_by_path(csv_file_path)

        db.close()

        print(f"Finish get_{key} web scraping...")
    except Exception as e:
        print(f"Error to scrape data: {e}")

def get_exportation():
    try:
        key = "exportation"
        tab="opt_06"
        dynamic_fields=["country", "amount_kg", "price_us"]

        print(f"Start get_{key} web scraping...")

        db = next(get_session_local())

        csv_file_path = run_scrape(key, tab, dynamic_fields, db=db)

        if csv_file_path != None:
            df = pd.read_csv(csv_file_path)

            if df.empty:
                print("Data not found")
                return
            
            print("Update data on database...")
            ExportationService.delete_documents(db)
            ExportationService.insert_many_documents(db, df.to_dict(orient='records'))
            remove_file_by_path(csv_file_path)

        db.close()

        print(f"Finish get_{key} web scraping...")
    except Exception as e:
        print(f"Error to scrape data: {e}")

async def scrape_data():
    print(PRODUCTION)
    if not PRODUCTION:
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(executor, get_productions),
                loop.run_in_executor(executor, get_commercialization),
                loop.run_in_executor(executor, get_processingn),
                loop.run_in_executor(executor, get_importation),
                loop.run_in_executor(executor, get_exportation),
            ]

            await asyncio.gather(*futures)
    else:
        await asyncio.to_thread(get_productions)
        await asyncio.to_thread(get_commercialization)
        await asyncio.to_thread(get_processingn)
        await asyncio.to_thread(get_importation)
        await asyncio.to_thread(get_exportation)

def start_scrape():
    asyncio.create_task(scrape_data())

