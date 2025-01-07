# utils.py
import mimetypes
import os


def get_mime_type(filename: str) -> str:
    mimetypes.init()
    mime_type, _ = mimetypes.guess_type(filename)

    if mime_type is None:
        return "application/octet-stream"

    extension = os.path.splitext(filename)[1].lower()
    mime_map = {
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    }

    return mime_map.get(extension, mime_type)
