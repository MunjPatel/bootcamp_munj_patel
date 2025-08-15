import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# looks for a .env file in the current and parent directories
def load_environ():
    load_dotenv()  
    print(".env loaded!")

# taking the key-value out of .env file
def get_key(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(name, default)