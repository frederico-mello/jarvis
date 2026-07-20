from bs4 import BeautifulSoup
from src.common.logging import get_logger

logger = get_logger(__name__)


class ExtractedPage:
    def __init__(self, title: str, text: str, metadata: dict):
        self.title = title
        self.text = text
        self.metadata = metadata


def extract_page_content(html: str, url: str) -> ExtractedPage:
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    title = ""
    if soup.title:
        title = soup.title.get_text(strip=True)

    text = soup.get_text(separator="\n", strip=True)

    metadata = {
        "url": url,
        "title": title,
        "description": _get_meta_content(soup, "description"),
        "keywords": _get_meta_content(soup, "keywords"),
        "author": _get_meta_content(soup, "author"),
    }

    return ExtractedPage(title=title, text=text, metadata=metadata)


def _get_meta_content(soup: BeautifulSoup, name: str) -> str | None:
    tag = soup.find("meta", attrs={"name": name})
    if tag and tag.get("content"):
        return tag["content"].strip()
    return None


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks
