from typing import Optional
import os

class FileUtils:
    """Utility class for file operations"""
    
    @staticmethod
    def get_file_extension(filename: str) -> Optional[str]:
        """Get file extension in lowercase"""
        if '.' in filename:
            return filename.split('.')[-1].lower()
        return None
    
    @staticmethod
    def is_allowed_file(filename: str, allowed_extensions: set) -> bool:
        """Check if file has allowed extension"""
        return ('.' in filename and 
                FileUtils.get_file_extension(filename) in allowed_extensions)