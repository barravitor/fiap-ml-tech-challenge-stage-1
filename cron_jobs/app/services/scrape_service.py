# app/services/scrape_service.py
import ast
import asyncio
import time
import pandas as pd
from datetime import datetime, timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from shared.services.index_service import ProductionsService, ProcessingnService, CommercializationService, ExportationService, ImportationService
from shared.db.database import get_session_local
from shared.config import EXTERNAL_URL, SELENIUM_DRIVE_ARGS, MAX_YEAR_DATE, PAGE_LOADING_WAITING_TIME_IN_SECONDS, PAGE_MAX_RETRY, PAGE_RETRY_DELAY_TIME_IN_SECONDS

async def get_selenium_drive():
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'

    try:
        args = ast.literal_eval(SELENIUM_DRIVE_ARGS)
    except Exception as e:
        print(f"Error parsing SELENIUM_DRIVE_ARGS: {e}")
        args = []

    for arg in args:
        options.add_argument(arg)

    process = await asyncio.create_subprocess_exec(
        'google-chrome', '--version',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()

    version = ""

    if process.returncode == 0:
        version = stdout.decode('utf-8').strip().split(" ")[-1]

    try:
        driver = await asyncio.to_thread(webdriver.Chrome, service=Service(ChromeDriverManager(driver_version=version).install()), options=options)
        return driver
    except Exception as e:
        print(f"Error creating Selenium driver: {e}")
        return None

async def get_generic_tables(tab, dynamic_fields, startingYear=1970) -> pd.DataFrame | None:
    try:
        start_time = time.time()

        if not tab:
            print("Error: 'tab' is required!")
            return
        
        if not len(dynamic_fields):
            print("Error: 'dynamic_fields = []' is required!")
            return

        driver = await get_selenium_drive()

        if not driver:
            return
        
        attempt = 0
        year = startingYear
        last_category = ""

        df = pd.DataFrame()

        while year <= int(MAX_YEAR_DATE):
            sub_tab = 1
            csv_items = []

            print(f"Processing data from tab {tab}, subtab {sub_tab}, of year {year}")

            if attempt >= int(PAGE_MAX_RETRY):
                break

            while True:
                try:
                    # await asyncio.to_thread(driver.get, f"{EXTERNAL_URL}?ano={year}&opcao={tab}&subopcao=subopt_0{sub_tab}")
                    driver.get(f"{EXTERNAL_URL}?ano={year}&opcao={tab}&subopcao=subopt_0{sub_tab}")

                    await asyncio.sleep(float(PAGE_LOADING_WAITING_TIME_IN_SECONDS))

                    total_btn_on_page = driver.find_elements(By.CSS_SELECTOR, '.btn_sopt')

                    if len(total_btn_on_page) > 0:
                        last_category = total_btn_on_page[sub_tab - 1].text

                    try:
                        table = driver.find_element(By.CSS_SELECTOR, 'table.tb_base.tb_dados')
                    except Exception as e:
                        print(f"Error finding the table: {e}")

                    if 'table' in locals():
                        rows = table.find_elements(By.TAG_NAME, "tr")
                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, "td")

                            if not cells:
                                continue

                            class_name = cells[0].get_attribute('class') if cells else "Element not found"

                            if class_name == "Element not found":
                                continue

                            if class_name == "tb_item" and len(total_btn_on_page) == 0:
                                last_category = cells[0].text

                            current_category = last_category

                            if cells[0].text == "Total" and len(total_btn_on_page) == 0:
                                current_category = "Total"

                            csv_element_item = {
                                "category": current_category,
                                "date": datetime.strptime(f"{year}-12-21", "%Y-%m-%d").date(),
                                "created_at": datetime.now(timezone.utc),
                            }

                            for index in range(len(dynamic_fields)):
                                csv_element_item[dynamic_fields[index]] = cells[index].text

                            csv_items.append(csv_element_item)

                    attempt = 0
                    if len(total_btn_on_page) == 0 or sub_tab >= len(total_btn_on_page):
                        break

                    sub_tab += 1
                except WebDriverException as e:
                    if attempt >= int(PAGE_MAX_RETRY):
                        break

                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}. Retrying in {PAGE_RETRY_DELAY_TIME_IN_SECONDS} seconds...")
                    await asyncio.sleep(float(PAGE_RETRY_DELAY_TIME_IN_SECONDS))

            if len(csv_items):
                df = pd.concat([df, pd.DataFrame(csv_items)], ignore_index=True)

            year += 1

        driver.quit()

        if attempt >= int(PAGE_MAX_RETRY):
            return

        print(f"Time to run: {(time.time() - start_time):.2f} seconds")

        return df
    except Exception as e:
        print(f"Error to execute get_generic_tables: {e}")
        return None

async def get_data(key, tab, dynamic_fields, service):
    data_frame = None
    try:
        with get_session_local() as db:
            print(f"Start get_{key} web scraping...")

            data_frame = await get_generic_tables(tab=tab, dynamic_fields=dynamic_fields)

            if data_frame is None or data_frame.empty:
                print("Data not found")
                return
                
            print(f"Update data on {key} database...")
            await asyncio.to_thread(service.delete_documents, db)
            await asyncio.to_thread(service.insert_many_documents, db, data_frame.to_dict(orient='records'))

            print(f"Finish get_{key} web scraping...")
    except Exception as e:
        print(f"Error to scrape get_{key} data: {e}")
    finally:
        data_frame = None

async def get_productions():
    await get_data(
        key="productions",
        tab="opt_02",
        dynamic_fields=["name", "amount_liters"],
        service=ProductionsService
    )

async def get_processingn():
    await get_data(
        key="processingn",
        tab="opt_03",
        dynamic_fields=["name", "amount_kg"],
        service=ProcessingnService
    )

async def get_commercialization():
    await get_data(
        key="commercialization",
        tab="opt_04",
        dynamic_fields=["name", "amount_liters"],
        service=CommercializationService
    )

async def get_importation():
    await get_data(
        key="importation",
        tab="opt_05",
        dynamic_fields=["country", "amount_kg", "price_us"],
        service=ImportationService
    )

async def get_exportation():
    await get_data(
        key="exportation",
        tab="opt_06",
        dynamic_fields=["country", "amount_kg", "price_us"],
        service=ExportationService
    )