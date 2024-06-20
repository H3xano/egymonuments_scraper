# Egypt Monuments Scraper

This Python script scrapes data from the Egypt Monuments website, fetching information about articles, archaeological sites, monuments, museums, collections, and sunken monuments. The data is saved as JSON files in corresponding directories.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/H3xano/egypt-monuments-scraper.git
    cd egypt-monuments-scraper
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the scraper script:

```bash
python scrape.py
```

The script will fetch data from the Egypt Monuments website and save it in JSON format in the respective directories (`articles`, `archaeological_sites`, `monuments`, `museums`, `collections`, `sunken_monuments`).

## Project Structure

```
egypt-monuments-scraper/
├── articles/
├── archaeological_sites/
├── collections/
├── monuments/
├── museums/
├── sunken_monuments/
├── .gitignore
├── README.md
├── requirements.txt
├── scraper.py
└── venv/
```

- `scraper.py`: The main script that performs the scraping.
- `requirements.txt`: Lists the dependencies required for the project.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `README.md`: The file you are currently reading.

## Dependencies

- `requests`: For making HTTP requests.
- `beautifulsoup4`: For parsing HTML content.

Install these dependencies with:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.