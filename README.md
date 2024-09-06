# Web Crawler Tool

A simple web crawler tool capable of recursively navigating web pages and storing the retrieved content into files. The tool filters JavaScript and PHP files into separate directories and organizes other file types into distinct paths within the file system.

## Features

- **Recursive Crawling**: Navigate through linked web pages starting from a given URL.
- **Content Storage**: Download and store HTML, JavaScript, and PHP files.
- **File Filtering**: Organize JavaScript and PHP files into separate directories.
- **Valid URL Checks**: Only valid URLs are crawled.

## Requirements

- Python 3.x
- `requests` library (install using `pip install requests`)
- `beautifulsoup4` library (install using `pip install beautifulsoup4`)

## Usage

To run the web crawler, execute the following command:

```bash
python web_crawler.py [start_url]
```

Replace `[start_url]` with the URL you want to start crawling from.

### Example

To crawl the website `https://example.com`:

```bash
python web_crawler.py https://example.com
```

### Directory Structure

The crawler saves files in the `web_content` directory with the following structure:

- `web_content/javascript`: Contains JavaScript files.
- `web_content/php`: Contains PHP files.
- `web_content/other`: Contains HTML and other files.

### Notes

- Ensure you have permission to crawl the website to avoid legal issues.
- This is a simple educational tool and may require adjustments for more complex use cases.
- The tool only follows links found in `<a>` tags.


### Instructions

1. **Install Dependencies**: Ensure you have Python installed and install the required packages using:

   ```bash
   pip install requests beautifulsoup4
   ```

2. **Run the Tool**: Execute the crawler by providing a starting URL.

   ```bash
   python web_crawler.py https://example.com
   ```

3. **Check Output**: The retrieved content will be saved in the `web_content` directory, organized by file type.
