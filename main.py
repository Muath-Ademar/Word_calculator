import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import concurrent.futures
import threading

class Page:
        def __init__(self, url: str, content: str):
                self.url = url
                self.content = content

def download_page(url: str) -> Page:

        try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                content = response.text
                return Page(response.url, content)
        except requests.HTTPError:
                print("HTTP error occurred")
                return None
        except requests.ConnectionError:
                print("connection error occurred")
                return None
        except requests.URLRequired:
                print("a valid URL is required")
                return None
        except requests.TooManyRedirects:
                print("Too many redirects")
                return None
def count_word_occurrences(p : Page, word: str) -> int:
        return p.content.lower().count(word.lower())

def get_links_in_page(p: Page) -> set:
        soup = BeautifulSoup(p.content, 'html.parser')
        links = set()
        for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                        abs_url = urljoin(p.url, href)
                        links.add(abs_url)
        return links

def word_score(p : Page, word: str, visitedUrls = None, page_number=0, max_page_number =3) ->int:
        if visitedUrls is None:
                visitedUrls = set()
        with visitedUrls_lock:
                if p.url in visitedUrls or page_number> max_page_number:
                        return 0
                visitedUrls.add(p.url)
        word_count = count_word_occurrences(p, word)
        
        links = get_links_in_page(p)
        
        print(f"the word {word} occurred {word_count} times in this url: {p.url}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures  = []
                for link in links:
                        with visitedUrls_lock:
                                if link not in visitedUrls:
                                        futures.append(executor.submit(download_page, link))
                for future in concurrent.futures.as_completed(futures):
                        linked_page = future.result()
                        if linked_page:
                                word_count += word_score(linked_page, word, visitedUrls, page_number +1, max_page_number)
        return word_count
                

visitedUrls_lock = threading.Lock()


url = "https://books.toscrape.com/"
word = "in"

page = download_page(url)
if not page:
        print("Failed to download page")
else:
        word_count = count_word_occurrences(page, word)
        print(f"The word {word} occurred {word_count} in this url: {page.url}")
        total_count = word_score(page, word, visitedUrls= set(), page_number=0, max_page_number=3)
        print(f"the word {word} occurred {total_count} across all pages")
        





# Is your solution CPU bound? Explain your answer.
#   its I/O bound since its waiting for the links in the webpage to be proccessed

#Suggest an algorithm that allows scaling out of this application over multiple servers/containers.  

# I would suggest a queue based algorithm, because it efficiently manages parallel processing by allowing multiple workers to process URLs concurrently





