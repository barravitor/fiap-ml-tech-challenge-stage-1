import asyncio
from cron_jobs.app.services.scrape_service import get_productions, get_processingn, get_commercialization, get_importation, get_exportation

async def start_scrape():
    await asyncio.gather(
        get_productions(),
        get_processingn(),
        get_commercialization(),
        get_importation(),
        get_exportation(),
    )

if __name__ == "__main__":
    asyncio.run(start_scrape())