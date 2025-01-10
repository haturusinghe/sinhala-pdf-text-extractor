import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import time
import argparse
import urllib3
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager with custom SSL context."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1_2,
            ssl_context=ctx
        )

def get_session():
    """Create a session with custom SSL adapter."""
    session = requests.Session()
    adapter = TLSAdapter()
    session.mount('https://', adapter)
    session.verify = False
    return session

def download_pdf(url, base_folder, page_num, session):
    """Download PDF using the provided session into a page-specific subfolder."""
    try:
        # Create page-specific subfolder
        folder = os.path.join(base_folder, f"page_{page_num}")
        if not os.path.exists(folder):
            os.makedirs(folder)

        response = session.get(url, timeout=30)
        if response.status_code == 200:
            filename = url.split('/')[-1]
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename} to {folder}")
            return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
    return False

def scrape_hansard_pdfs(base_url, output_folder, skip_pages=0, max_pages=None, page_load_wait=5):
    """Scrape PDFs from parliament website."""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session = get_session()
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    page_num = skip_pages * 20
    pages_processed = 0
    
    while True:
        if max_pages != -1 and pages_processed >= max_pages:
            print(f"Reached maximum number of pages ({max_pages})")
            break
            
        url = f"{base_url}?start={page_num}"
        print(f"Processing page {pages_processed + 1} (start={page_num})")
        
        try:
            response = session.get(url, timeout=page_load_wait)
            time.sleep(page_load_wait)
            
            if response.status_code != 200:
                print(f"Failed to fetch page: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', class_='tablearticle')
            
            if not table:
                print("No more tables found")
                break
                
            pdf_links = set()
            for link in table.find_all('a', href=True):
                href = link['href']
                if href.endswith('.pdf'):
                    pdf_links.add(urljoin(base_url, href))
            
            if not pdf_links:
                print("No PDF links found on page")
                break
                
            for pdf_url in pdf_links:
                download_pdf(pdf_url, output_folder, pages_processed + 1, session)
                time.sleep(1)
            
            page_num += 20
            pages_processed += 1
            time.sleep(2)
            
        except requests.Timeout:
            print(f"Timeout while fetching page. Retrying after {page_load_wait} seconds...")
            time.sleep(page_load_wait)
            continue
        except Exception as e:
            print(f"Error processing page: {str(e)}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Hansard PDFs from parliament.lk')
    parser.add_argument('--output_dir', default='hansard_pdfs', help='Directory to save downloaded PDFs')
    parser.add_argument('--skip-pages', type=int, default=0, help='Number of pages to skip')
    parser.add_argument('--max-pages', type=int, default=2, help='Maximum number of pages to process')
    parser.add_argument('--page-load-wait', type=int, default=10, help='Wait time in seconds for page loading')
    
    args = parser.parse_args()
    
    base_url = "https://www.parliament.lk/en/business-of-parliament/hansards"
    scrape_hansard_pdfs(
        base_url, 
        args.output_dir,
        skip_pages=args.skip_pages,
        max_pages=args.max_pages,
        page_load_wait=args.page_load_wait
    )
