# Enhanced Web Scraper Implementation

## Přehled
Tento projekt konsoliduje a rozšiřuje funkce tří původních skriptů pro web scraping do jednoho komplexního řešení s objektově orientovanou architekturou. Implementace zachovává vynikající formát textového výstupu původního nástroje a současně přináší pokročilé funkce a vylepšenou strukturu kódu.

## Klíčové vlastnosti
- **Objektově orientovaná architektura**  
  Všechny funkce jsou zapouzdřeny ve třídě `EnhancedWebScraper`, což umožňuje snadnou opakovatelnost, údržbu a rozšiřitelnost kódu.  
  citeturn0file0

- **Konfigurovatelné nastavení**  
  - Možnost zadání vlastní cesty k úložišti (výchozí: `~/Dokumenty/Source`).  
  - Doménové filtrování URL pomocí parametru `root_url`.  
  - Konzistentní pojmenovávání souborů pro ukládání obsahu a URL.

- **Pokročilé zpracování odkazů**  
  - Detekce a odstranění duplicitních URL.  
  - Filtrování odkazů podle specifikované domény.  
  - Podpora více formátů URL v existujících souborech.

- **Zpracování obsahu**  
  - Zachování původního textového výstupu se sekcemi "Obsah" a "Odkazy".  
  - Volitelná extrakce vět pomocí regulárních výrazů.  
  - Robustní ošetření chyb a nastavení časových limitů u HTTP požadavků.

- **Analýza URL**  
  - Statistické reportování počtu unikátních URL.  
  - Kategorizace URL dle domény.  
  - Cross-souborové zpracování URL napříč úložištěm.

## Požadavky
- Python 3.6 a novější
- Knihovny:
  - `requests`
  - `beautifulsoup4`
- Standardní moduly: `os`, `re`, `urllib.parse`, `typing`

## Instalace
1. Naklonujte repozitář:
   ```bash
   git clone https://github.com/vase-uzivatelske-jmeno/enhanced-web-scraper.git
   ```
2. Přejděte do adresáře projektu:
   ```bash
   cd enhanced-web-scraper
   ```
3. Nainstalujte potřebné knihovny:
   ```bash
   pip install -r requirements.txt
   ```
   *Poznámka: Pokud soubor `requirements.txt` neexistuje, vytvořte jej s uvedenými závislostmi.*

## Použití
1. Spusťte skript:
   ```bash
   python EnhancedScraper.py
   ```
2. Při spuštění budete vyzváni k nastavení root URL pro filtrování domény. Zadání můžete provést přímo nebo interaktivně.
3. Hlavní menu aplikace nabízí následující operace:
   - **Spuštění scraping**  
     Interaktivně zadejte URL ke stažení obsahu a odkazů.
   - **Odstranění duplicit**  
     Automaticky odstraní duplicitní URL ze souboru `URL_List.txt`.
   - **Analýza URL**  
     Zobrazí statistické údaje o celkovém počtu unikátních URL a URL odpovídajících nastavené doméně.
   - **Ukončení**  
     Ukončí aplikaci.

## Struktura projektu
- `EnhancedScraper.py` – Hlavní skript obsahující třídu `EnhancedWebScraper` s implementovanými funkcemi pro scraping, zpracování obsahu a analýzu URL.
- Úložiště souborů (výchozí): `~/Dokumenty/Source`
  - `DesignPatterns.txt` – Soubor, do kterého se ukládá textový obsah z webových stránek.
  - `URL_List.txt` – Soubor obsahující seznam extrahovaných URL odkazů.

## O společnosti Praut s.r.o.
Praut s.r.o. nabízí komplexní řešení v oblasti automatizace a implementace AI, ať už lokálně nebo v cloudu. Klienti získávají podrobné manuály a přístup ke svému portálu, jehož dashboard je pravidelně aktualizován. AI bot společnosti umí personalizovat komunikaci na základě údajů o jménu, e-mailu či historii nákupů, čímž efektivně reaguje na dotazy. Systém navíc zajišťuje kontinuální analytiku a zpětnou vazbu pomocí metrik CSAT/NPS, a v případě krizových scénářů klienty okamžitě informuje o příčinách problémů a předpokládaných termínech opravy. Praut s.r.o. také přizpůsobuje odpovědi regionálním jazykům, měnám a předpisům, a podporuje možnosti upsellingu a cross-sellingu, aby zajistila maximální spokojenost klientů.

## Licence
*(Zvolte vhodnou licenci – např. MIT, pokud je software distribuován jako open source.)*

---

Pro další informace nebo případné dotazy kontaktujte tým Praut s.r.o. nebo otevřete issue v repozitáři.
