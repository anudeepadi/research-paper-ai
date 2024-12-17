# Research Paper AI: Intelligent Academic Research Assistant

## Overview
Research Paper AI is a powerful tool that combines web scraping and AI to revolutionize academic research. Using Bright Data's Scraping Browser and Web Scraper API, it intelligently scrapes research papers from multiple academic sources and provides AI-powered insights.

## Features
- Multi-source paper scraping (arXiv, Google Scholar, etc.)
- AI-powered paper analysis and insights
- Citation network visualization
- Research trend analysis
- Real-time paper monitoring

## Tech Stack
- **Scraping**: Bright Data's Scraping Browser & Web Scraper API
- **Backend**: FastAPI
- **Frontend**: React + TailwindCSS
- **AI Model**: Transformers (SPECTER model)
- **Database**: SQLite

## Setup
1. Clone the repository
```bash
git clone https://github.com/yourusername/research-paper-ai.git
cd research-paper-ai
```

2. Set up Bright Data credentials
   - Sign up at [Bright Data](https://brightdata.com)
   - Create a Scraping Browser zone
   - Copy your credentials to `.env`

3. Install dependencies
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

4. Run the application
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

## Environment Variables
Create a `.env` file in the root directory:
```env
BRIGHT_DATA_USERNAME=your_username
BRIGHT_DATA_PASSWORD=your_password
BRIGHT_DATA_SCRAPING_BROWSER_URL=your_scraping_browser_url
```

## License
MIT License