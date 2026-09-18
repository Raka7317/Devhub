from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile


router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf",
    ".txt"
}


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
CHUNK_SIZE = 1024 * 1024  # 1 MB


@router.post("/")
async def upload_file(
    file: UploadFile = File(...)
):
    # 1. Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    # 2. Get extension
    extension = Path(file.filename).suffix.lower()

    # 3. Validate extension
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )

    # 4. Generate safe filename
    safe_filename = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIR / safe_filename

    total_size = 0

    try:
        with open(file_path, "wb") as buffer:

            while True:
                chunk = await file.read(CHUNK_SIZE)

                if not chunk:
                    break

                total_size += len(chunk)

                # 5. Stop if file exceeds 5 MB
                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File too large. Maximum size is 5 MB."
                    )

                buffer.write(chunk)

    except HTTPException:
        # Delete partially written file
        if file_path.exists():
            file_path.unlink()

        raise

    finally:
        await file.close()

    return {
        "filename": safe_filename,
        "size": total_size,
        "message": "File uploaded successfully"
    }