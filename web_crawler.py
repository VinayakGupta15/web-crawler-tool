import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse

# Base directory where files will be stored
BASE_DIR = 'web_content'

# Directories for specific file types
JS_DIR = os.path.join(BASE_DIR, 'javascript')
PHP_DIR = os.path.join(BASE_DIR, 'php')
OTHER_DIR = os.path.join(BASE_DIR, 'other')

# Initialize directories
for directory in [JS_DIR, PHP_DIR, OTHER_DIR]:
    os.makedirs(directory, exist_ok=True)

# Define user agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; WebCrawler/1.0; +http://example.com/bot)'
}

# Rate limit: seconds to wait between requests
RATE_LIMIT = 1  # 1 second


def is_valid_url(url):
    """Check if a URL is valid."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def save_content(url, content, content_type):
    """Save content to a file based on its type."""
    # Determine the correct directory based on content type
    if 'javascript' in content_type or url.endswith('.js'):
        directory = JS_DIR
        extension = '.js'
    elif 'php' in content_type or url.endswith('.php'):
        directory = PHP_DIR
        extension = '.php'
    else:
        directory = OTHER_DIR
        extension = '.html'

    # Use the URL path as filename, replace '/' with '_' and remove query parameters
    filename = urlparse(url).path.replace('/', '_').split('?')[0]
    if not filename or filename == '_':
        filename = 'index'
    
    # Add the correct file extension if missing
    if not filename.endswith(extension):
        filename += extension

    filepath = os.path.join(directory, filename)
    
    # Save content to file
    with open(filepath, 'wb') as f:
        f.write(content)
    print(f"Saved: {filepath}")


def crawl(url, visited):
    """Recursively crawl a website."""
    if url in visited:
        return
    visited.add(url)
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an error on bad HTTP status
        print(f"Crawling: {url}")

        content_type = response.headers.get('Content-Type', '')
        save_content(url, response.content, content_type)

        if 'html' in content_type:
            soup = BeautifulSoup(response.text, 'html.parser')

            for a_tag in soup.find_all('a', href=True):
                link = urljoin(url, a_tag['href'])
                if is_valid_url(link) and link not in visited:
                    crawl(link, visited)

            # Check for scripts
            for script_tag in soup.find_all('script', src=True):
                script_url = urljoin(url, script_tag['src'])
                if is_valid_url(script_url) and script_url not in visited:
                    crawl(script_url, visited)

            # Check for PHP includes or links
            for link_tag in soup.find_all(['link', 'a', 'iframe'], href=True):
                link_url = urljoin(url, link_tag['href'])
                if link_url.endswith('.php') and is_valid_url(link_url) and link_url not in visited:
                    crawl(link_url, visited)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e} - URL: {url}")
    
    # Implement rate limiting
    time.sleep(RATE_LIMIT)


def main():
    parser = argparse.ArgumentParser(description='Simple Web Crawler')
    parser.add_argument('url', help='The URL to start crawling from')
    args = parser.parse_args()

    start_url = args.url
    if not is_valid_url(start_url):
        print(f"Invalid URL: {start_url}")
        return

    visited = set()
    crawl(start_url, visited)


if __name__ == '__main__':
    main()