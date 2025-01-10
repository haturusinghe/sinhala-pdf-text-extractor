import re

class UnicodeHandler:
    # Sinhala Unicode range
    SINHALA_UNICODE_RANGE = range(0x0D80, 0x0DFF + 1)
    SINHALA_PATTERN = re.compile(r'[\u0D80-\u0DFF]+')
    
    @staticmethod
    def is_sinhala_char(char: str) -> bool:
        """Check if character is in Sinhala Unicode range."""
        if not char:
            return False
        return ord(char) in UnicodeHandler.SINHALA_UNICODE_RANGE
    
    @staticmethod
    def contains_sinhala(text: str) -> bool:
        """Check if text contains Sinhala characters."""
        return bool(UnicodeHandler.SINHALA_PATTERN.search(text))
    
    @staticmethod
    def extract_sinhala_text(text: str) -> List[str]:
        """Extract only Sinhala text segments."""
        if not text:
            return []
        return UnicodeHandler.SINHALA_PATTERN.findall(text)
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize Unicode text."""
        if not text:
            return ""
        # Remove zero-width spaces and other invisible characters
        text = ''.join(char for char in text if ord(char) >= 32)
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()
