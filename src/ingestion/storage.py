from pathlib import Path
from datetime import datetime
from src.config.settings import settings
from src.common.logging import get_logger
from src.common.exceptions import ValidationError

logger = get_logger(__name__)


UPLOAD_DIR = Path("storage/uploads")


def ensure_storage() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def store_original(file_data: bytes, document_id: str, original_name: str) -> Path:
    ensure_storage()
    ext = Path(original_name).suffix.lower()
    filename = f"{document_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{ext}"
    file_path = UPLOAD_DIR / filename
    file_path.write_bytes(file_data)
    logger.info("Original file stored", path=str(file_path), document_id=document_id)
    return file_path


def get_original_path(document_id: str) -> Path | None:
    for f in UPLOAD_DIR.iterdir():
        if f.name.startswith(document_id):
            return f
    return None


def delete_original(document_id: str) -> bool:
    path = get_original_path(document_id)
    if path:
        path.unlink()
        logger.info("Original file deleted", path=str(path), document_id=document_id)
        return True
    return False
