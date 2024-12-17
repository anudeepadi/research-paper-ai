from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio

from config import BRIGHT_DATA_CONFIG, API_SETTINGS
from scrapers.bright_scraper import BrightScraper

app = FastAPI(
    title=API_SETTINGS['title'],
    description=API_SETTINGS['description'],
    version=API_SETTINGS['version']
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Bright Data scraper
scraper = BrightScraper(BRIGHT_DATA_CONFIG)

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10
    sources: Optional[List[str]] = ["arxiv", "google_scholar"]

class Paper(BaseModel):
    title: str
    authors: List[str]
    abstract: str
    pdf_url: Optional[str]
    source: str
    scraped_date: str

@app.post("/search", response_model=List[Paper])
async def search_papers(request: SearchRequest):
    """
    Search for papers across multiple sources using Bright Data's Scraping Browser
    """
    try:
        tasks = []
        if "arxiv" in request.sources:
            tasks.append(scraper.scrape_arxiv(request.query, request.max_results))
        if "google_scholar" in request.sources:
            tasks.append(scraper.scrape_google_scholar(request.query, request.max_results))
        
        # Run all scraping tasks concurrently
        results = await asyncio.gather(*tasks)
        
        # Flatten results from all sources
        all_papers = []
        for source_results in results:
            all_papers.extend(source_results)
            
        return all_papers[:request.max_results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup when shutting down"""
    await scraper.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)