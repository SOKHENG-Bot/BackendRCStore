import os
import uuid
from datetime import datetime
from django.utils.text import get_valid_filename


def get_upload_path(instance, filename: str, folder: str = "upload") -> str:
    name, ext = os.path.splitext(filename)
    ext = ext or ""
    random_filename = f"{uuid.uuid4().hex[:12]}-{ext}"
    now = datetime.now()
    date_path = f"{now.year}/{now.month:02d}/{now.day:02d}"
    return os.path.join(folder, date_path, get_valid_filename(random_filename))
