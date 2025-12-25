from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse


static_router = APIRouter(tags=["static"])


@static_router.get("/", response_class=HTMLResponse)
async def root():
    """
    Serves the index.html file on the root URL.
    """
    index_path = Path(__file__).parent.parent / "static" / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(), status_code=200)
    else:
        raise HTTPException(status_code=404, detail="index.html not found")
