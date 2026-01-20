# CharacterTables

A comprehensive tool designed to parse and organize character information from various popular mobile games into structured tables. This tool simplifies data extraction and analysis for gamers and developers alike.

## Supported Games

Currently, CharacterTables supports data extraction from the following games:

-   **Genshin Impact (GI)**
-   **Zenless Zone Zero (ZZZ)**
-   **Fate/Grand Order (FGO)**

## Tech Stack

This project leverages a robust set of Python libraries to handle API interactions, data processing, and translation:

-   **[Python 3.12](https://www.python.org/)**: The core programming language.
-   **[pandas](https://pandas.pydata.org/)**: For powerful data manipulation and CSV export.
-   **[hakushin-py](https://pypi.org/project/hakushin-py/)**: API wrapper for Zenless Zone Zero data.
-   **[ambr-py](https://pypi.org/project/ambr-py/)**: API wrapper for Genshin Impact data (via Ambr.top).
-   **[atlasacademy-py](https://github.com/Max-Xie-593/FGOAtlasAcademyAPI)**: API wrapper for Fate/Grand Order data (via Atlas Academy).
-   **[multipledispatch](https://pypi.org/project/multipledispatch/)**: For function overloading capabilities.
-   **[deep-translator](https://pypi.org/project/deep-translator/)**: For automated translation needs.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Max-Xie-593/CharacterTables.git
    cd CharacterTables
    ```

2.  **Ensure Python 3.12 is installed.**

3.  **Install dependencies using pipenv:**
    ```bash
    pipenv install
    ```
    *Alternatively, you can install packages manually from the `Pipfile` if you don't use pipenv.*

## Usage

The tool is accessed via the command line using `driver.py`. It supports two main modes: `characters` (for fetching data) and `pandas` (for converting data).

### 1. Fetch Character Data
Extract character information from a specific game into a JSON file.

**Syntax:**
```bash
python driver.py characters <game>
```

**Examples:**
```bash
# Fetch Genshin Impact characters
python driver.py characters GI

# Fetch Zenless Zone Zero characters
python driver.py characters ZZZ

# Fetch Fate/Grand Order characters
python driver.py characters FGO
```

### 2. Convert to CSV
Convert the fetched JSON data into a clean CSV format for spreadsheet analysis.

**Syntax:**
```bash
python driver.py pandas <game>
```

**Examples:**
```bash
# Convert Genshin Impact data to CSV
python driver.py pandas GI

# Convert Zenless Zone Zero data to CSV
python driver.py pandas ZZZ
```

### Help
To see all available options and help messages:
```bash
python driver.py --help
# or for specific commands
python driver.py characters --help
```
