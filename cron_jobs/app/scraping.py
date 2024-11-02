import asyncio
from shared.db.database import create_table
from .services.scrape_service import get_productions, get_processingn, get_commercialization, get_importation, get_exportation

async def start_scrape():
    create_table()

    await asyncio.gather(
        get_productions(),
        get_processingn(),
        get_commercialization(),
        get_importation(),
        get_exportation(),
    )

if __name__ == "__main__":
    asyncio.run(start_scrape())