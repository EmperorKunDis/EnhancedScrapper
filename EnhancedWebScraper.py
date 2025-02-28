import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re
from typing import Tuple, List, Set, Optional

class EnhancedWebScraper:
    """
    Vylepšený nástroj pro web scraping s filtrováním dle domény,
    extrakcí obsahu a mechanismy prevence duplicit.
    """
    
    def __init__(self, storage_dir: str = None) -> None:
        """
        Inicializace webového scraperu s konfigurací umístění úložiště.
        
        Parametry:
            storage_dir: Vlastní cesta k adresáři úložiště. Ve výchozím nastavení je to "Dokumenty/Zdroj" uživatele.
        """
        self.root_url = ""
        if storage_dir:
            self.storage_dir = storage_dir
        else:
            self.storage_dir = os.path.join(os.path.expanduser("~"), "Dokumenty", "Zdroj")
        
        # Zajistit, že adresář úložiště existuje
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Cesty k souborům pro perzistentní ukládání
        self.content_file = os.path.join(self.storage_dir, "NavrhoveVzory.txt")
        self.url_list_file = os.path.join(self.storage_dir, "URL_seznam.txt")

    def set_root_url(self, url: str = None) -> None:
        """
        Nastavení kořenové URL pro filtrování dle domény.
        
        Parametry:
            url: Řetězec kořenové URL. Pokud není zadáno, vyzve uživatele k zadání.
        """
        if url:
            self.root_url = url
        else:
            self.root_url = input("Zadejte kořenovou URL (např. https://example.com/): ").strip()
        print(f"Kořenová URL nastavena na: {self.root_url}")

    def scrape_website(self, url: str) -> Tuple[Optional[str], Optional[List[Tuple[str, str]]]]:
        """
        Procházení obsahu webové stránky a extrakce odkazů.
        
        Parametry:
            url: Cílová URL pro prohledávání.
            
        Návratová hodnota:
            N-tice obsahující (textový obsah stránky, seznam odkazů) nebo (None, None) při neúspěchu.
        """
        try:
            # Odeslání požadavku na webovou stránku s časovým limitem
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parsování HTML obsahu
            soup = BeautifulSoup(response.text, "html.parser")
            text_content = soup.get_text(separator=" ", strip=True)
            
            # Extrahování a normalizace odkazů
            links = []
            for a_tag in soup.find_all("a", href=True):
                link = urljoin(url, a_tag["href"])
                link_text = a_tag.text.strip()
                
                # Filtrování odkazů dle kořenové URL, pokud je specifikována
                if not self.root_url or link.startswith(self.root_url):
                    links.append((link, link_text))
                    
            return text_content, links
            
        except requests.RequestException as e:
            print(f"Chyba při zpracování {url}: {e}")
            return None, None

    def save_to_file(self, content: str, filename: str) -> None:
        """
        Přidání obsahu do specifikovaného souboru.
        
        Parametry:
            content: Textový obsah k uložení.
            filename: Název souboru v rámci adresáře úložiště.
        """
        file_path = os.path.join(self.storage_dir, filename)
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(content + "\n\n")

    def read_url_list(self) -> Set[str]:
        """
        Načtení dříve zpracovaných URL ze souboru seznamu URL.
        
        Návratová hodnota:
            Množina zpracovaných URL.
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
        Odstranění duplicitních URL ze souboru seznamu URL.
        
        Návratová hodnota:
            Počet odstraněných duplicit.
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
        Extrahování platných vět z textového obsahu.
        
        Parametry:
            text: Vstupní text ke zpracování.
            
        Návratová hodnota:
            Seznam správně formátovaných vět.
        """
        # Regex vzor pro dělení vět
        sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s(?=[A-Z])'
        sentences = re.split(sentence_pattern, text)
        
        # Filtrování platných, správně formátovaných vět
        valid_sentences = [s.strip() for s in sentences if re.match(r'^[A-Z].*[.!?]$', s.strip())]
        return valid_sentences

    def filter_urls_by_domain(self, urls: List[str]) -> List[str]:
        """
        Filtrování URL tak, aby obsahovaly pouze ty odpovídající kořenové doméně.
        
        Parametry:
            urls: Seznam URL ke filtrování.
            
        Návratová hodnota:
            Filtrovaný seznam URL odpovídajících doméně.
        """
        if not self.root_url:
            return urls
            
        return [url for url in urls if url.startswith(self.root_url)]

    def scrape_urls_interactive(self) -> None:
        """
        Interaktivní cyklus pro prohledávání URL.
        """
        existing_urls = self.read_url_list()
        print(f"Nalezeno {len(existing_urls)} již dříve zpracovaných URL.")
        
        while True:
            url = input("Zadejte URL k prozkoumání (nebo 'konec'/'exit' pro ukončení): ")
            if url.lower() in ["konec", "exit"]:
                break

            text, hyperlinks = self.scrape_website(url)

            if text and hyperlinks:
                # Zpracování a uložení obsahu
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
