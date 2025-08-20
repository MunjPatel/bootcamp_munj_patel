## 📂 Data Storage

This project follows a structured approach to storing financial data, ensuring reproducibility and clarity.

### Folder Structure
The data directory is organized into two main subfolders:

```bash
project_root/
│
├── data/
│ ├── raw/ # Unprocessed/raw market data (CSV)
│ └── processed/ # Cleaned & transformed data (Parquet)
│
├── notebooks/ # Jupyter notebooks for experiments
└── .env # Environment variables (DATA_DIR_RAW, DATA_DIR_PROCESSED)
```

### Formats Used
- **CSV (raw)**  
  - Easy to inspect manually.  
  - Good for archiving full downloads directly from APIs (e.g., Yahoo Finance).  

- **Parquet (processed)**  
  - Columnar storage format (efficient for analytics & ML workflows).  
  - Faster read/write performance compared to CSV.  
  - Lower disk footprint due to compression.  

### Environment Variable Setup
Data directories are controlled via a `.env` file for flexibility. The `.env.example`file contains sxample structure of env.

In code, these are loaded using *python-dotenv* library:

```bash
from dotenv import load_dotenv
import os, pathlib

load_dotenv()

RAW_DIR = pathlib.Path(os.path.join('..', os.getenv("DATA_DIR_RAW", "data/raw")))
PROC_DIR = pathlib.Path(os.path.join('..', os.getenv("DATA_DIR_PROCESSED", "data/processed")))
```

The code is configured such that paths remain configurable and portable across machines.
