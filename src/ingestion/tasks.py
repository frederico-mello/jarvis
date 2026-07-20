import asyncio
from src.ingestion.worker import worker
from src.ingestion.crawler import discover_pages, fetch_page
from src.ingestion.detector import detect_changes, apply_changes, SourceDiff
from src.ingestion.extractor import extract_page_content, chunk_text
from src.graph.driver import get_driver
from src.graph.provenance import create_source, create_chunk
from src.common.logging import get_logger

logger = get_logger(__name__)


@worker.task(bind=True, max_retries=3, default_retry_delay=60)
def crawl_public_pages(self) -> dict:
    logger.info("Starting scheduled crawl")
    try:
        urls = asyncio.run(discover_pages())
        diffs = asyncio.run(detect_changes(urls))
        new_urls = [d.url for d in diffs if d.action == "new"]
        removed = [d for d in diffs if d.action == "removed"]

        apply_changes(removed)

        for url in new_urls:
            process_new_page.delay(url)

        logger.info("Crawl complete", discovered=len(urls), new=len(new_urls), removed=len(removed))
        return {"discovered": len(urls), "new": len(new_urls), "removed": len(removed)}
    except Exception as exc:
        logger.error("Crawl failed", error=str(exc))
        raise self.retry(exc=exc)


@worker.task(bind=True, max_retries=3, default_retry_delay=30)
def process_new_page(self, url: str) -> dict | None:
    logger.info("Processing new page", url=url)
    try:
        page = asyncio.run(fetch_page(url))
        if page is None:
            return None

        extracted = extract_page_content(page.html, url)
        chunks = chunk_text(extracted.text)

        driver = get_driver()
        source_id = f"web_{url.replace('/', '_').replace(':', '_')}"

        with driver.session() as session:
            session.execute_write(create_source, source_id, "web_page", url)
            for i, chunk_text_content in enumerate(chunks):
                chunk_id = f"{source_id}_chunk_{i}"
                session.execute_write(create_chunk, chunk_id, chunk_text_content, source_id)

        driver.close()
        logger.info("Page processed", url=url, chunks=len(chunks))
        return {"url": url, "chunks": len(chunks)}
    except Exception as exc:
        logger.error("Failed to process page", url=url, error=str(exc))
        raise self.retry(exc=exc)
