"""File open/save utilities"""

import os
from typing import Optional, Tuple
from app.config.constants import MAX_CODE_SIZE_BYTES


class FileHandler:
    """Handles file operations for code files"""

    @staticmethod
    def read_file(file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Read a code file from disk

        Returns:
            Tuple of (content, error_message)
        """
        if not os.path.exists(file_path):
            return None, "File does not exist"

        file_size = os.path.getsize(file_path)
        if file_size > MAX_CODE_SIZE_BYTES:
            return None, f"File is too large. Maximum size is {MAX_CODE_SIZE_BYTES // 1024}KB"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content, None
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    content = f.read()
                return content, None
            except Exception as e:
                return None, f"Error reading file: {str(e)}"
        except Exception as e:
            return None, f"Error reading file: {str(e)}"

    @staticmethod
    def save_file(file_path: str, content: str) -> Optional[str]:
        """
        Save content to a file

        Returns:
            Error message if failed, None if successful
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return None
        except Exception as e:
            return f"Error saving file: {str(e)}"

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension from path"""
        return os.path.splitext(file_path)[1].lower()
