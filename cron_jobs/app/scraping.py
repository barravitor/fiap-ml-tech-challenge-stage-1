import asyncio
from shared.db.database import create_table
from shared.config import PRODUCTION
from .services.scrape_service import get_productions, get_processingn, get_commercialization, get_importation, get_exportation

async def start_scrape_in_parabellum():
    await asyncio.gather(
        get_productions(),
        get_processingn(),
        get_commercialization(),
        get_importation(),
        get_exportation(),
    )

async def start_scrape():
    await get_productions(),
    await get_processingn(),
    await get_commercialization(),
    await get_importation(),
    await get_exportation(),

if __name__ == "__main__":
    create_table()

    if PRODUCTION:
        asyncio.run(start_scrape())
    else:
        asyncio.run(start_scrape_in_parabellum())