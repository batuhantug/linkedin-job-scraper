import re
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def clean_text(text):
    """Remove special characters and extra whitespace from text"""
    if text:
        return re.sub(r'\s+', ' ', text.strip())
    return '' 