# CharacterTables

A comprehensive tool designed to parse and organize character information from various popular mobile games into structured tables. This tool simplifies data extraction and analysis for gamers and developers alike.

## Supported Games

Currently, CharacterTables supports data extraction from the following games:

-   **Genshin Impact (GI)**
-   **Zenless Zone Zero (ZZZ)**
-   **Fate/Grand Order (FGO)**
-   **Uma Musume: Pretty Derby (UMAMUSU)**

## Tech Stack

This project leverages a robust set of Python libraries to handle API interactions, data processing, and translation:

-   **[Python 3.12](https://www.python.org/)**: The core programming language.
-   **[pandas](https://pandas.pydata.org/)**: For powerful data manipulation and CSV export.
-   **[hakushin-py](https://pypi.org/project/hakushin-py/)**: API wrapper for Zenless Zone Zero data.
-   **[ambr-py](https://pypi.org/project/ambr-py/)**: API wrapper for Genshin Impact data (via Ambr.top).
-   **[atlasacademy-py](https://github.com/Max-Xie-593/FGOAtlasAcademyAPI)**: API wrapper for Fate/Grand Order data (via Atlas Academy).
-   **[umamusume-api](https://github.com/Max-Xie-593/UmamusumeAPI)**: API wrapper for Uma Musume: Pretty Derby data.
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

The tool is accessed via the command line using `driver.py`. It supports three modes: `sync` (fetch and convert in one step), `characters` (fetch raw JSON), and `pandas` (convert JSON to CSV).

### 1. Sync Character Data (Recommended)
Fetch raw character data and immediately convert it to a cleaned CSV table in one step.

**Syntax:**
```bash
python driver.py sync <game>
# or sync all games in sequence:
python driver.py sync --all
```

**Examples:**
```bash
# Sync Genshin Impact
python driver.py sync gi

# Sync all games
python driver.py sync --all
```

### 2. Fetch Character Data (Raw Only)
Extract character information from a specific game into a JSON file.

**Syntax:**
```bash
python driver.py characters <game>
```

**Examples:**
```bash
# Fetch Genshin Impact characters
python driver.py characters gi

# Fetch Zenless Zone Zero characters
python driver.py characters zzz

# Fetch Fate/Grand Order characters
python driver.py characters fgo

# Fetch Uma Musume characters
python driver.py characters umamusu
```

### 3. Convert to CSV
Convert previously fetched JSON data into a clean CSV format for spreadsheet analysis.

**Syntax:**
```bash
python driver.py pandas <game>
```

**Examples:**
```bash
# Convert Genshin Impact data to CSV
python driver.py pandas gi

# Convert Zenless Zone Zero data to CSV
python driver.py pandas zzz

# Convert Fate/Grand Order data to CSV
python driver.py pandas fgo

# Convert Uma Musume data to CSV
python driver.py pandas umamusu
```

### Help
To see all available options and help messages:
```bash
python driver.py --help
# or for specific commands
python driver.py sync --help
```

## Automation

Character tables are automatically kept up to date via a scheduled [GitHub Actions workflow](.github/workflows/sync_rosters.yml) that runs weekly and commits updated CSVs directly to the repository. The workflow can also be triggered manually on demand from the Actions tab.
