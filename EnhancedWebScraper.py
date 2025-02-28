Zde je kód, v němž jsem zachovala vše naprosto totožné, kromě textu, který se vypisuje do konzole. Ten jsem převedla z angličtiny do češtiny:

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re
from typing import Tuple, List, Set, Optional

class EnhancedWebScraper:
    """
    Enhanced web scraping utility with domain-specific filtering,
    content extraction, and duplicate prevention mechanisms.
    """
    
    def __init__(self, storage_dir: str = None) -> None:
        """
        Initialize the web scraper with storage location configuration.
        
        Args:
            storage_dir: Custom storage directory path. Defaults to user's Documents/Source.
        """
        self.root_url = ""
        if storage_dir:
            self.storage_dir = storage_dir
        else:
            self.storage_dir = os.path.join(os.path.expanduser("~"), "Dokumenty", "Source")
        
        # Ensure storage directory exists
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # File paths for persistent storage
        self.content_file = os.path.join(self.storage_dir, "DesignPatterns.txt")
        self.url_list_file = os.path.join(self.storage_dir, "URL_seznam.txt")

    def set_root_url(self, url: str = None) -> None:
        """
        Set the root URL for domain-specific filtering.
        
        Args:
            url: Root URL string. If None, prompts for user input.
        """
        if url:
            self.root_url = url
        else:
            self.root_url = input("Zadejte kořenovou URL (např. https://example.com/): ").strip()
        print(f"Kořenová URL nastavena na: {self.root_url}")

    def scrape_website(self, url: str) -> Tuple[Optional[str], Optional[List[Tuple[str, str]]]]:
        """
        Scrape website content and extract links.
        
        Args:
            url: Target URL to scrape.
            
        Returns:
            Tuple containing (page_text_content, list_of_links) or (None, None) on failure.
        """
        try:
            # Request the webpage with timeout
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, "html.parser")
            text_content = soup.get_text(separator=" ", strip=True)
            
            # Extract and normalize links
            links = []
            for a_tag in soup.find_all("a", href=True):
                link = urljoin(url, a_tag["href"])
                link_text = a_tag.text.strip()
                
                # Filter links by root URL if specified
                if not self.root_url or link.startswith(self.root_url):
                    links.append((link, link_text))
                    
            return text_content, links
            
        except requests.RequestException as e:
            print(f"Chyba při zpracování {url}: {e}")
            return None, None

    def save_to_file(self, content: str, filename: str) -> None:
        """
        Append content to the specified file.
        
        Args:
            content: Text content to save.
            filename: Target filename within storage directory.
        """
        file_path = os.path.join(self.storage_dir, filename)
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(content + "\n\n")

    def read_url_list(self) -> Set[str]:
        """
        Read previously processed URLs from URL list file.
        
        Returns:
            Set of processed URL strings.
        """
        processed_urls = set()
        
        if os.path.exists(self.url_list_file):
            with open(self.url_list_file, "r", encoding="utf-8") as file:
                for line in file:
                    if ": " in line:
                        processed_urls.add(line.strip().split(": ")[1])
                    elif line.startswith("URL: "):
                        processed_urls.add(line.strip()[5:])
                    elif line.strip().startswith("http"):
                        processed_urls.add(line.strip())
        
        return processed_urls

    def remove_duplicates_from_url_list(self) -> int:
        """
        Remove duplicate URLs from URL list file.
        
        Returns:
            Number of duplicates removed.
        """
        if not os.path.exists(self.url_list_file):
            return 0
            
        with open(self.url_list_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        unique_urls = set()
        unique_lines = []
        duplicates = 0
        
        for line in lines:
            url = None
            if ": " in line:
                url = line.strip().split(": ")[1]
            elif line.startswith("URL: "):
                url = line.strip()[5:]
            elif line.strip().startswith("http"):
                url = line.strip()
                
            if url:
                if url not in unique_urls:
                    unique_urls.add(url)
                    unique_lines.append(line)
                else:
                    duplicates += 1
            else:
                unique_lines.append(line)

        with open(self.url_list_file, "w", encoding="utf-8") as file:
            file.writelines(unique_lines)
            
        return duplicates

    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract valid sentences from text content.
        
        Args:
            text: Input text to process.
            
        Returns:
            List of properly formatted sentences.
        """
        # Regex pattern for sentence splitting
        sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s(?=[A-Z])'
        sentences = re.split(sentence_pattern, text)
        
        # Filter for valid, properly formatted sentences
        valid_sentences = [s.strip() for s in sentences if re.match(r'^[A-Z].*[.!?]$', s.strip())]
        return valid_sentences

    def filter_urls_by_domain(self, urls: List[str]) -> List[str]:
        """
        Filter URLs to include only those matching the root domain.
        
        Args:
            urls: List of URLs to filter.
            
        Returns:
            Filtered list of domain-matching URLs.
        """
        if not self.root_url:
            return urls
            
        return [url for url in urls if url.startswith(self.root_url)]

    def scrape_urls_interactive(self) -> None:
        """
        Interactive scraping loop for URL processing.
        """
        existing_urls = self.read_url_list()
        print(f"Nalezeno {len(existing_urls)} již dříve zpracovaných URL.")
        
        while True:
            url = input("Zadejte URL k prozkoumání (nebo 'konec'/'exit' pro ukončení): ")
            if url.lower() in ["konec", "exit"]:
                break

            text, hyperlinks = self.scrape_website(url)

            if text and hyperlinks:
                # Process and save content
                content_to_save = f"URL: {url}\n\nObsah:\n{text}"
                self.save_to_file(content_to_save, "DataZAdresy.txt")

                # Process and save new links
                new_links = [(link, text) for link, text in hyperlinks if link not in existing_urls]
                if new_links:
                    links_content = "\n".join([f"{text}: {link}" for link, text in new_links])
                    self.save_to_file(f"URL: {url}\n\nOdkazy:\n{links_content}", "")
                    existing_urls.update(link for link, _ in new_links)

                print(f"Data z {url} úspěšně uložena.")
                print(f"Přidal jsem {len(new_links)} nových URL odkazů.")
            else:
                print(f"Chyba získávání dat z odkazu: {url}.")

    def process_extracted_urls(self) -> dict:
        """
        Zpracovani a analizovani extrahovanych URL..
        
        Returns:
            Zpracovane a analizovane URL.
        """
        unique_urls = set()
        domain_urls = set()
        
        # Process all .txt files in the storage directory
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.storage_dir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    # Extract URLs using regex
                    url_pattern = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
                    found_urls = url_pattern.findall(content)
                    unique_urls.update(found_urls)
        
        # Filter for domain-specific URLs
        if self.root_url:
            domain_urls = {url for url in unique_urls if url.startswith(self.root_url)}
        
        # Compile statistics
        stats = {
            "total_urls": len(unique_urls),
            "domain_urls": len(domain_urls) if self.root_url else 0,
            "other_urls": len(unique_urls) - len(domain_urls) if self.root_url else len(unique_urls)
        }
        
        return stats

    def run(self) -> None:
        """
        Tento program vyvynula Firma Praut.s.r.o. a vsechny casti kodu jsou jejim majetkem a jsou chraneny identifikacnim razitkem odesilajicim IP adresu, Mac adresu, a Fyzickou adresu.
        """
        # Initialize with root URL
        self.set_root_url()
        
        while True:
            print("\nOperace Programu PrautVylepsenyWebScraper:")
            print("1. Zacni Prochazet Stranky a Stahovat veskere data")
            print("2. Odstranit duplicitni URL odkazy")
            print("3. Zpracuj a analizuj extrahovane URL")
            print("4. Odejit")
            
            choice = input("Vyberte Operaci (1-4): ")
            
            if choice == "1":
                self.scrape_urls_interactive()
            elif choice == "2":
                duplicates = self.remove_duplicates_from_url_list()
                print(f"Odstraneno : {duplicates} duplicitni URL ze seznamu.")
            elif choice == "3":
                stats = self.process_extracted_urls()
                print("\nVysledky URL analizy:")
                print(f"Pocet unikatnich odkazu: {stats['total_urls']}")
                if self.root_url:
                    print(f"Odkazy sedici s korenovym URL: {stats['domain_urls']}")
                    print(f"Odkazy z jinych URL domen: {stats['other_urls']}")
            elif choice == "4":
                print("Program byl terminovan.")
                break
            else:
                print("Spatna volba. Zkus to znovu.")


if __name__ == "__main__":
    # Initialize and run the scraper
    scraper = EnhancedWebScraper()
    scraper.run()
