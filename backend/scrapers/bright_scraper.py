import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional
import urllib.parse

class BrightScraper:
    def __init__(self, config: Dict):
        """Initialize Bright Data scraper with configuration"""
        self.username = config['username']
        self.password = config['password']
        self.host = config['host']
        self.proxy_url = f"http://{self.username}:{self.password}@{self.host}"
        self.session = None
    
    async def _init_session(self):
        """Initialize aiohttp session with Bright Data proxy"""
        if not self.session:
            # Configure proxy with authentication
            proxy_auth = aiohttp.BasicAuth(self.username, self.password)
            conn = aiohttp.TCPConnector(verify_ssl=False)  # For testing only
            self.session = aiohttp.ClientSession(
                connector=conn,
                trust_env=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
    
    async def scrape_arxiv(self, query: str, max_results: int = 10) -> List[Dict]:
        """Scrape papers from arXiv using Bright Data proxy"""
        await self._init_session()
        
        # Encode the query for URL
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://arxiv.org/search/?query={encoded_query}&searchtype=all"
        
        try:
            async with self.session.get(search_url, proxy=self.proxy_url) as response:
                if response.status != 200:
                    print(f"Error: Status code {response.status}")
                    return []
                    
                html = await response.text()
                return await self._parse_arxiv_results(html, max_results)
        except Exception as e:
            print(f"Error scraping arXiv: {str(e)}")
            return []
    
    async def _parse_arxiv_results(self, html: str, max_results: int) -> List[Dict]:
        """Parse arXiv search results HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # Debug print for HTML structure
        print("Parsing HTML structure...")
        
        # Look for papers in the search results
        papers = soup.select('.arxiv-result')
        if not papers:
            print("No papers found with .arxiv-result selector")
            papers = soup.select('li.arxiv-result')  # Alternative selector
        
        for paper in papers[:max_results]:
            try:
                # Extract paper details with extensive error checking
                title_elem = paper.select_one('.title')
                title = title_elem.text.strip() if title_elem else "Title not found"
                
                authors_elem = paper.select('.authors a')
                authors = [a.text.strip() for a in authors_elem] if authors_elem else ["Authors not found"]
                
                abstract_elem = paper.select_one('.abstract-full')
                if not abstract_elem:
                    abstract_elem = paper.select_one('.abstract')
                abstract = abstract_elem.text.strip() if abstract_elem else "Abstract not found"
                
                pdf_link = paper.select_one('a[href*=".pdf"]')
                pdf_url = pdf_link['href'] if pdf_link else None
                
                results.append({
                    'title': title,
                    'authors': authors,
                    'abstract': abstract,
                    'pdf_url': pdf_url,
                    'source': 'arXiv',
                    'scraped_date': datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"Error parsing paper: {str(e)}")
                continue
        
        return results
    
    async def scrape_google_scholar(self, query: str, max_results: int = 10) -> List[Dict]:
        """Scrape papers from Google Scholar using Bright Data proxy"""
        await self._init_session()
        
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://scholar.google.com/scholar?q={encoded_query}"
        
        try:
            async with self.session.get(search_url, proxy=self.proxy_url) as response:
                if response.status != 200:
                    print(f"Error: Status code {response.status}")
                    return []
                
                html = await response.text()
                return await self._parse_scholar_results(html, max_results)
        except Exception as e:
            print(f"Error scraping Google Scholar: {str(e)}")
            return []
    
    async def _parse_scholar_results(self, html: str, max_results: int) -> List[Dict]:
        """Parse Google Scholar search results HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for paper in soup.select('.gs_r')[:max_results]:
            try:
                title_elem = paper.select_one('.gs_rt')
                title = title_elem.text.strip() if title_elem else "Title not found"
                
                authors_elem = paper.select_one('.gs_a')
                authors = [authors_elem.text.strip()] if authors_elem else ["Authors not found"]
                
                snippet_elem = paper.select_one('.gs_rs')
                snippet = snippet_elem.text.strip() if snippet_elem else "Abstract not found"
                
                results.append({
                    'title': title,
                    'authors': authors,
                    'abstract': snippet,
                    'pdf_url': None,
                    'source': 'Google Scholar',
                    'scraped_date': datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error parsing Scholar paper: {str(e)}")
                continue
        
        return results
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()