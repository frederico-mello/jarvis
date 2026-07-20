import hashlib
from datetime import datetime
from typing import AsyncIterator
import httpx
from bs4 import BeautifulSoup
from src.config.settings import settings
from src.common.logging import get_logger

logger = get_logger(__name__)


class PageResult:
    def __init__(self, url: str, html: str, content_hash: str, fetched_at: datetime):
        self.url = url
        self.html = html
        self.content_hash = content_hash
        self.fetched_at = fetched_at


async def discover_pages() -> list[str]:
    logger.info("Discovering pages", base_url=settings.crawler_base_url)
    discovered: set[str] = set()
    to_visit: list[str] = [settings.crawler_base_url]

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        while to_visit and len(discovered) < settings.crawler_max_pages:
            url = to_visit.pop(0)
            if url in discovered:
                continue
            try:
                response = await client.get(url)
                response.raise_for_status()
                discovered.add(url)
                soup = BeautifulSoup(response.text, "lxml")
                for link in soup.find_all("a", href=True):
                    href = link["href"]
                    full_url = _resolve_url(url, href)
                    if full_url and full_url.startswith(settings.crawler_base_url) and full_url not in discovered:
                        to_visit.append(full_url)
            except Exception as exc:
                logger.warning("Failed to fetch page", url=url, error=str(exc))

    logger.info("Discovery complete", total=len(discovered))
    return list(discovered)


async def fetch_page(url: str) -> PageResult | None:
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            content_hash = hashlib.sha256(response.text.encode()).hexdigest()
            return PageResult(
                url=url,
                html=response.text,
                content_hash=content_hash,
                fetched_at=datetime.utcnow(),
            )
    except Exception as exc:
        logger.warning("Failed to fetch page", url=url, error=str(exc))
        return None


def _resolve_url(base: str, href: str) -> str | None:
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        from urllib.parse import urlparse
        parsed = urlparse(base)
        return f"{parsed.scheme}://{parsed.netloc}{href}"
    if href.startswith("#") or href.startswith("mailto:"):
        return None
    from urllib.parse import urljoin
    return urljoin(base, href)
