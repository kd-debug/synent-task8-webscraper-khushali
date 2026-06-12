import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin

class WebScraper:
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        self.url = url
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.soup = None
        self.raw_html = None

    def fetch_content(self) -> bool:
        """Fetches the HTML content of the URL."""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            self.raw_html = response.text
            self.soup = BeautifulSoup(self.raw_html, 'lxml')
            return True
        except Exception as e:
            print(f"Error fetching {self.url}: {e}")
            return False

    def extract_data(self, selector: str, attribute: Optional[str] = None) -> List[str]:
        """Extracts data from the page using a CSS selector."""
        if not self.soup:
            return []
        
        elements = self.soup.select(selector)
        if attribute:
            data = []
            for el in elements:
                val = el.get(attribute)
                if val:
                    # Convert to absolute URL if it's a link or image
                    if attribute in ['href', 'src']:
                        val = urljoin(self.url, val)
                    data.append(val.strip())
            return data
        return [el.get_text().strip() for el in elements]

    def get_common_data(self) -> Dict[str, List[str]]:
        """Automatically tries to extract common data like titles and links."""
        if not self.soup:
            return {}
        
        data = {
            "Titles": [t.get_text().strip() for t in self.soup.find_all(['h1', 'h2', 'h3']) if t.get_text().strip()],
            "Links": [urljoin(self.url, a.get('href')) for a in self.soup.find_all('a', href=True)],
            "Images": [urljoin(self.url, img.get('src')) for img in self.soup.find_all('img', src=True)]
        }
        return data

    def to_dataframe(self, data: Dict[str, List[Any]]) -> pd.DataFrame:
        """Converts extracted data to a DataFrame, handling unequal lengths."""
        # Find the maximum length to pad other lists
        max_len = max(len(v) for v in data.values()) if data else 0
        padded_data = {k: v + [None] * (max_len - len(v)) for k, v in data.items()}
        return pd.DataFrame(padded_data)
