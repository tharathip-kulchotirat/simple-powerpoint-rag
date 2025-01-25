import tempfile
from pathlib import Path
from contextlib import contextmanager
from functools import wraps
from loguru import logger

def secure_tempfile(func):
    @wraps(func)
    def wrapper(uploaded_file, *args, **kwargs):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = Path(tmp_file.name)
            
            result = func(tmp_path, *args, **kwargs)
            return result
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
                logger.debug(f"Cleaned up temporary file: {tmp_path}")
    return wrapper

@contextmanager
def temp_directory_context():
    """Secure temporary directory context manager"""
    temp_dir = tempfile.TemporaryDirectory()
    try:
        yield Path(temp_dir.name)
    finally:
        temp_dir.cleanup()
        logger.debug(f"Cleaned up temporary directory: {temp_dir.name}")