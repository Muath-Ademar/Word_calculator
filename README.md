# Web Scraper for Word Occurrence Counting

This project is a web scraper that counts the occurrences of a specific word across a website and its linked pages. It uses concurrent programming to speed up the process and can be scaled out over multiple servers or containers.

## Features

- **Concurrent Downloading**: Uses `concurrent.futures.ThreadPoolExecutor` to download multiple pages concurrently.
- **Word Counting**: Counts the occurrences of a specified word in the content of each page.
- **Link Extraction**: Extracts all links from a page and follows them to count word occurrences in linked pages.
- **Depth Limitation**: Limits the depth of link following to prevent excessive crawling.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/web-scraper.git
   cd web-scraper
   ```

2. Install the required libraries:
   ```bash
   pip install requests beautifulsoup4
   ```

## Usage

1. Modify the `url` and `word` variables in the script to specify the starting URL and the word to search for.

2. Run the script:
   ```bash
   python scraper.py
   ```

## Example Output

```plaintext
The word "in" occurred 42 times in this url: https://books.toscrape.com/
The word "in" occurred 10 times in this url: https://books.toscrape.com/catalogue/category/books_1/index.html
The word "in" occurred 5 times in this url: https://books.toscrape.com/catalogue/category/books/travel_2/index.html
...
The word "in" occurred 1234 times across all pages
```

## Scaling Out

This application is I/O bound as it spends most of its time waiting for web pages to be downloaded. To scale out this application over multiple servers or containers, a queue-based algorithm can be used. Here’s a high-level approach:

1. **Centralized Queue**: Use a message queue (e.g., RabbitMQ, Kafka) to store URLs to be processed.
2. **Worker Nodes**: Deploy multiple worker nodes (servers/containers) that pull URLs from the queue, download the pages, and count word occurrences.
3. **Result Aggregation**: Use a centralized database or another queue to aggregate results from all worker nodes.

## Code Overview

- **Page Class**: Represents a web page with its URL and content.
- **download_page Function**: Downloads the content of a web page.
- **count_word_occurrences Function**: Counts the occurrences of a word in a page's content.
- **get_links_in_page Function**: Extracts all links from a page.
- **word_score Function**: Recursively counts word occurrences in a page and its linked pages, up to a specified depth.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README to better fit your project's needs!
